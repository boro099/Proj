#!/usr/bin/env python3
"""
Sync LeetCode data to GitHub repository
"""

import os
import json
import requests
from datetime import datetime

LEETCODE_API = "https://leetcode.com/api/user"
PROGRESS_FILE = "progress.json"

def get_leetcode_data():
    """Fetch LeetCode user data"""
    session = os.getenv("LEETCODE_SESSION")
    username = os.getenv("LEETCODE_USERNAME")
    
    if not session or not username:
        print("❌ Missing LEETCODE_SESSION or LEETCODE_USERNAME environment variables")
        return None
    
    try:
        headers = {
            "Cookie": f"LEETCODE_SESSION={session}",
            "User-Agent": "Mozilla/5.0"
        }
        
        # Fetch user profile
        response = requests.get(
            f"{LEETCODE_API}/{username}/",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to fetch LeetCode data: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error fetching LeetCode data: {e}")
        return None

def save_progress(data):
    """Save progress to file"""
    if data:
        progress = {
            "username": data.get("username"),
            "solved": data.get("submitStats", {}).get("acSubmissionNum", [{}])[0].get("count", 0),
            "total": data.get("submitStats", {}).get("acSubmissionNum", [{}])[0].get("submissions", 0),
            "last_updated": datetime.now().isoformat()
        }
        
        with open(PROGRESS_FILE, "w") as f:
            json.dump(progress, f, indent=2)
        
        print(f"✅ LeetCode progress updated: {progress['solved']} problems solved")
    else:
        print("❌ No data to save")

if __name__ == "__main__":
    data = get_leetcode_data()
    save_progress(data)
