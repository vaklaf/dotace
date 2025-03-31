from dataclasses import dataclass

from .ischema import IScheme
from ....library.custom_enums import DataType


@dataclass
class VysTitulyScheme(IScheme):
    ZADOSTI_URL = ('zadostiurl',DataType.STR,1)
    TITUL_ID = ('titulid', DataType.STR,2)
    TYP_PROGRAMU = ('typprogramu',DataType.STR,3)
    NAZEV_PROGRAMU = ('nazevprogamu',DataType.STR,4)
    KONTAKTNI_OSOBY = ('kontaktniosoby',DataType.STR,5)
    FIN_ALOKACE = ('alokace',DataType.FLOAT,6)
    DATUM_ZAHAJENI_SBERU_ZADOSTI = ('datumzacatkusberuzadosti',DataType.DATE,7)
    DATUM_UKONCENI_SBERU_ZADOSTI = ('datumkoncesberuzadosti',DataType.DATE,8)
    
@dataclass
class VysZadostiScheme(IScheme):
    ZADOST_ID = ('zadostid',DataType.STR,1)
    ZADATEL_NAZEV = ('zadatelnazev',DataType.STR,2)
    PROJEK_NAZEV = ('projektnazev',DataType.STR,3)
    CASTKA_POZADOVANA = ('castkapozadovana',DataType.FLOAT,4)
    CASTKA_SCHVALENA = ('castkaschvalena',DataType.FLOAT,5)
    CASTKA_VYPLACENA = ('castkavyplacena',DataType.FLOAT,6)
    USNESENI =  ('usneseni',DataType.STR,7)
    USENESENI_LINK = ('usnesenivysledek',DataType.STR,8)