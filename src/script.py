import requests
import sys
import logging

logging.basicConfig(level=logging.INFO, filename="get_hero.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

def _convert_height(element: dict) -> float:
    height_parts = element['appearance']['height'][1].split()

    if len(height_parts) != 2:
        logging.warning(f"There is no information about the height {element['name']}")
        return -1
    
    value = float(height_parts[0])
    unit = height_parts[1].lower()
    if unit in ('cm', 'centimetres', 'centimeters'):
        pass
    elif unit in ('m', 'metres', 'meters'):
        value *= 100
    else:
        logging.warning(f"Unknown unit of measurement for the hero's height: {element['name']}")
        return -1

    return value

def _get_all_heroes():
    #Get list of all heroes
    get_all_url = "https://akabab.github.io/superhero-api/api/all.json"
    try:
        response = requests.get(get_all_url)
        response.raise_for_status()
    except Exception as e:
        logging.error(f"Couldn't get a response. Error: {e}")
        return None
    return response.json()

def get_highest_hero(gender: str, is_working: bool) -> str:
    logging.info("Getting heroes data...")
    all_heroes_data = _get_all_heroes()
    if not all_heroes_data:
        return None

    #Filter list by conditions
    logging.info("Filtering heroes by conditions...")
    filtered_data: list = []
    for element in all_heroes_data:
        is_hero_working = False if element['work']['occupation'] == "-" else True
        if element['appearance']['gender'].lower() == gender.lower() and is_hero_working == is_working:
                filtered_data.append(element)
    
    #Sort heroes by height
    logging.info("Finding for the highest hero...")
    sorted_data = sorted(filtered_data, key=_convert_height, reverse=True)

    if sorted_data:
        hero_name = sorted_data[0]['name'] if sorted_data[0]['name'] else "Nameless hero"
        logging.info("The search is completed")
        return sorted_data[0]['id'], hero_name
    else:
        logging.warning("Couldn't find the hero")
        return None

if __name__ == "__main__":
    get_highest_hero(sys.argv[1], bool(int(sys.argv[2])))
    # print(get_highest_hero(sys.argv[1], bool(int(sys.argv[2]))))
