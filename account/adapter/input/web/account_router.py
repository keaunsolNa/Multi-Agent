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
        role_id=account.role_id,
        created_at=account.created_at,
        updated_at=account.updated_at
    )

@account_router.get("/list", response_model=list[AccountResponse])
def list_accounts():
    account = usecase.list_account()
    return [
        AccountResponse(
            user_uuid=a.user_uuid,
            oauth_id=a.oauth_id,
            oauth_type=a.oauth_type,
            nickname=a.nickname,
            name=a.name,
            profile_image=a.profile_image,
            email=a.email,
            phone_number=a.phone_number,
            active_status=a.active_status,
            role_id=a.role_id,
            updated_at=a.updated_at,
            created_at=a.created_at,
        ) for a in account
    ]

@account_router.get("/{user_uuid}", response_model=AccountResponse)
def get_account_by_user_uuid(user_uuid: str):
    account = usecase.get_account_by_user_uuid(user_uuid)
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
        updated_at=account.updated_at,
        created_at=account.created_at,
        role_id=account.role_id
    )

@account_router.get("/{oauth_type}/{oauth_id}", response_model=AccountResponse)
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
        updated_at=account.updated_at,
        created_at=account.created_at,
        role_id=account.role_id
    )

@account_router.put("/update", response_model=AccountResponse)
def update_account(request: CreateAccountRequest):
    account = usecase.update(request)
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
        role_id=account.role_id,
        updated_at=account.updated_at,
        created_at=account.created_at
    )

@account_router.delete("/delete/{user_uuid}")
def delete_account(user_uuid: str):
    try:
        success = usecase.delete_account(user_uuid)
        if success:
            return {"message": "Deleted successfully", "status": "success"}
        else:
            raise HTTPException(status_code=404, detail="Account not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
