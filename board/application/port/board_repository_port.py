from abc import ABC, abstractmethod
from typing import Optional

from board.domain.baord import Board


class BoardRepositoryPort(ABC):

    @abstractmethod
    def save(self, board: Board) -> Board:
        pass

    @abstractmethod
    def list_boards(self) -> list[Board]:
        pass

    @abstractmethod
    def get_board(self, board_id: int) -> Optional[Board]:
        pass

    @abstractmethod
    def update_board(self, board: Board) -> Board:
        pass