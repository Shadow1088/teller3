

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
        if a == 'q':
            running = False
        answers = get_answers(q[0][0])
        answers_text = [answer[1] for answer in answers]
        if compare_1N(a, answers_text):
            print("Great! You got it!")
        else:
            print(f"That is not right.. The two best answers were: '{answers_text[0]}' and '{answers_text[1]}'")
    while mode == "ask":
        q = input("What is your question?: ")
        q_intent = [word.lower() for word in q.split(" ") if word.lower() in ('when', 'how', 'why', 'what', 'should', 'where', 'who')]
        if q_intent != []:
            same_intent_questions = [question for question in get_q() if question[2]==q_intent[0]]
            if same_intent_questions != []:
                sims = compare_1N(q, [q[1] for q in same_intent_questions])
                if sims:
                    question = same_intent_questions[sims.index(max(sims))]
                    print(question)
                    answers = get_answers(question[0])
                    if len(answers)>1:
                        print(f"The two best answers I can think of are: '{answers[0]}' and '{answers[1]}'")
                        continue
                    print(f"Best answer I can think if is: {answers[0]}")
                    continue
        print("I dont know that!")
        answer_text = input("What is the answer?: ")
        if q_intent==[]:q_intent[0]=""
        if len(answer_text)>10<50:
            insert_q(q, "en", q_intent[0])
            insert_a(get_qid(q), answer_text, user[1])
        answer_notes = input("Wanna add some additional informations to that?")
        if len(answer_notes)>10:
            insert_a_note(get_aid(get_qid(q), user[1]), answer_notes)