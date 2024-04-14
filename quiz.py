# dummy quiz app
# use ApiClient later
import requests
import json
import random
import time
import os


class ApiClient:
    def __init__(self, uri):
        print("Do you have an account?")
        has_acc = input("Enter 'yes' or 'no': ").lower().strip() == "yes"
        self.uri = uri
        self.username = input("Your username: ")
        self.password = input("Your password: ")
        r = requests.post(
            self.route("/login" if has_acc else "/register"),
            json={"username": self.username, "password": self.password},
        )

        status = r.status_code
        res = r.json()
        if status != 200:
            print("Error:", res["message"])
            exit(1)
        print(res)
        self.token = res["token"]

    def route(self, route):
        return self.uri + "/api" + route

    def api(self, verb, route, body=None):
        if verb == "POST":
            res = requests.post(
                self.route(route),
                headers={"Authorization": "Bearer " + self.token},
                json=body,
            )
        else:
            res = requests.get(
                self.route(route), headers={"Authorization": "Bearer " + self.token}
            )

        return (res.status_code, json.loads(res.text))


print("Connecting...")
time.sleep(0.3 + random.random())

# todo use ApiClient and print the actual address. This code is just to get a feel for what the quiz interface might be like ...
print("Connected to university.example/")
name = input("Your username? ")
print(f"Welcome, {name}!")
time.sleep(random.random())

print("Your available quizzes:")

quizzes = json.loads(
    open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "quizzes.json")
    ).read()
)

for idx, itm in enumerate(quizzes):
    print(idx, itm["name"])

sel = -1
while sel == -1:
    try:
        inp = input("Attempt a quiz now [Number/quit]? ")
        if inp == "quit":
            exit(1)
        sel = int(inp)
        if sel >= len(quizzes) or sel < 0:
            sel = -1
    except ValueError:
        print("Numerics only!")


def present_and_score_question(question):
    print(f"Q. {question['body']}\n")

    alph = list("abcd")
    for i in range(4):
        print(f"\t{alph[i]}. {question['options'][i]}")

    print()
    ans = ""
    while ans.lower() not in alph:
        ans = input("Your answer? ")

    if ans.lower() == question["answer"].lower():
        return 1
    return 0


print(f"Starting quiz \"{quizzes[sel]['name']}\"")

score = 0
quiz = quizzes[sel]["questions"]
total = len(quiz)
for question in quiz:
    score += present_and_score_question(question)

perc = score / total * 100

remark = "Excellent work!"
if 0 <= perc <= 40:
    remark = "Oops. Better luck next time!"
elif 41 <= perc <= 70:
    remark = "Good work."


print(f"You scored {score}/{total}. {remark}")
