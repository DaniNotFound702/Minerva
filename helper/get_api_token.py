from selenium import webdriver
from urllib.parse import urlparse, parse_qs
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os
from time import sleep
from json import loads

load_dotenv()
SCHOOL = os.getenv("SCHOOL")
if not SCHOOL:
    raise ValueError("SCHOOL is not set in the environment variables.")
EMAIL = os.getenv("EMAIL")
if not EMAIL:
    raise ValueError("EMAIL is not set in the environment variables.")
PASSWORD = os.getenv("PASSWORD")
if not PASSWORD:
    raise ValueError("PASSWORD is not set in the environment variables.")

base_url = "https://" + str(SCHOOL) + ".zportal.nl/api/3/" + "oauth?sso=true"

def get_api_token():
    PATH = "/usr/bin/chromedriver"
    service = Service(executable_path=PATH)
    
    # 1. Schakel DevTools performance logging in om headers op te vangen
    options = Options()
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(base_url)
        sleep(1)

        email_input = driver.find_element(By.NAME, "loginfmt")
        email_input.send_keys(EMAIL)

        summit_button = driver.find_element(By.ID, "idSIButton9")
        summit_button.click()
        sleep(1)

        # Wachtwoord invullen
        password_input = driver.find_element(By.ID, "i0118")
        password_input.send_keys(PASSWORD)
        sleep(1)

        summit_button = driver.find_element(By.ID, "idSIButton9")
        summit_button.click()
        sleep(1)

        # Eventuele "Aangemeld blijven?" pop-up doorklikken
        try:
            stay_signed_in = driver.find_element(By.ID, "idSIButton9")
            stay_signed_in.click()
        except Exception:
            pass

        # Wacht even tot de browser de Zermelo API-calls met de Authorization header uitvoert
        sleep(4)

        # 2. Doorzoek de netwerklogs naar de Authorization header
        logs = driver.get_log("performance")
        token = None

        for entry in logs:
            try:
                log_data = loads(entry["message"])["message"]
                
                # We controleren uitgaande netwerkverzoeken
                if log_data.get("method") == "Network.requestWillBeSent":
                    request = log_data.get("params", {}).get("request", {})
                    headers = request.get("headers", {})

                    # Zoek naar de header (zowel met hoofd- als kleine letters)
                    auth_header = headers.get("Authorization") or headers.get("authorization")
                    
                    if auth_header and "Bearer" in auth_header:
                        # Haal het woord 'Bearer ' eraf zodat je puur het token overhoudt
                        token = auth_header.replace("Bearer", "").strip()
                        break
            except (KeyError, ValueError):
                continue

        if token:
            # Sla het token op in een .env-bestand
            with open(".env", "r") as f:
                lines = f.readlines()
            cleaned_lines = [
                line for line in lines 
                if not line.strip().startswith("AUTHORIZATION=")
            ]
            cleaned_lines.append(f"AUTHORIZATION=Bearer {token}\n")   

            with open(".env", "w") as env_file:
                env_file.writelines(cleaned_lines)
        else:
            return None

    finally:
        driver.quit()

