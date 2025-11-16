from pydantic import BaseModel

class CreateAccountRequest(BaseModel):
    user_uuid: str
    oauth_id: str
    oauth_type: str
    nickname: str
    name:str
    profile_image: str
    email: str
    phone_number: str
    active_status: str
    role_id: str