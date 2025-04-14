'''
Module for Plzensky kraj region
'''
import json
import csv
from urllib.parse import urlencode, urlunparse, urlparse
from pathlib import Path
from random import randint
from time import sleep

import requests

from src.apis.events import post_event
from src.library.utilities.others import build_output_path
from src.library.utilities.others import rewrite_url
from src.library.transformation_by_data_type import transformation_by_data_type
from .schemes.ischema import IScheme
from .schemes.cls_plk_schemes import PlkZadostiScheme, PlkZadostIndividualniScheme, PlkTitulyScheme
from .cls_abstract_region import AbstractRegion


class PlkRegion(AbstractRegion):
    '''
    Class for Plzensky kraj region
    '''
    _key: str = 'plk'
    _urls: list = [
        (
            'https://dotace.plzensky-kraj.cz/verejnost/dotacnitituly?_name=DotacniTituly',
            PlkTitulyScheme
        ),
        (
            'https://dotace.plzensky-kraj.cz/verejnost/zadosti?_name=Zadosti&_search=false&nd=1742109491719&rows=25&page=1&sidx=&sord=asc',
            PlkZadostiScheme
        ),
        ('https://dotace.plzensky-kraj.cz/verejnost/individualni-zadosti?_name=IndividualniZadosti&_search=false&nd=1742131019737&rows=25&page=1&sidx=&sord=asc',
         PlkZadostIndividualniScheme
         )
    ]
    _pages_processed: int = 0
    _pages_total: int = 0

    def __init__(self, params: dict,output_suffix:str) -> None:
        self._name = params[self._key]['name']
        self.output_path = build_output_path(Path(
            params['paths']['outputs_root']), params['paths']['output_folder_prefix'], self._key)
        self.output_files_suffix = output_suffix

    def crawl(self):
        '''
        Crawls data from Plzensky kraj region website
        '''

        post_event('start_porocess_region', {'module':__name__,'data':{'data': self._name}})
        for url_idx, _ in enumerate(self._urls):
            if self._pages_total == 0:
                self._get_page({'url_idx':url_idx,'page': 1}, True)
                self._pages_processed += 1

                for i in range(2,self._pages_total + 1):
                    self._get_page({'url_idx':url_idx,'page': i})
                    self._pages_processed += 1
                    sleep(randint(1, 5))

            self._pages_total = 0
            self._pages_processed = 0


        post_event('end_porocess_region', {'module':__name__,'data':{'data': self._name}})

    def _get_page(self, params: dict,is_initial_round: bool = False):
        '''
        Gets the page from the website
        '''
        url_idx = params['url_idx']
        page = params['page']

        parsed_url = urlparse(self._urls[url_idx][0])
        scope = parsed_url.path.split('/')[-1]
        query_params = dict([param.split('=')
                            for param in parsed_url.query.split('&')])

        if page > 1:
            query_params['page'] = str(page)

        new_query = urlencode(query_params)

        new_url = urlunparse((parsed_url.scheme, parsed_url.netloc,
                             parsed_url.path, parsed_url.params, new_query, parsed_url.fragment))

        response = requests.get(new_url,timeout=10)
        response.raise_for_status()

        if response.status_code == 200:
            self._pages_processed += 1
            try:
                data = response.json()
            except json.JSONDecodeError as err:
                print(f"Chyba při parsování JSON: {err}")
                return

        data_rows = []
        
        scheme:IScheme = self._urls[url_idx][1]
        scheme_inst = scheme()
        
        if is_initial_round:
            self._pages_total = data.get('total')

        for item in data.get('rows'):
            cell = item.get('cell')
            row = [transformation_by_data_type(cell.get(attr[0]),attr[1]) for attr in scheme_inst.get_list_values()]
            row.insert(0,f'{parsed_url.scheme}//{parsed_url.netloc}{parsed_url.path}')
            data_rows.append(row)

            csv_file = self.output_path / \
                f'{self._key}_{scope}_{self.output_files_suffix}.csv'

        if is_initial_round is True and page == 1:
            post_event('create_output_file',{'module':__name__,'data':{'data':csv_file}})
            __class__.write_to_csv(
                data_rows, csv_file, scheme.get_sorted_scheme_members(),True)
        else:
            __class__.write_to_csv(data_rows, csv_file,[])

    @staticmethod
    def write_to_csv(data: list, csv_file: Path,header: list, init: bool = False) -> None:
        '''
        Writes data to CSV file
        '''
        with open(csv_file, 'a', newline='\n', encoding="utf-8") as file_handle:
            writer = csv.writer(file_handle,delimiter=';')
            if init is True:
                header.insert(0,'ZDROJ')
                writer.writerow(header)
            writer.writerows(data)

    def __str__(self):
        return f'{self._name} region'
