####################################################################################
#
# yWaves class yLaw by JOD
#
# implemented are resistance to flow relationships by Manning and Dary Weisbach,
# constant velocity for linear advection and
# Brooks-Corey for infiltration simulation with a kinematic wave
# keywords in input file are constant, manning, darcyWeissbach, brooksCorey 
# see also yRead readLaws()
#
####################################################################################


import yOptions
import math


######################################################################################


class yLawClass:                                                                                     
                       
    
    number = -1
    lawType = -1         # 0: constant, 1: manning, 2: darcyWeisbach, 3: brooksCorey (for infiltration)
    values = []
                                                                                                                                                                    
    def __init__ ( self, number ):
    
    
        self.number = number
        
        
###################################################################################### 


    def celerity ( self, slope, stateVariable ):
    
        
        if ( self.lawType == 0 ):       # constant
         
            return self.values[0] 
            
        elif ( self.lawType == 1  ):    # manning
        
            return self.values[0] * math.sqrt ( slope ) * pow ( abs ( stateVariable ), 0.6666667 )
            
        elif ( self.lawType == 2  ):    # darcyWeisbach
        
            return self.values[0] * math.sqrt ( slope ) * math.sqrt ( abs ( stateVariable ) )   
            
        elif ( self.lawType == 3  ):   # brooksCorey
                                                         
            return self.values[0] * pow ( abs ( stateVariable ) , self.values[1] )
                             
        else: 
         
            print ( "Error in laws.clerity(): Law unknown" )    


                
###################################################################################### 

