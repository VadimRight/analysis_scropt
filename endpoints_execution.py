import requests
import json
import os


with open("./jsons/test_user.json") as test_user_file:
    test_user_data = json.load(test_user_file)

url = "http://localhost:8000"
file_path='./Screen.png'


user_registration = requests.post(f"{url}/register", json=test_user_data)


token_response = requests.post(
    f"{url}/token", 
    data={"username": "test", "password": "test", "grant_type": "password"}, 
    headers={"content-type": "application/x-www-form-urlencoded"}
)
token_json = token_response.json()
token = token_json["access_token"]  


headers = {"Authorization": f"Bearer {token}"}


requests.get(f"{url}/profile", headers=headers)


f = open(file_path, 'rb')


create_post = requests.post(f"{url}/new_post", headers=headers, params={'text': 'test', 'name': 'test'}, files={'image': (os.path.basename(file_path), f, 'multipart/form-data')}).json()
post_id=create_post[0]["id"]

requests.delete(f"{url}/profile/posts={post_id}", headers=headers, params={"id":f"{post_id}"})
requests.delete(f"{url}/profile/delete_user", json={"username": "test"}, headers=headers)


f.close()
