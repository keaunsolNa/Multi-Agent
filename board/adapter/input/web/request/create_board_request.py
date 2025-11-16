from pydantic import BaseModel

class CreateBoardRequest(BaseModel):
    board_type: str
    user_id: str
    title: str
    content: str
