from src.auth.models import User
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.auth.schemas import UserCreateModel
from src.auth.utils import generate_passwd_hash, verify_password


class AuthService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)

        result = await session.execute(statement)

        user = result.scalars().first()

        return user


    async def user_exists(self, email: str, session: AsyncSession):
        user = self.get_user_by_email(email, session)
        if user:
            return True 
        return False
    
    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()
        new_user = User(**user_data_dict)
        new_user.password = generate_passwd_hash(user_data_dict['password'])

        await session.add(new_user)
        await session.commit()

        return new_user
    
