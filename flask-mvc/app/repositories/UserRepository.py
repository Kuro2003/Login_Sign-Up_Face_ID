from app.packages.auth.models.User import User
from app.repositories.BaseRepository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User) # Gọi hàm khởi tạo của BaseRepository và truyền vào model User
        
        
