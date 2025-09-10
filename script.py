import requests

url = "https://student-info-api.netlify.app/.netlify/functions/submit_student_info"

data = {
    "UCID": "emh29",
    "first_name":"Emir",
    "last_name":"Hussain",
    "github_username":"emir7777",
    "discord_username":"emrhsn1119_19776",
    "favorite_cartoon": "Regular Show",
    "favorite_language": "Python",
    "movie_or_game_or_book":"John Wick",
    "section": "103"
}

def validate_data(data):
    required_keys = [
        "UCID", "first_name", "last_name", "github_username",
        "discord_username", "favorite_cartoon", "favorite_language",
        "movie_or_game_or_book", "section"
    ]
    
    for key in required_keys:
        if key not in data:
            return False, f"Missing key: {key}"
        if not isinstance(data[key], str) or not data[key].strip():
            return False, f"Invalid value for key: {key}"
    
    if data["section"] not in ["101", "103"]:
        return False, "Section must be one of '101' or '103'"
    
    return True, "All data is valid"

def is_duplicate(ucid, section):
    get_url = f"https://student-info-api.netlify.app/.netlify/functions/submit_student_info?UCID={ucid}&section={section}"
    try:
        response = requests.get(get_url)
        response.raise_for_status()
        result = response.json()
        
        if result:
            return True
    except requests.exceptions.RequestException:
        pass
    return False

is_valid, message = validate_data(data)

if is_valid == False:
    print("Data validation failed:", message)
elif is_duplicate(data["UCID"], data["section"]):
    print(f"Duplicate entry found for UCID: {data['UCID']} in section: {data['section']}")
else:
    try:
        response = requests.post(url, json=data)
        response.raise_for_status() 
        print("Status Code: ", response.status_code)
        print("Response JSON: ", response.json())
    except requests.exceptions.HTTPError as h:
        print("HTTP error occurred:", h)
        try:
            print("Error details:", response.json())
        except Exception:
            print("No JSON response received.")
    except requests.exceptions.RequestException as e:
        print("Request error occurred:", e)


def retrieve_data(ucid, section):
    get_url = f"https://student-info-api.netlify.app/.netlify/functions/submit_student_info?UCID={ucid}&section={section}"
    try:
        response = requests.get(get_url)
        response.raise_for_status() 
        print("Retrieved Data: ", response.json())
    except requests.exceptions.RequestException as e:
        print("Error retrieving data:", e)

retrieve_data("emh29", "103")