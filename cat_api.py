import requests
import json

url = "https://api.thecatapi.com/v1/images/search?size=med&mime_types=jpg&format=json&has_breeds=true&order=RANDOM&page=0&limit=1"

def __check_valid_reponse_code(request):
    if request.status_code == 200:
        return request.json()

    return False

def get_cat(CAT_API_KEY):
    payload={}
    headers = {
    'Content-Type': 'application/json',
    'x-api-key': CAT_API_KEY
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = __check_valid_reponse_code(response)


    return data
