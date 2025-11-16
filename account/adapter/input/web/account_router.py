from fastapi import APIRouter, HTTPException

from account.adapter.input.web.request.create_account_request import CreateAccountRequest
from account.adapter.input.web.response.account_response import AccountResponse
from account.application.usecase.account_usecase import AccountUseCase
from account.infrastructure.repository.account_repository_impl import AccountRepositoryImpl

account_router = APIRouter()
usecase = AccountUseCase(AccountRepositoryImpl())


@account_router.post("/create", response_model=AccountResponse)
async def create_account(request: CreateAccountRequest):
    account = await usecase.create_account(request.user_uuid, request.oauth_id, request.oauth_type, request.nickname,
                                           request.name, request.profile_image, request.email, request.phone_number,
                                           request.active_status, request.role_id)
    return AccountResponse(
        user_uuid=account.user_uuid,
        oauth_id=account.oauth_id,
        oauth_type=account.oauth_type,
        nickname=account.nickname,
        name=account.name,
        profile_image=account.profile_image,
        email=account.email,
        phone_number=account.phone_number,
        active_status=account.active_status,
        role_id=account.role_id
    )


@account_router.get("/read/{oauth_type}/{oauth_id}", response_model=AccountResponse)
def get_account_by_oauth_id(oauth_type: str, oauth_id: str):
    account = usecase.get_account_by_oauth_id(oauth_type, oauth_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return AccountResponse(
        user_uuid=account.user_uuid,
        oauth_id=account.oauth_id,
        oauth_type=account.oauth_type,
        nickname=account.nickname,
        name=account.name,
        profile_image=account.profile_image,
        email=account.email,
        phone_number=account.phone_number,
        active_status=account.active_status,
        role_id=account.role_id
    )
