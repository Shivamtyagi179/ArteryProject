# Artery Safe Internet Learning Module
# READ-ONLY | NO EXECUTION | NO EXPLOITS

import requests

class SafeInternet:
    def __init__(self):
        print("[SafeInternet] Ready (read-only mode)")

    def fetch_text(self, url):
        # very basic safety check
        blocked_keywords = [
            "exploit", "hack", "crack", "bypass",
            "malware", "ransomware", "ddos"
        ]

        for word in blocked_keywords:
            if word in url.lower():
                print("[SafeInternet] Blocked unsafe topic")
                return ""

        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.text[:2000]  # limit data
            else:
                return ""
        except Exception as e:
            print("[SafeInternet] Error fetching data")
            return ""
    def fetch_json(self, url):
        # very basic safety check
        blocked_keywords = [
            "exploit", "hack", "crack", "bypass",
            "malware", "ransomware", "ddos"
        ]

        for word in blocked_keywords:
            if word in url.lower():
                print("[SafeInternet] Blocked unsafe topic")
                return {}

        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return {}
        except Exception as e:
            print("[SafeInternet] Error fetching data")
            return {}