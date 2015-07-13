####################################################################################
#
# yWaves class yBalance by JOD
#
# operator splitting
# advection, pressure, source term steps
# (upwinded) Saint-Venant source terms for friction and gravity still missing
#
####################################################################################


import yNetwork
import yGrid
import yMathematics
import yOutput
import yOptions
import yNumerics
import math



####################################################################################


class yBalanceClass:


    balanceType     = 0    # 0: mass, 1 momentum
  
    grid0           = -1
    grid1           = -1
      
    
#################################################

    
    def __init__ ( self, yNetwork, balanceType ):

   
        self.balanceType = balanceType
          
        if ( balanceType == 0 ):   # mass
        
            self.grid0 = yNetwork.yGrids[0]
            self.grid1 = yNetwork.yGrids[1]
        
        elif ( balanceType == 1 ):  # momentum
        
            self.grid0 = yNetwork.yGrids[1]     # switch grid (and primary variable)
            self.grid1 = yNetwork.yGrids[0]
        
        else:
        
            print ( "Error: Balance type not given" )
            
        
#####################################################################################          
               

    def advanceTimeStep ( self, yTimeStepping, yLaws, yOptions, yNumerics ):  

         
        self.prepareCalculation ( yTimeStepping, yLaws, yOptions, yNumerics )
        
        self.calculate ( yTimeStepping )

        
#####################################################################################          
                         
                                                                      
    def prepareCalculation ( self, yTimeStepping, yLaws, yOptions, yNumerics ): 
                                                      
      
        for i in range ( 0, len ( self.grid0.yNodes ), 1 ):
             
            yNumerics.assignPrimaryVariableSlope ( self.grid0, self.grid1, i )             
                
        
        for j in range ( 0, len ( self.grid1.yNodes ), 1 ):   
                                                                                                 
            yNumerics.assignVelocity ( self.grid0, self.grid1, j, yTimeStepping, yLaws, yOptions.momentum, self.balanceType )    
         
                        
        if ( self.balanceType == 0 ):    
        
            yTimeStepping.provideTimestep ()     
            
                        
        for j in range ( 0, len ( self.grid1.yNodes ), 1 ): 
                                                  
            if ( self.grid0.yNodes[i].ghost == 0 or self.balanceType == 0 ):
                                                                                                   
                yNumerics.provideFlux ( self.grid0, self.grid1, j, yTimeStepping, self.balanceType ) 
               
                                                                                        
        self.grid0.incorporateBoundaryConditions ( )     
                
                
####################################################################################          
                          
                                                                     
    def calculate ( self, yTimeStepping ):    
                                                 
               
        for i in range ( 0, len ( self.grid0.yNodes ), 1 ):   
                                                                             
            if ( self.grid0.yNodes[i].ghost == 0 and self.grid0.yNodes[i].boundaryCondition == "NO" or self.grid0.yNodes[i].boundaryCondition == "NOFLOW" ):                    
                
                self.advectionStep ( i, yTimeStepping )
 
                self.pressureStep ( i, yTimeStepping )
                           
                self.incorporateSourceTerms ( i, yTimeStepping )
                                                                                                                                                                                                            
            
#####################################################################################  
                                  
                                   
    def advectionStep ( self, nodeNumber, yTimeStepping ):

  
        sum_flux = 0     
          
        for j in range ( 0, len ( self.grid0.yNodes[nodeNumber].upwindNodesNumber ), 1 ):
               
            sum_flux = sum_flux  + self.grid1.yNodes[self.grid0.yNodes[nodeNumber].upwindNodesNumber[j]].flux / self.grid1.yNodes[self.grid0.yNodes[nodeNumber].upwindNodesNumber[j]].dx
            
        for j in range ( 0, len ( self.grid0.yNodes[nodeNumber].downwindNodesNumber ), 1 ):                                               
                                                                                                                                           
            sum_flux = sum_flux  - self.grid1.yNodes[self.grid0.yNodes[nodeNumber].downwindNodesNumber[j]].flux / self.grid1.yNodes[self.grid0.yNodes[nodeNumber].downwindNodesNumber[j]].dx       
        
                
        if ( self.balanceType == 0 ): # mass
                    
            self.grid0.yNodes[nodeNumber].primaryVariable[1] = self.grid0.yNodes[nodeNumber].primaryVariable[0] + sum_flux * yTimeStepping.dt   
            
        
        else: # momentum
        
            self.grid0.yNodes[nodeNumber].primaryVariable[1] = ( self.grid0.yNodes[nodeNumber].primaryVariable[0] * self.grid0.primaryVariableCentered ( nodeNumber, 0 ) + sum_flux * yTimeStepping.dt ) / self.grid0.primaryVariableCentered ( nodeNumber, 1 )
        
                   
#####################################################################################  


    def pressureStep ( self, nodeNumber, yTimeStepping ):

        if ( self.balanceType == 1 ): # momentum          
                                                                                            # NO JUNCTION
            self.grid0.yNodes[nodeNumber].primaryVariable[1] =  self.grid0.yNodes[nodeNumber].primaryVariable[1] + yOptions.gravity * ( self.grid1.yNodes[self.grid0.yNodes[nodeNumber].upwindNodesNumber[0]].primaryVariable[1] + self.grid1.yNodes[self.grid0.yNodes[nodeNumber].upwindNodesNumber[0]].geometry - self.grid1.yNodes[self.grid0.yNodes[nodeNumber].downwindNodesNumber[0]].primaryVariable[1] - self.grid1.yNodes[self.grid0.yNodes[nodeNumber].downwindNodesNumber[0]].geometry ) * yTimeStepping.dt / ( self.grid0.yNodes[nodeNumber].dx )   
            #self.grid0.yNodes[nodeNumber].primaryVariable[1] = self.grid0.yNodes[nodeNumber].primaryVariable[1] + yOptions.gravity * ( self.grid1.yNodes[self.grid0.yNodes[nodeNumber].upwindNodesNumber[0]].primaryVariable[1]  - self.grid1.yNodes[self.grid0.yNodes[nodeNumber].downwindNodesNumber[0]].primaryVariable[1] ) * self.yTimeStepping.dt / ( self.grid0.yNodes[nodeNumber].dx * self.grid0.yNodes[nodeNumber].dx ) 
        
               
#####################################################################################  


    def incorporateSourceTerms ( self, nodeNumber, yTimeStepping ):            
    
    
        if ( self.balanceType == 0): # mass
           
            self.grid0.yNodes[nodeNumber].primaryVariable[1] = self.grid0.yNodes[nodeNumber].primaryVariable[1] + self.grid0.yNodes[nodeNumber].sourceTerm * yTimeStepping.dt
        
        else: # momentum
            
            pass
            #self.grid0.yNodes[nodeNumber].primaryVariable[1] = self.grid0.yNodes[nodeNumber].primaryVariable[1] - yOptions.gravity * pow ( self.grid0.yNodes[nodeNumber].primaryVariable[1], 2.) / ( pow ( self.grid0.yNodes[nodeNumber].conductance, 2. ) * pow ( network.partnerGridPrimaryVariableCenteredNew ( nodeNumber, self.grid0, self.grid1 ), 1.33333 )  )
   
                                                                                                                                 
#####################################################################################                

                                                 
