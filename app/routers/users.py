from .. import models, schemas
from fastapi import APIRouter, status, HTTPException, Depends
from ..database import get_db
from sqlalchemy.orm import Session
from ..utils import hashing,verify
from ..oauth2 import create_accesstoken
from .auth import send_otp
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..config import setting
from ..utils import verify,validate_email


router = APIRouter(
    tags=["USERS"]
)


@router.post('/createuser', status_code=status.HTTP_202_ACCEPTED,)
def Create_user(user: schemas.CreateUsers , db: Session = Depends(get_db)):

    validate = validate_email(user.email)
    if not validate:
        return "Email is not valid"


    if not user.password == user.con_pass:
        return "Password not match"
    
    
    phone_no = user.phn_number
    username = user.username
    email = user.email
    password = user.password
    users = db.query(models.Users).filter(models.Users.email == email).first()
    if users:
        return {"Email Exsists!"}
    else:
        s = send_otp(email)
        hashed_password = hashing(password)
        new_user = models.Users(
            email=email, password=hashed_password, username=username, otp=s, phone_number=phone_no)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return "Otp Sent Successfully" 
        

@router.post("/createusers/verifyotp", status_code=status.HTTP_201_CREATED)
def VerifyusersOtp(parms : schemas.Verifyotp, db: Session = Depends(get_db)):
    query_mail = db.execute(
        f"""SELECT "otp" FROM users WHERE email  = '{parms.email}' """).first()
    if  query_mail == None:
        return "Enter Your Email Correctly "
    if query_mail["otp"] == parms.otp:
        data = db.query(models.Users).filter(models.Users.email == parms.email).first()
        if data:
            data.otp = None
            db.commit()
            return {"Registered Successfully!"}
        return "An error Occured!"
    db.execute(f""" DELETE FROM users WHERE "email" = '{parms.email}' """)
    db.commit()
    print("Account deleted successfully!")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"Wrong Otp {parms.otp}")
    
    
@router.post('/login')
def Login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user_login = db.query(models.Users).filter(
        models.Users.email == user_credentials.username).first()
    if not user_login:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if not verify(user_credentials.password, user_login.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    # create token
    access_token = create_accesstoken(data={"user_id": user_login.id})

    return {"Access_token": access_token}



"""@router.get("/users/{id}", response_model=schemas.Userresponse)
def Get_User(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id: {id} does not exists.")
    return user"""



@router.post("/user/resetpassword")
def Reset_Password(email : schemas.Reset_password,db : Session = Depends(get_db)):

    user = db.query(models.Users).filter(models.Users.email == email.email).first()
    if not user == None:
        s = send_otp(email.email)
        user.otp = s
        db.commit()
        return "OTP sent Successfully!"
    else:
        return "No user with this Email"


@router.post("/user/resetpassword/otp")
def Reset_Password_Otp(parms : schemas.Password_otp, db: Session = Depends(get_db)):
    # query
    user = db.query(models.Users).filter(
        models.Users.email == parms.email).first()
    query_mail = db.execute(
        f"""SELECT "otp" FROM users WHERE email  = '{parms.email}' """).first()
    if user == None:
        return "No User with this Email"
    if query_mail["otp"] == parms.otp:
        user.password = None
        user.otp = None
        user.password = hashing(parms.new_password)
        db.commit()
        return "Password Reset Success"
    else:
        user.otp = None
        db.commit()
        return "Wrong Otp, Try again!"      

@router.post("/deleteuser",status_code=status.HTTP_200_OK)
def delete_user(email : schemas.Deleteuser_email,db : Session = Depends(get_db)): 
    user = db.query(models.Users).filter(models.Users.email == email.email).first()
    if user: 
        s = send_otp(email.email)
        user.otp = s
        db.commit()
        return "Otp send successfully"
    return "Email not exists"

@router.delete("/deleteuser/verifyotp",status_code=status.HTTP_202_ACCEPTED)
def deleteuser_verifyotp(parms : schemas.Deleteuser_otp,db : Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == parms.email).first()

    if user:
        query_mail = db.execute(
            f"""SELECT "otp" FROM users WHERE email  = '{parms.email}' """).first()
        if query_mail["otp"] == parms.otp:
            db.query(models.Users).filter(
                models.Users.email == parms.email).delete()
            db.commit()
            return "Account deleted successfully"
        user.otp = None
        db.commit()
        return "wrong otp"
    return "Email not exists"


@router.get("/getallusers/{password}",status_code=status.HTTP_202_ACCEPTED)
def getall_users(password: str,db: Session = Depends(get_db)):

    query_mail = db.execute(
        f"""SELECT "password" FROM admin WHERE email  = '{setting.ADMIN_MAIL}' """).first()


    if query_mail == None:
        return "Contact Admin to access this Endpoint"


    query = dict(query_mail)
    q = query['password']
    
    
    if not verify(password, q):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Password : {password} ")

    user = db.query(models.Users).all()
    for i in user:
        #print(i.id,i.email,i.phone_number)
        return {
        "id" : i.id,
        "email" : i.email,
        "username" : i.username,
        "phone_number" : i.phone_number
        
    }
    
