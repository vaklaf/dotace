'''
Module for Zlínský region
'''
import json
import csv

import pandas as pd
import urllib3

from pathlib import Path
from bs4 import BeautifulSoup as bs
from random import randint
from datetime import datetime as dt
from time import sleep
from enum import Enum
from itertools import cycle

from src.apis.events import post_event
from src.library.uitilities import build_output_path
from src.library.uitilities import get_html_content
from src.library.uitilities import inject_timestamp_to_file_name
from src.library.uitilities import rewrite_url
from src.library.custom_enums import CurrencySymbolPosition as CSP
from .schemes.ischema import IScheme
from .schemes.cls_zlk_schemes import ZlkTitulyScheme,ZlkDtlScheme
from .cls_abstract_region import AbstractRegion
from src.library.downloader.file_downloader import clear_downloads_folder


PDF_FILES = 'pdf_files'
KEY_WORDS: list = ['vysledky', 'výsledky','rozhodnuti','rozhodnutí','podporene','podpořené']

class ZlkRegion(AbstractRegion):
    '''
    Class for Zlínský kraj region
    '''
    _key: str = 'zlk'
    _urls:list[tuple[str,IScheme]] = [
        (
            'https://zlinskykraj.cz/archiv-dotaci?f-year=2021',
            ZlkTitulyScheme
        ),
        (
            'https://zlinskykraj.cz/aktualne-vyhlasene-vyzvy-dotacnich-programu-zlinskeho-kraje',
            ZlkTitulyScheme
        )
    ]

    archived_years:list[str] = []

    def __init__(self,params: dict,output_suffix:str)->None:
        self._name = params
        self.output_path = build_output_path(Path(
            params['paths']['outputs_root']), params['paths']['output_folder_prefix'], self._key)
        self.output_files_suffix = output_suffix

    def crawl(self):

        post_event('start_porocess_region', {'module':__name__,'data':{'data': self._name}})
        url = self._urls[0][0]
        scheme:IScheme = self._urls[0][1]
        headers = scheme.get_sorted_scheme_members()
        headers_advanced = ['ROK','ZDROJ']+headers
        all_data:pd.DataFrame = pd.DataFrame({},columns=headers_advanced)
        #1 get_range_of_archived_years
        content = get_html_content(url)
        soup = bs(content,'html.parser')

        select_element = soup.find_all('select',{'id':'rok'})
        years = [o.text for o in select_element[0].find_all('option')]

        pagination = soup.find('p',class_='pagination')

        sorted_years =  sorted(years[1:])

        for year in sorted_years:
            post_event('processing_year',{'module':__name__,'data':{'data':year}})
          
            # Builing new url, finding first page for currently prcessed year.
            new_url = rewrite_url(url, new_query= {'f-year':year,'page':1})
            post_event('processing_page',{'module':__name__,'data':{'data':str(1)}})
            # Fetching content and processing in by BS.
            content = get_html_content(new_url)
            soup = bs(content,'html.parser')
            # Trying found p element with class name not_found_item
            p_not_found_element  = soup.find('p',class_='not_found_item')

            # If p_not_found_element exists, skipping next steps a continue with next year.
            if p_not_found_element:
                post_event('no_data_exist', {'module':__name__,'data':{'data':f'{self._key}:{year}:{p_not_found_element.text}'}})
                continue

            # Otherwise I am looking for element p with classname pagination.
            # This element always exists when p_not_found_element doesn't.
            pagination = soup.find('p',class_='pagination')
            # Looking for all links in pagination. Count of a tags gives me
            # information how many next rounds for looping will be needed.
            a_pages = pagination.find_all('a')
            pages_count = len(a_pages)
            post_event('total_pages_to_process',{'module':__name__,'data':{'data':pages_count}})

            # Trying to get dat from the first page
            data = self._get_appeals_list(content)
            # If data exists creating temporary pd.DataFrame, which
            # in the next step concatenate with all_data pd DataFrame.
            # After concatenation cleaning temporary dataframe.
            if data:
                df_tmp = pd.DataFrame.from_records(data,columns=headers)
                df_tmp.insert(0,'ROK',year)
                df_tmp.insert(1,'ZDROJ',new_url)
                all_data = pd.concat([all_data,df_tmp],ignore_index=True)
                df_tmp = None
            else:
                continue

            # If pages_count is greater then 1 going through next runs
            # Because the page 1 has been processed setting up start page to 2.
            if pages_count > 1:

                # While page is lower then pages_count + 1
                # Building new new_url, fetching and processing new content
                # and concatenate it with all data.
                for i in range (2,pages_count+1):
                    post_event('processing_page',{'module':__name__,'data':{'data':str(i)}})
                    new_url = rewrite_url(url, new_query={'f-year':year,'page':i})

                    data = self._get_appeals_list(content)
                    df_tmp = pd.DataFrame.from_records(data,columns=headers)
                    df_tmp.insert(0,'ROK',year)
                    df_tmp.insert(1,'ZDROJ',new_url)
                    all_data = pd.concat([all_data,df_tmp],ignore_index=True)
                    df_tmp = None
            # If only one page exists skipping next steps and continue to next year.
            else:
                continue

            post_event('processed_year',{'module':__name__,'data':{'data':year}})
        
        csv_file = f'{self._key}_tituly_{self.output_files_suffix}.csv'

        __class__._write(all_data,self.output_path,csv_file)
        
        scheme = ZlkDtlScheme()
        columns = scheme.get_sorted_scheme_members()
        download_folder = self.output_path / 'files'
        clear_downloads_folder(download_folder)
        
        df_details = pd.DataFrame([],columns=columns)
        
        details:list=[]
        titles = list(all_data['TITUL'])
        urls = list(all_data['DETAIL_LINK'])
        
        print(f'{len(titles)}:{len(urls)}')
        details_links = zip(titles,urls)
        
        for z in details_links:

            content = get_html_content(z[1])
            if content:
                details =  self._get_appeal_details(content)
            else:
                post_event('no_data_exists',{'module':__name__,'data':{'data':z[1]}})
            
            
            r:list = []
            rs:list[list[str]] = []
            if details:
                
                details_count = len(details)   

                for idx,detail in enumerate(details):
                    detail = list(detail)
                    detail[0] = inject_timestamp_to_file_name(detail[0],self.output_files_suffix)
                    _r = list(z)+list(detail) + [details_count,idx+1]
                    if _r not in rs:
                        post_event('file_found',{
                            'module':__name__,
                            'data':{
                                'data':detail[0]
                            },
                            'file':{
                                'path':download_folder,
                                'url':detail[1],
                                'file_name':detail[0]
                            }
                        })
                        rs.append(_r)
                
                df_tmp =  pd.DataFrame.from_records(rs,columns=columns)
                df_details = pd.concat([df_details,df_tmp],ignore_index=True)
                df_tmp = None
                rs = []
                                         
                sleep(randint(7,10))
            
            else:
                continue
                
        details_csv_file = self.output_path / f'{self._key}_details_{self.output_files_suffix}.csv'
                
        df_details.to_csv(details_csv_file,index=False)
                   
        post_event('end_porocess_region', {'module':__name__,'data':{'data': self._name}})

    def _get_appeals_list(self,content:str)->list[list[str]]:
        appeals:list = []
        rows:list = []
        _row:list = []


        appeals_list = bs(content,'html.parser').find('div', class_='appeals-list')

        appeals = appeals_list.find_all('div',class_='appeals-list-item')
        
        post_event('rows_found',{'module':__name__,'data':{'data':len(appeals)}})

        for appeal in appeals:
            p_h3 = appeal.find('p',class_='h3')
            _row.append(p_h3.text)
            div_element =  appeal.find('div')

            if div_element:
                for element in div_element.find_all(recursive=False):
                    if element.name == 'p':
                        a_tag = element.find('a')
                        if a_tag:
                            _row.append(a_tag['href'])
                        else:
                            for span_tag in element.find_all('span'):
                                text_after_span = ""
                                next_element = span_tag.next_sibling
                                while next_element and next_element != 'span' and next_element.name !='a':
                                    if isinstance(next_element,str):
                                        text_after_span = next_element
                                    if next_element.name == 'br':
                                        break
                                    next_element = next_element.next_sibling
                                cleaned_text = text_after_span.strip()
                                if cleaned_text:
                                    _row.append(cleaned_text)
                                else:
                                    _row.append('')
            if _row not in rows:
                rows.append(_row)
                _row = []

        rows = list(map(lambda row: (row[:5] + [row[5].split()[1]] + [row[5].split()[3]] + row[6:]), rows))

        return rows
    
    def _get_appeal_details(self, content: str)->list[tuple[str,str]]:
        
        soup = bs(content, 'html.parser')
        file_list = soup.find('div', class_='files-list')
        filtered_links: list = []
        if file_list:
            all_links = file_list.find_all('a')
            filtered_links = [
                (str.strip(link.text.split('(')[0]),link['href']) for link in all_links
                if any(keyword in link.text.lower() for keyword in KEY_WORDS)
            ]
            
        return filtered_links
        

    @staticmethod        
    def _write(df:pd.DataFrame,opath:Path,file_name:str,sep=';'):
        post_event('create_output_file',{'module':__name__,'data':{'data':file_name}})
        df.to_csv(opath / file_name,index=False,sep=sep)
        post_event('output_file_created',{'module':__name__,'data':{'data':file_name}})
    
    def __str__(self):
        return f'{self._name} region'