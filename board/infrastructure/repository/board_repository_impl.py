from datetime import datetime
from typing import Optional

from sqlalchemy import func

from board.application.port.board_repository_port import BoardRepositoryPort
from board.domain.baord import Board
from board.infrastructure.orm.board_orm import BoardORM
from config.database.session import get_db_session


class BoardRepositoryImpl(BoardRepositoryPort):
    def __init__(self):
        from sqlalchemy.orm import Session
        self.db: Session = get_db_session()

    def save(self, board: Board) -> Board:
        orm_board = BoardORM(
            title=board.title,
            content=board.content,
            board_type=board.board_type,
            user_id=board.user_id,
        )

        self.db.add(orm_board)
        self.db.commit()
        self.db.refresh(orm_board)

        board.id = orm_board.id
        orm_board.view_count = 0
        orm_board.created_at = orm_board.created_at
        orm_board.updated_at = orm_board.updated_at
        return board

    def list_boards(self) -> list[Board]:
        orm_boards = self.db.query(BoardORM).all()
        boards = []
        for orm_board in orm_boards:
            board = Board(
                title=orm_board.title,
                content=orm_board.content,
                board_type=orm_board.board_type,
                user_id=orm_board.user_id,
            )
            board.id = orm_board.id
            board.view_count = orm_board.view_count
            board.created_at = orm_board.created_at
            board.updated_at = orm_board.updated_at
            boards.append(board)
        return boards

    def get_board(self, board_id: int) -> Optional[Board]:
        orm_board = self.db.query(BoardORM).filter(BoardORM.id == board_id).first()
        if orm_board:
            board = Board(
                title=orm_board.title,
                content=orm_board.content,
                board_type=orm_board.board_type,
                user_id=orm_board.user_id,
            )
            board.id = orm_board.id
            board.view_count = orm_board.view_count
            board.created_at = orm_board.created_at
            board.updated_at = orm_board.updated_at
            return board
        return None

    def update_board(self, board: Board):
        # view_count는 기존 값에 1을 더해서 업데이트
        self.db.query(BoardORM).filter(BoardORM.id == board.id).update(
            {
                "title": board.title,
                "content": board.content,
                "board_type": board.board_type,
                "updated_at": datetime.utcnow(),
                "view_count": func.coalesce(BoardORM.view_count, 0) + 1
            },
            synchronize_session=False
        )
        self.db.commit()
        board = self.get_board(board.id)
        return board