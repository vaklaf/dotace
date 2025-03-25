'''
This module contains the event handlers for the logger.
'''

from .events import subscirbe
from  ..lib.logger.loglevel import LogLevel
from  ..lib.logger.custom_message import CustomMessage
from  ..lib.logger.logger import log


def handle_module_not_found(data):
    log(LogLevel.CRITICAL,CustomMessage(data={
        'module':data['module'],
        'message':'Module not found',
        'data':data['data']
    }))

def handle_page_not_found(exception):
    '''Handles the page not found event'''
    log(exception)

def handle_start_porocess_region(data):
    '''Handles the start process region event'''
    log(LogLevel.INFO, CustomMessage(data=
        {'module':data['module'],
         'message':'Strarted crawling region',
         'data':data['data']
         })
        )
    
def handle_end_porocess_region(data):
    '''Handles the end process region event'''
    log(LogLevel.INFO,CustomMessage(data=
        {'module':data['module'],
         'message':'Finished crawling region',
         'data':data['data']
         })
        )

def handle_page_crawled(data):
    '''Handles the page crawled event'''
    log(LogLevel.INFO,CustomMessage(data=
        {'module':data['module'],
         'message':'User created',
         'data':data['data']
         })
        )
    
def handle_create_output_file(data):
    ''' Handle the output file creating'''
    log(LogLevel.INFO,CustomMessage(data=
        {'module':data['module'],
         'message':' Creating output file',
         'data':data['data']
         })
        )
         
def handle_output_file_created(data):
    log(LogLevel.INFO, {'module':data['module'],
         'message':' Output file created.',
         'data':data['data']
         })

def handle_no_applications_found(data):
    log(LogLevel.WARNING,{'module':data['module'],
         'message':' No applications found.',
         'data':data['data']
         })
        
def handle_rows_found(data):
    log(LogLevel.WARNING,{'module':data['module'],
         'message':' Rows found:.',
         'data':data['data']
         })

def setup_logger_event_handlers():
    '''Sets up the event handlers for the logger'''
    subscirbe('page_not_found', handle_page_not_found)
    subscirbe('start_porocess_region', handle_start_porocess_region)
    subscirbe('end_porocess_region', handle_end_porocess_region)
    subscirbe('page_crawled', handle_page_crawled)
    subscirbe('create_output_file',handle_create_output_file)
    subscirbe('output_file_created',handle_output_file_created)
    subscirbe('no_applications_found',handle_no_applications_found)
    subscirbe('rows_found',handle_rows_found)

