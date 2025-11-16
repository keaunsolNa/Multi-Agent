from abc import ABC, abstractmethod

from account.domain.account import Account


class AccountRepositoryPort(ABC):

    @abstractmethod
    async def save(self, account: Account) -> Account:
        pass