from dataclasses import dataclass

from .ischema import IScheme
from ....library.custom_enums import DataType


@dataclass
class ZlkTitulyScheme(IScheme):
    TITUL = ('titulid', DataType.STR,2,'merge')
    OBLAST = ('typprogramu',DataType.STR,3,'')
    FIN_ALOKACE = ('nazevprogamu',DataType.STR,4,'')
    OZNACENI = ('kontaktniosoby',DataType.STR,5,'')
    DATUM_VYHLASENI = ('datumvyhlaseni',DataType.DATE,6,'')
    DATUM_ZAHAJENI_SBERU_ZADOSTI = ('datumzacatkusberuzadosti',DataType.DATE,7,'')
    DATUM_UKONCENI_SBERU_ZADOSTI = ('datumkoncesberuzadosti',DataType.DATE,8,'')
    DETAIL_LINK = ('detaillink',DataType.STR,9,'merge')
    

class ZlkDtlScheme(IScheme):
    TITUL = ('titulid', DataType.STR,1,'merge')
    DETAIL_LINK = ('detaillink',DataType.STR,2,'merge')
    FILE_NAME = ('filename',DataType.STR,3,'')
    FILE_LINK = ('filelink',DataType.STR,4,'')
    FILES_COUNT = ('Filescount',DataType.INT,5,'')
    FILE_NUMBER = ('flenumber',DataType.INT,6,'')     

