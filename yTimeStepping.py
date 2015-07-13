####################################################################################
#
# yWaves class yTimeStepping by JOD
#
# fixed or adaptive based on CFL-condition (and a safety factor)
#
####################################################################################


import ySimulator


####################################################################################


class yTimeSteppingClass:                                                                                     
                       
    
    adaptive             = 0                                                                          
    dt                   = -1. 
    dt_max               = -1.                                                                                                          
    current              = -1.            
    end                  = -1. 
    step                 = 0           
     
    maxVelocity          = 0
    savetyFactor         = 0
    
    
                                                                                                                                                                               
    def __init__ ( self, current ):
    
    
        self.current = current
           
        self.step   = 1
        self.factor = 1.
        
		
###################################################################################### 

        
    def provideTimestep ( self ): 
    
    
        self.factor = 1
    
        if ( self.adaptive == 1 ):
        
            factor = self.savetyFactor / ( self.maxVelocity * self.dt ) 
            
            factor = max ( self.factor_min, min ( factor, self.factor_max) ) 
            
            self.dt = self.dt * factor
                                       
        else:    
            
            if ( self.maxVelocity * self.dt  > 1 ):

                print ( "Warning: | sigma | > 1" ) 
            
        
        if ( self.current + self.dt > self.end ):    
                       
            self.dt = self.end - self.current 
            
            
        self.current = self.current + self.dt              
        self.step = self.step + 1         
                
        
        print ( "  Simulation time: " + str ( self.current ) )
        print ( "  Timestep size "  + str( self.dt ) )
        
        
###################################################################################### 
          
