'''
This module contains the event handlers for the logger.
'''

from .events import subscirbe
from  ..library.logger.loglevel import LogLevel
from  ..library.logger.custom_message import CustomMessage
from  ..library.logger.logger import log


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
    
def handle_processing_year(data):
    log(LogLevel.INFO,{'module':data['module'],
         'message':' Processing_year:',
         'data':data['data']
         })

def handle_processed_year(data):
    log(LogLevel.INFO,{'module':data['module'],
         'message':' Year processed.',
         'data':data['data']
         })
    
def handle_no_data_exist(data):
    log(LogLevel.WARNING,{'module':data['module'],
         'message':' No data exists.',
         'data':data['data']
         })

def handle_total_pages_to_process(data):
    log(LogLevel.INFO,{'module':data['module'],
         'message':'Pages to process',
         'data':data['data']
         })
    
def handle_processing_page(data):
    log(LogLevel.INFO,{'module':data['module'],
         'message':'Pages to process',
         'data':data['data']
         })
    
def handle_connection_error(data):
    log(LogLevel.CRITICAL,{'module':data['module'],
         'message':'Pages to process',
         'data':data['data']
         })
    
def handle_file_already_exists_error(data):
    log(LogLevel.ERROR,{'module':data['module'],
         'message':'File already exists.',
         'data':data['data']
         })
    
def handle_folder_cannot_be_created_error(data):
    log(LogLevel.ERROR,{'module':data['module'],
         'message':'Folder cannot be created.',
         'data':data['data']
         })

def handle_downloading_failure_error(data):
    log(LogLevel.CRITICAL,{'module':data['module'],
         'message':'Downloading failure.',
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
    subscirbe('processing_year',handle_processing_year)
    subscirbe('processed_year',handle_processed_year)
    subscirbe('no_data_exist',handle_no_data_exist)
    subscirbe('total_pages_to_process',handle_total_pages_to_process)
    subscirbe('processing_page',handle_processing_page)
    subscirbe('connection_error',handle_connection_error)
    subscirbe('file_already_exists_error',handle_file_already_exists_error)
    subscirbe('folder_cannot_be_created_error',handle_folder_cannot_be_created_error)
    subscirbe('downloading_failure_error',handle_downloading_failure_error)