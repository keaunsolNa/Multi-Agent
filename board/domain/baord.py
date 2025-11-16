from datetime import datetime

class Board:
    def __init__(self, board_type: str, user_id: str, title: str, content: str):
        self.board_type = board_type
        self.user_id = user_id
        self.title = title
        self.content = content
        self.view_count = 0
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def update(self, board_type, title, content):
        self.board_type = board_type
        self.title = title
        self.content = content
        return self