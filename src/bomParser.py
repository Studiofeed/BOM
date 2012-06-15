'''
Created on 2012-03-29

@author: timvb
'''
import os, sys
import csv
import logging
import gschemSchematic

class BOMParserError(Exception):
    pass



class BOMParser(object):
    '''
    Class to parse a pre-generated BOM from i.e. gnetlist -g partslist3
    '''


    def __init__(self, filename, sep=",", header=True, attributes=[], skip_lines=0, logger=None):
        '''
        BOM Parser Constructor
        '''
        if not logger:
            self.logger = logging.getLogger('bomParser.BOMParser')
            self.logger.setLevel(logging.DEBUG)
            self.logger.addHandler(logging.StreamHandler(sys.__stdout__))
        else:
            self.logger = logger
        self.file = filename
        self.sep = sep
        self.header = header
        self.attributes = attributes
        self.componentList = []
        self.skip_lines = skip_lines
        if not os.path.isfile(self.file):
            raise BOMParserError("BOM file does not exist: %s"%(self.file))
        
        
        self.csvreader = csv.reader(open(self.file, 'r'), delimiter=self.sep)
        self.logger.info( "Prepared to read delimited file: %s"%(self.file))
        
    def parse(self):
        skip_counter=0
        self.logger.info( "skipping %i lines"%(self.skip_lines))
        while skip_counter < self.skip_lines:
            skip_counter += 1
            self.csvreader.next()
        if self.header:
            self.logger.info( "Reading header")
            header = self.csvreader.next()
            
            #clean up header's in case of leading periods
            dummy_header = []
            for attribute in header:
                dummy_header.append(attribute.strip('.'))
            header = dummy_header
            del dummy_header
            
        else:
            header = self.attributes
        print header
        attributeLength = len(header)
        for row in self.csvreader:
            #ignore rows beginning with a .
            if row[0][0] == '.':
                continue
            #check that the row length equals attributeLength
            if len(row) != attributeLength:
                self.logger.error( "incorrect data length in row: %i"%(self.csvreader.line_num))
                continue
            #print row
            
            dummy_attributes = []
            for i in range(attributeLength):
                dummy_attributes.append((header[i], row[i]))
            
            comp = gschemSchematic.SchematicComponent(dummy_attributes)
            
            self.componentList.append(comp) 
            del comp
            
        return self.componentList
    
class PartsListParser(BOMParser):
    
    def __init__(self, filename, logger=None):
        if not logger:
            self.logger = logging.getLogger('bomParser.PartsListParser')
            self.logger.setLevel(logging.DEBUG)
            self.logger.addHandler(logging.StreamHandler(sys.__stdout__))
        else:
            self.logger = logger
                    
        BOMParser.__init__(self, filename, sep="\t", header=True, skip_lines=1, logger=self.logger)  
                 
if __name__ == "__main__":
    
    base_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
    filename = os.path.join(base_path, "test_data", "test.partslist.bom")
    
    parser = PartsListParser(filename)
    components = parser.parse()