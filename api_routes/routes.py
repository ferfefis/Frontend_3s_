import requests


base_url = "https://api.thecatapi.com/v1"

def get_gatos():
    url = f"{base_url}/breeds"

    headers = {
        "x-api-key": "live_CRTm3Cubvonyr8DBT4DxHgmbNi6mATIueW1Q0EHeqtr8VgHChet9032l5pCi0Hm4"
    }

    resposta = requests.get(url, headers=headers)

    return resposta.json()

def get_image():
    url = "https://api.thecatapi.com/v1/images/search"

    resposta = requests.get(url)

    return resposta.json()[0]