####################################################################################
#
# yWaves class ySimulator by JOD
#
####################################################################################


import yNetwork
import yBalance
import yGrid
import yTimeStepping
import yOptions
import yNumerics
import yRead 
import yNode
import yOutput
import math
import time    
#import pdb; pdb.set_trace()  


####################################################################################


class ySimulatorClass:


    fileName = []
        
    yNetwork       = -1
    yTimeStepping  = -1
    yOptions       = -1
    yNumerics      = -1
    yBalances      = []
    yLaws          = []  
    yOutputs       = []

                                
    def __init__ ( self, fileName ):

   
        self.fileName = fileName 

                    
#####################################################################################    
#
# run simulation

    def run ( self ):
    
       
        self.prae ()
        
        self.execute ()    
        
        self.post ()
    
     
#####################################################################################
#
# read input, construct network
# states which grid hosts nodes (can be connected to many links) 
# and which grid hosts links (always connected to 2 nodes)
# (via yNetwork connectNodes2Links() called by construct())
#

    def prae ( self ):
    
       
        nodes = []
        links = []
       
             
        nodesGrid = yGrid.yGridClass ( 0, nodes )   
        linksGrid = yGrid.yGridClass ( 1, links )   
               
        self.yNetwork = yNetwork.yNetworkClass ( [nodesGrid, linksGrid] )
        self.yTimeStepping = yTimeStepping.yTimeSteppingClass ( 0. ) 
        self.yOptions = yOptions.yOptionsClass ()
        self.yNumerics = yNumerics.yNumericsClass ()
        
        re = yRead.yReadClass ( self.fileName, self.yNetwork, self.yTimeStepping, self.yOptions, self.yNumerics, self.yLaws, self.yOutputs )
        re.readFile ()
       
        mass = yBalance.yBalanceClass ( self.yNetwork, 0 )
        momentum = yBalance.yBalanceClass ( self.yNetwork, 1 )
        self.yBalances.append ( mass )
        self.yBalances.append ( momentum )
              
        self.yNetwork.construct ()
        update ( self.yNetwork, self.yTimeStepping )  
        
		# DEBUG
        # yOutput.plotResults ( self.yOutputs, self.yNetwork, self.yTimeStepping ) 
        # raw_input ( "Press key to execute time steps" )        
        # yOutput.printGrid ( self.yNetwork )
        
        
#####################################################################################
#
# advance through time steps        

    def execute ( self):

        while ( self.yTimeStepping.current < self.yTimeStepping.end - yOptions.epsilon ): 
        
            
            print ( "#######################################################\n" ) 
            print ( "Timestep: "  + str( self.yTimeStepping.step ) + "\n" ) 
            
            # mass
            self.yBalances[0].advanceTimeStep ( self.yTimeStepping, self.yLaws, self.yOptions, self.yNumerics )
            
          
            if ( self.yOptions.momentum == 1 ):
            
                self.yBalances[1].advanceTimeStep ( self.yTimeStepping, self.yLaws, self.yOptions, self.yNumerics )
            
            update ( self.yNetwork, self.yTimeStepping )  
                              
             
            #if ( math.fmod (stp.current, 10) == 0. ):
                                                                                                            
            yOutput.plotResults ( self.yOutputs, self.yNetwork, self.yTimeStepping ) 
    
            
###################################################################################### 
#
# after calculation done
           
    def post ( self ):                                                      
     
    
        # screen output stream
        # yOutput.writeResults ( self.yNetwork, self.yTimeStepping ) 
        
        self.releaseMemory ()
        
        
######################################################################################    
#
# finally         

    def releaseMemory ( self ):


        del self.fileName        
        del self.yNetwork       
        del self.yTimeStepping  
        del self.yOptions   
        
             
        while ( len ( self.yBalances ) > 0 ):
        
            del self.yBalances[len ( self.yBalances ) - 1]
          
              
        while ( len ( self.yOutputs ) > 0 ):
        
            del self.yOutputs[len ( self.yOutputs ) - 1]
            

###################################################################################### 
#
# to proceed to next time step

def update ( yNetwork, yTimeStepping ):            
        

        yTimeStepping.maxVelocity = yOptions.epsilon 
    
        yNetwork.yGrids[0].updatePrimaryVariables () 
        yNetwork.yGrids[1].updatePrimaryVariables () 
        
        yNetwork.assignFroudeNumber () 

                          
######################################################################################   
  
