

from settings import *
from app_funcs import *
from db_funcs import *


user = []

def introduction():
    global user
    if (input("Do you already have an account? If so, press [Enter]")) != '': create_user()
    user = login_user()

introduction()
print(f"Ahoj {user[0]}, ja jsem deda vseveda.")

mode = get_mode(modes)

print(f"Vybral jsi: {mode}\n")

if mode != "":
    running = True


while running:
    while mode == "test":
        q = random_entry("questions") # question tuple
        if q==[]:
            continue
        a = input(str(q[0][1]) + ": ") # answer
        answers = get_answers(q[0][0])
        answers_text = [answer[1] for answer in answers]
        print(*answers_text)
        