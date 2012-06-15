'''
Created on 2012-04-25

@author: timvb
'''

import urllib2
from bs4 import BeautifulSoup

class BaseVendorParser(object):
    '''
    A Base Vendor Parser object.  This will store all generic vendor information and provide method definitions to override
    '''


    def __init__(self, url=None):
        '''
        Constructor
        '''
        self.url = url
        
    
    def parse(self, id):
        '''
        parse the vendor and return a VendorComponent
        '''    
        
        pass

class VendorComponent(object):
    '''
    An object which will store information on a single component retrieved from a vendor parse
    
    '''
    
    def __init__(self, **kwargs):
        
        self.vendor = kwargs.get('vendor', None)
        self.vendorNumber = kwargs.get('vendorNumber', None)
        self.manufacturerNumber = kwargs.get('manufacturerNumber', None)
        self.description = kwargs.get('description', None)
        self.quantityAvailable = kwargs.get('quantityAvailable', 0)
        self.prices = {}
        