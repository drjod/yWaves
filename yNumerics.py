####################################################################################
#
# yWaves class yNumerics by JOD
#
####################################################################################


import yNetwork


####################################################################################


class yNumericsClass:                                                                                     
                       
    
    methodNumber             = -1            # 0: upwind, 1: LaxWendroff, 2: BeamWarming,                                                                
                                             # 3: Fromm, 4: VanLeer, 5: minmod            
    
    
                                                                                                                                                                               
    def __init__ ( self ):
    
    
        pass    
           

##################################################################################### 
        
                                            
    def assignVelocity ( self, grid0, grid1, nodeNumber, timeStepping, yLaws, momentum, balanceType ):           
    
        if ( balanceType == 0 ): # mass
        
            if ( momentum == 1 ):   # Saint-Venant
            
                pass    # velocity calculated in momentum balance
              
            else:
                
                grid1.yNodes[nodeNumber].primaryVariable[0] = grid1.yNodes[nodeNumber].primaryVariable[1] = \
                yLaws[grid1.yNodes[nodeNumber].lawNumber].celerity ( grid1.yNodes[nodeNumber].geometry , grid1.primaryVariableCentered ( nodeNumber, 0 ) )   
        
                        # for timeStepping
            if ( abs ( grid1.yNodes[nodeNumber].primaryVariable[0] / grid1.yNodes[nodeNumber].dx ) > timeStepping.maxVelocity ): 
           
                timeStepping.maxVelocity = abs ( grid1.yNodes[nodeNumber].primaryVariable[0] )
           
            
        else:  # momentum
        
            grid1.yNodes[nodeNumber].velocityCentered = grid1.primaryVariableCentered ( nodeNumber, 0 )  # for flux
                
            
#####################################################################################  


    def provideFlux ( self, grid0, grid1, nodeNumber, yTimeStepping, balanceType ):
    
            
        if ( balanceType == 0 ): # mass
        
            velocity = grid1.yNodes[nodeNumber].primaryVariable[0]
                        
             
        else:  
                
            velocity = grid1.yNodes[nodeNumber].velocityCentered  # NO  JUNCTION  
        
                               
        if ( velocity > 0 ): 
                                                # NO JUNCTION
            primVar_Adv = grid0.yNodes[ grid1.yNodes[nodeNumber].upwindNodesNumber[0]].primaryVariable[0] + \
            0.5 * ( 1 - velocity * yTimeStepping.dt / grid1.yNodes[nodeNumber].dx ) * grid0.yNodes[grid1.yNodes[nodeNumber].upwindNodesNumber[0]].primaryVariableSlope 
                                
        else:
        
            primVar_Adv = grid0.yNodes[ grid1.yNodes[nodeNumber].downwindNodesNumber[0]].primaryVariable[0] - \
            0.5 * ( 1 + velocity * yTimeStepping.dt / grid1.yNodes[nodeNumber].dx ) * grid0.yNodes[grid1.yNodes[nodeNumber].downwindNodesNumber[0]].primaryVariableSlope 
           
        ######
                        
        if ( balanceType == 0 ): # mass       
                
            grid1.yNodes[nodeNumber].flux = primVar_Adv * velocity
            
                   
        else:  # momentum
                                     # NO  JUNCTION
            grid1.yNodes[nodeNumber].flux = primVar_Adv * 0.5 * \
            ( grid0.yNodes[ grid1.yNodes[nodeNumber].upwindNodesNumber[0]].flux - grid0.yNodes[grid1.yNodes[nodeNumber].downwindNodesNumber[0]].flux )  
        
         
##################################################################################### 


    def assignPrimaryVariableSlope ( self, grid0, grid1, nodeNumber ):
    
    
        grid0.yNodes[nodeNumber].primaryVariableSlope = 0   
     
        # NO JUNCTION
      
        if ( self.methodNumber == 0 ):   # upwind
        
            pass
            
            
        elif ( self.methodNumber == 1 ): # laxWendroff  
              
             if ( len ( grid0.yNodes[nodeNumber].downwindNodesNumber ) > 0 ):
             
                if ( len ( grid1.yNodes[grid0.yNodes[nodeNumber].downwindNodesNumber[0]].downwindNodesNumber ) > 0 ):
                
                    DownDown = grid0.yNodes[grid1.yNodes[grid0.yNodes[nodeNumber].downwindNodesNumber[0]].downwindNodesNumber[0]].primaryVariable[0]
                    grid0.yNodes[nodeNumber].primaryVariableSlope = DownDown - grid0.yNodes[nodeNumber].primaryVariable[0]                                                                  
                     
                    
        elif ( self.methodNumber == 2 ): # beamWarming 
                   
            if ( len ( grid0.yNodes[nodeNumber].upwindNodesNumber ) > 0 ):
            
                if ( len ( grid1.yNodes[grid0.yNodes[nodeNumber].upwindNodesNumber[0]].upwindNodesNumber ) > 0 ):
                
                    UpUp = grid0.yNodes[grid1.yNodes[grid0.yNodes[nodeNumber].upwindNodesNumber[0]].upwindNodesNumber[0]].primaryVariable[0]    
                    grid0.yNodes[nodeNumber].primaryVariableSlope = grid0.yNodes[nodeNumber].primaryVariable[0] - UpUp   
                          
                         
        elif ( self.methodNumber == 3 ): # Fromm  
                
            if ( len ( grid0.yNodes[nodeNumber].upwindNodesNumber ) > 0 ):
          
                if ( len ( grid1.yNodes[grid0.yNodes[nodeNumber].upwindNodesNumber[0]].upwindNodesNumber ) > 0 ):
            
                    UpUp = grid0.yNodes[grid1.yNodes[grid0.yNodes[nodeNumber].upwindNodesNumber[0]].upwindNodesNumber[0]].primaryVariable[0]    
       
                    if ( len ( grid0.yNodes[nodeNumber].downwindNodesNumber ) > 0 ):
            
                        if ( len ( grid1.yNodes[grid0.yNodes[nodeNumber].downwindNodesNumber[0]].downwindNodesNumber ) > 0 ):
                     
                            DownDown = grid0.yNodes[grid1.yNodes[grid0.yNodes[nodeNumber].downwindNodesNumber[0]].downwindNodesNumber[0]].primaryVariable[0]
                            grid0.yNodes[nodeNumber].primaryVariableSlope =  0.5 * ( DownDown - UpUp )
            
                            
        elif ( self.methodNumber == 4 ): # vanLeer  
            
            if ( len ( grid0.yNodes[nodeNumber].upwindNodesNumber ) > 0 ):
          
                if ( len ( grid1.yNodes[grid0.yNodes[nodeNumber].upwindNodesNumber[0]].upwindNodesNumber ) > 0 ):
             
                    UpUp = grid0.yNodes[grid1.yNodes[grid0.yNodes[nodeNumber].upwindNodesNumber[0]].upwindNodesNumber[0]].primaryVariable[0]    
       
                    if ( len ( grid0.yNodes[nodeNumber].downwindNodesNumber ) > 0 ):
            
                        if ( len ( grid1.yNodes[grid0.yNodes[nodeNumber].downwindNodesNumber[0]].downwindNodesNumber ) > 0 ):
                     
                            DownDown = grid0.yNodes[grid1.yNodes[grid0.yNodes[nodeNumber].downwindNodesNumber[0]].downwindNodesNumber[0]].primaryVariable[0]
                            grid0.yNodes[nodeNumber].primaryVariableSlope =  primaryVariableSlopeVanLeer ( grid0, nodeNumber, UpUp, DownDown )
            
                            
        elif ( self.methodNumber == 5 ): # minmod   
               
            if ( len ( grid0.yNodes[nodeNumber].upwindNodesNumber ) > 0 ):
          
                if ( len ( grid1.yNodes[grid0.yNodes[nodeNumber].upwindNodesNumber[0]].upwindNodesNumber ) > 0 ):
             
                    UpUp = grid0.yNodes[grid1.yNodes[grid0.yNodes[nodeNumber].upwindNodesNumber[0]].upwindNodesNumber[0]].primaryVariable[0]    
       
                    if ( len ( grid0.yNodes[nodeNumber].downwindNodesNumber ) > 0 ):
            
                        if ( len ( grid1.yNodes[grid0.yNodes[nodeNumber].downwindNodesNumber[0]].downwindNodesNumber ) > 0 ):
                     
                            DownDown = grid0.yNodes[grid1.yNodes[grid0.yNodes[nodeNumber].downwindNodesNumber[0]].downwindNodesNumber[0]].primaryVariable[0]
                            grid0.yNodes[nodeNumber].primaryVariableSlope = primaryVariableSlopeMinmod ( grid0, nodeNumber, UpUp, DownDown )
            
        else: 
        
            print ("Error in waterDepthSlope calculation: Numerical method not defined !!!")  
    
    
#####################################################################################
            

def primaryVariableSlopeVanLeer ( grid0, nodeNumber, UpUp, DownDown ):

         
    hlp = ( DownDown - grid0.yNodes[nodeNumber].primaryVariable[0] ) * ( grid0.yNodes[nodeNumber].primaryVariable[0] - UpUp )
    
    if ( hlp > 0 ):         
                                                  
        return  2 * hlp / ( DownDown - UpUp )
    
    else:
        
        return  0    

            
#####################################################################################
#
# global functions
#
            

def primaryVariableSlopeMinmod ( grid0, nodeNumber, UpUp, DownDown ):

                                   
    a = grid0.yNodes[nodeNumber].primaryVariable[0] - UpUp                                               
    b = DownDown - grid0.yNodes[nodeNumber].primaryVariable[0]
     
    if ( a * b > 0 ):
        
        if ( abs ( a ) < abs ( b )  ):
        
            return  a 
            
        else:
        
            return  b
            
    else:
    
        return  0    
                    
            
##################################################################################### 
                                                                                             
