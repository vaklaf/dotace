from .custom_enums import DataType,CurrencySymbolPosition as CSP
from typing import Any

NON_BREAKING_SPACE_UNI = '\xa0'

def transformation_by_data_type(value:Any,dataType:DataType):
    
    def catoff_time_part(value:str)->str:
        return value[:10]
    
    def change_date_format(value:str)->str:
        parts:list=value.split('-')
        return f'{parts[2]}.{parts[1]}.{parts[0]}'
    
    def transform_date(value:str)->str:
        return change_date_format(catoff_time_part(value))

    def replace_dec_dot_by_dec_comma(value:str)->str:
        return value.replace('.', ',')[:-2]
    
    transformations:dict = {
        DataType.DATE:transform_date,
        DataType.FLOAT:replace_dec_dot_by_dec_comma
    }
    
    if dataType not in transformations or value is None:
        return value
    else:
        return transformations[dataType](value)
    

def cut_off_currency(value:str,currency_symbol:str,symbol_position:CSP)->str:
    _symbol_length = len(currency_symbol)
    return value[:-_symbol_length] if symbol_position==CSP.BEHIND else value[_symbol_length+1:]


def remove_nbsp(value)->str:
    return value.replace(NON_BREAKING_SPACE_UNI, '')

def format_number_for_excel(value)->str:
    _number = float(value.replace(',','.'))
    return f"{_number:.2f}".replace('.', ',')