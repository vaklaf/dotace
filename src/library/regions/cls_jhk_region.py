import requests
from bs4 import BeautifulSoup
import os
import time
import re
import zipfile
import io
from datetime import datetime as dt

TEXTY = ["Došlé a podpořené žádosti", "Žádosti podané do"]
roky = [str(y) for y in  range(2015,dt.now().year+1)]
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

''' Středo český kraj region class. '''
from pathlib import Path

from src.apis.events import post_event
from src.library.utilities.others import build_output_path
from src.library.utilities.others import inject_timestamp_to_file_name
from src.library.downloader.downloader import rewrite_url
from .cls_abstract_region import AbstractRegion
from src.library.downloader.downloader import clear_downloads_folder

class JhkRegion(AbstractRegion):
    '''
    Class for Jihocesky kraj region
    '''
    _texty = ["Došlé a podpořené žádosti", "Žádosti podané do"]
    _roky = [str(y) for y in  range(2015,dt.now().year+1)]   
    _key: str = 'jhk'
    _urls:list[str] = [
            'https://www.kraj-jihocesky.cz/cs/ku_dotace/schvalene?rok=2020&op=Vyhledej'
    ]
    
    def __init__(self,params: dict,output_suffix:str)->None:
        self._name = params
        self.output_path = build_output_path(Path(
            params['paths']['outputs_root']), params['paths']['output_folder_prefix'], self._key)
        self.output_files_suffix = output_suffix

    def crawl(self):

        post_event('start_porocess_region', {'module':__name__,'data':{'data': self._name}})
        url = self._urls[0]
        for rok in self._roky:
            url = rewrite_url(url, new_params={'rok':rok})
            html_content = self._get_html(url)
            if not html_content:
                post_event('error', {'module':__name__,'data':{'data': self._name}})
                return


        
        post_event('end_porocess_region', {'module':__name__,'data':{'data': self._name}})
        
    def get_donations_list(self,html_content:str)-> list[tuple]:
        '''
        Get the list of donations from the region.
        '''
        soup = BeautifulSoup(html_content, 'html.parser')
        
        container = soup.find('dl', class_='styled ckeditor-accordion2')
        
        dt_elements = container.find_all('dt')
        dt_dl_pairs = [(dt, dt.find_next_sibling('dd')) for dt in dt_elements if dt.find_next_sibling('dd')]
        return dt_dl_pairs
        
    def parse_dt_dl_pair(self, dt_dl_pair:tuple)-> dict:
        '''
        Parse the dt and dl pair to get the data.
        '''
        dt, dl = dt_dl_pair
        print(self.get_donation_header(dt))
    
    def get_donation_header(self, dt: str)-> str:
        '''
        Get the header of the donation.
        '''
        header = dt.find('a',class_='ckeditor-accordion-toggler accordion-link').text
        header = re.sub(r'[()\./§<>:"/\\|?*]', '', header)
        header = re.sub(r'\s+', '_', header)
        return header