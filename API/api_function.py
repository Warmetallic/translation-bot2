import requests
from decouple import config

# DeepL API endpoint
deepl_api_endpoint = "https://api-free.deepl.com/v2/translate"

api_key = config("API_KEY")


def api_connect(text, target_lang):
    user_input = text
    # Specify the parameters for the DeepL API request
    params = {
        "auth_key": api_key,  # Your DeepL API key
        "text": user_input,
        "target_lang": target_lang,  # Target language (e.g., Russian)
    }

    res = requests.get(deepl_api_endpoint, params=params)
    return res
