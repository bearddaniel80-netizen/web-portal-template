from enum import Enum

from pydantic import BaseModel


class ApplicationState(str, Enum):
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    FAILED = "failed"


class ApplicationStatus(BaseModel):
    id: str
    state: ApplicationState