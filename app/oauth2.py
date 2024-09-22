from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta
from app.evn_valid import setting
from fastapi import HTTPException,status,Depends
from jose import jwt,JWTError
from sqlalchemy.orm.session import Session
from app.database import get_db
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


SECRET_KEY=setting.SECRET_KEY
REFRESH_SECRET_KEY=setting.REFRESH_SECRET_KEY
ALGORITHM=setting.ALGORITHM
ACCESS_EXPIRY_TIME=setting.ACCESS_EXPIRE_TIME
REFRESH_EXPIRE_MINUTES=setting.REFRESH_EXPIRE_MINUTES



def create_access_token(data:dict):
    to_encode_data=data.copy()
    try:
        expire=datetime.utcnow()+timedelta(minutes=ACCESS_EXPIRY_TIME)
        to_encode_data.update({"exp":expire})
        token=jwt.encode(to_encode_data,SECRET_KEY,algorithm=ALGORITHM)
    except Exception as e:
        raise HTTPException(detail="something went wrong"+str(e),status_code=status.HTTP_400_BAD_REQUEST)
    return token

def create_refresh_token(data:dict):
    to_encode_data=data.copy()
    try:
        expire=datetime.utcnow()+timedelta(minutes=REFRESH_EXPIRE_MINUTES)
        to_encode_data.update({"exp":expire})
        token=jwt.encode(to_encode_data,REFRESH_SECRET_KEY,algorithm=ALGORITHM)
    except Exception as e:
        raise HTTPException(detail="something went wrong"+str(e),status_code=status.HTTP_400_BAD_REQUEST)
    return token



def verify_token(token,credentials_exceptions):
    try:
        payload=jwt.decode(token,REFRESH_SECRET_KEY,algorithms=[ALGORITHM])
        id = payload.get("user_id")
        if id is None:
            raise credentials_exceptions
    except JWTError:
        raise credentials_exceptions
    return id



def get_current_user(token:Depends=(oauth2_scheme),db:Session = Depends(get_db)):
    credentials_exceptions=HTTPException(
         status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid credentials",
        headers={"WWW-AUTHENTICATE": "BEARER"},
    )
    id=verify_token(token,credentials_exceptions)
    user = db.query(User).filter(User.id == id).first()
    return user

