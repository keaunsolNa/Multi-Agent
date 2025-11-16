from typing import Optional

from sqlalchemy.orm import Session

from account.application.port.account_repository_port import AccountRepositoryPort
from account.domain.account import Account
from account.infrastructure.orm.account_orm import AccountORM
from config.database.session import get_db_session


class AccountRepositoryImpl(AccountRepositoryPort):
    def __init__(self):
        self.db: Session = get_db_session()

    async def save(self, account: Account) -> Account:

        orm_account = AccountORM(
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

        self.db.add(orm_account)
        self.db.commit()
        self.db.refresh(orm_account)

        account.user_uuid = orm_account.user_uuid
        account.created_at = orm_account.created_at
        account.updated_at = orm_account.updated_at
        return account