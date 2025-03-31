from enum import Enum


class DataType(Enum):
    STR = 1
    DATE = 2
    INT = 3
    FLOAT = 4
    
class CurrencySymbolPosition(Enum):
    IN_FRONT = 1
    BEHIND = 2