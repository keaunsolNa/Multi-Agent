from typing import Optional, List

from account.adapter.input.web.request.create_account_request import CreateAccountRequest
from account.application.port.account_repository_port import AccountRepositoryPort
from account.domain.account import Account


class AccountUseCase:
    def __init__(self, account_repo: AccountRepositoryPort):
        self.account_repo = account_repo

    async def create_account(self, user_uuid: str, oauth_id:str, oauth_type: str, nickname: str, name:str, profile_image:str, email:str, phone_number:str, active_status:str, role_id:str):
        account = Account(user_uuid=user_uuid, oauth_id=oauth_id, oauth_type=oauth_type, nickname=nickname, name=name, profile_image=profile_image, email=email, phone_number=phone_number, active_status=active_status, role_id=role_id)
        return await self.account_repo.save(account)

    def list_account(self) -> List[Account]:
        return self.account_repo.list_all()

    def get_account_by_oauth_id(self, oauth_type:str, oauth_id: str) -> Optional[Account]:
        return self.account_repo.get_by_oauth_id(oauth_type, oauth_id)

    def update(self, account: CreateAccountRequest):
        account = self.account_repo.update(account)
        return account