#-----------------------[IMPORT MODEL]-------------------#
import requests
import random
import os
from dotenv import load_dotenv



#----------------[MAIN CODE]----------------#
def url_path():
    load_dotenv()
    url = os.getenv("BASE_URL")

    file_path = os.path.join(os.path.dirname(__file__), "user_agents.txt")

    # read all user agents
    with open(file_path, "r", encoding="utf-8") as f:
        user_agents = f.read().splitlines()

    headers = {
        "User-Agent": random.choice(user_agents)
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.content
    else:
        print("Request failed:", response.status_code)
        return None