'''Main entry point of the application'''
import yaml

from .lib.uitilities import get_output_file_time_suffix
from .lib.logger.logger import setup_logger
from .lib.cls_regions import Regions
from .api.logger_listener import setup_logger_event_handlers
from .lib.regions.schemes.cls_plk_schemes import *

def load_configuration()-> dict:
    # '''Loads the configuration from the configuration file'''
    with open('configuration.yml', 'r',encoding='utf-8') as ymlfile:
        return yaml.safe_load(ymlfile)
    


def main():
    '''Main entry point of the application'''
    _output_sufix = get_output_file_time_suffix()
    _cfg = load_configuration()
    setup_logger(_cfg['paths']['logs_root'],_output_sufix)
    setup_logger_event_handlers()
    rgns = Regions(_cfg,_output_sufix)
    rgns.crawl()

def run():
    '''Runs the application'''
    main()
