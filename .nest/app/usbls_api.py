import requests
import json
import prettytable
import pandas as pd

API_KEY = "48228204749841eba929dcb6ddef4af0"
BASE_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

# fetch data from BLS API
def fetch_salary_data(series_id):
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "seriesid": [series_id],
        "startyear": "2023",
        "endyear": "2023",
        "registrationkey": API_KEY
    }
    
    response = requests.post(BASE_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}, {response.text}")
        return None
