import os
import json
from datetime import datetime

def log_api_message(url, headers, response_data):
    # Zorg dat de log map bestaat
    os.makedirs("./logs/messages", exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S%f")
    messagefile = f"./logs/messages/message-{timestamp}.json"
    
    # Voeg request info toe aan de kopie van de data
    log_data = response_data.copy()
    log_data["request"] = {
        "url": url,
        "headers": headers
    }
    
    with open(messagefile, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, ensure_ascii=False, indent=4, sort_keys=True)

