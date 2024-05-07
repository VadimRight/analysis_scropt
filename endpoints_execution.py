import requests
import json
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

url = "http://localhost:8000"
path_to_data_file = "./local_machine_res/data.txt"
mode = int(input("If you want to send requests to server on your local machine print 0, if in docker print 1: "))
if mode == 1:
    url = "http://localhost:8001"
    path_to_data_file = "./docker_res/data.txt"
    logging.info(f"Mode set to Docker, using URL {url} and data path {path_to_data_file}")
else:
    logging.info(f"Mode set to Local, using URL {url} and data path {path_to_data_file}")

for i in range(4):
    with open("./jsons/test_user.json") as test_user_file:
        test_user_data = json.load(test_user_file)
    logging.info("Loaded user test data")

    file_path = './Screen.png'
    payload = {'text': 'test', 'name': 'test'}

    user_registration = requests.post(f"{url}/register", json=test_user_data)
    logging.info(f"User registration status: {user_registration.status_code}")

    token_response = requests.post(
        f"{url}/token", 
        data={"username": "test", "password": "test", "grant_type": "password"}, 
        headers={"content-type": "application/x-www-form-urlencoded"}
    )
    token_json = token_response.json()
    token = token_json.get("access_token")
    logging.info(f"Token received: {token}")

    headers = {"Authorization": f"Bearer {token}"}

    current_user = requests.get(f"{url}/profile", headers=headers).json()
    username = current_user[0]["username"]
    logging.info(f"Current username: {username}")

    with open(file_path, 'rb') as f:
        files = {'image': (os.path.basename(file_path), f, 'multipart/form-data')}
        create_post = requests.post(f"{url}/new_post", headers=headers, params=payload, files=files).json()
        post_id = create_post[0]["id"]
        logging.info(f"Post created with ID: {post_id}")

        # Ensure each critical operation logs both its action and outcome
    response = requests.get(f"{url}/profile", headers=headers)
    logging.info(f"Profile accessed: {response.status_code}")

    response = requests.get(f"{url}/users/{username}", headers=headers, params={"username": f"{username}"})
    logging.info(f"User data retrieved: {response.status_code}")

    response = requests.patch(f"{url}/profile/posts={post_id}/edit_name", headers=headers, params={"name": "test"})
    logging.info(f"Post name edited: {response.status_code}")

    with open(file_path, 'rb') as f:
        files = {'image': (os.path.basename(file_path), f, 'multipart/form-data')}
        response = requests.patch(f"{url}/profile/posts={post_id}/edit_image", headers=headers, params={"id": f"{post_id}"}, files=files)
        logging.info(f"Post image edited: {response.status_code}")

    response = requests.delete(f"{url}/profile/posts={post_id}", headers=headers, params={"id": post_id})
    logging.info(f"Post deleted: {response.status_code}")

    response = requests.patch(f"{url}/profile/change_username/", headers=headers, params={"username": "test1"})
    logging.info(f"Username changed: {response.status_code}")

    response = requests.patch(f"{url}/profile/change_email/", headers=headers, params={"email": "test@example.com"})
    logging.info(f"Email changed: {response.status_code}")

    response = requests.get(f"{url}/profile", headers=headers)
    logging.info(f"Profile re-accessed: {response.status_code}")

    response = requests.delete(f"{url}/profile/delete_user", headers=headers)
    logging.info(f"User deleted: {response.status_code}")

if os.path.exists(path_to_data_file):
    os.remove(path_to_data_file)
    logging.info(f"Deleted existing data file at {path_to_data_file}")

response = requests.get(f"{url}/download-txt")
if response.status_code == 200:
    with open(path_to_data_file, 'wb') as f:
        f.write(response.content)
    logging.info(f"Downloaded text file saved to {path_to_data_file}")
else:
    logging.error("Failed to retrieve the file")


