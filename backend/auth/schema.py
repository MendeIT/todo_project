from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

import crud
from api.schemas.users import UserLoginSchemas
from auth.utils import create_jwt_token, vaidate_password
from db.database import get_session


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


auth_router = APIRouter(
    prefix="/jwt",
    tags=["JWT"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/jwt/login")


@auth_router.post("/login", response_model=TokenInfo)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session)
):
    user = await crud.get_user_by_username(
        session=db,
        username=form_data.username
    )

    if not vaidate_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_jwt_token(
        user=UserLoginSchemas(
            username=user.username,
            password=form_data.password
        ),
        user_id=user.id
    )

    return TokenInfo(access_token=access_token, token_type="Bearer")
