import sqlite3

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

from .database_query import *
from .models import *
from .utils import *

app = FastAPI()

USERS_DB_URL = "./api/var/primary/fuse/users.db"

users_connection = sqlite3.connect(USERS_DB_URL)
users_connection.isolation_level = None

@app.on_event("shutdown")
async def shutdown():
    users_connection.close()

@app.get(path='/db_liveness', operation_id='check_db_health')
async def check_db_health():
    try:
        users_connection.cursor()
        return JSONResponse(content= {'status': 'ok'}, status_code = status.HTTP_200_OK)
    except Exception as ex:
        return JSONResponse(content= {'status': 'not connected'}, status_code = status.HTTP_503_SERVICE_UNAVAILABLE)
    

##########   USERS ENDPOINTS        ######################
@app.post(path='/users/create', operation_id='create_user', response_model = CreateUserResponse)
async def create_user(user_info: CreateUserRequest):
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
async def authenticate_user(username: str, password: str):
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

