## https://developers.google.com/maps/documentation/places/web-service/details#maps_http_places_details_fields-py

import requests
import argparse

def check_business_status(api_key, business_name):
    msg = ''
    
    url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={business_name}&key={api_key}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if data['results']:
            place_id = data['results'][0]['place_id']

            details_url = f'https://maps.googleapis.com/maps/api/place/details/json?placeid={place_id}&key={api_key}'

            details_response = requests.get(details_url)

            if details_response.status_code == 200:
                details_data = details_response.json()
                opening_hours = details_data['result']['opening_hours']

                if opening_hours['open_now']:
                    msg = "The business is currently open."
                else:
                    msg = "The business is currently closed."
            else:
                msg = "Error: Failed to retrieve place details."
        else:
            msg = "No results found for the given business name."
    else:
        msg = "Error: Failed to retrieve data from the Places API."
        
    return msg


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check business status using Google Places API')
    parser.add_argument('--api_key', required=True, help='Your Google Places API key')
    parser.add_argument('--business_name', required=True, help='Name of the business')

    args = parser.parse_args()
    print(check_business_status(args.api_key, args.business_name))
