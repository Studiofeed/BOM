'''
Created on 2012-04-25

@author: timvb
'''

import urllib2, urllib
from vendor import BaseVendorParser, VendorParserError
import bs4
from bs4 import BeautifulSoup

class DigikeyVendorParser(BaseVendorParser):
    
    def __init__(self):
        BaseVendorParser.__init__(self, url='http://search.digikey.com/scripts/DkSearch/dksus.dll', dataVar='name')
        self.component.vendor = 'Digikey'
        
        #Define vendor headers and corresponding VendorComponent Attributes
        self.headers = {'Digi-Key Part Number':'vendorNumber',
                        'Manufacturer':'manufacturer',
                        'Manufacturer Part Number':'manufacturerNumber',
                        'Description':'description',
                        'Quantity Available': 'quantityAvailable'}
        

        

    def parse(self, id):
        '''
        Parse the page for required info, return a vendor component
        '''
        retry_count = 0
        page = self.getPage(id)
        self.soup = BeautifulSoup(page)
        try:
            #Get price info
            self.parsePricing()
            
            #Get part info
            self.parseInfo()
        except:
            #retry
            retry_count += 1
            if retry_count >= self.maxTries:
                raise VendorParserError('Max Retries exceeded')
            self.parse(id)
        return self.component
        
    def parsePricing(self):
        '''
        Get the pricing structure for this part
        '''
        
        
        priceTable = self.soup.find('table', id='pricing')
        
        prices = priceTable.findChildren('tr')[1:]
        
        for priceRow in prices:
            tmp = priceRow.findAll('td')
            quantity = int(tmp[0].contents[0].replace(',',''))
            price = float(tmp[1].contents[0].replace(',',''))
            
            del tmp
            
            self.component.prices[quantity] = price
           
        
        
    
    def parseInfo(self):
        '''
        parse the part info
        '''
        
        for (searchTerm, attribute) in self.headers.items():
            
            value = self._parsePartAttribute(searchTerm)
            self.component.__setattr__(attribute, value)
        
    def _parsePartAttribute(self, searchTerm, func=str):
        '''
        Searches the page for the text given, returns the value of the next item in the parent
        '''     
       
        #Find attribute table header tag
        attrTag = self.soup.find('th', text=searchTerm)
        
        #Get parent table row
        attrParent = attrTag.find_parent('tr')
        
        #select next table data
        value = attrParent.find_next('td').contents[0]
        
        #check if value is a Tag
        if isinstance(value, bs4.Tag):
            value = value.contents[0]
            pass
        return func(value)

    def getPage(self, id):
        encoded = urllib.urlencode({self.dataVar : str(id)})
        data = 'Detail&' + encoded
        url = self.url + '?' + data
        
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5 (Solaris 10) Gecko')
        page = urllib2.urlopen(url)
        
        return page.read()
if __name__ == "__main__":
    
    id = '5001K-ND'
    
    parser = DigikeyVendorParser()
    component = parser.parse(id)
    
    print component.vendorNumber
    print component.quantityAvailable
    print component.prices