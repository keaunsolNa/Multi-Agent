from pydantic import BaseModel

class UpdateBoardRequest(BaseModel):
    id: int
    board_type: str
    user_id: str
    title: str
    content: str

