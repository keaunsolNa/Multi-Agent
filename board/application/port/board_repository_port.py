from abc import ABC, abstractmethod

from board.domain.baord import Board


class BoardRepositoryPort(ABC):

    @abstractmethod
    def save(self, board: Board) -> Board:
        pass