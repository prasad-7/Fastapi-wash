
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .routers import users,auth,admin,washes
from .config import setting
from . import models
from .database import engine




# creating the instance
app = FastAPI(title="Mr Api", version="0.1.0",)
models.Base.metadata.create_all(bind=engine)



# cors middleware
origins =['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# connecting to the database

while True:
    try:
        conn = psycopg2.connect(host=setting.HOST,database=setting.DATABASE,user=setting.USER,
                                password=setting.PASSWORD, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("database connection was successful!!")
        break
    except Exception as error:
        print("Connection to the database was fail ", error)
        time.sleep(4)


# welcome 

@app.get("/")
def welcome():
    return "Welcome, you have connected to this  Api Endpoint"


#   Routers


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(washes.router)
