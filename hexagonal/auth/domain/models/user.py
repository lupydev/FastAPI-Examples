from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass
class User:
    id: UUID
    email: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # Ejemplo de regla de negocio
    def deactivate(self):
        if not self.is_active:
            raise ValueError("Inactive user cannot be deactivated again.")
        self.is_active = False

    def change_password(self, new_hashed_password: str):
        if not new_hashed_password:
            raise ValueError("Password cannot be empty")
        self.hashed_password = new_hashed_password
