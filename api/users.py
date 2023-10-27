import sqlite3
import contextlib
import logging


from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from .database_query import *
from .models import *
from .utils import *

current_index = 0
 
USERS_PRIMARY_DB_URL = "./api/var/primary/fuse/users.db"
USERS_SECONDARY_DB_URLS = ["./api/var/secondary-1/fuse/users.db", "./api/var/secondary-2/fuse/users.db"]

class Settings(BaseSettings, env_file=".env", extra="ignore"):
    database: str
    logging_config: str

def get_logger():
    return logging.getLogger(__name__)

def get_primary_db(logger: logging.Logger = Depends(get_logger)):
    with contextlib.closing(sqlite3.connect(USERS_PRIMARY_DB_URL, check_same_thread = False)) as db:
        db.row_factory = sqlite3.Row
        db.isolation_level = None
        db.set_trace_callback(logger.debug)
        yield db

def get_secondary_db(logger: logging.Logger = Depends(get_logger)):
    global current_index
    with contextlib.closing(sqlite3.connect(USERS_SECONDARY_DB_URLS[current_index], check_same_thread = False)) as db:
        db.row_factory = sqlite3.Row
        db.isolation_level = None
        db.set_trace_callback(logger.debug)
        yield db
    current_index = (current_index + 1) % len(USERS_SECONDARY_DB_URLS)

settings = Settings()
app = FastAPI()

logging.config.fileConfig(settings.logging_config, disable_existing_loggers = False)
    

##########   USERS ENDPOINTS        ######################
@app.post(path='/users/create', operation_id='create_user', response_model = CreateUserResponse)
async def create_user(user_info: CreateUserRequest, users_connection = Depends(get_primary_db)):
    # check if username is available
    if username_exists(users_connection, user_info.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'username="{user_info.username}" already exist!')

    # check if valid role
    if not user_info.role in ['instructor', 'registrar', 'student']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"role={user_info.role} is not valid!")

    # hash the password before adding it to database
    hashed_password = hash_password(user_info.password)
    user_info.password = hashed_password

    # create entry in users table
    response = add_user(users_connection, user_info)

    if response == QueryStatus.SUCCESS:
        return CreateUserResponse(message="user added successfully")
    
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="some error occurred in database")


@app.get(path="/users/authenticate", operation_id="authenticate_user")
async def authenticate_user(username: str, password: str, users_connection = Depends(get_secondary_db)):
    # check if username exists
    if not username_exists(users_connection, username):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"username or password is invalid!")
    
    # check if password is correct
    user = get_user(users_connection, username)
    password_hash = user[5] # based on users schema
    if not verify_password(password, password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"username or password is invalid!")
    
    userid = user[0]
    role = user[6]
    jwt_claims = generate_claims(username, userid, role)
    return JSONResponse(status_code=status.HTTP_200_OK, content=jwt_claims)

