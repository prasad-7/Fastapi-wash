from datetime import datetime, timedelta
from passlib.context import CryptContext
from datetime import datetime 
from .config import setting


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
format_data = "%d/%m/%y %H:%M"
days_accept = setting.DAYS_ACCEPTED
start_working_time = setting.OFFICE_START
end_working_time = setting.OFFICE_END - 1

def hashing(password: str):
    return pwd_context.hash(password)

def verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def start_end(time,hours):
    req = time + timedelta(hours=hours)
    return req

def string_to_datetime(time):
    d = datetime.strptime(time,"%Y-%m-%d %H:%M:%S.%f")
    return d

def format_date(time):
    a = datetime.strftime(time, format_data)
    st = datetime.strptime(a, format_data)
    return st

def booking_accept_after(time):
    if time > datetime.now() + timedelta(days=days_accept):
        return True

def sort_working_time(time):
    now = datetime.now()
    sunrise = datetime(now.year, now.month, now.day, hour=start_working_time, minute=0)
    sunset = datetime(now.year, now.month, now.day, hour=end_working_time, minute=0)
    if time.hour >= sunrise.hour and time.hour <= sunset.hour:
        return True
    

def pasttime_cancel(time):
    if time < datetime.now():
        return True


def get_slots(hours, appointments, duration):

    available_slot = []
    current_available_slot =[]
    list_of_slot =[]
    odd =[]
    even =[]
    working_slots = []


    slots = sorted([(hours[0], hours[0])] +
                   appointments + [(hours[1], hours[1])])
    for start, end in ((slots[i][1], slots[i + 1][0]) for i in range(len(slots) - 1)):
        assert start <= end,  "Cannot attend all appointments"
        while start + timedelta(hours=duration) <= end:
            #start += timedelta(hours=duration)
            #print(start, start + timedelta(hours=duration))
            available_slot.append((start, start + timedelta(hours=duration)))
            start += timedelta(hours=duration)
    
    for i in available_slot:
        for j in i:
            if j >= datetime.now():
                current_available_slot.append(j)

    if current_available_slot[0] == current_available_slot[1]:
        current_available_slot.pop(0)

    for i in range(0,len(current_available_slot)):
        if i % 2:
            even.append(current_available_slot[i])
        else:
            odd.append(current_available_slot[i])
    
    
    for i,j in zip(odd,even):
        list_of_slot.append([i,j])

    for i in list_of_slot:
        if sort_working_time(i[0]):
            working_slots.append(i)

    
    return working_slots




