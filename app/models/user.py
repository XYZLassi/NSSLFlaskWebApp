from typing import Optional

from flask_login import UserMixin
from nssl.entites import LoginData


class User(UserMixin):

    def __init__(self, login_data: Optional[LoginData] = None):
        self.user_id: int = 0
        self.username: str = ''
        self.token: str = ''

        if login_data:
            self.user_id = login_data.id
            self.username = login_data.username
            self.token = login_data.token

    @property
    def id(self):
        return self.user_id
