'''
Created on 2012-04-04

@author: timvb
'''
import unittest
import gschemSchematic as gs

class TestGschemComponent(unittest.TestCase):


    def setUp(self):
        self.attr = {'refdes':'R1', 'value':'100k', 'device':'RESISTOR', 'symbol':'test.sym'}

 
    def tearDown(self):
        pass


    def testComponentInit(self):
        attr = self.attr
        c = gs.SchematicComponent(**attr)
        for (attribute, value) in attr.items():
            
            self.assertEqual(c.getAttribute(attribute), value, 'Component Attribute Init Fail: %s\nExpecting: %s'%(attribute, value))


    def testVendorInfo(self):
        
        pass
class TestGschemComponentList(unittest.TestCase):


    def setUp(self):
        attr = {'refdes':'R1', 'value':'50k', 'device':'RESISTOR', 'symbol':'test.sym'}
        c1 = gs.SchematicComponent(**attr)
        attr = {'refdes':'R3', 'value':'10k', 'device':'RESISTOR', 'symbol':'test.sym'}
        c2 = gs.SchematicComponent(**attr)
        attr = {'refdes':'R2', 'value':'100k', 'device':'RESISTOR', 'symbol':'test.sym'}
        c3 = gs.SchematicComponent(**attr)
        attr = {'refdes':'C2', 'value':'10uF', 'device':'CAPACITOR', 'symbol':'test.sym'}
        c4 = gs.SchematicComponent(**attr)
        attr = {'refdes':'C1', 'value':'100uF', 'device':'CAPACITOR', 'symbol':'test.sym'}
        c5 = gs.SchematicComponent(**attr)        
        self.cl = gs.SchematicComponentList()
        for component in [c1,c2,c3,c4,c5]:
            self.cl.append(component)
            
    def tearDown(self):
        pass

    def testLength(self):
        self.assertEqual(len(self.cl), 5, "SchematicComponentList length function not correct")
    def testIndex(self):
        try:
            c = self.cl[0]
        except Exception, msg:
            self.fail("SchematicComponentList getindex function failed with the following message: %s"%(msg))
        
        try:
            c = self.cl[-1]
        except Exception, msg:
            self.fail("SchematicComponentList getindex not accepting negative indices")
    def testSlice(self):
        try:
            c = self.cl[1:3]
        except Exception, msg:
            self.fail("SchematicComponentList getslice function failed with the following message: %s"%(msg))  
        self.assertEqual(len(c), 2, 'Length of slice result not correct')    
        self.assertEqual(c[0].getAttribute('value'), '10k', "Slice components not correct")
        self.assertEqual(c[1].getAttribute('refdes'), 'R2', "Slice components not correct") 
             
    def testFind(self):
        r = self.cl.find('device', 'CAPACITOR')
        self.assertEqual(len(r), 2, "Length of find() ('device', 'CAPACITOR') not correct")
        
        r = self.cl.find('value', '10k')
        self.assertEqual(len(r), 1, "Length of find() ('value', '10k') not correct")
        self.assertEqual(r[0].getAttribute('refdes'), 'R3', "Improper component found in find() ('value', '10k')")
    
    def testSort(self):
        cl = self.cl.find('device', 'RESISTOR')
        cl.sort('value')
        self.assertEqual(cl[0].getAttribute('value'), '10k', 'Sort function not correct')  
        
        cl = self.cl.find('device', 'CAPACITOR')
        cl.sort('refdes')
        self.assertEqual(cl[0].getAttribute('value'), '100uF', 'Sorting by refdes not correct ')  

    def testFindAndPop(self):
        original_length = len(self.cl)
        
        capacitors = self.cl.findAndPop('device', 'CAPACITOR')
        self.assertIsNotNone(capacitors, "No match found!")
        
        #assert that all the capacitors have been removed
        self.assertEqual(len(capacitors)+len(self.cl), original_length, "Components missing after findAndPop()")
        
        #check to make sure there are no more remaining devices in the main component list
        self.assertEqual(len(self.cl.find('device', 'CAPACITOR')), 0, "There are remaining matching components after findAndPop")
        
        
        
test_cases = [TestGschemComponent, TestGschemComponentList]
def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for test_class in test_cases:
        test_suite = loader.loadTestsFromTestCase(test_class)
        suite.addTests(test_suite)
    return suite

 
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()