from dotenv import load_dotenv
import os
import json
import requests
import pandas as pd

# Load env vars from .env file
load_dotenv()

# Access env vars
BLS_API_KEY  = os.environ.get('BLS_API_KEY')
BLS_ENDPOINT = os.environ.get('BLS_ENDPOINT')

# fetch data from BLS API
def fetch_BLS_data(series, **kwargs):
    """
    Pass in a list of BLS timeseries to fetch data and return the series
    in JSON format. Arguments can also be provided as kwargs:
        - startyear (4 digit year)
        - endyear (4 digit year)
        - catalog (True or False)
        - calculations (True or False)
        - annualaverage (True or False)
        - registrationKey (api key from BLS website)
    If the registrationKey is not passed in, this function will use the
    BLS_API_KEY fetched from the environment.
    """
    
    # Error handler for API limited to 25 series per req
    if len(series) < 1 or len(series) > 25:
        raise ValueError("Must pass in between 1 and 25 series ids")
    
    # Create headers and payload post data
    headers = {'Content-Type': 'application/json'}
    payload = {
        'seriesid': series,
        'registrationKey': BLS_API_KEY,
    }

    # Update the payload with the keyword arguments and convert to JSON
    payload.update(kwargs)
    payload = json.dumps(payload)

    # Fetch the response from the BLS API
    response = requests.post(BLS_ENDPOINT, data=payload, headers=headers)
    response.raise_for_status()

    # Parse the JSON result
    result = response.json()
    if result['status'] != 'REQUEST_SUCCEEDED':
        raise Exception(result['message'][0])
    return result


series = ['OEUS250000000000013108211', 'OEUS250000000000013116111', 'OEUS250000000000013201111', 
          'OEUS250000000000013205111', 'OEUS250000000000015122111', 'OEUS250000000000015209911', 
          'OEUS250000000000017207111', 'OEUS250000000000019102911', 'OEUS250000000000019201211',
          'OEUS250000000000019301111', 'OEUS250000000000019303911', 'OEUS250000000000019309411',
          'OEUS250000000000025112311', 'OEUS250000000000025112611']

data = fetch_BLS_data(series, startyear = 2023, endyear = 2023)

if data:
    # Parse data as needed
    series = data.get("Results", {}).get("series", [])
    results = []
    for item in series:
        series_id = item.get("seriesID")
        for entry in item.get("data", []):
            results.append({
                "seriesID": series_id,
                "year": entry.get("year"),
                "period": entry.get("period"),
                "value": entry.get("value"),
            })
    
    # Convert to DataFrame for easier handling
    df = pd.DataFrame(results)
    df.to_csv("massachusetts_salaries.csv", index=False)
    print("Data saved to massachusetts_salaries.csv")

info = pd.read_csv('./massachusetts_salaries.csv')
info.head()