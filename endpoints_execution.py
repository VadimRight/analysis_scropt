import requests
import json
import os

for i in range(4):
    with open("./jsons/test_user.json") as test_user_file:
        test_user_data = json.load(test_user_file)
    
    url = "http://localhost:8000"
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
    
