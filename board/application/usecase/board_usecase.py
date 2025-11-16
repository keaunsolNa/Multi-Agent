from typing import Optional

from board.adapter.input.web.request.create_board_request import CreateBoardRequest
from board.adapter.input.web.request.update_board_request import UpdateBoardRequest
from board.domain.baord import Board


class BoardUseCase:
    def __init__(self, board_repo):
        self.board_repo = board_repo

    def create_board(self, board_type:str, user_id:str, title: str, content: str) -> Board:
        board = Board(board_type=board_type, user_id=user_id, title=title, content=content)
        return self.board_repo.save(board)

    def list_boards(self) -> list[Board]:
        return self.board_repo.list_boards()

    def get_board(self, board_id: int) -> Optional[Board]:
        return self.board_repo.get_board(board_id)

    def update_board(self, board: Board) -> Board:
        return self.board_repo.update_board(board)

    def update_board_from_request(self, request: UpdateBoardRequest) -> Board:
        # 요청 모델을 Board 도메인 객체로 변환
        board = Board(
            board_type=request.board_type,
            user_id=request.user_id,
            title=request.title,
            content=request.content
        )
        board.id = request.id
        return self.board_repo.update_board(board)

    def delete_board(self, board_id: int) -> bool:
        return self.board_repo.delete_board(board_id)