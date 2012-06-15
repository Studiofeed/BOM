'''
Created on 2012-04-06

@author: timvb
'''
import unittest
import bomOrganizer as bo
import gschemSchematic as gs
import schematicParser as sp
import os

class TestBomComponent(unittest.TestCase):
    
    def setUp(self):
        '''
        
        '''
        attr =  {'refdes':'R1', 'value': '10k', 'device':'RESISTOR', 'vendor-number':'1234567A'}
        self.bomComp = bo.BOMComponent(**attr)
        
    def testInit(self):
        self.assertIsInstance(self.bomComp, gs.SchematicComponent, "Improper subclass of BomComponent")
        self.assertIsNotNone(self.bomComp.getAttribute('refdes'), 'Empty Refdes')
        self.assertIsNotNone(self.bomComp.getAttribute('vendor-number'), 'Empty vendor-number')
        
        attr =  {'refdes':'R1', 'value': '10k', 'device':'RESISTOR', 'vendor-number':'1234567A'}
        comp = gs.SchematicComponent(**attr)
        self.bomComp = bo.BOMComponent(comp)
        self.assertEqual(self.bomComp, comp, "Component in init argument not being processed")
        
    def testAddComponent(self):
        attr = {'refdes':'R10', 'value': '10k', 'device':'RESISTOR', 'vendor-number':'1234567A'}
        comp = gs.SchematicComponent(**attr)
        self.bomComp.addComponent(comp)
        self.assertEqual(self.bomComp.getQuantity(), 2, "Quantity attribute not being updated")
        
    def testEq(self):
        attr = {'refdes':'R10', 'value': '10k', 'device':'RESISTOR', 'vendor-number':'1234567A'}
        comp = gs.SchematicComponent(**attr)
        result = (self.bomComp == comp)
        self.assertTrue(result, "Equal components not being recognized")
        attr = {'refdes':'R10', 'value': '10k', 'device':'RESISTOR', 'vendor-number':'123234567A'}
        comp = gs.SchematicComponent(**attr)
        result = (self.bomComp == comp)  
        self.assertFalse(result, "Unqual components not being recognized")  
        
    def testSort(self):
        attr = {'refdes':'R10', 'value': '10k', 'device':'RESISTOR', 'vendor-number':'1234567A'}
        comp = gs.SchematicComponent(**attr)
        self.bomComp.addComponent(comp)
        attr = {'refdes':'R4', 'value': '10k', 'device':'RESISTOR', 'vendor-number':'1234567A'}
        comp = gs.SchematicComponent(**attr)
        self.bomComp.addComponent(comp)
        #print "Before sort: %s"%(self.bomComp.refdes)
        self.bomComp.sort()
        self.assertEqual(self.bomComp.refdes[0], 'R1', 'Wrong first refdes after sort')
        self.assertEqual(self.bomComp.refdes[1], 'R4', 'Wrong second refdes after sort')
        self.assertEqual(self.bomComp.refdes[2], 'R10', 'Wrong third refdes after sort')
        #print "After sort: %s"%(self.bomComp.refdes)
                 
class TestBomOrganizer(unittest.TestCase):


    def setUp(self):


        
        self.schFilename = os.path.join(os.getcwd(), 'testSchematic.sch')
        
    def _createDummyComponentList(self):
        '''
        Create SchematicComponentList and populate with components
        '''
        attr = {'refdes':'R1', 'value': '10k', 'device':'RESISTOR', 'vendor-number':'1234567'}
        c1 = gs.SchematicComponent(**attr)
        attr = {'refdes':'R3', 'value': '10k', 'device':'RESISTOR', 'vendor-number':'1234567'}
        c2 = gs.SchematicComponent(**attr)
        attr = {'refdes':'R2', 'value': '100k', 'device':'RESISTOR', 'vendor-number':'1234567A'}
        c3 = gs.SchematicComponent(**attr)
        attr = {'refdes':'C2', 'value': '10uF', 'device':'CAPACITOR', 'vendor-number':'1234567B'}
        c4 = gs.SchematicComponent(**attr)
        attr = {'refdes':'C4', 'value': '1uF', 'device':'CAPACITOR', 'vendor-number':'1234567C'}
        c5 = gs.SchematicComponent(**attr)
        attr = {'refdes':'C1', 'value': '1uF', 'device':'CAPACITOR', 'vendor-number':'1234567B'}
        c6 = gs.SchematicComponent(**attr)
        attr = {'refdes':'L1', 'value': '22nH', 'device':'INDUCTOR', 'vendor-number':'1234567D'}
        c7 = gs.SchematicComponent(**attr)  
            
        cl = gs.SchematicComponentList()
        for component in [c1, c2, c3,c4,c5,c6,c7]:
            cl.append(component)  
        return cl
    
    def _getSchematicComponentList(self):
        return sp.SchematicParser(self.schFilename).parse()
        
    def tearDown(self):
        if hasattr(self, 'bom'):
            del self.bom


    def testOrganize(self):
        self.bom = bo.BOMOrganizer(self._createDummyComponentList())
        self.assertEqual(self.bom.getBOM()[0].getQuantity(), 2, "Organize function not correct")
        
        #TODO: Add more detailed tests to BOMOrganizer

    def testParsedSchematic(self):
        self.bom = bo.BOMOrganizer(self._getSchematicComponentList())
        self.assertEqual(self.bom.getBOM()[0].getQuantity(), 4, "BOMOrganizer problem parsing from schematic")
    
    def testParsedSchematicWithVendorParse(self):
        
        self.bom = bo.BOMOrganizer(self._getSchematicComponentList())
        self.bom.addVendorInfo()   
    def testIter(self):
        self.bom = bo.BOMOrganizer(self._createDummyComponentList())
        for component in self.bom:
            self.assertTrue(component.hasAttribute('refdes'))
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()