import requests
import json
import os


url = "http://localhost:8000"
path_to_data_file = "./local_machine_res/data.txt"
mode = int(input("If you want to send requests to server on you local machine print 0, if in docker print 1: "))

if mode == 1:
    url = "http://localhost:8001"
    path_to_data_file = "./docker_res/data.txt"


for i in range(50):
    with open("./jsons/test_user.json") as test_user_file:
        test_user_data = json.load(test_user_file)
    
    file_path='./Screen.png'
    
    
    payload = {'text': 'test', 'name': 'test'}
    
    user_registration = requests.post(f"{url}/register", json=test_user_data)
    
    
    token_response = requests.post(
        f"{url}/token", 
        data={"username": "test", "password": "test", "grant_type": "password"}, 
        headers={"content-type": "application/x-www-form-urlencoded"}
    )
    token_json = token_response.json()
    token = token_json["access_token"]  
    
    
    headers = {"Authorization": f"Bearer {token}"}
    
    
    current_user = requests.get(f"{url}/profile", headers=headers).json()
    username = current_user[0]["username"]
    
    
    with open(file_path, 'rb') as f:
        files = {'image': (os.path.basename(file_path), f, 'multipart/form-data')}
        create_post = requests.post(f"{url}/new_post", headers=headers, params=payload, files=files).json()
    
    post_id=create_post[0]["id"]
    
    
    requests.get(f"{url}/profile", headers=headers)
    requests.get(f"{url}/users/{username}", headers=headers, params={"username": f"{username}"})
    requests.patch(f"{url}/profile/posts={post_id}/edit_name", headers=headers, params={"name": "test"})
    
    
    with open(file_path, 'rb') as f:
        files = {'image': (os.path.basename(file_path), f, 'multipart/form-data')}
        requests.patch(f"{url}/profile/posts={post_id}/edit_image", headers=headers, params={"id":f"{post_id}"}, files=files)
    
    
    requests.delete(f"{url}/profile/posts={post_id}", headers=headers, params={"id":f"{post_id}"})
    requests.patch(f"{url}/profile/change_username/", headers=headers, params={"username":"test1"})
    requests.patch(f"{url}/profile/change_email/", headers=headers, params={"email":"test@example.com"})
    requests.get(f"{url}/profile", headers=headers)
    requests.delete(f"{url}/profile/delete_user", headers=headers)



response = requests.get(f"{url}/download-txt")

# Ensure the request was successful
if response.status_code == 200:
    # Write the content to a file
    with open(path_to_data_file, 'wb') as f:
        f.write(response.content)
else:
    print("Failed to retrieve the file")
