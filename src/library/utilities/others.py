from pathlib import Path
from datetime import datetime as dt


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


def inject_timestamp_to_file_name(file_name:str,timestamp:str)-> str:
    parts = file_name.split('.')
    return f'{parts[0]}_{timestamp}.{parts[1]}'