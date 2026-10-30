import logging
import os
import requests
from dotenv import load_dotenv
from helper.log_api_message import log_api_message

load_dotenv()
SCHOOL = os.getenv("SCHOOL")
AUTHORIZATION = os.getenv("AUTHORIZATION")

base_url = "https://" + str(SCHOOL) + ".zportal.nl/api/3/"
HEADERS = {
    "Authorization": AUTHORIZATION
}


def get_endpoint(endpoint, parameters):
    url = f"{base_url}{endpoint}?{parameters}"
    try:
        req = requests.get(url, headers=HEADERS)

        json_data = req.json()
        log_api_message(url, HEADERS, json_data)

        api_response = json_data.get("response", {})
        status = api_response.get("status")

        if status != 200:
            message = api_response.get("message", "Onbekende fout")
            logging.error(f"Fout in get_endpoint: {status} {message}")
            if status == 401:
                logging.info("Token verlopen. Nieuw token ophalen en opnieuw proberen...")
                from helper.get_api_token import get_api_token
                get_api_token()
                logging.info("Nieuw token opgehaald. Probeer opnieuw door opnieuw te starten.")
                quit()
            if status == 403:
                logging.error("Toegang geweigerd. Controleer de machtigingen van de API-token.")
                return None
            raise Exception(f"API Error {status}: {message}")

        return json_data["response"]["data"]
    except requests.exceptions.RequestException as e:
        logging.error(f"Netwerk of HTTP fout in get_endpoint: {e}")
        raise
    except Exception as e:
        logging.error(f"Onverwachte fout in get_endpoint: {e}")
        raise