import requests
from bs4 import BeautifulSoup
import time
import json
import sys
import random

with open('configs/settings.json', 'r') as f:
    data = json.load(f)

def get_data(url):
    response = requests.get(url)
    html_content = response.text
    return html_content

def menu():
    print("1. Wybierz kategorie do pobrania\n2. Zmiana częstotliwości requestów\n9. Wyjdź")
    answer = input("")
    if answer == "1":
        categories()
    if answer == "2":
        frequencyOfRequests()
    if answer == "9":
        exit()
    else:
        print("Nieprawidłowa opcja!")
        menu()

def frequencyOfRequests():
    print("Podana niżej liczba jest ilością requestów NA SEKUNDĘ! (domyślna wartość: 5)")
    answer = input("")
    if answer.isdigit():
        data["requests"] = int(answer)
        with open('configs/settings.json', 'w') as f:
            json.dump(data, f)
        menu()
    else:
        print("Nieprawidłowa opcja!")
        frequencyOfRequests()


def categories():
    category_map = {
        "1": {"name": "papier", "maxPage": 28},
        "2": {"name": "artykuly-biurowe", "maxPage": 809},
        "3": {"name": "kolekcje-produktow", "maxPage": 48},
        "4": {"name": "urzadzenia-biurowe", "maxPage": 15},
        "5": {"name": "colop-e-mark", "maxPage": 1},
        "6": {"name": "artykuly-komputerowe-i-mobilne", "maxPage": 30},
        "7": {"name": "druki-szkolne", "maxPage": 8},
        "8": {"name": "artykuly-szkolne", "maxPage": 59},
        "9": {"name": "przybory-kreatywne", "maxPage": 88},
        "10": {"name": "artykuly-spozywcze", "maxPage": 12},
        "11": {"name": "utrzymanie-czystosci", "maxPage": 13},
        "12": {"name": "profesionalne-odswiezacze-kala", "maxPage": 7},
        "13": {"name": "dla-zwierzat", "maxPage": 153},
        "14": {"name": "meble", "maxPage": 84},
        "15": {"name": "pieczatki-i-stemple", "maxPage": 12},
        "16": {"name": "artykuly-reklamowe", "maxPage": 40},
        "17": {"name": "katalogi-gazetki-drukowane", "maxPage": 1},
        "18": {"name": "nagrody", "maxPage": 6},
        "19": {"name": "strong-kalendarze-2024-r-/strong", "maxPage": 1},
        "20": {"name": "katalog-osaa-2024", "maxPage": 252},
        "21": {"name": "katalog-szkolny-2023/2024", "maxPage": 52},
        "22": {"name": "produkty-covid19", "maxPage": 2},
        "99": {"name": "pelny-asortyment-dostawcow", "maxPage": 1431}
    }

    print("\n".join([f"{key}. {value['name'].capitalize()}" for key, value in category_map.items()]))
    answer = input("")
    chosen_category = category_map.get(answer)
    if chosen_category:
        getPart(chosen_category)
    else:
        print("Nieprawidłowy numer kategorii!")
        categories()

def progressBar(countValue, total, suffix=''):
    filledUpLength = int(round(100 * countValue / float(total)))
    percentage = round(100.0 * countValue/float(total),1)
    bar = '=' * filledUpLength + '-' * (100 - filledUpLength)
    sys.stdout.write('[%s] %s%s ...%s\r' %(bar, percentage, '%', suffix))
    sys.stdout.flush()

def getPart(category):
    time_sleep = 1 / data["requests"]

    for page_num in range(1, category["maxPage"] + 1):
        url = f"https://eazbiuro.pl/pl/list/{category['name']}?page={page_num}"
        html_content = get_data(url)
        soup = BeautifulSoup(html_content, 'html.parser')
        
        names = soup.find_all(class_='product-name')
        prices = soup.find_all(class_='price-net')
        codes = soup.find_all(class_='symbol')
        
        with open(f"downloads/{category['name']}.txt", "a", encoding="utf-8") as file:
            for name, price, code in zip(names, prices, codes):
                file.write(name.text.strip())
                file.write("; " + price.text.strip())
                file.write("; " + code.text.strip() + "\n")
        
        progressBar(page_num, category["maxPage"])
        time.sleep(time_sleep)

    print("Skrypt skończył swoją pracę! :)")

menu()
