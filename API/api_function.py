import aiohttp
from decouple import config
import os

# DeepL API endpoint
deepl_api_endpoint = "https://api-free.deepl.com/v2/translate"
deepl_document_endpoint = "https://api-free.deepl.com/v2/document"
deepl_document_status_endpoint = "https://api-free.deepl.com/v2/document/{document_id}"
deepl_document_download_endpoint = (
    "https://api-free.deepl.com/v2/document/{document_id}/result"
)

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


async def api_connect_document(file_path, target_lang, source_lang=None):
    """Connect to the DeepL API for document translation."""
    async with aiohttp.ClientSession() as session:
        form = aiohttp.FormData()
        form.add_field("auth_key", api_key)
        form.add_field("target_lang", target_lang)
        if source_lang:
            form.add_field("source_lang", source_lang)

        # Open file in binary mode
        with open(file_path, "rb") as file:
            form.add_field("file", file, filename=os.path.basename(file_path))

            try:
                async with session.post(deepl_document_endpoint, data=form) as response:
                    if response.status != 200:
                        error_message = await response.text()
                        print(f"Error response from API: {error_message}")
                        return {"error": error_message}

                    json_response = await response.json()
                    print(f"API response: {json_response}")

                    if (
                        "document_id" in json_response
                        and "document_key" in json_response
                    ):
                        return json_response
                    else:
                        print(
                            f"'document_id' or 'document_key' not found in the response: {json_response}"
                        )
                        return {
                            "error": "document_id or document_key not found in the response"
                        }
            except Exception as e:
                print(f"Exception occurred during file upload: {e}")
                return {"error": str(e)}


async def check_translation_status(document_id, document_key):
    """Check the translation status of a document."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                deepl_document_status_endpoint.format(document_id=document_id),
                data={"auth_key": api_key, "document_key": document_key},
            ) as response:
                if response.status != 200:
                    error_message = await response.text()
                    print(f"Error response from API: {error_message}")
                    return {"error": error_message}

                json_response = await response.json()
                print(f"Status response: {json_response}")
                return json_response
        except Exception as e:
            print(f"Exception occurred while checking status: {e}")
            return {"error": str(e)}


async def download_translated_document(document_id, document_key, output_path):
    """Download the translated document."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                deepl_document_download_endpoint.format(document_id=document_id),
                data={"auth_key": api_key, "document_key": document_key},
            ) as response:
                if response.status != 200:
                    error_message = await response.text()
                    print(f"Error response from API: {error_message}")
                    return {"error": error_message}

                with open(output_path, "wb") as f:
                    f.write(await response.read())
                print(f"Translated document downloaded to: {output_path}")
                return {"success": True, "file_path": output_path}
        except Exception as e:
            print(f"Exception occurred while downloading document: {e}")
            return {"error": str(e)}
