import aiohttp
from decouple import config

# DeepL API endpoint
deepl_api_endpoint = "https://api-free.deepl.com/v2/translate"

api_key = config("API_KEY")


async def api_connect(text, target_lang):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            deepl_api_endpoint,
            data={
                "auth_key": api_key,
                "text": text,
                "target_lang": target_lang,
            },
        ) as response:
            return await response.json()
