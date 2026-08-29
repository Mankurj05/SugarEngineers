import uuid
import datetime
from pydantic import BaseModel, Field

# Base mixin for deterministic responses
class BaseResponse(BaseModel):
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    generated_at: str = Field(default_factory=lambda: datetime.datetime.now(datetime.UTC).isoformat())

class ErrorResponse(BaseResponse):
    success: bool = False
    data: None = None
    error: dict
