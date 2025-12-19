from passlib.context import CryptContext

from ....domain.ports.security_service import SecurityService

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class PasslibSecurityService(SecurityService):
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
