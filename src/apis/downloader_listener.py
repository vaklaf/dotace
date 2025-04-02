from pathlib import Path
from functools import wraps

from .events import subscirbe
from .events import post_event
from ..library.downloader.file_downloader import download_file


def log(fn):
    
    def wrapper(data):
        post_event('downloading_file',{'module':__name__,
            'data':{
                'data':f"{data['file']['file_name'] } z {data['file']['url']}"
                    }})
        fn(data)     
        post_event('file_downloaded',{'module':__name__,'data':{
                'data':f"{data['file']['file_name'] } z {data['file']['url']}"
                    }})
    return wrapper

@log
def handle_file_found(data: dict):
    file = data['file']    
    download_file(output_path=file['path']
                  ,url=file['url'],file_name=file['file_name'])



def setup_downloader_events_listener():
    subscirbe('file_found',handle_file_found)
