'''
Created on 2012-04-17

@author: timvb
'''
import unittest
import schematicParser as sp
import bomOrganizer as bo
import bomPrinter as bp

import logging
import os
class Test(unittest.TestCase):


    def setUp(self):
        '''
        Set up test variables and loggers
        '''
        self.schFilename = os.path.join(os.getcwd(), 'testSchematic.sch')
        self.bomFilename = os.path.join(os.getcwd(), 'testSchematic.bom')
        self.logger = logging.getLogger('testSchematicParser')
        self.logger.setLevel(logging.INFO)
        #handler = logging.StreamHandler()
        handler = logging.NullHandler()
        self.logger.addHandler(handler)
        
        '''
        BomOrganizer
        '''
        
        '''
        Parse Schematic File
        '''
        self.parser = sp.SchematicParser(self.schFilename, self.logger)
        self.bomOrganizer = bo.BOMOrganizer(self.parser.parse())

    def tearDown(self):
        pass


    def testInitBaseBOMPrinter(self):
        baseBomPrinter = bp.BaseBOMPrinter(self.bomFilename, self.bomOrganizer)
        baseBomPrinter.printBOM()

    def testPrintingVendorParse(self):
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()