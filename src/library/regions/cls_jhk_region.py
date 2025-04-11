import requests
from bs4 import BeautifulSoup
import os
import time
import re
import zipfile
import io
from datetime import datetime as dt

TEXTY = ["Došlé a podpořené žádosti", "Žádosti podané do"]
roky = [str(y) for y in  range(2020,dt.now().year+1)]
# roky = ['2024']

for rok in roky:
    BASE_URL = "https://www.kraj-jihocesky.cz/cs"
    PAGE_URL = f"https://www.kraj-jihocesky.cz/cs/ku_dotace/schvalene?rok={rok}&op=Vyhledej"

    main_folder = "soubory_jhk_final"
    os.makedirs(main_folder, exist_ok=True)

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    MAX_RETRIES = 3
    def fetch_page():
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.get(PAGE_URL, headers=HEADERS, timeout=30)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                print(f"Pokus {attempt + 1} selhal: {e}")
                time.sleep(5)
        return None

    page_content = fetch_page()
    if not page_content:
        print("Nepodařilo se stáhnout stránku, ukončuji skript.")
        continue

    soup = BeautifulSoup(page_content, "html.parser")
    links = soup.find_all("a")

    dt_elements = soup.find_all("dt")
    h2_elements = [dt.find('h2') for dt in dt_elements]
    nazvy = [h2elm.find('b').text for h2elm in h2_elements if h2elm]

    def nazvy_clean(nazev):
        nazev = re.sub(r'[()\./§<>:"/\\|?*]', '', nazev)
        nazev = re.sub(r'\s+', '_', nazev)
        return nazev

    nazvy_folder = [nazvy_clean(item) for item in nazvy]

    filtered_links = [link for link in links if (TEXTY[0] in link.text or TEXTY[1]  in link.text)]
    
    test_zip = list(zip(nazvy, nazvy_folder, filtered_links))
    
    for nazev, folder, link in test_zip:
        href = link.get("href")
        if not href:
            continue
        
        url = BASE_URL + href[2:]
        link_name = link.text.split("(")
        file_ext = link_name[1][:-1] if len(link_name) > 1 else "unknown"
        
        name_soubor = f'{rok}_{link_name[0].strip().replace(" ", "_")}.{file_ext}'
        name_soubor = re.sub(r'[<>:"/\\|?*]', '_', name_soubor)

        target_folder = os.path.join(main_folder, folder)
        os.makedirs(target_folder, exist_ok=True)
        file_path = os.path.join(target_folder, name_soubor)
        
        if os.path.exists(file_path):
            print(f"Soubor {file_path} již existuje, přeskočeno.")
            continue
        
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()

            if file_ext == "zip":
                with zipfile.ZipFile(io.BytesIO(response.content), 'r') as zip_ref:
                    zip_ref.extractall(target_folder)
                    print(f"ZIP rozbalen do: {target_folder}")
            else:
                with open(file_path, "wb") as file:
                    file.write(response.content)
                    print(f"Staženo: {file_path}")
        
        except requests.RequestException as e:
            print(f"Chyba při stahování {url}: {e}")
    
print("Stažení dokončeno.")
