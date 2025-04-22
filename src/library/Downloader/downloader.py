import requests
import shutil

from pathlib import Path
from urllib.parse import urlencode, urlunparse, urlparse,parse_qs,parse_qsl
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

import urllib3

from requests.exceptions import ConnectTimeout

from .exeptions import DownloadingFailure,FolderCannotBeCreated

service = ChromeService(executable_path='./drivers/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(300)


def download_file(output_path:Path, url:str, file_name:str):
    """
    Stáhne soubor z dané URL a uloží ho do zadané složky.

    Args:
        output_path (Path): Cesta ke složce, kam se má soubor uložit.
        url (str): URL adresa souboru ke stažení.
        file_name (str): Název souboru, pod kterým se má uložit.
        
    Raises:
        FileExistsAlready: Pokud cílový soubor již existuje.
        DownloadingFailure: Pokud stahování souboru selže (síťová chyba, HTTP chyba).
        FolderCannotBeCreated: Pokud nelze vytvořit cílovou složku.
    """
    target_path = output_path / file_name

    if target_path.exists():
        return
        #raise FileExistsAlready(target_path)


    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Vyvolá výjimku pro chybové HTTP status kódy

        target_path.parent.mkdir(parents=True,exist_ok=True) # Vytvoří složku, pokud neexistuje

        with open(target_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
    except requests.exceptions.RequestException as e:
        raise DownloadingFailure(f"Error while downloading file form: '{url}': {e}")
    except OSError as e:
        raise FolderCannotBeCreated(f"Error while creating '{str(output_path)}': {e}")

def clear_downloads_folder(path:Path):
    """
    Vymaže veškerý obsah zadané složky (soubory a podsložky).

    Args:
        path: Objekt pathlib.Path reprezentující cestu ke složce.
    """
    if not path.is_dir():
        print(f"Chyba: Zadaná cesta '{path}' není složka.")
        return

    for item in path.iterdir():
        try:
            if item.is_file():
                item.unlink()  # Smaže soubor
            elif item.is_dir():
                shutil.rmtree(item)  # Rekurzivně smaže složku a její obsah
            print(f"Smazáno: {item}")
        except Exception as e:
            print(f"Chyba při mazání '{item}': {e}")

def get_html_content(url)->str:
    
    try:
        response = urllib3.request("GET",url)
        if response.status == 200:
            content = response.data
            return content
    except ConnectTimeout:
        raise ConnectTimeout(url)
    
def rewrite_url(
    url: str,
    new_scheme: str | None = None,
    new_netloc: str | None = None,
    new_path: str | None = None,
    new_params: dict | None = None,
    remove_params: bool = False,
    new_query: dict | None = None,
    remove_query: bool = False,
    new_fragment: str | None = None,
    remove_fragment: bool = False,
) -> str:
    '''
    Rewrites the URL with new components. 
    If a component is not provided, it will keep the original one.
    '''
    _parsedUrl = urlparse(url)
    dict_query = parse_qs(_parsedUrl.query)
    dict_params = parse_qs(_parsedUrl.params)

    # Update query
    if new_query:
        for key, value in new_query.items():
            dict_query[key] = [str(value)]
        new_query_string = urlencode(dict_query, doseq=True)
    else:
        new_query_string = _parsedUrl.query if not remove_query else ''

    # Update params
    if new_params:
        for key, value in new_params.items():
            dict_params[key] = [str(value)]
        new_params_string = urlencode(dict_params, doseq=True)
    else:
        new_params_string =  _parsedUrl.params if not remove_params else ''

    # Update other parts of the URL
    scheme = new_scheme if new_scheme else _parsedUrl.scheme
    netloc = new_netloc if new_netloc else _parsedUrl.netloc
    path = new_path if new_path else _parsedUrl.path
    fragment = new_fragment if new_fragment else _parsedUrl.fragment

    # Reconstruct the URL
    return urlunparse((scheme, netloc, path, new_params_string, new_query_string, fragment))

def get_html_by_selenium(url:str)->str:
    """
    Stáhne HTML obsah stránky pomocí Selenium WebDriver.

    Args:
        url (str): URL adresa stránky.
    
    Returns:
        str: HTML obsah stránky.
    """
    driver.get(url)
    return driver.page_source