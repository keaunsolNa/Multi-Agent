from abc import ABC, abstractmethod
from typing import Optional

from account.adapter.input.web.request.create_account_request import CreateAccountRequest
from account.domain.account import Account


class AccountRepositoryPort(ABC):

    @abstractmethod
    async def save(self, account: Account) -> Account:
        pass

    @abstractmethod
    def list_all(self) -> list[Account]:
        pass

    @abstractmethod
    def get_by_oauth_id(self, oauth_type: str, user_oauth_id: str) -> Optional[Account]:
        pass

    @abstractmethod
    def update(self, account: CreateAccountRequest) -> Account:
        pass