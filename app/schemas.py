from datetime import  datetime
from typing import  Optional
from pydantic import BaseModel,EmailStr



# receving model 


class CreateUsers(BaseModel):
    email : EmailStr
    password : str
    con_pass: str
    username : str


class CreateAdmin(BaseModel):
    email: EmailStr
    password: str
    conf_pass: str
    otp : int

class Washes(BaseModel):
    type : str 
    description : str
    price : float
    req : float

class updatewash_time(BaseModel):
    before: int = 2
    after : int = 2

class Reset_password(BaseModel):
    email : EmailStr

class Bookwashes(BaseModel):
    type : int
    start_time : datetime
    end_time : datetime

class Time(BaseModel):
    t1 = datetime
    t2 = datetime

class Verifyotp(BaseModel):
    otp : int
    email : EmailStr

class Password_otp(BaseModel):
    otp : int
    email: EmailStr
    new_password : str

class status_update(BaseModel):
    id : int
    status : bool


class Custom_booking_query(BaseModel):
    start_time : datetime
    end_time : datetime

class Custom_booking_time(BaseModel):
    time : datetime

class Office_time(BaseModel):
    start : int = 9
    end : int = 18

class Deleteuser_otp(BaseModel):
    email : EmailStr
    otp : int

class Deleteuser_email(BaseModel):
    email : EmailStr


#RESPONSE MODEL


class Userresponse(BaseModel):
    id : int
    email : EmailStr
    username : str


    class Config:
        orm_mode = True

class Adminresponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class Addwash_Response(BaseModel):
    id : int
    type: str
    description: str
    price: int
    time_req : int

    class Config:
        orm_mode = True


class AddwashError(BaseModel):
    NOTE: str = "An Error Occured, Not Added"

class EmailExist(BaseModel):
    NOTE : str = "Email Already Exsists"

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    id : Optional[str] = None


class Updatewash_Response(BaseModel):
    id: int
    type: str
    description: str
    price: int

    class Config:
        orm_mode = True


class WashesBy_id(BaseModel):
    type : str
    description: str
    price: int
    created_at : datetime

    class Config:
        orm_mode = True


class Allwashes(BaseModel):
    id : int
    type: str
    description: str
    price: int

    class Config:
        orm_mode =  True


    class Config:
        orm_mode = True



