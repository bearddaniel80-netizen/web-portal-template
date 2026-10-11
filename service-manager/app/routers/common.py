from .model import ApplicationState
from .docker import DockerCompose

import yaml
from fastapi import HTTPException
from pathlib import Path

class Application:
    def __init__(self):
        CONFIG_FILE = Path("/config/applications.yaml")

        with CONFIG_FILE.open() as file:
            config = yaml.safe_load(file)

        self.applications = config["applications"]
        self.current_application: str | None = None
        self.states: dict[str, ApplicationState] = {
            application_id: ApplicationState.STOPPED
            for application_id in applications
        }

    def get_application(self, application_id: str) -> dict:
        application = self.applications.get(application_id)

        if application is None:
            raise HTTPException(
                status_code=404,
                detail=f"Unknown application: {application_id}",
            )

        return application

    def compose_for(self, application_id: str) -> DockerCompose:
        application = self.get_application(application_id)

        return DockerCompose(
            application["compose_file"]
        )

# ----------------------
# STATUS
# ----------------------
    def status(self, application_id: str) -> dict:
        return self.get_application(application_id)

# ----------------------
# START
# ----------------------
    def start(self, application_id: str):

        self.get_application(application_id)

        if self.current_application == application_id:
            return {
                "id": application_id,
                "state": self.states[application_id],
            }

        if self.current_application is not None:
            raise HTTPException(
                status_code=409,
                detail=f"{self.current_application} is currently active",
            )

        self.states[application_id] = ApplicationState.STARTING

        try:
            self.compose_for(application_id).up()

            self.states[application_id] = ApplicationState.RUNNING
            self.current_application = application_id

            return {
                "id": application_id,
                "state": self.states[application_id],
            }

        except Exception:
            self.states[application_id] = ApplicationState.FAILED
            raise HTTPException(
                status_code=500,
                detail=f"Failed to start {application_id}",
            )

# ----------------------
# STOP
# ----------------------
    def stop(self, application_id: str):

        self.get_application(application_id)

        if self.states[application_id] == ApplicationState.STOPPED:
            return {
                "id": application_id,
                "state": ApplicationState.STOPPED,
            }

        self.states[application_id] = ApplicationState.STOPPING

        try:
            self.compose_for(application_id).down()

            self.states[application_id] = ApplicationState.STOPPED

            if self.current_application == application_id:
                self.current_application = None

            return {
                "id": application_id,
                "state": self.states[application_id],
            }

        except Exception:
            states[application_id] = ApplicationState.FAILED
            raise HTTPException(
                status_code=500,
                detail=f"Failed to stop {application_id}",
            )

# ----------------------
# ACTIVE
# ----------------------
    def active(self, application_id: str):    
        self.get_application(application_id)

        if self.current_application == application_id:
            return {
                "id": application_id,
                "state": ApplicationState.RUNNING,
            }

        # Stop whatever is currently active.
        if self.current_application is not None:
            previous = self.current_application

            self.states[previous] = ApplicationState.STOPPING

            try:
                self.compose_for(previous).down()
                self.states[previous] = ApplicationState.STOPPED
            except Exception:
                self.states[previous] = ApplicationState.FAILED

                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to stop {previous}",
                )

            self.current_application = None

        # Start requested application.
        self.states[application_id] = ApplicationState.STARTING

        try:
            self.compose_for(application_id).up()

            self.states[application_id] = ApplicationState.RUNNING
            self.current_application = application_id

            return {
                "id": application_id,
                "state": ApplicationState.RUNNING,
            }

        except Exception:
            self.states[application_id] = ApplicationState.FAILED

            raise HTTPException(
                status_code=500,
                detail=f"Failed to start {application_id}",
            )