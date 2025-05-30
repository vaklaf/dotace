'''Main entry point of the application'''
import yaml

from .library.utilities.others import get_output_file_time_suffix
from .library.logger.logger import setup_logger
from .library.cls_regions import Regions
from .apis.logger_listener import setup_logger_event_handlers
from .apis.downloader_listener import setup_downloader_events_listener
from .library.regions.schemes.cls_plk_schemes import *

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
    setup_downloader_events_listener()
    rgns = Regions(_cfg,_output_sufix)
    rgns.crawl()

def run():
    '''Runs the application'''
    main()
