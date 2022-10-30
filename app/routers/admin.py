from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db
from typing import Union
from sqlalchemy.orm import Session
from .. import models, utils, oauth2, schemas,utils
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .auth import send_otp
from ..config import setting

router = APIRouter(tags=["Admin"])


@router.post("/createadmin", status_code=status.HTTP_201_CREATED)
def Create_Admin(user: schemas.CreateAdmin, db: Session = Depends(get_db)):

    admin_email = setting.ADMIN_MAIL

    admin = db.query(models.Admin).filter(models.Admin.email == user.email).first()
    if admin:
        return {"Admin Already Exists!"}

    # hashing the password.
    hashed_password = utils.hashing(user.password)
    user.password = hashed_password
    try:
        s = send_otp(admin_email)
        data = db.query(models.Admin).filter(
            models.Admin.email == admin_email).first()

        if data:
            data.otp = s
            db.commit()
            new_admin = models.Admin(**user.dict())
            db.add(new_admin)
            db.commit()
            db.refresh(new_admin)
            return "Otp send successfully"
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"An error occured")


@router.post("/createadmin/verifyotp", status_code=status.HTTP_201_CREATED)
def VerifyusersOtp(parms: schemas.Verifyotp, db: Session = Depends(get_db)):

    admin_email = setting.ADMIN_MAIL

    mail = db.query(models.Admin).filter(
        models.Admin.email == parms.email).first()

    if mail == None:
        return "Enter Your Email Correctly"

    query_mail = db.execute(
        f"""SELECT "otp" FROM admin WHERE email  = '{admin_email}' """).first()
    
    if query_mail == None:
        return "Enter Your Email Correctly"
    
    if query_mail["otp"] == parms.otp:

        data = db.query(models.Admin).filter(
            models.Admin.email == admin_email).first()
    
        if data:
            data.otp = None
            db.commit()
            return {"Registered Successfully!"}
        return "An error Occured!"
    
    db.execute(f""" DELETE FROM admin WHERE "email" = '{parms.email}' """)
    data = db.query(models.Admin).filter(
        models.Admin.email == admin_email).first()
    data.otp = None
    db.commit()
    print("Account deleted successfully!")
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


@router.post('/addwashes', status_code=status.HTTP_201_CREATED, response_model=Union[schemas.Addwash_Response, schemas.AddwashError])
def Add_Washes(wash: schemas.Washes, db: Session = Depends(get_db)):
    try:
        wash = models.Washes(type=wash.type,description=wash.description,price=wash.price,time_req=wash.req)
        db.add(wash)
        db.commit()
        db.refresh(wash)
        return wash
    except:
        return wash


@router.put('/updatewashes/{id}', status_code=status.HTTP_201_CREATED, response_model=schemas.Updatewash_Response)
def Update_Washes(id:int , wash: schemas.Washes, db: Session = Depends(get_db)):

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
            return data
    except:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED, detail=f"An Error Occured, Not Added")


@router.get("/getallbooking", status_code=status.HTTP_200_OK)
def booking(db: Session = Depends(get_db)):
    current_booking = db.query(models.BookWashes).all()
    return current_booking

@router.post("/bookingcustomizetime", status_code=status.HTTP_200_OK)
def custom_time(parms : schemas.Custom_booking_query ,db: Session = Depends(get_db)):
    query = db.execute(
        f""" SELECT id,type,completed,created_at FROM bookwashes WHERE created_at >= '{parms.start_time}' AND created_at <= '{parms.end_time}' """).all()
    if query == None:
        return "An error Occured"
    return query