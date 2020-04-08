from typing import Optional

from flask_login import UserMixin
from nssl.entites import UserData


class User(UserMixin):

    def __init__(self, user_data: Optional[UserData] = None):
        self.user_id: int = 0
        self.username: str = ''
        self.token: str = ''

        if user_data:
            self.user_id = user_data.id
            self.username = user_data.username
            self.token = user_data.token

    @property
    def id(self):
        return self.user_id
