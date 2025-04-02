''' Třída pro zpracování jednotlivých regionů '''

import importlib.machinery
import os

from requests.exceptions import ConnectTimeout

from ..apis.events import post_event

class Regions:
    ''' Třída pro zpracování jednotlivých regionů '''

    def __init__(self, cofiguration,output_suffix):
        self._regions: dict = {
            k: v for k, v in cofiguration['regions'].items() if v['process'] == 1}
        self._configuration = cofiguration
        self._output_suffix = output_suffix

    def crawl(self):
        ''' Provede crawling jednotlivých regionů '''

        for key, value in self._regions.items():
            try:
                # Dynamický import modulu
                module_path = os.path.abspath(
                    os.path.join(os.path.dirname(__file__),
                                 'regions', f'cls_{key}_region.py'))
                loader = importlib.machinery.SourceFileLoader(
                    f'src.library.regions.cls_{key}_region', module_path)
                spec = loader.load_module()

                loader.exec_module(spec)

                # # Dynamické volání třídy
                class_name = f'{key.capitalize()}Region'
                region_class = getattr(spec, class_name)
                region_instancne = region_class(
                    {key: value, 'paths': self._configuration['paths']},
                    self._output_suffix)

                # # Zavolání metody crawl
                region_instancne.crawl()

            except ImportError:
                post_event('module_not_found',{'module':__name__,'data':{'data':class_name}})
            except AttributeError as err:
                print(f'Error1: {err}')
            except ConnectTimeout as err:
                post_event('connection_error',{'module':__name__,'data':{'data':err}})
            except Exception as err:
                print(f'Error2: {err}')
