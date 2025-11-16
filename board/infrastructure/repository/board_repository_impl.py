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
            board.created_at = orm_board.created_at
            board.updated_at = orm_board.updated_at
            boards.append(board)
        return boards
