#---------------------[IMPORT MODEL]----------------#
import os
import random
import time

import requests
from dotenv import load_dotenv

#-----------------[LOAD ENVIRONMENT VARIABLES]----------------#
load_dotenv()

#---------------------[FETCH REDDIT JSON]----------------#
def load_user_agents():
    file_path = os.path.join(os.path.dirname(__file__), "user_agents.txt")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"User-Agent file not found: {file_path}")
        return []


# Fetch Reddit JSON with User-Agent rotation and filter posts from last 24 hours
def fetch_reddit_json():
    """Fetch Reddit JSON using User-Agent rotation."""
    agents = load_user_agents()
    if not agents:
        print("No User-Agents available. Add entries to scr/user_agents.txt.")
        return None

    headers = {"User-Agent": random.choice(agents)}
    url = (os.getenv("BASE_URL_JSON") or "").strip()  # API endpoint
    if not url:
        print("BASE_URL_JSON is missing in .env")
        return None

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        listing = data.get("data")
        if not isinstance(listing, dict):
            print("Invalid response shape: missing 'data' object.")
            return None

        children = listing.get("children", [])
        if not isinstance(children, list):
            print("Invalid response shape: 'data.children' must be a list.")
            return None

        # Filter posts from last 24 hours
        now = time.time()
        one_day_ago = now - 24 * 3600

        new_posts = []
        for post in children:
            post_data = post.get("data", {})
            if post_data.get("created_utc", 0) >= one_day_ago:
                new_posts.append(post)
        listing["children"] = new_posts
        return data

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except ValueError as e:
        print(f"Invalid JSON response: {e}")
        return None
