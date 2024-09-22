from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from sqlalchemy.orm.session import Session
from app.models import User
from app.utils import  verify_password
from app.oauth2 import create_access_token


router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("/")
def login(
    request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)
):
    user=db.query(User).filter(User.email==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    if not verify_password(request.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials"
        )
    access_token = create_access_token(
        data={"user_id": user.id}
    )
    refresh_token = create_access_token(
        data={"user_id": user.id}
    )
    return [
        {"access_token": access_token, "token_type": "bearer"},
        {"refresh_token": refresh_token, "token_type": "bearer"}
    ]
    