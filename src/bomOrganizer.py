'''
Created on 2012-04-05

@author: timvb
'''
import gschemSchematic as gs
import vendors.digikey as dk

import logging
import re

class BOMException(Exception):
    pass
class BOMComponent(gs.SchematicComponent):
    '''
    Subclass of SchematicComponent to be able to easily append refdeses
    '''
    
    def __init__(self, *args, **kwargs):
        if not kwargs.get('logger', None):
            self.logger = logging.getLogger('bomOrganizer.BOMOrganizer')
            self.logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            self.logger.addHandler(handler)
        if args:
            if isinstance(args[0], gs.SchematicComponent):
                gs.SchematicComponent.__init__(self)
                self.attributes = args[0].getAttributes()
                for attribute in args[0].getAttributes():
                    self.setAttribute(attribute, args[0].getAttribute(attribute))
                self.refdes = [args[0].getAttribute('refdes')]
        else:
                
            gs.SchematicComponent.__init__(self, **kwargs)
        
            self.refdes = [kwargs.get('refdes', None)]
        
        self.uniqueAttribute = kwargs.get('unique', 'vendor-number')
        
        if not self.getAttribute(self.uniqueAttribute):
            
            self.logger.warning("Component %s missing required attribute: %s"%(str(self), self.uniqueAttribute))
        
        new_attributes = ['quantity', 'manufacturer', 'manufacturer-number', 'prices']    
        
        self.quantity = int(self.getAttribute('refdes') is not None)
        self.attributes.append('quantity')
        self.prices = {}
        
    def addComponent(self, component):
        assert isinstance(component, gs.SchematicComponent)
        if not component.hasAttribute(self.uniqueAttribute):
            raise BOMException("Component %s does not have the required unique attribute: %s"%(str(component), self.uniqueAttribute))
        comp_refdes = component.getAttribute('refdes')
        self.refdes.append(comp_refdes)
        self.quantity += 1
        
    def __eq__(self, other):
        
        assert isinstance(other, gs.SchematicComponent)
        return other.getAttribute(self.uniqueAttribute) == self.getAttribute(self.uniqueAttribute)
    
    def getQuantity(self):
        return self.quantity
    
        
    def sort(self):
        '''
        Sort refdeses alphanumerically
        '''
        def chunkify(s):
            '''return a list of numbers and non-numeric substrings of +str+
        
            the numeric substrings are converted to integer, non-numeric are left as is
            '''
            chunks = re.findall("(\d+|\D+)",s)
            chunks = [re.match('\d',x) and int(x) or x for x in chunks] #convert numeric strings to numbers
            return chunks   
                 
        def sortAttr(a, b):
            chunka = chunkify(a)
            chunkb = chunkify(b)
            
            return cmp(chunka, chunkb)
        
        try:
            self.refdes.sort(cmp=sortAttr)
        except Exception, msg:
            self.logger.error("Error in bomOrganizer.sort(): %s"%(msg))
            return False
        else:
            return True
        

        
class BOMOrganizer(object):
    '''
    BOMOrganizer reconfigures and sorts schematic component lists and prepares the component list for printing
    '''


    def __init__(self, componentList=None, sortOrder=('device', 'value', 'refdes'), logger=None, uniqueAttribute='vendor-number', parseVendor=False):
        '''
        Constructor
        '''
        if not isinstance(sortOrder, (list, tuple)):
            return TypeError("sortOrder keyword must be of type list or tuple")
        
        if not logger:
            self.logger = logging.getLogger('bomOrganizer.BOMOrganizer')
            self.logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            self.logger.addHandler(handler)
            
        else:
            self.logger = logger
            
        self.componentList = componentList
        
        self.organized = []
        self.sortOrder = sortOrder
        self.uniqueAttribute = uniqueAttribute
        self.parseVendor = parseVendor
        
        if self.componentList:
            self.organize()
            
    def __iter__(self):
        return self.organized.__iter__()
    
    def addComponentList(self, componentList):
        '''
        append an entire component list to the current list and re-organize
        '''
        self.componentList += componentList
        self.organize()
        
    def findComponent(self, component):
        '''
        Determine whether component exists in list of organized BOMComponents
        '''
        for index, bomComponent in enumerate(self.organized):
            if bomComponent.getAttribute(self.uniqueAttribute) == component.getAttribute(self.uniqueAttribute):
                return index
            
        return None
        
    def organize(self):
        '''
        Function to prepare a component list to be displayed.  This is done by first sorting the list by device attribute, 
        then each device block is sorted vendor-number to ensure uniqueness.  All matching device/vendor-number components will be grouped together to be displayed 
        '''
        
        #Get sort component list by device
        self.componentList.sort(attribute='device')
        
        for component in self.componentList:
            foundIndex = self.findComponent(component)
            if foundIndex is not None:
                
                '''
                Component exists, add it to 
                '''
                self.organized[foundIndex].addComponent(component)
                
            else:
                '''
                Create new organized component
                '''
                
                self.organized.append(BOMComponent(component))
            
        #Sort refdesses of all organized components    
        for component in self.organized:
            component.sort()
            
    
    def getBOM(self):
        return self.organized
        
    def addVendorInfo(self, index=-1):
        '''
        inserts the information provided by scraping the vendor web site.
        
        if kwarg index is not -1, then only the item at that index will be modified, otherwise all components will be attempted
        '''
        
        if index >= 0:
            #get info for single component
            
            component = self.componentList[index]
            
            self.logger.debug("Adding Vendor Information for component: %s"%(component))
            component.addVendorInfo()   
        else:
            
            self.logger.info("Getting Vendor Information for all Components")
            
            for component in self.componentList:
                component.addVendorInfo()
                
            self.logger.debug('Done')