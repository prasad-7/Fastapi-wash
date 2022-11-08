from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db
from typing import Union
from sqlalchemy.orm import Session
from .. import models, utils, oauth2, schemas,utils
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .auth import send_otp
from ..config import setting
from ..utils import hashing,verify

router = APIRouter(tags=["Admin"])


# utils variables


@router.get("/createadmin", status_code=status.HTTP_201_CREATED)
def Create_Admin(db: Session = Depends(get_db)):

    admin_email = setting.ADMIN_MAIL
    
    s = send_otp(admin_email)

    if s:
        admin = models.Admin(email=admin_email,otp=s)
        db.add(admin)
        db.commit()
        return "Otp send successfully!"
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"An error occured")

   


@router.post("/createadmin/verifyotp", status_code=status.HTTP_201_CREATED)
def VerifyusersOtp(parms: schemas.CreateAdmin, db: Session = Depends(get_db)):

    admin_email = setting.ADMIN_MAIL

    mail = db.query(models.Admin).filter(
        models.Admin.email == parms.email).first()

    if mail == None:
        db.execute(f""" DELETE FROM admin WHERE "email" = '{admin_email}' """)
        db.commit()
        return "Enter Your Email Correctly"

    query_mail = db.execute(
        f"""SELECT "otp" FROM admin WHERE email  = '{parms.email}' """).first()
    
    if query_mail == None:
        return "Enter Your Email Correctly"

    if not parms.password == parms.conf_pass:
        db.execute(f""" DELETE FROM admin WHERE "email" = '{parms.email}' """)
        db.commit()
        return "Password not Match"
    
    if query_mail["otp"] == parms.otp:
        hashed_password = hashing(parms.password)
        mail.password = hashed_password
        mail.otp = None
        db.commit()
        return "Registered Successfully!"
    
    db.execute(f""" DELETE FROM admin WHERE "email" = '{parms.email}' """)
    db.commit()
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"Wrong Otp {parms.otp}")


@router.post('/adminlogin')
def AdminLogin(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user_login = db.query(models.Admin).filter(
        models.Admin.email == user_credentials.username).first()
    if not user_login:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user_login.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    # create token
    access_token = oauth2.create_accesstoken(data={"user_id": user_login.id})

    return {"Access_token": access_token}


@router.post('/addwashes', status_code=status.HTTP_201_CREATED)
def Add_Washes(wash: schemas.Washes, db: Session = Depends(get_db)):

    query_mail = db.execute(
        f"""SELECT "password" FROM admin WHERE email  = '{setting.ADMIN_MAIL}' """).first()

    if query_mail == None:
        return "Contact Admin to access this Endpoint"

    query = dict(query_mail)
    q = query['password']

    if not verify(wash.password, q):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Password : {wash.password} ")
    try:
        wash = models.Washes(type=wash.type,description=wash.description,price=wash.price,time_req=wash.req)
        db.add(wash)
        db.commit()
        db.refresh(wash)
        return wash
    except:
        return wash


@router.put('/updatewashes/{id}', status_code=status.HTTP_201_CREATED)
def Update_Washes(id:int , wash: schemas.Washes, db: Session = Depends(get_db)):

    query_mail = db.execute(
        f"""SELECT "password" FROM admin WHERE email  = '{setting.ADMIN_MAIL}' """).first()

    
    if query_mail == None:
        return "Contact Admin to access this Endpoint"

    query = dict(query_mail)
    q = query['password']

    if not verify(wash.password, q):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Password : {wash.password} ")

    #Query
    data = db.query(models.Washes).filter(models.Washes.id == id).first()
    if data == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Wash with id : {id} Not found")

    try:
        if data:
            data.type = wash.type
            data.description = wash.description
            data.price = wash.price
            data.time_req = wash.req
            db.commit()
            #return data.type,data.description,data.price
            return {
                "type" : data.type,
                "description" : data.description,
                "price":data.price,
                "required_time": data.time_req
            }

            
    
    except:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED, detail=f"An Error Occured, Not Added")


@router.get("/getallbooking/{password}", status_code=status.HTTP_200_OK)
def booking(password: str, db: Session = Depends(get_db)):

    query_mail = db.execute(
        f"""SELECT "password" FROM admin WHERE email  = '{setting.ADMIN_MAIL}' """).first()

    print(query_mail)

    if query_mail == None:
        return "Contact Admin to access this Endpoint"

    query = dict(query_mail)
    q = query['password']

    if not verify(password, q):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Password : {password} ")

    current_booking = db.query(models.BookWashes).all()
    return current_booking

@router.post("/customerbooking", status_code=status.HTTP_200_OK)
def custom_time(parms : schemas.Custom_booking_query ,db: Session = Depends(get_db)):

    query_mail = db.execute(
        f"""SELECT "password" FROM admin WHERE email  = '{setting.ADMIN_MAIL}' """).first()

    if query_mail == None:
        return "Contact Admin to access this Endpoint"

    query = dict(query_mail)
    q = query['password']

    if not verify(parms.password, q):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Password : {parms.password} ")
    query = db.execute(
        f""" SELECT id,type,completed,created_at FROM bookwashes WHERE created_at >= '{parms.start_time}' AND created_at <= '{parms.end_time}' """).all()
    if query == None:
        return "An error Occured"
    return query

