import requests

endpoint = "http://127.0.0.1:8000/api/"

# get_response = requests.get(endpoint,json={"product_id": 123})
get_response = requests.post(endpoint,json={"title": "Riyan J"})

# print(get_response.text)
print(get_response.json())