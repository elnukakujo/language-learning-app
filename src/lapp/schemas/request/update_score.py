from .base import BaseRequest

class UpdateScoreRequest(BaseRequest):
    element_id: str
    success: bool