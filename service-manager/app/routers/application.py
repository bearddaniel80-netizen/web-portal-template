from .model import ApplicationState, ApplicationStatus
from .common import Application
from ..security.api_key_check import verify_internal_key

from fastapi import Header, APIRouter

router = APIRouter(prefix="/api/applications")
app = Application()

# ----------------------
# STATUS
# ----------------------
@router.get("/{application_id}/status", response_model=ApplicationStatus)
def status(
    application_id: str,
    x_internal_key: str | None = Header(default=None),
):
    verify_internal_key(x_internal_key)
    app.status(application_id)

    return ApplicationStatus(
        id=application_id,
        state=app.states[application_id],
    )

# ----------------------
# START
# ----------------------
@router.post("/{application_id}/start")
def start(
    application_id: str,
    x_internal_key: str | None = Header(default=None),
):
    verify_internal_key(x_internal_key)
    return app.start(application_id)

# ----------------------
# STOP
# ----------------------
@router.post("/{application_id}/stop")
def stop(
    application_id: str,
    x_internal_key: str | None = Header(default=None),
):
    verify_internal_key(x_internal_key)
    return app.stop(application_id)

# ----------------------
# ACTIVE
# ----------------------
@router.post("/{application_id}/activate")
def activate(
    application_id: str,
    x_internal_key: str | None = Header(default=None),
):
    verify_internal_key(x_internal_key)
    app.activate(application_id)