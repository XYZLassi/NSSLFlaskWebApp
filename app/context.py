from base.ram_storage import RamStorage

from .models.user import User

UserStorage: RamStorage[User] = RamStorage[User]()
