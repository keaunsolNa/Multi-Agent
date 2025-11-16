from fastapi import APIRouter, HTTPException

from account.application.usecase.account_usecase import AccountUseCase
from account.infrastructure.repository.account_repository_impl import AccountRepositoryImpl
from board.adapter.input.web.request.create_board_request import CreateBoardRequest
from board.adapter.input.web.response.board_response import BoardResponse
from board.application.usecase.board_usecase import BoardUseCase
from board.infrastructure.repository.board_repository_impl import BoardRepositoryImpl

board_router = APIRouter()
usecase = BoardUseCase(BoardRepositoryImpl())
user_case = AccountUseCase(AccountRepositoryImpl())

@board_router.post("/create", response_model=BoardResponse)
def create_board(request: CreateBoardRequest):
    user = user_case.get_account_by_user_uuid(request.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    board = usecase.create_board(request.board_type, request.user_id, request.title, request.content)
    return BoardResponse(
        board_type=board.board_type,
        user_id=board.user_id,
        title=board.title,
        content=board.content,
        view_count=board.view_count,
        created_at=board.created_at,
        updated_at=board.updated_at,
    )