''' Středo český kraj region class. '''
from pathlib import Path

from src.apis.events import post_event
from src.library.uitilities import build_output_path
from src.library.uitilities import inject_timestamp_to_file_name
from .cls_abstract_region import AbstractRegion
from src.library.downloader.file_downloader import clear_downloads_folder

class StcRegion(AbstractRegion):
    '''
    Class for Zlínský kraj region
    '''
    _key: str = 'stc'
    _urls:list[str] = [
            'https://stredoceskykraj.cz/documents/36434/20021177/prehled_zadosti_dotace.xlsx'
    ]
    
    def __init__(self,params: dict,output_suffix:str)->None:
        self._name = params
        self.output_path = build_output_path(Path(
            params['paths']['outputs_root']), params['paths']['output_folder_prefix'], self._key)
        self.output_files_suffix = output_suffix

    def crawl(self):

        post_event('start_porocess_region', {'module':__name__,'data':{'data': self._name}})
        url = self._urls[0]
        
        file_name = url.split('/')[-1]
        file_name = inject_timestamp_to_file_name(file_name, self.output_files_suffix)
        
        post_event('file_found',{
                            'module':__name__,
                            'data':{
                                'data':file_name
                            },
                            'file':{
                                'path':self.output_path,
                                'url':url,
                                'file_name':file_name
                            }
                        })
        
        post_event('end_porocess_region', {'module':__name__,'data':{'data': self._name}})