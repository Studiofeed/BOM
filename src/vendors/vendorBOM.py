'''
Created on 2012-04-13

@author: timvb

Module to store vendor specific BOM information
'''

class BaseVendor(object):
    '''
    classdocs
    '''

    delimiter = '\t'
    attributes = ['quantity', 'vendor-nr']

        
    
class Digikey(BaseVendor):
    '''
    Digikey vendor file
    '''
    
    pass
    