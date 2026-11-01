from selenium import webdriver
from urllib.parse import urlparse, parse_qs
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import os
from time import sleep
from json import loads




def get_api_token(school, email, password, chromedriver_path="/usr/bin/chromedriver", wait_time=2):
    if not school:
        raise ValueError("School is not provided.")
    if not email:
        raise ValueError("Email is not provided.")
    if not password:
        raise ValueError("Password is not provided.")
    base_url = "https://" + str(school) + ".zportal.nl/api/3/" + "oauth?sso=true"

    PATH = chromedriver_path
    service = Service(executable_path=PATH)
    
    # 1. Schakel DevTools performance logging in om headers op te vangen
    options = Options()
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(base_url)
        sleep(wait_time)

        email_input = driver.find_element(By.NAME, "loginfmt")
        email_input.send_keys(email)

        summit_button = driver.find_element(By.ID, "idSIButton9")
        summit_button.click()
        sleep(wait_time)

        # Wachtwoord invullen
        password_input = driver.find_element(By.ID, "i0118")
        password_input.send_keys(password)
        sleep(wait_time)

        summit_button = driver.find_element(By.ID, "idSIButton9")
        summit_button.click()
        sleep(wait_time)

        try:
            stay_signed_in = driver.find_element(By.ID, "idSIButton9")
            stay_signed_in.click()
        except Exception:
            pass
        
        sleep(wait_time*2)

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
            return token
        else:
            return None

    finally:
        driver.quit()

