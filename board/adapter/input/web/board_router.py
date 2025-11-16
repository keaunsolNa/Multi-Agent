from fastapi import APIRouter, HTTPException

from account.application.usecase.account_usecase import AccountUseCase
from account.infrastructure.repository.account_repository_impl import AccountRepositoryImpl
from board.adapter.input.web.request.create_board_request import CreateBoardRequest
from board.adapter.input.web.request.update_board_request import UpdateBoardRequest
from board.adapter.input.web.response.board_response import BoardResponse
from board.application.usecase.board_usecase import BoardUseCase
from board.domain.baord import Board
from board.infrastructure.repository.board_repository_impl import BoardRepositoryImpl

board_router = APIRouter()
usecase = BoardUseCase(BoardRepositoryImpl())
user_case = AccountUseCase(AccountRepositoryImpl())

@board_router.post("/create", response_model=BoardResponse)
def create_board(request: CreateBoardRequest):
    user = user_case.get_account_by_user_uuid(request.user_id)
    print("DEBUG USER", user)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    board = usecase.create_board(request.board_type, request.user_id, request.title, request.content)
    return BoardResponse(
        id=board.id,
        board_type=board.board_type,
        user_id=board.user_id,
        title=board.title,
        content=board.content,
        view_count=board.view_count,
        created_at=board.created_at,
        updated_at=board.updated_at,
    )

@board_router.get("/list", response_model=list[BoardResponse])
def list_boards():
    board = usecase.list_boards()
    return [
        BoardResponse(
            id= b.id,
            board_type= b.board_type,
            user_id=b.user_id,
            title=b.title,
            content=b.content,
            view_count=b.view_count,
            created_at=b.created_at,
            updated_at=b.updated_at
        ) for b in board
    ]

@board_router.get("/{board_id}", response_model=BoardResponse)
def get_board(board_id: int):
    board = usecase.get_board(board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")

    board.view_count += 1
    board = usecase.update_board(board)
    return BoardResponse(
        id=board.id,
        board_type=board.board_type,
        user_id=board.user_id,
        title=board.title,
        content=board.content,
        view_count=board.view_count,
        created_at=board.created_at,
        updated_at=board.updated_at,
    )

@board_router.put("/update", response_model=BoardResponse)
def update_board(request: UpdateBoardRequest):
    board = usecase.update_board_from_request(request)
    return BoardResponse(
        id=board.id,
        board_type=board.board_type,
        user_id=board.user_id,
        title=board.title,
        content=board.content,
        view_count=board.view_count,
        created_at=board.created_at,
        updated_at=board.updated_at,
    )

@board_router.delete("/delete/{board_id}")
def delete_board(board_id: int):
    try:
        success = usecase.delete_board(board_id)
        if success:
            return {"message": "Deleted successfully", "status": "success"}
        else:
            raise HTTPException(status_code=404, detail="Board not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")