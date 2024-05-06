import requests as requests
import time
import json


with open("./jsons/test_user.json") as test_user_file:
    test_user_data = json.load(test_user_file)
with open("./jsons/auth_test.json") as test_auth_file:
    test_auth_data = json.load(test_auth_file)



user_regitstration = requests.post("http://localhost:8000/register", json = test_user_data)
time.sleep(500/1000)
token_auth = requests.post("http://localhost:8000/token", data={"username": "test", "password": "test", "grant_type": "password"}, headers={"content-type": "application/x-www-form-urlencoded"})
requests.delete("http://localhost:8000/profile/delete_user", json={"username": "test"})
