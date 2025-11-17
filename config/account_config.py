from account.application.usecase.account_usecase import AccountUseCase
from account.infrastructure.repository.account_repository_impl import AccountRepositoryImpl

# 전역 변수
_account_usecase_instance = None

def get_account_usecase() -> AccountUseCase:
    global _account_usecase_instance
    if _account_usecase_instance is None:
        _account_usecase_instance = AccountUseCase(AccountRepositoryImpl())
    return _account_usecase_instance
