from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from datetime import datetime
import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Password hashing

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# User registration
async def register_user(db: AsyncSession, email: str, password: str, full_name: str = None):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user:
        return None  # User already exists
    hashed_pw = hash_password(password)
    new_user = User(email=email, hashed_password=hashed_pw, full_name=full_name)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# User login
async def authenticate_user(db: AsyncSession, email: str, password: str):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        return None
    # Generate session token
    session_token = secrets.token_urlsafe(32)
    user.session_token = session_token
    user.last_login = datetime.utcnow()
    await db.commit()
    await db.refresh(user)
    return user

# Session validation
def get_current_user_from_token(db: AsyncSession, session_token: str):
    return db.execute(select(User).where(User.session_token == session_token))

# Logout
async def logout_user(db: AsyncSession, user: User):
    user.session_token = None
    await db.commit()
    await db.refresh(user)
    return user 