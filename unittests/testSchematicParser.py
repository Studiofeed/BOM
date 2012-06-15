'''
Created on 2012-04-04

@author: timvb
'''
import unittest
import os
import logging
import gschemSchematic as gs
import schematicParser as sp

class TestSchematicParser(unittest.TestCase):


    def setUp(self):
        
        self.filename = os.path.join(os.getcwd(), 'testSchematic.sch')
        self.logger = logging.getLogger('testSchematicParser')
        self.logger.setLevel(logging.INFO)
        #handler = logging.StreamHandler()
        handler = logging.NullHandler()
        self.logger.addHandler(handler)

    def tearDown(self):
        pass


    def testBadFileNames(self):
        self.filename = os.path.join(os.getcwd(), 'idontexist.sch')
        self.assertRaises(sp.SchematicFileError, sp.SchematicParser, self.filename, self.logger)
        self.filename = os.path.join(os.getcwd(), 'badFileExtension.txt')
        self.assertRaises(sp.SchematicFileError, sp.SchematicParser, self.filename, self.logger)

    def testParser(self):
        parser = sp.SchematicParser(self.filename, logger=self.logger)
        
        try:
            cl = parser.parse()
        except Exception, msg:
            self.fail("Schematic Parser threw an error: %s"%(msg))
        
        self.assertIsInstance(cl, gs.SchematicComponentList, "Schematic Parser does not return a SchematicComponentList object")
        self.assertTrue(len(cl)>0, "Empty Schematic Component List returned from Parser")
    
    def testMultipleRefdesCatching(self):
        parser = sp.SchematicParser(self.filename, logger=self.logger)
        parser.ignoreMultipleRefdes = True
        try:
            cl = parser.parse()
        except Exception, msg:
            self.fail("Schematic Parser threw an error: %s"%(msg))        
        
        for comp in cl:
            matchingRefdes = cl.find('refdes', comp.getAttribute('refdes'))
            if len(matchingRefdes) > 1:
                self.fail("A matching refdes was found when it was set to be ignored.  Component: %s"%(comp))
        parser = sp.SchematicParser(self.filename, logger=self.logger)
        parser.ignoreMultipleRefdes = False  
        
        for comp in cl:
            matchingRefdes = cl.find('refdes', comp.getAttribute('refdes'))
            if len(matchingRefdes) > 1:
                self.logger.info("Multiple refdes found and set to not be ignored: %s"%(comp))
        
#TODO: Test slotting recognition.  
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()