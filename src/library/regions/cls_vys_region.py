'''
Module for Plzensky kraj region
'''
import json
import csv

import pandas as pd
import urllib3

from urllib.parse import urlencode, urlunparse, urlparse
from pathlib import Path
from bs4 import BeautifulSoup as bs
from random import randint
from time import sleep
from enum import Enum

from src.apis.events import post_event
from src.library.uitilities import build_output_path
from src.library.uitilities import get_html_content
from src.library.transformation_by_data_type import cut_off_currency
from src.library.transformation_by_data_type import remove_nbsp
from src.library.transformation_by_data_type import format_number_for_excel
from src.library.custom_enums import CurrencySymbolPosition as CSP
from .schemes.ischema import IScheme
from .schemes.cls_vys_schemes import VysTitulyScheme,VysZadostiScheme
from .cls_abstract_region import AbstractRegion



class Scope(Enum):
    TTILES = 0
    APPLICATIONS = 1

class VysRegion(AbstractRegion):
    '''
    Class for Plzensky kraj region
    '''
    _key: str = 'vys'
    _urls:list[tuple[str,IScheme]] = [
        (
            'https://www.fondvysociny.cz/dotace/default/vse?kat=999',
            VysTitulyScheme
        )
    ]
    
    
    def __init__(self,params: dict,output_suffix:str)->None:
        self._name = params
        self.output_path = build_output_path(Path(
            params['paths']['outputs_root']), params['paths']['output_folder_prefix'], self._key)
        self.output_files_suffix = output_suffix
        
    def crawl(self):
        
        post_event('start_porocess_region', {'module':__name__,'data':{'data': self._name}})
        for url_idx,_ in enumerate(self._urls):
            url = self._urls[url_idx][0]
            parsed_url =  urlparse(url)
            scope = parsed_url.path.split('/')[2]
            # Step 1 - All titles
            csv_file = f'{self._key}_{scope}_{self.output_files_suffix}.csv'
            scheme:IScheme = self._urls[url_idx][1]
            headers:list[str] = scheme.get_sorted_scheme_members()
            content = get_html_content(url)
            data_rows:list[list[str]] = self._parse_content(content,scope=Scope.TTILES)
            df = pd.DataFrame.from_records(data_rows,columns=headers)
            df.insert(0,'ZDROJ',url)
            __class__._write(df,self.output_path,csv_file)
            # # Step 2 - Get requsest
            _paths = list(df[headers[0]].unique())
            scheme = VysZadostiScheme
            headers = scheme.get_sorted_scheme_members()
            headers.insert(0,'ZDROJ')
            scope = _paths[0].split('/')[2]
            csv_file = f'{self._key}_{scope}_{self.output_files_suffix}.csv'
            df = pd.DataFrame({},columns=headers)
            for _path in _paths:
                new_url = urlunparse((parsed_url.scheme, parsed_url.netloc,
                             _path, parsed_url.params, parsed_url.query, parsed_url.fragment))
                content = get_html_content(new_url)
                sleep(randint(5,15))
                data_rows = self._parse_content(content,Scope.APPLICATIONS)
                if data_rows == [['']]:
                    post_event('no_applications_found',{'module':__name__,'data':{'data':new_url}})
                    continue
                df_x = pd.DataFrame.from_records(data_rows,columns=headers[1:])
                df_x.insert(0,'ZDROJ',new_url)
                df = pd.concat([df,df_x],ignore_index=True)
                data_rows = []
                df_x = pd.DataFrame(None)
                
                __class__._write(df,self.output_path,csv_file)
            
            
        post_event('end_porocess_region', {'module':__name__,'data':{'data': self._name}})
        
        
    def _parse_content(slef,content:str,scope:Scope)->list[list[str]]:
        data:list[list[str]] = []
        rows = [] 
        soup = bs(content,'html.parser')
        _row:list = []
        
        if scope == Scope.TTILES:
            rows = soup.find_all('tr',class_='barva')
            post_event('rows_found',{'module':__name__,
                'data':{'data':
                    {'scope':scope.name,'rows':len(rows)}}})
            
            for ridx,row in enumerate(rows):
                tds = row.find_all('td')
                for tidx,td in enumerate(tds):
                    
                    match tidx:
                        case 0:
                            _row.append(td.find('a',href=True)['href'])
                            _row.append(td.text)
                        case 3:
                            _row.append(remove_nbsp(td.text.strip(" ,")))
                        case 4:
                            _row.append(format_number_for_excel(
                                remove_nbsp(
                                    cut_off_currency(td.text,'Kč',CSP.BEHIND))))
                        case _:
                            _row.append(remove_nbsp(td.text))
                        
                        
                    if _row in data:                
                        continue
                    
                data.append(_row)
                _row = []
            
        
        elif scope == Scope.APPLICATIONS:
            container  = soup.find('div',class_='container')
            if container:                       
                tables = container.find_all('table')
                print(f'Nalezno {len(tables)} tabulek')
                relevant_tables = tables[3:]
                if  relevant_tables==[]: 
                    return [['']]
                print(f'Relevantních tabulek {len(relevant_tables)}')
                
                for table in relevant_tables:
                    rows = table.find_all('tr')
                    post_event('rows_found',{'module':__name__,
                        'data':{'data':
                            {'scope':scope.name,'rows':len(rows)-1}}})

                    print(len(rows[1:]))
                    for row in rows[1:]:
                        #print(f'Zpracovávám řádek {idx+1} z {len(rows)}.')
    
                        tds = row.find_all('td')
                        for tidx,td in enumerate(tds):

                            match tidx:
                                case 6:
                                    _row.append(td.text)
                                    a = td.find('a',href=True)
                                    _row.append(a['href'] if not a is None else ' ' )
                                case 3,4,5:
                                    _row.append(format_number_for_excel(
                                        remove_nbsp(td.txt)
                                    ))
                                case _:
                                    _row.append(remove_nbsp(td.text))
                        
                            if _row  in data:
                                continue
                            
                        data.append(_row)   
                        _row = []
         
        return data
    
    @staticmethod        
    def _write(df:pd.DataFrame,opath:Path,file_name:str,sep=';'):
        post_event('create_output_file',{'module':__name__,'data':{'data':file_name}})
        df.to_csv(opath / file_name,index=False,sep=sep)
        post_event('output_file_created',{'module':__name__,'data':{'data':file_name}})
    
    def __str__(self):
        return f'{self._name} region'