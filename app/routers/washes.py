from datetime import datetime, timedelta
from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db
from typing import List
from sqlalchemy.orm import Session
from .. import models, utils, oauth2, schemas
from ..config import setting
from ..utils import verify

router = APIRouter(tags=["Booking"])



@router.get('/washesbyid/{id}', response_model=schemas.WashesBy_id)
def Washesby_Id(id: int, db: Session = Depends(get_db)):

    wash = db.query(models.Washes).filter(models.Washes.id == id).first()
    if not wash:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Wash in this id : {id}")
    return wash


@router.get("/getallwash", response_model=List[schemas.Allwashes])
def Get_Allwashes(db: Session = Depends(get_db)):

    wash = db.query(models.Washes).all()
    return wash

@router.post("/bookwashes")
def Book_Washes(parms : schemas.Bookwashes, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_currentuser)):
    

    if current_user.id == None:
        return "Access token expired"

    # Queries
    query = db.query(models.Washes).filter(models.Washes.id == parms.type).first()
 
    typ = db.execute(
        f"""SELECT "type" FROM washes WHERE id = {parms.type} """).first()

    username = db.execute(
        f"""SELECT "username" FROM users WHERE id = {current_user.id} """).first()

    if username == None or not username:
        return "Provide Auth token"
    
    u = dict(username)
    user = u["username"]


    # conditions
    if not query:
        return f"No wash with this Id :  {parms.type}"
    if not typ:
        return f"No type  with this id : {parms.type}"
    else:
        d = dict(typ)
        v = d["type"]

    officetime = utils.sort_working_time(parms.start_time)

    if not officetime:
        return "Booking accepted in office time only"
    
    booking_accepttime = utils.booking_accept_after(parms.start_time)
    past_cancel = utils.pasttime_cancel(parms.start_time)

    if booking_accepttime or past_cancel:
        return "Bookig Accepted only 2 days before"
    
    # Start Time

    s_time = utils.format_date(parms.start_time)
    e_time = utils.format_date(parms.end_time)

    

    if query:
        add_wash = models.BookWashes(wash_id=parms.type,user_id=current_user.id,
                                     start_time=s_time, type=v, end_time=e_time, user_name=user)
        db.add(add_wash)
        db.commit()
        db.refresh(add_wash)

        return "Booked Successfully!"    
    return f"This Time slot is not Available"
    

@router.get("/getslots/{id}",status_code=status.HTTP_200_OK)
def Get_slots(id : int , db: Session = Depends(get_db)):
    
    # Queries
    query = db.query(models.Washes).filter(
        models.Washes.id == id).first()
    tim_req = db.execute(
        f"""SELECT "time_req" FROM washes WHERE id = {id} """).first()

    # Conditions
    if not query:
        return f"No wash with this Id :  {id}"
    t = tim_req['time_req']

    # Time Calculation
    current_time = datetime.now()
    current_time = utils.format_date(current_time)
    start_current_time = datetime.now() #- timedelta(hours=4)
    query_time = datetime.now() + timedelta(days=2)
    future_time = utils.format_date(query_time)

    # Getting the slots
    q =  db.execute(f""" SELECT start_time,end_time FROM bookwashes WHERE start_time >= '{start_current_time}' AND end_time <= '{future_time}' """).all()
    #Parameters for get slots
    hours = start_current_time,query_time
    d = t

    available_slots = utils.get_slots(hours=hours,appointments=q,duration=d)
    return available_slots


@router.post("/washstatusupdate", status_code=status.HTTP_200_OK)
def status_update(status : schemas.status_update, db: Session = Depends(get_db)):

    query_mail = db.execute(
        f"""SELECT "password" FROM admin WHERE email  = '{setting.ADMIN_MAIL}' """).first()

    if query_mail == None:
        return "Contact Admin to access this Endpoint"

    query = dict(query_mail)
    q = query['password']

    if not verify(status.password, q):
        return "Invalid Password"

    data = db.query(models.BookWashes).filter(
        models.BookWashes.id == status.id).first()
    if data == None:
        return "No Booking Available in this id"
    data.completed = status.status
    db.commit()
    return "Status updated successfully"

@router.post("/currentbooking", status_code=status.HTTP_200_OK)
def current_booking(time_ : schemas.Custom_booking_time  ,db : Session = Depends(get_db) ,current_user: int = Depends(oauth2.get_currentuser) ):

    notification = db.execute(
        f"""SELECT type,start_time,end_time,completed FROM bookwashes WHERE created_at >= '{time_.time}'AND  user_id =  {current_user.id} """).all()
    return notification

@router.get("/allbookedwashes/{password}",status_code=status.HTTP_200_OK,)
def allbookwashes(password: str, db: Session = Depends(get_db)):

    query_mail = db.execute(
        f"""SELECT "password" FROM admin WHERE email  = '{setting.ADMIN_MAIL}' """).first()

    if query_mail == None:
        return "Contact Admin to access this Endpoint"

    query = dict(query_mail)
    q = query['password']

    if not verify(password, q):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Password : {password} ")
    wash = db.query(models.BookWashes).all()
    return wash
    