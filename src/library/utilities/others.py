from pathlib import Path
from datetime import datetime as dt
from urllib.parse import urlencode, urlunparse, urlparse,parse_qs,parse_qsl

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

def rewrite_url(
    url: str,
    new_scheme: str | None = None,
    new_netloc: str | None = None,
    new_path: str | None = None,
    new_params: dict | None = None,
    new_query: dict | None = None,
    new_fragment: str | None = None
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
        new_query_string = _parsedUrl.query

    # Update params
    if new_params:
        for key, value in new_params.items():
            dict_params[key] = [str(value)]
        new_params_string = urlencode(dict_params, doseq=True)
    else:
        new_params_string = _parsedUrl.params

    # Update other parts of the URL
    scheme = new_scheme if new_scheme else _parsedUrl.scheme
    netloc = new_netloc if new_netloc else _parsedUrl.netloc
    path = new_path if new_path else _parsedUrl.path
    fragment = new_fragment if new_fragment else _parsedUrl.fragment

    # Reconstruct the URL
    return urlunparse((scheme, netloc, path, new_params_string, new_query_string, fragment))


def inject_timestamp_to_file_name(file_name:str,timestamp:str)-> str:
    parts = file_name.split('.')
    return f'{parts[0]}_{timestamp}.{parts[1]}'