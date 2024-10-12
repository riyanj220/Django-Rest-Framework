import requests

endpoint = "http://127.0.0.1:8000/api/products/1/update"

data = {
    "title":"Riyan J",
    "price":100.0,
    "content":"This is a sample product."
}

get_response = requests.put(endpoint , json=data)

print(get_response.json())