'''
Created on 2012-04-26

@author: timvb
'''
import unittest
import vendors
import vendors.digikey as dk


class TestDigikeyVendor(unittest.TestCase):


    def testParse(self):
        id = '5001K-ND'
        parser = dk.DigikeyVendorParser()
        component = parser.parse(id)
        
        self.assertTrue(isinstance(component, vendors.vendor.VendorComponent), "Vendor parser not returning a VendorComponent Object!")
        self.assertEqual(component.manufacturer, "Keystone Electronics", "Parser did not return proper manufacturer")
        self.assertTrue(len(component.prices)>0, "component.prices dict empty")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()