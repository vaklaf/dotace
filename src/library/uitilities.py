from pathlib import Path
from datetime import datetime as dt
from urllib.parse import urlencode, urlunparse, urlparse,parse_qs

import urllib3

from requests.exceptions import ConnectTimeout


def get_html_content(url)->str:
    
    try:
        response = urllib3.request("GET",url)
        if response.status == 200:
            content = response.data
            return content
    except ConnectTimeout:
        raise ConnectTimeout(url)

def build_output_path(output_root: Path, output_folder_prefix: str, region_key: str) -> Path:
    path = Path().cwd() / output_root / f"{output_folder_prefix}_{region_key}"
    check_output_path(path)
    return path

def check_output_path(output_path: Path) -> None:
    if not output_path.exists():
        output_path.mkdir(parents=True)
    elif not output_path.is_dir():
        raise NotADirectoryError(f"Output path {output_path} is not a directory.")

def get_output_file_time_suffix() -> str:
    return dt.now().strftime('%Y%m%d_%H%M%S')

def rewrite_url(url: str, new_query: dict | None = None) -> str:
        _parsedUrl = urlparse(url)
        dict_query = parse_qs(_parsedUrl.query)

        if new_query:
            for key, value in new_query.items():
                dict_query[key] = [str(value)]
            new_query_string = urlencode(dict_query, doseq=True)
        else:
            new_query_string = _parsedUrl.query

        return urlunparse((_parsedUrl.scheme, _parsedUrl.netloc, _parsedUrl.path, _parsedUrl.params, new_query_string, _parsedUrl.fragment))


def inject_timestamp_to_file_name(file_name:str,timestamp:str)-> str:
    parts = file_name.split('.')
    return f'{parts[0]}_{timestamp}.{parts[1]}'