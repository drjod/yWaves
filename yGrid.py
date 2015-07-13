####################################################################################
#
# yWaves class yGrid by JOD
#
# each yGrid has partnerGrid 
# yGrid hosts yNodes for primary variables
# while partnerGrid hosts yNodes for secondary variables
# in case mass balance
# yGrid primaryVariable is scalar entity (water depth)
# yGrid primarySecondaryble is vector entity (velocity, we are in 1D, so also scalar)
# in case momentum balance this turns (yGrid becomes partnerGrid and vice Versa)
#
####################################################################################


import yNode
import yMathematics


#####################################################################################


class yGridClass:


    number        = -1
    yNodes        = []
    slope         = -1
    partnerGrid   = -1
    
    
    def __init__ ( self, number, yNodes ):

        self.number = number
        self.yNodes = yNodes
        
        
#####################################################################################          

  
    def incorporateBoundaryConditions ( self ):     
                           
        
        for i in range (0, len ( self.yNodes ), 1):                                                                                                                                                                                                                                                          
                             
            if ( self.yNodes[i].ghost == 0 ):      
                                                                                                                                                   
                if ( self.yNodes[i].boundaryCondition  == "NOFLOW" ):                 
                 
                    self.partnerGrid.yNodes[self.yNodes[i].upwindNodesNumber[0]].flux = 0
                
                #elif ( grid0.yNodes[nodeNumber].boundaryCondition  == "NORMAL" ):
                
                #     self.grid0.yNodes[nodeNumber].flux = 
                #     laws[grid1.yNodes[nodeNumber].lawNumber].celerity ( grid1.yNodes[nodeNumber].geometry , yNetwork.primaryVariableCentered ( nodeNumber, grid0, grid1 ) )  
                           
                elif ( self.yNodes[i].boundaryCondition  != "NO" ):   # than value    
                
                    self.yNodes[i].primaryVariable[0] = self.yNodes[i].primaryVariable[1] = float ( self.yNodes[i].boundaryCondition ) 
            
            
        # CRITICAL DEPTH    
                        
						
#####################################################################################
 
       
    def primaryVariableCentered ( self, nodeNumber, timing ):
        
        
        avg = yMathematics.average
        primVar_up = []
        primVar_down = []  
        
        for j in range (0, len ( self.yNodes[nodeNumber].upwindNodesNumber ), 1 ): 
        
           primVar_up.append ( self.partnerGrid.yNodes[self.yNodes[nodeNumber].upwindNodesNumber[j]].primaryVariable[timing] ) 
            
        for j in range (0, len ( self.yNodes[nodeNumber].downwindNodesNumber ), 1 ):     
                                                                                      
            primVar_down.append ( self.partnerGrid.yNodes[self.yNodes[nodeNumber].downwindNodesNumber[j]].primaryVariable[timing] )       
        
        return avg ( [avg ( primVar_up, 0 ), avg ( primVar_down, 0 )], 0 )  # AVERAGING
        
 
#####################################################################################
        
               
    def updatePrimaryVariables ( self ):
    
    
        numberOfUpwindNodes = -1    
        nodeGridFlac = 0
    
            
        if ( len ( self.yNodes) > len ( self.partnerGrid.yNodes ) ):  # NodesGrid  (else LinksGrid)
        
            nodeGridFlac = 1
        
       
    
        for i in range ( 0, len ( self.yNodes ), 1 ):   # update values on nodes
            
            if ( self.yNodes[i].ghost == 1 ):
                
            
                if ( nodeGridFlac ):     
                  
                    numberOfUpwindNodes = len ( self.yNodes[i].upwindNodesNumber )
                    
                else:
                
                    numberOfUpwindNodes = len ( self.partnerGrid.yNodes[self.yNodes[i].upwindNodesNumber[0]].upwindNodesNumber )
                                       
                    
                    
                if ( numberOfUpwindNodes > 0 ):  # NO JUNCTION
                    
                    self.yNodes[i].primaryVariable[0] = self.yNodes[i].primaryVariable[1] = \
                    self.yNodes[self.partnerGrid.yNodes[self.yNodes[i].upwindNodesNumber[0]].upwindNodesNumber[0]].primaryVariable[1]
                    #self.yNodes[self.partnerGrid.yNodes[self.grids[0].yNodes[self.partnerGrid.yNodes[self.yNodes[i].upwindNodesNumber[0]].upwindNodesNumber[0]].upwindNodesNumber[0]].upwindNodesNumber[0]].primaryVariable[1]  
                    
                                                                  
                else: 
                                      
                    self.yNodes[i].primaryVariable[0] = self.yNodes[i].primaryVariable[1] = \
                    self.yNodes[self.partnerGrid.yNodes[self.yNodes[i].downwindNodesNumber[0]].downwindNodesNumber[0]].primaryVariable[1]
                    #self.yNodes[self.partnerGrid.yNodes[self.yNodes[self.partnerGrid.yNodes[self.yNodes[i].downwindNodesNumber[0]].downwindNodesNumber[0]].downwindNodesNumber[0]].downwindNodesNumber[0]].primaryVariable[1]  
                    
                                       
            else: 
                
                self.yNodes[i].primaryVariable[0] = self.yNodes[i].primaryVariable[1] 
               
                              
#####################################################################################
