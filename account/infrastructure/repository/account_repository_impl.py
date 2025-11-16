from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from account.adapter.input.web.request.create_account_request import CreateAccountRequest
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

    def list_all(self) -> list[Account]:
        orm_accounts = self.db.query(AccountORM).all()
        accounts = []
        for orm_account in orm_accounts:
            account = Account(
                user_uuid=orm_account.user_uuid,
                oauth_id=orm_account.oauth_id,
                oauth_type=orm_account.oauth_type,
                nickname=orm_account.nickname,
                name=orm_account.name,
                role_id=orm_account.role_id,
                email=orm_account.email,
                phone_number=orm_account.phone_number,
                active_status=orm_account.active_status,
                profile_image=orm_account.profile_image
            )
            account.created_at = orm_account.created_at
            account.updated_at = orm_account.updated_at
            accounts.append(account)
        return accounts

    def get_by_oauth_id(self, oauth_type: str, user_oauth_id: str) -> Optional[Account]:
        orm_account = self.db.query(AccountORM).filter(AccountORM.oauth_type == oauth_type,
                                                       AccountORM.oauth_id == user_oauth_id).first()
        if orm_account:
            account = Account(
                user_uuid=orm_account.user_uuid,
                oauth_id=orm_account.oauth_id,
                oauth_type=orm_account.oauth_type,
                nickname=orm_account.nickname,
                name=orm_account.name,
                profile_image=orm_account.profile_image,
                email=orm_account.email,
                phone_number=orm_account.phone_number,
                active_status=orm_account.active_status,
                role_id=orm_account.role_id
            )
            account.created_at = orm_account.created_at
            account.updated_at = orm_account.updated_at
            return account
        return None

    def update(self, account: CreateAccountRequest):
        self.db.query(AccountORM).filter(AccountORM.user_uuid == account.user_uuid).update(
            {
                "nickname": account.nickname,
                "name": account.name,
                "profile_image": account.profile_image,
                "email": account.email,
                "phone_number": account.phone_number,
                "active_status": account.active_status,
                "role_id": account.role_id,
                "updated_at": datetime.utcnow()
            }
        )
        self.db.commit()
        account = self.get_by_oauth_id(account.oauth_type, account.oauth_id)
        return account

    def delete(self, user_uuid: str) -> bool:
        deleted_count = self.db.query(AccountORM).filter(AccountORM.user_uuid == user_uuid).delete()
        self.db.commit()
        return deleted_count > 0