from board.domain.baord import Board


class BoardUseCase:
    def __init__(self, board_repo):
        self.board_repo = board_repo

    def create_board(self, board_type:str, user_id:str, title: str, content: str) -> Board:
        board = Board(board_type=board_type, user_id=user_id, title=title, content=content)
        return self.board_repo.save(board)

    def list_boards(self) -> list[Board]:
        return self.board_repo.list_boards()
