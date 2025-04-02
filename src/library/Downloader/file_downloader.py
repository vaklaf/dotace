import requests
import shutil

from pathlib import Path

from .exeptions import DownloadingFailure,FolderCannotBeCreated

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