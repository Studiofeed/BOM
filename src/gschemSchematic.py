'''
Created on 2012-03-29

@author: timvb
'''
import re
import vendors

class SchematicComponent(object):
    '''
    A base object for a schematic component.  Keeps track of all individual attributes
    '''
    
    def __init__(self, **kwargs):
        #Mandatory attributes
        self.refdes=None
        self.device=None
        self.value=None
        self.symbol=None
        self.parseVendor=False
        self.attributes = ['refdes', 'value','device','symbol']
        #Initial attributes
        for attr, value in kwargs.items():
            self.setAttribute(attr, value)
            #update component attributes list
            if attr not in self.attributes:
                self.attributes.append(attr)
        
        

    
    def __eq__ (self, y):
        if type(y) != type(self):
            raise TypeError("Comparing object must be of same type")
        eq = True
        
        
        #attrx = self.attributes.remove('refdes')
        #attry = y.attributes.remove('refdes')
        
        for attr in self.attributes:
            if attr == "refdes":
                continue
            if self.getAttribute(attr) != y.getAttribute(attr):
                eq = False
        
        return eq
        
    def __repr__(self):
        return str(self.refdes)+"["+str(self.value)+"]"
    
    def hasAttribute(self, attribute):
        return self.getAttribute(attribute)
            
        
    def getAttribute(self, attribute):
        if attribute in self.attributes:
            return self.__getattribute__(attribute)
        else:
            return None
        
    def setAttribute(self, attribute, value):
        if attribute == "refdes":
            value = value.split('.')[0]
        return self.__setattr__(attribute, value)

    
    def getAttributes(self):
        
        return self.attributes 
      
    def addVendorInfo(self):
        vendor = self.getAttribute('vendor')
        vendor_number = self.getAttribute('vendor-number')
        if (not vendor) or (not vendor_number):
            return None
        
        if vendor == 'Digikey':
            parser = vendors.digikey.DigikeyVendorParser()
            
        vendor_component = parser.parse(vendor_number)
        
        if not vendor_component:
            return None
        
        for attribute in self.attributes:
            vendor_attribute = vendor_component.__getattribute__(attribute)
            if vendor_attribute:
                self.setAttribute(attribute, vendor_attribute)
        
        
            
class SchematicComponentList(list):
    '''
    Schematic Component List.  A custom list for components
    '''
    def __init__(self):
        #list.__init__(self)
        pass
        #self.components = []
        
    def append(self, obj):
        
        if type(obj) == type(SchematicComponent()):
            super(SchematicComponentList, self).append(obj)
    
       
    
    def find(self, attribute, value):
        '''
        Returns all components matching the attribute value given
        '''
        c = SchematicComponentList()
        for component in filter(lambda component: component.getAttribute(attribute)==value, self):
            c.append(component)
            
        return c
    
    def findAndPop(self, attribute, value):
        '''
        Similar to find() but removes the matching entries from the list
        '''
        matches = self.find(attribute, value)
        for match in matches:
            self.remove(match)
        return matches   
    def sort(self, attribute='refdes'):
        '''
        Sort the list alphanumerically by a given attribute
        '''
        def chunkify(s):
            '''return a list of numbers and non-numeric substrings of +str+
        
            the numeric substrings are converted to integer, non-numeric are left as is
            '''
            chunks = re.findall("(\d+|\D+)",s)
            chunks = [re.match('\d',x) and int(x) or x for x in chunks] #convert numeric strings to numbers
            return chunks   
                 
        def sortAttr(a, b):
            chunka = chunkify(a.getAttribute(attribute))
            chunkb = chunkify(b.getAttribute(attribute))
            
            return cmp(chunka, chunkb)
        
        
        super(SchematicComponentList, self).sort(sortAttr)
"""        
class SchematicComponentList(object):
    '''
    Schematic Component List.  A custom list for components
    '''
    def __init__(self):
        
        self.components = []
        
    def append(self, obj):
        
        if type(obj) == type(SchematicComponent()):
            return self.components.append(obj)
    
    def __repr__(self):
        return self.components.__repr__()
       
    def pop(self, index=None):
        
        return self.components.pop(index)
    
    def find(self, attribute, value):
        
        c = SchematicComponentList()
        for component in filter(lambda component: component.getAttribute(attribute)==value, self.components):
            c.append(component)
            
        return c
    
    def __len__(self):
        return self.components.__len__()    
    
    def __getitem__(self, index):
        return self.components.__getitem__(index)
    
    def __getslice__(self, i, j):
        return self.components.__getslice__(i,j)
    
    def sort(self, attribute='refdes'):
        '''
        Sort the list alphanumerically by a given attribute
        '''
        def chunkify(s):
            '''return a list of numbers and non-numeric substrings of +str+
        
            the numeric substrings are converted to integer, non-numeric are left as is
            '''
            chunks = re.findall("(\d+|\D+)",s)
            chunks = [re.match('\d',x) and int(x) or x for x in chunks] #convert numeric strings to numbers
            return chunks   
                 
        def sortAttr(a, b):
            chunka = chunkify(a.getAttribute(attribute))
            chunkb = chunkify(b.getAttribute(attribute))
            
            return cmp(chunka, chunkb)
        
        
        return self.components.sort(sortAttr)
"""