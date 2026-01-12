from sentence_transformers import SentenceTransformer, util
from time import time
from bcrypt import gensalt, hashpw, checkpw
import base64
from random import randrange

from db_funcs import *
from settings import *

model = SentenceTransformer(model_name)

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

def get_mode(modes:list) -> str:
    mode = ""
    while 1:
        mode = input(f"Prosim, vyber jeden z modu:  {[mode for mode in modes]}: ")
        if mode in modes:
            break
    return mode

def compare_1N(sentence:str, other:list[str]):
    if not other:
        return False
    embedding = model.encode(sentence, convert_to_tensor=True)
    embeddings = model.encode(other, convert_to_tensor=True)
    cosine_scores = util.cos_sim(embedding, embeddings)
    cos_list = cosine_scores.tolist()[0]
    return cos_list

def show_q_a() -> tuple[list, list]:
    question = get_q()[randrange(0,len(get_q()))]
    answers = get_answers(question[0])
    return (question, answers)

def vote_q_a(user_id:int, qa:tuple): #-> bool:
    try:
        print(f"QUESTION: {qa[0][1]}")
        a = qa[1][randrange(0, len(qa))]
        print(f"ANSWER: {a[1]}")
        v = input("Upvote or Downvote? (U/d), (1/0), ([ENTER]/[SPACE][ENTER])")
        if v.lower() == 'q':
            return
        if v.lower() in ("upvote", "u", "1", ""):
            v = "upvote" 
        else: v = "downvote"
        insert_a_vote(a[0], user_id, v)
        return v
    except Exception as e:
        return e
