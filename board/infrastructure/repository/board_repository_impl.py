from board.application.port.board_repository_port import BoardRepositoryPort
from board.domain.baord import Board
from board.infrastructure.orm.board_orm import BoardORM

from config.database.session import get_db_session

class BoardRepositoryImpl(BoardRepositoryPort):
    def __init__(self):
        self.db = Session = get_db_session()

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

        orm_board.view_count = 0
        orm_board.created_at = board.created_at
        orm_board.updated_at = board.updated_at
        return board