import requests
import time

def Getting_Game_Id():
    # Define the URL
    _url = "https://ca.1xbet.com/service-api/LiveFeed/GetSportsShortZip?sports=85&champs=2665392&lng=en&gr=828&country=85&virtualSports=true&groupChamps=true"

    # Send a GET request
    response = requests.get(_url)

    if response.status_code == 200:
        try:
            data = response.json()
            # List to store all the data from the loop
            all_data = []

            # Loop through possible indices
            for idx in [20, 21, 22, 23, 24, 25, 26, 27]:
                try:
                    for i in range(5):
                        # Extract values
                        Game_Id = data["Value"][idx]["L"][2]["G"][i]["I"]
                        Score = data["Value"][idx]["L"][2]["G"][i]["SC"]["FS"]
                        Time = data["Value"][idx]["L"][2]["G"][i]["SC"]["TS"]

                        # Store values in a dictionary with a loop ID
                        loop_data = {
                            "loop_id": f"loop{i}",
                            "Game_Id": Game_Id,
                            "Score": Score,
                            "Time": Time
                        }
                        all_data.append(loop_data)  # Append to the list
                    break  # Exit loop if successful
                except (IndexError, KeyError):  # Handle missing or invalid indices
                    continue

            # List to store data with empty scores
            empty_score_data = []

            # Check for entries with an empty Score
            for entry in all_data:
                if not entry["Score"]:  # If Score is empty or None
                    empty_score_data.append({
                        "loop_id": entry["loop_id"],
                        "Game_Id": entry["Game_Id"],
                        "Time": entry["Time"]
                    })

            if empty_score_data:
                # Get the entry with the lowest Time
                lowest_time_entry = min(
                    empty_score_data,
                    key=lambda x: int(x["Time"]) if isinstance(x["Time"], (str, int)) else float("inf")
                )
                # Return the corresponding Game_Id
                return lowest_time_entry['Game_Id']
            else:
                print("No entries with an empty Score were found.")
                return None

        except Exception as e:
            print(f"There was an error: {e}")
            return None
    else:
        print("Failed to get data from the server.")
        return None

def Recording():
    print("Started the Recording Phase")
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            Team1=data["Value"]["O1"]
            Team2=data["Value"]["O2"]
            W1_Odd=data["Value"]["GE"][0]["E"][0][0]["C"]
            X_Odd=data["Value"]["GE"][0]["E"][1][0]["C"]
            W2_Odd=data["Value"]["GE"][0]["E"][2][0]["C"]
            Time=data["Value"]["SC"]["TS"]

            print(Team1)
            time.sleep(30)
        except:
            print("There is an error somewhere")
   

def Record_Setup():
    global url
    ID_GAME = Getting_Game_Id()
    url = f"https://ca.1xbet.com/service-api/LiveFeed/GetGameZip?id={ID_GAME}&lng=en&isSubGames=true&GroupEvents=true&countevents=250&grMode=4&topGroups=&country=85&marketType=1"
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            Time=data["Value"]["SC"]["TS"]
            for i in range(Time):
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    Time = data["Value"]["SC"]["TS"]
                    print(Time)
                if Time < 32:
                    Recording()
                time.sleep(30)
        except Exception as e:
            print(f"there is an Error somewhere:{e}")
Record_Setup()

