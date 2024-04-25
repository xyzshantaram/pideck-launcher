import requests
import json


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
