import requests
import sys

def sort_height(element: dict) -> float:
    value = float(element['appearance']['height'][1].split()[0])
    unit = element['appearance']['height'][1].split()[1]
    return value if unit == 'cm' else value * 100

def getHighestHero(gender: str, is_working: bool) -> str:
    #Get list of all heroes
    try:
        all_hero_response = requests.get("https://akabab.github.io/superhero-api/api/all.json")
    except Exception as e:
        print("Couldn't get a response. Error: ", e)
        return None
    all_hero_data = all_hero_response.json()
    
    #Filter list by conditions
    filtered_data = [] 
    for element in all_hero_data:
        is_hero_working = False if element['work']['occupation'] == "-" else True
        if element['appearance']['gender'] == gender and is_hero_working == is_working:
                filtered_data.append(element)
    
    #Sort heroes by height
    sorted_data = sorted(filtered_data, key=sort_height, reverse=True)
    return sorted_data[0]['name']

if __name__ == "__main__":
    print(getHighestHero(sys.argv[1], bool(int(sys.argv[2]))))
