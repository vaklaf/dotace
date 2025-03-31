from dataclasses import dataclass

from .ischema import IScheme
from src.library.custom_enums import DataType

@dataclass
class PlkTitulyScheme(IScheme):
    ''' Scheme for `Dotační tituly`'''
    NAZEV_ODBORU = ('nazevodboru',DataType.STR,1)
    NAZEV_PROGRAMU = ('nazevprogramu',DataType.STR,2)
    NAZEV_TITULU = ('nazev_titulu',DataType.STR,3)
    ROK_TITULU = ('roktitulu',DataType.STR,4)
    ZADOSTI_OD = ('zadostiod',DataType.DATE,5)
    ZADOSTI_DO = ('zadostido',DataType.DATE,6)
    
    
    def get_list_values(self) -> list[tuple[str,int]]:
        '''
        Get list of values
        '''
        return [
                (self.NAZEV_ODBORU[0],self.NAZEV_ODBORU[1]), 
                (self.NAZEV_PROGRAMU[0],self.NAZEV_PROGRAMU[1]), 
                (self.NAZEV_TITULU[0],self.NAZEV_TITULU[1]), 
                (self.ROK_TITULU[0],self.ROK_TITULU[1]), 
                (self.ZADOSTI_OD[0],self.ZADOSTI_OD[1]), 
                (self.ZADOSTI_DO[0],self.ZADOSTI_DO[1]), 
            ]
        

@dataclass
class PlkZadostiScheme(IScheme):
    '''
    Scheme for requests
    '''
    NAZEV_TITULU =  ('nazevtitulu',DataType.STR,1)
    ROK_TITULU = ('roktitulu',DataType.STR,2)
    SUCJECT_IC = ('subjektic',DataType.STR,3)
    SUBJECT_NAZEV = ('subjektnazev',DataType.STR,4)
    ZADOST_CISLO = ('cislozadosti',DataType.STR,5)
    AKCE_NAZEV = ('nazevakce',DataType.STR,6)
    CASTKA_POZADOVANA = ('pozadovanacastka',DataType.FLOAT,7)
    CASTKA_SCHVALENA = ('schvalenacastka',DataType.FLOAT,8)
    CASTKA_CERPANA =  ('cerpanacastka',DataType.FLOAT,9)
    DATUM_PODPISU_SMLOUVY = ('datumpodpisusmlouvy',DataType.DATE,10)
    ZADOST_STAV = ('stavzadosti',DataType.STR,11)

 
    def get_list_values(self) -> list[tuple[str,int]]:
        '''
        Get list of values
        '''
        return [
                (self.NAZEV_TITULU[0],self.NAZEV_TITULU[1] ),
                (self.ROK_TITULU[0],self.ROK_TITULU[1] ),
                (self.SUCJECT_IC[0],self.SUCJECT_IC[1] ),
                (self.SUBJECT_NAZEV[0],self.SUBJECT_NAZEV[1]), 
                (self.ZADOST_CISLO[0],self.ZADOST_CISLO[1] ),
                (self.AKCE_NAZEV[0],self.AKCE_NAZEV[1] ),
                (self.CASTKA_POZADOVANA[0],self.CASTKA_POZADOVANA[1] ),
                (self.CASTKA_SCHVALENA[0],self.CASTKA_SCHVALENA[1] ),
                (self.CASTKA_CERPANA[0],self.CASTKA_CERPANA[1] ),
                (self.DATUM_PODPISU_SMLOUVY[0],self.DATUM_PODPISU_SMLOUVY[1] ),
                (self.ZADOST_STAV[0],self.ZADOST_STAV[1])
            ]
        

@dataclass
class PlkZadostIndividualniScheme(IScheme):
    '''
    Scheme for individual requests
    '''
    SUCJECT_IC = ('subjektic',DataType.STR,1)
    SUBJECT_NAZEV = ('subjektnazev',DataType.STR,2)
    ZADOST_CISLO = ('cislozadosti',DataType.STR,3)
    AKCE_NAZEV = ('nazevakce',DataType.STR,4)
    CASTKA_POZADOVANA = ('pozadovanacastka',DataType.FLOAT,5)
    CASTKA_SCHVALENA = ('schvalenacastka',DataType.FLOAT,6)
    CASTKA_CERPANA =  ('cerpanacastka',DataType.FLOAT,7)
    DATUM_PODPISU_SMLOUVY = ('datumpodpisusmlouvy',DataType.DATE,8)
    ZADOST_STAV = ('stavzadosti',DataType.STR,9)

    def get_list_values(self)-> list[tuple[str,int]]:
        '''
        Get list of values
        '''
        return [
            (self.SUCJECT_IC[0],self.SUCJECT_IC[1]),
            (self.SUBJECT_NAZEV[0],self.SUBJECT_NAZEV[1]),
            (self.ZADOST_CISLO[0],self.ZADOST_CISLO[1]),
            (self.AKCE_NAZEV[0],self.AKCE_NAZEV[0]),
            (self.CASTKA_POZADOVANA[0],self.CASTKA_POZADOVANA[1]),
            (self.CASTKA_SCHVALENA[0],self.CASTKA_SCHVALENA[1]),
            (self.CASTKA_CERPANA[0],self.CASTKA_CERPANA[1]),
            (self.DATUM_PODPISU_SMLOUVY[0],self.DATUM_PODPISU_SMLOUVY[1]),
            (self.ZADOST_STAV[0],self.ZADOST_STAV[1])
            ]
        

