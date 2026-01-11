from sentence_transformers import SentenceTransformer, util
from time import time
from bcrypt import gensalt, hashpw, checkpw
import base64

from db_funcs import *
from settings import *

#model = SentenceTransformer(model_name)

def func_timer(base_fn):
    def enhanced_fn():
        start = time()
        base_fn()
        end = time()
        print(f"{base_fn.__name__} took {end-start} seconds.")
    return enhanced_fn

#@func_timer
def create_user():
    try:
        valid_username = False
        username = ""
        while not valid_username:
            username = input("Create an username: ")
            if username not in getall_usernames():
                valid_username = True
        pswd = input("Create your password: ")
        password_verified = False
        while not password_verified:
            if input("Re-type your password: ") == pswd:
                password_verified = True
        bytes = pswd.encode('utf-8')
        salt = gensalt()
        hash = hashpw(bytes, salt)
        insert_user(username, (base64.b64encode(hash)).decode("ascii"))
        return True
    except Exception as e:
        print(e)
        return False

def login_user():
    username = input("Input your username: ")
    hash_bytes = base64.b64decode(get_hash(username).encode("ascii"))
    
    while 1:
        pswd = input("Input your password: ")
        bytes = pswd.encode('ascii')
        if checkpw(bytes, hash_bytes):
            print("logged in")
            break

    return [username, get_uid(username)]

def get_mode(modes:list):
    mode = ""
    while 1:
        mode = input(f"Prosim, vyber jeden z modu:  {[mode for mode in modes]}: ")
        if mode in modes:
            break
    return mode


#login_user()
#print(create_user())


