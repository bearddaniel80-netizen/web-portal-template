from pathlib import Path

import yaml
from fastapi import FastAPI, HTTPException

from .docker import DockerCompose
from .models import ApplicationState, ApplicationStatus


app = FastAPI(title="Service Manager")


CONFIG_FILE = Path("/config/applications.yaml")


with CONFIG_FILE.open() as file:
    config = yaml.safe_load(file)


applications = config["applications"]


current_application: str | None = None
states: dict[str, ApplicationState] = {
    application_id: ApplicationState.STOPPED
    for application_id in applications
}


def get_application(application_id: str) -> dict:
    application = applications.get(application_id)

    if application is None:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown application: {application_id}",
        )

    return application


def compose_for(application_id: str) -> DockerCompose:
    application = get_application(application_id)

    return DockerCompose(
        application["compose_file"]
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get(
    "/applications/{application_id}/status",
    response_model=ApplicationStatus,
)
def status(application_id: str):
    get_application(application_id)

    return ApplicationStatus(
        id=application_id,
        state=states[application_id],
    )


@app.post("/applications/{application_id}/start")
def start(application_id: str):
    global current_application

    get_application(application_id)

    if current_application == application_id:
        return {
            "id": application_id,
            "state": states[application_id],
        }

    if current_application is not None:
        raise HTTPException(
            status_code=409,
            detail=f"{current_application} is currently active",
        )

    states[application_id] = ApplicationState.STARTING

    try:
        compose_for(application_id).up()

        states[application_id] = ApplicationState.RUNNING
        current_application = application_id

        return {
            "id": application_id,
            "state": states[application_id],
        }

    except Exception:
        states[application_id] = ApplicationState.FAILED
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start {application_id}",
        )


@app.post("/applications/{application_id}/stop")
def stop(application_id: str):
    global current_application

    get_application(application_id)

    if states[application_id] == ApplicationState.STOPPED:
        return {
            "id": application_id,
            "state": ApplicationState.STOPPED,
        }

    states[application_id] = ApplicationState.STOPPING

    try:
        compose_for(application_id).down()

        states[application_id] = ApplicationState.STOPPED

        if current_application == application_id:
            current_application = None

        return {
            "id": application_id,
            "state": states[application_id],
        }

    except Exception:
        states[application_id] = ApplicationState.FAILED
        raise HTTPException(
            status_code=500,
            detail=f"Failed to stop {application_id}",
        )


@app.post("/applications/{application_id}/activate")
def activate(application_id: str):
    global current_application

    get_application(application_id)

    if current_application == application_id:
        return {
            "id": application_id,
            "state": ApplicationState.RUNNING,
        }

    # Stop whatever is currently active.
    if current_application is not None:
        previous = current_application

        states[previous] = ApplicationState.STOPPING

        try:
            compose_for(previous).down()
            states[previous] = ApplicationState.STOPPED
        except Exception:
            states[previous] = ApplicationState.FAILED

            raise HTTPException(
                status_code=500,
                detail=f"Failed to stop {previous}",
            )

        current_application = None

    # Start requested application.
    states[application_id] = ApplicationState.STARTING

    try:
        compose_for(application_id).up()

        states[application_id] = ApplicationState.RUNNING
        current_application = application_id

        return {
            "id": application_id,
            "state": ApplicationState.RUNNING,
        }

    except Exception:
        states[application_id] = ApplicationState.FAILED

        raise HTTPException(
            status_code=500,
            detail=f"Failed to start {application_id}",
        )