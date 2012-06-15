'''
Created on 2012-04-05

@author: timvb
'''
import unittest
import testGschemComponents as gc, testSchematicParser as sp

def suite():
    
    suite = unittest.TestSuite()
    #unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass)
    suite1 = unittest.defaultTestLoader.loadTestsFromModule(gc)
    suite2 = unittest.defaultTestLoader.loadTestsFromModule(sp)
    suite.addTests([suite1, suite2])
    
    
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    test_suite = suite()
    
    runner.run(test_suite)