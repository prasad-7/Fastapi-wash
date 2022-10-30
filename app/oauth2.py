from jose import JWTError,jwt
from datetime import datetime,timedelta
from fastapi import status, HTTPException,Depends
from sqlalchemy.orm import Session
from .schemas import TokenData
from . import database,models
from fastapi.security import OAuth2PasswordBearer
from.config import setting


auth_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = setting.SECRET_KEY
ALGORITHM = setting.ALGORITHM
ACCESS_EXPIRE_TIME_MINUTES =setting.ACCESS_EXPIRE_TIME_MINUTES

def create_accesstoken(data: dict):

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=ACCESS_EXPIRE_TIME_MINUTES)
    to_encode.update({"expire": str(expire)})
    jwt_token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return jwt_token


def verify_accesstoken(token : str, credentials_execption):

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expire_time = decoded["expire"]
        strtime = datetime.strptime(expire_time, '%Y-%m-%d %H:%M:%S.%f')
        if datetime.utcnow() <= strtime:
            id: str = decoded.get("user_id")
            token_data = TokenData(id=id)
        else:
            raise credentials_execption
        
        
    except JWTError as e:
        print(e)
        raise credentials_execption
    return token_data

def get_currentuser(token:str = Depends(auth_scheme),db: Session = Depends(database.get_db)):
    credentials_execption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Not authenticated",
                                    headers={"www-Athenticate":"Bearer"})
    token = verify_accesstoken(token=token,credentials_execption=credentials_execption)
    user = db.query(models.Users).filter(models.Users.id == token.id).first()

    return user

