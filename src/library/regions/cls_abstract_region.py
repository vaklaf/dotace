'''
Created on 25. 11. 2018
'''


from abc import ABC, abstractmethod


class AbstractRegion(ABC):
    '''
    Abstract class for all regions
    '''

    @abstractmethod
    def crawl(self):
        '''
        Abstract method for crawling data from region website
        '''
        
