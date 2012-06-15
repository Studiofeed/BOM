'''
Created on 2012-04-25

@author: timvb
'''

import urllib, urllib2
from bs4 import BeautifulSoup

class VendorParserError(Exception):
    pass

class BaseVendorParser(object):
    '''
    A Base Vendor Parser object.  This will store all generic vendor information and provide method definitions to override
    '''


    def __init__(self, url=None, dataVar=None):
        '''
        Constructor
        '''
        self.url = url
        user_agent = 'Mozilla/5 (Solaris 10) Gecko'
        self.urlheaders = { 'User-Agent' : user_agent }
        self.dataVar = dataVar
        self.soup = None
        self.component = VendorComponent()
        self.maxTries = 5
    
    def parse(self, id):
        '''
        parse the vendor and return a VendorComponent
        '''    
        
        pass
    
    def buildUrl(self, id):
        
        return self.url + id
    
    def getPage(self, id):
        '''
        data = urllib.urlencode({self.dataVar: id})
        req = urllib2.Request(self.url, data, self.urlheaders)
        page  = urllib2.urlopen(req)
        if page:
            return page.read() 
        else: return None
        '''
        pass

class VendorComponent(object):
    '''
    An object which will store information on a single component retrieved from a vendor parse
    
    '''
    
    def __init__(self, **kwargs):
        
        self.vendor = kwargs.get('vendor', None)
        self.vendorNumber = kwargs.get('vendorNumber', None)
        self.manufacturer = kwargs.get('manufacturer', None)
        self.manufacturerNumber = kwargs.get('manufacturerNumber', None)
        self.description = kwargs.get('description', None)
        self.quantityAvailable = kwargs.get('quantityAvailable', 0)
        self.package = kwargs.get('package',None)
        self.prices = {}
        