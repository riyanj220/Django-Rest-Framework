import requests
headers = {'Authorization': 'Token 5c8e4662a3af260f117ea2f4213d7c48415ff022'}
endpoint = "http://127.0.0.1:8000/api/products/"

data = {
    "title":"This field is done!",
    "price":22.99
}

get_response = requests.post(endpoint,json=data , headers=headers)

print(get_response.json())