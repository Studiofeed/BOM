'''
Created on 2012-03-29

@author: timvb
'''

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch

import bomOrganizer as bo

class ReportlabReport(object):
    '''
    Reportlab Report to be used for BOM
    '''


    def __init__(self, filename, **kwargs):
        '''
        ReportlabReport Constructor
        '''
        
        self.filename = filename
        bom = kwargs.get('bom', None)
        if bom is not None and not isinstance(bom, bo.BOMOrganizer):
            raise TypeError("bom keyword argument must be an instance of bomOrganizer.BOMOrganizer")
        self.bomOrganizer=bom
        
    def getBomOrganizer(self):
        return self.bomOrganizer
    
    
        
        
        