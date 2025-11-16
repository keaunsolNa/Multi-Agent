from pydantic import BaseModel
from datetime import datetime


class BoardResponse(BaseModel):
    id: int
    board_type: str
    user_id: str
    title: str
    content: str
    view_count: int
    created_at: datetime
    updated_at: datetime
