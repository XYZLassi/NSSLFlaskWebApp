from .models.user import User
from .ram_storage import RamStorage

UserStorage: RamStorage[User] = RamStorage[User]()
