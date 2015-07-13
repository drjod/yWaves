####################################################################################
#
# yWaves class yOutput by JOD
#
# dynamically updated graphs - plotResults()
# or numbers on shell - writeResults()
# supports time series and profiles 
#
####################################################################################


import yNetwork
import ySimulator
import math
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


####################################################################################


class yOutputClass:
   

    number = -1
    gridNumber         = -1
    nodesNumber        = []
    variables          = []
    seriesTimes        = []
    seriesValues       = []
    
    
    def __init__ ( self, number, gridNumber, nodesNumber, variables, seriesTimes, seriesValues ):
  
        
        self.number = number
        self.gridNumber = gridNumber
        self.nodesNumber = nodesNumber
        self.variables = variables
        self.seriesTimes = seriesTimes
        self.seriesValues = seriesValues
               
        plt.ion()
        plt.figure ( 1 ) 
        
        
######################################################################################  


    def plotProfiles ( self, net, stp, gs ):  
      
        
         plt.subplot ( gs[self.number, 0] )
            
         if ( self.number == 0 ):
         
             plt.title ( "Simulation time: " + str ( stp.current ) + " s" )        
                  
         if ( self.gridNumber == 0 ):
            
             plt.xlabel ( "Node number" )
            
         elif ( self.gridNumber == 1 ):   
         
             plt.xlabel ( "Link number" ) 
                
         else:
            
             print ("Error in plot Results: Grid not known") 
                  
                
         for i in range ( 0, len ( self.variables ), 1 ): 
            
             values = []
             plt.ylabel ( self.variables[i] )        
                
             for ii in range ( 0, len ( self.nodesNumber ), 1 ):
                   
                   values.append ( net.yGrids[self.gridNumber].yNodes[self.nodesNumber[ii]].getValue ( self.variables[i] ) )
                                     
             lineColor = selectLineColor ( self.variables[i] )
             plt.plot( self.nodesNumber, values, color = lineColor, linewidth=2.5, linestyle="-" )
             
             
######################################################################################  


    def plotTimeSeries ( self, net, stp, gs ):  
        
          
        plt.subplot ( gs[self.number, 0] )
        
        plt.xlabel ( "Time" )
        
        if ( self.gridNumber == 0 ):
        
            plt.title ( "Node " + str ( self.nodesNumber[0] ) )  
        
        else:
        
            plt.title ( "Link " + str ( self.nodesNumber[0] ) )  
         
         
        self.seriesTimes.append ( stp.current )
        
        
        for i in range ( 0, len ( self.variables ), 1 ): 
        
            self.seriesValues.append ( net.yGrids[self.gridNumber].yNodes[self.nodesNumber[0]].getValue ( self.variables[i] ) )
                       
            outputValues = []
            
            for j in range ( 0, len (self.seriesValues ), 1 ):     
            
                if ( math.fmod ( j , len ( self.variables ) ) == i ): 

                    outputValues.append ( self.seriesValues[j] )
                                    
            plt.ylabel ( self.variables[i] )
            lineColor = selectLineColor ( self.variables[i] )
            plt.plot ( self.seriesTimes, outputValues, color = lineColor, linewidth=2.5, linestyle="-" )
                             
            
######################################################################################  
#
# global functions
#    
	
def plotResults ( outputs, net, stp ):  
    
    gs = gridspec.GridSpec ( len ( outputs ), 1 )
    gs.update( left = .18, right=.95 , hspace = 1. )
  
    for i in range (0, len ( outputs ), 1):
            
        if ( len ( outputs[i].nodesNumber ) != 1 ):
        
            outputs[i].plotProfiles ( net, stp, gs )
                
        else:    
              
            outputs[i].plotTimeSeries ( net, stp, gs )    
            
            
            
    plt.draw ()
    
    #if ( stp.step > 0 ) :
    #
    #    plt.clf () 
    
    if ( stp.current >= stp.end ) :
    
        raw_input( "Simulation finished" )   
         
                     
######################################################################################  
#
# screen output

def writeResults (yNetwork, stp ):  
      
    print ( "Simulation time: " + str ( stp.current ) )
    print ( "Water depths:" )
       
    for i in range ( 0, len ( yNetwork.yGrids[0].yNodes ), 1 ):
    
        if ( yNetwork.yGrids[0].yNodes[i].ghost == 0 ):
    
            print ( str (i) + ": " + str ( yNetwork.yGrids[0].yNodes[i].primaryVariable[1] ) )
    
    print ( "Velocities:" )    
        
    for j in range ( 0, len ( yNetwork.yGrids[1].yNodes ), 1 ):
    
        if ( yNetwork.yGrids[1].yNodes[j].ghost == 0 ):
       
            print ( str (j) + ": " + str ( yNetwork.yGrids[1].yNodes[j].primaryVariable[1] ) )  
                          
    
    print ( "Flow rates:" )    
        
    for j in range ( 0, len ( yNetwork.yGrids[1].yNodes ), 1 ):
    
        if ( yNetwork.yGrids[1].yNodes[j].ghost == 0 ):
       
            print ( str (j) + ": " + str ( yNetwork.yGrids[0].yNodes[j].primaryVariable[1] *  \
            0.5 * ( yNetwork.yGrids[1].yNodes[yNetwork.yGrids[0].yNodes[j].upwindNodesNumber[0]].primaryVariable[1] + \
            yNetwork.yGrids[1].yNodes[yNetwork.yGrids[0].yNodes[j].downwindNodesNumber[0]].primaryVariable[1] ) ) )            
           
           
    plt.close()        
    
        
######################################################################################             
 

def selectLineColor ( variable ):

    
    if ( variable == "waterDepth" ):
    
        return str ( "blue" )
    
    if (variable == "velocity" ):
               
        return str ( "red" )    
                   
    elif  ( variable == "flux" ):
               
        return  str ( "green" )
            
    elif  ( variable == "froudeNumber" ):
               
        return  str ( "orange" )
                          
    else:
               
        print ( "Error in selectLineColor: Variable not known" )  
    
 
    #if ( number > 5):   
    # 
    #    print ( "Warning in plotResults: Number of colors restricted to 6" )
    #    
    #    
    #    
    #if ( number == 0 ):
    #            
    #    return str ( "blue" )    
    #       
    #elif ( number == 1 ):
    #   
    #    return str ( "red" )
    #        
    #elif ( number == 2 ):
    #   
    #    return str ( "green" )
    #    
    #elif ( number == 3 ):
    #   
    #    return str ( "orange" )
    #    
    #elif ( number == 4 ):
    #   
    #    return str ( "pink" )
    #        
    #else:          
    #   
    #    return str ( "yellow" )
    #    

###################################################################################### 
#
# e.g. for DEBUG
                                              
def printGrid ( yNetwork ):
      
        print ( "############### yGrids[0] #####" )  
                
        for i in range (0, len ( yNetwork.yGrids[0].yNodes ), 1 ): 
        
            print ( "Number:            " + str ( yNetwork.yGrids[0].yNodes[i].number ) )
            #print ( "Geometry (Elev):   " + str ( yNetwork.yGrids[0].yNodes[i].geometry ) )   
            #print ( "dx (Length):       " + str ( yNetwork.yGrids[0].yNodes[i].dx )  )    
            #print ( "Ghost:             " + str ( yNetwork.yGrids[0].yNodes[i].ghost )  )   
            #print ( "Boundary cond:     " + str ( yNetwork.yGrids[0].yNodes[i].boundaryCondition )  )          
        
                                                                                                                                                 
            for j in range ( 0, len ( yNetwork.yGrids[0].yNodes[i].upwindNodesNumber ), 1 ):         
                                                                                                  
                print ( "up: " + str ( yNetwork.yGrids[0].yNodes[i].upwindNodesNumber[j] ) )         
                                                                                                  
            for j in range ( 0, len ( yNetwork.yGrids[0].yNodes[i].downwindNodesNumber ), 1 ):       
                                                                                                  
                print ( "down: " + str ( yNetwork.yGrids[0].yNodes[i].downwindNodesNumber[j] ) )     
            
        
        print ( "############### yGrids[1] #####" )  
        for i in range (0, len ( yNetwork.yGrids[1].yNodes ), 1 ): 
                                                              
            print ( "Number:             "  + str ( yNetwork.yGrids[1].yNodes[i].number ) )           
            #print ( "Geometry (Slope):   "  + str ( yNetwork.yGrids[1].yNodes[i].geometry ) )  
            #print ( "dx (Length):        "  + str ( yNetwork.yGrids[1].yNodes[i].dx ) )  
            #print ( "LawNumber:          "  + str ( yNetwork.yGrids[1].yNodes[i].lawNumber ) )             
            #print ( "Ghost:              "  + str ( yNetwork.yGrids[1].yNodes[i].ghost ) )  
    
            
            for j in range ( 0, len ( yNetwork.yGrids[1].yNodes[i].upwindNodesNumber ), 1 ): 
                
                print ( "up: " + str ( yNetwork.yGrids[1].yNodes[i].upwindNodesNumber[j] ) )
            
            for j in range ( 0, len ( yNetwork.yGrids[1].yNodes[i].downwindNodesNumber ), 1 ): 
                
                print ( "down: " + str ( yNetwork.yGrids[1].yNodes[i].downwindNodesNumber[j] ) ) 
        

######################################################################################  
  
