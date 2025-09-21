import requests
import csv
from flask import Flask, jsonify

app = Flask(__name__)

# Global variable to store cached results
cached_characters = None



def fetch_characters(basicFilter,originFilter = None):
    url = 'https://rickandmortyapi.com/api/character/?'
    all_characters = []
    for key, value in basicFilter.items():
        url += f'{key}={value}&'

    while url:  # Handles pagination by processing each page
        response = requests.get(url)

        # Validate response
        if response.status_code != 200:
            print(f"Error: Failed to fetch data. Status code: {response.status_code}")
            break

        data = response.json()
        characters = data['results']

        # Filter characters whose origin is from Earth
        earth_characters = [
            char for char in characters if originFilter in char['origin']['name'].lower()
        ]

        all_characters.extend(earth_characters)

        # Proceed to the next page
        url = data['info']["next"] if data['info']['next'] != 'null' else None

    return all_characters

def get_character_details(filtered_characters):
    character_details = [
        {
            "name": char["name"],
            "location": char["location"]["name"],
            "image": char["image"]
        }
        for char in filtered_characters
    ]
    return character_details

def write_to_csv(character_details_array, csv_filename):
    # Define the header for the CSV
    header = ["Name", "Location", "Image"]

    # Open the CSV file for writing
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()  # Write the header row

        # Write each character's details as a row in the CSV
        for char in character_details_array:
            writer.writerow({"Name": char["name"], "Location": char["location"], "Image": char["image"]})

    print(f"Data successfully written to {csv_filename}.")


# Cache the results on the first request
def cache_characters():
    global cached_characters
    basic_filter = {
        "status": "Alive",
        "species": "Human"
    }
    origin_filter = "earth"
    characters_with_earth_origin = fetch_characters(basic_filter, origin_filter)
    cached_characters = get_character_details(characters_with_earth_origin)
    print("Character data has been cached.")  # Optional log for debugging

# REST API endpoint to return filtered characters
@app.route('/api/characters', methods=['GET'])
def get_filtered_characters():
    return jsonify(cached_characters)

@app.route('/healthcheck', methods=['GET'])
def get_healthcheck():
    return "healthy"

if __name__ == '__main__':
    if cached_characters is None:
        cache_characters()
    app.run(debug=True,port=80, host="0.0.0.0")


# filtered_chars = fetch_characters(basic_filter, "earth")
# filtered_info_chars = get_character_details(filtered_chars)
# csv_filename = "filtered_characters.csv"
# write_to_csv(filtered_info_chars, csv_filename)

