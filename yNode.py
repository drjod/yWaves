####################################################################################
#
# yWaves class yNode by JOD
#
# hosts primary / secondary variable, froude number, flux
# source term / boundary condition
# ghost nodes on 1D domain boundaries
#
####################################################################################


class yNodeClass:
  

    number                          = -1.
    upwindNodesNumber               = []  
    downwindNodesNumber             = []    
    ghost                           = -1     
                               
    primaryVariable                 = [0.,0.]    # [old, new], grid1: waterdepth, grid2: velocity   
    primaryVariableSlope            = -1.        
    velocityCentered                = 0.           
    
    froudeNumber                    = -1.
    flux                            = 0.         # massFlux, momentumFlux_dtdx 
                   
                   
    geometry                        = -1.        # grid1: elevation, grid2: slope
    dx                              = -1.        # grid2: length of link 
    lawNumber                       = -1
    
    boundaryCondition               = "NO"       # NO or primaryVariable 
    sourceTerm                      = 0          # grid1: mass:
       
    
    def __init__ ( self, number, primaryVariable, ghost, upwindNodesNumber, downwindNodesNumber ):
       
    
        self.number                  = number              
        self.primaryVariable         = primaryVariable
        self.ghost                   = ghost
        self.upwindNodesNumber       = upwindNodesNumber
        self.downwindNodesNumber     = downwindNodesNumber
     
                    
####################################################################################              
            
			
    def getValue ( self, variable ):
    
    
        if ( variable == "waterDepth" or variable == "velocity" ):
                   
            return self.primaryVariable[1]      
                       
        elif  ( variable == "flux" ):
               
            return self.flux   
                
        elif  ( variable == "froudeNumber" ):
                   
            return self.froudeNumber
                              
        else:
                   
            print ( "Error in printResults: Variable not known" )  
          
                      
####################################################################################  
