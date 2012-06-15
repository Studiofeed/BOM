'''
Created on 2012-03-28

@author: timvb
'''
import os, sys
import logging
import re
import gschemSchematic as gs

class BaseSchematicParserError(Exception):
    pass

class SchematicFileError(BaseSchematicParserError):
    pass

class SchematicParserError(BaseSchematicParserError):
    pass

class SchematicParser(object):
    '''
    SchematicParser reads a gschem .sch file and compiles a list of all components
    '''


    def __init__(self, filename, logger=None):
        '''
        Constructor
        '''
        if not logger:
            self.logger = logging.getLogger('schematicParser.SchematicParser')
            self.logger.setLevel(logging.DEBUG)
            self.logger.addHandler(logging.StreamHandler(sys.__stdout__))
        else:
            self.logger = logger
            
        self.restrictedDevices = ['INPUT', 'OUTPUT', 'NET']
        
        #Check .sch filetype
        if os.path.splitext(filename)[1] != ".sch":
            raise SchematicFileError("Given file must have a .sch extension")
        #Check file exists
        if os.path.isfile(filename):
            self.file=filename
        else:
            raise SchematicFileError("Schematic File does not exist: %s"%(file))
        
        
        
        self.component_re = re.compile(r"^C(.*?)\n\{(.*?)\}", re.M|re.S)
        self.attribute_re = re.compile(r"^(.+)=(.+)", re.M)
        
        self.componentList = gs.SchematicComponentList()
        
        self.ignoreMultipleRefdes = True
        
    def parse(self):
        '''
        Parses schematic file.  Returns a list of Schematic Components
        '''
        f = open(self.file, 'r')
        file_data = f.read()
        f.close()
        #get components
        components = self.component_re.findall(file_data)
        
        if not components:
            raise SchematicParserError("Invalid regexp match")
        
        else:
            self.logger.debug("A total of %i components were found"%(len(components)))
        
        for component in components:
            header_data = component[0]
            attribute_data = component[1]
            symbol_file = header_data.split()[-1]
            
            #search for attributes
            attributes  = self.attribute_re.findall(attribute_data)
            
            if not attributes:
                raise SchematicParserError("No attributes found for component: %s"%(symbol_file))
            
            #Create dictionary for component creation
            attributes = dict(attributes)
            #add symbol file to attributes
            attributes['symbol'] = symbol_file
            comp = gs.SchematicComponent(**attributes)
            if not comp.getAttribute('device') or not comp.getAttribute('refdes'):
                self.logger.warning('Ignoring component: %s'%(comp.getAttribute('symbol')))
                continue
            if (comp.getAttribute('device') in self.restrictedDevices):
                self.logger.warning( "Ignoring restricted device: %s"%(comp))
                continue
            
            #rename refdes for slotting
            if comp.hasAttribute('num_slots') or comp.hasAttribute('slot'):
                refdes = comp.getAttribute('refdes')+"."+str(comp.getAttribute('slot'))
                comp.setAttribute('refdes', refdes)
                del refdes
                
            #Catch identical refdes components
            refdesMatches = self.componentList.find('refdes', comp.getAttribute('refdes'))
            if refdesMatches:
                self.logger.warning('%i identical refdes match(es) found! %s'%(len(refdesMatches), comp.getAttribute('refdes')))
                if self.ignoreMultipleRefdes:
                    self.logger.info('Ignoring component: %s'%(comp.getAttribute('refdes')))
                    continue
                #Identical refdes found, is num_slots defined
                
                    
                    
                
            #create components and attach to component list
            #dummy = SchematicComponent(attributes)
            self.componentList.append(comp)
            del comp
            #del dummy
        self.logger.info('Schematic parse returned %i valid components'%(len(self.componentList)))
        
        #Sort list
        self.componentList.sort()
        return self.componentList