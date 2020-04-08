from dataclasses import dataclass


@dataclass(frozen=True)
class LoginData:
    id: int = 0
    username: str = 'anonymous'
    token: str = ''
