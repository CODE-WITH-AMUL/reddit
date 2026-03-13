#---------------------[MAIN APPLICATION]----------------#
import os
from scr.reddit import fetch_reddit_json
from scr.py_to_csv import save_to_files
from scr.py_to_html import _save_html
#---------------------[LOGO]----------------#
def logo():
    return """
       _____                      _               _______          _ 
  / ____|                    (_)             |__   __|        | |
 | (___   ___ _ __ __ _ _ __  _ _ __   __ _     | | ___   ___ | |
 \\___ \\ / __| '__/ _` | '_ \\| | '_ \\ / _` |    | |/ _ \\ / _ \\| |
 ____) | (__| | | (_| | |_) | | | | | (_| |    | | (_) | (_) | |
 |_____/ \\___|_|  \\__,_| .__/|_|_| |_|\\__, |    |_|\\___/ \\___/|_|
                       | |             __/ |
                       |_|            |___/
   Version 1.0 - Amul Sharma
"""

def fetch_posts(data):
    if not data:
        print("Failed to fetch content.")
        return []

    def _normalize_text(value, fallback):
        if not isinstance(value, str):
            return fallback
        normalized = " ".join(value.split())
        return normalized if normalized else fallback

    posts_data = []
    posts = data.get("data", {}).get("children", [])
    if not isinstance(posts, list):
        print("Invalid post structure in response.")
        return []

    for post in posts[:50]:  # Top 50 posts
        p = post.get("data", {})
        title = _normalize_text(p.get("title"), "No Title")
        description = _normalize_text(p.get("selftext"), "No Description")
        upvotes = p.get("ups", 0) if isinstance(p.get("ups"), int) else 0
        posts_data.append([title, description, upvotes])

    return posts_data


def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(logo())

    data = fetch_reddit_json()
    posts = fetch_posts(data)

    if posts:
        save_to_files(posts)
        print(f"\nSaved {len(posts)} startup ideas to 'startup_ideas.csv' and 'startup_ideas.txt'")
    else:
        print("No posts found.")


if __name__ == "__main__":
    main()
