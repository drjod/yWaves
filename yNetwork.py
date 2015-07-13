##############################################################
#
# yWaves class yNetwork by JOD
#
##############################################################


import yGrid
import yNode
import yMathematics
import yOptions
import yLaws
import copy
import math



##############################################################
#
# hosts grid and partner grid 
#

class yNetworkClass:


    yGrids = []
    
   
    def __init__ ( self, yGrids ):

      
        self.yGrids = yGrids
        
        self.yGrids[0].partnerGrid = self.yGrids[1]     # each grid has partner grid
        self.yGrids[1].partnerGrid = self.yGrids[0]     
                    

##############################################################   


    def construct ( self ):

                  
        # self.grids[0].incorporateBoundaryConditions ()
        # self.grids[1].incorporateBoundaryConditions ()      
        
        self.connectNodes2Links ()
                  
        self.addGhostLinks ()    
                
        self.addGhostNodes ()
          
        self.assignDx2Nodes ()                     
                
        self.assignLinkSourceTerms2Nodes ()
                     
                          
##############################################################
#
# append on nodes hosted by yGrids[0] all existing links (according to input file)
# yGrids[1] hosts links.
# This is decided by ySimulator prae()
#                         
                                              
    def connectNodes2Links ( self ):
    
           
        for i in range (0, len ( self.yGrids[1].yNodes ), 1 ):
        
            for j in range ( 0, len ( self.yGrids[1].yNodes[i].upwindNodesNumber ), 1 ): 
            
                self.yGrids[0].yNodes[self.yGrids[1].yNodes[i].upwindNodesNumber[j]].downwindNodesNumber.append ( self.yGrids[1].yNodes[i].number )
            
            for j in range ( 0, len ( self.yGrids[1].yNodes[i].downwindNodesNumber ), 1 ): 
            
                self.yGrids[0].yNodes[self.yGrids[1].yNodes[i].downwindNodesNumber[j]].upwindNodesNumber.append ( self.yGrids[1].yNodes[i].number )


############################################################## 
#
# for 1D domain boundaries
#

    def addGhostLinks ( self ):    
                
                        
        for i in range (0, len ( self.yGrids[0].yNodes ), 1 ):            
             
            if ( len ( self.yGrids[0].yNodes[i].upwindNodesNumber ) == 0 ): # no upwindLinks
        
                self.yGrids[0].yNodes[i].upwindNodesNumber. append ( len ( self.yGrids[1].yNodes ) ) # new link is downwind link of a node      
                nodeNew = copy.deepcopy ( self.yGrids[1].yNodes[self.yGrids[0].yNodes[i].downwindNodesNumber[0]] )    
                            
                while ( len ( nodeNew.upwindNodesNumber ) > 0 ):
                
                    del nodeNew.upwindNodesNumber[len ( nodeNew.upwindNodesNumber ) - 1]
                    
                while ( len ( nodeNew.downwindNodesNumber ) > 0 ):
                
                    del nodeNew.downwindNodesNumber[len ( nodeNew.downwindNodesNumber ) - 1]
                    
                nodeNew.downwindNodesNumber.append ( self.yGrids[0].yNodes[i].number )
                nodeNew.ghost = 1  
                nodeNew.number = len ( self.yGrids[1].yNodes )   
                                                      
                self.yGrids[1].yNodes.append ( nodeNew )
                                   
             
            if ( len ( self.yGrids[0].yNodes[i].downwindNodesNumber ) == 0 ): # no downwindLinks
        
                self.yGrids[0].yNodes[i].downwindNodesNumber. append ( len ( self.yGrids[1].yNodes ) ) # new link is downwind link of a node      
                nodeNew = copy.deepcopy ( self.yGrids[1].yNodes[self.yGrids[0].yNodes[i].upwindNodesNumber[0]] )  
                              
                while ( len ( nodeNew.downwindNodesNumber ) > 0 ):
                
                    del nodeNew.downwindNodesNumber[len ( nodeNew.downwindNodesNumber ) - 1]
                    
                while ( len ( nodeNew.upwindNodesNumber ) > 0 ):
                
                    del nodeNew.upwindNodesNumber[len ( nodeNew.upwindNodesNumber ) - 1]
                    
                nodeNew.upwindNodesNumber.append ( self.yGrids[0].yNodes[i].number )
                nodeNew.ghost = 1            
                nodeNew.number = len ( self.yGrids[1].yNodes )   
                       
                self.yGrids[1].yNodes.append ( nodeNew )      
                
                
############################################################## 
#
# for 1D domain boundaries
#


    def addGhostNodes ( self ):  
                                           

        for j in range (0, len ( self.yGrids[1].yNodes ), 1 ):            
             
            if ( len ( self.yGrids[1].yNodes[j].upwindNodesNumber ) == 0 ): # no upwindNodes
        
             
                self.yGrids[1].yNodes[j].upwindNodesNumber.append ( len ( self.yGrids[0].yNodes ) )
                #                                    new node is upwind node of a ghost link                  1: ghost node
                nodeNew = copy.deepcopy ( self.yGrids[0].yNodes[self.yGrids[1].yNodes[j].downwindNodesNumber[0]] )
                while ( len ( nodeNew.upwindNodesNumber ) > 0 ):
                
                    del nodeNew.upwindNodesNumber[len ( nodeNew.upwindNodesNumber ) - 1]
                    
                while ( len ( nodeNew.downwindNodesNumber ) > 0 ):
                
                    del nodeNew.downwindNodesNumber[len ( nodeNew.downwindNodesNumber ) - 1]
                    
                nodeNew.number = len ( self.yGrids[0].yNodes )         
                nodeNew.downwindNodesNumber.append ( self.yGrids[1].yNodes[j].number )
                nodeNew.ghost = 1                                               # NO JUNCTION                  
                nodeNew.geometry = nodeNew.geometry + self.yGrids[1].yNodes[j].geometry  * self.yGrids[1].yNodes[j].dx
                self.yGrids[0].yNodes.append ( nodeNew )  
                    
            
            if ( len ( self.yGrids[1].yNodes[j].downwindNodesNumber ) == 0 ): # no downwindNodes
        
   
                self.yGrids[1].yNodes[j].downwindNodesNumber.append ( len ( self.yGrids[0].yNodes ) ) 
                #                                        new node is downwind node of a ghost link            1: ghost node 
                nodeNew = copy.deepcopy ( self.yGrids[0].yNodes[self.yGrids[1].yNodes[j].upwindNodesNumber[0]] )
                
                while ( len ( nodeNew.upwindNodesNumber ) > 0 ):
                
                    del nodeNew.upwindNodesNumber[len ( nodeNew.upwindNodesNumber ) - 1]
                    
                while ( len ( nodeNew.downwindNodesNumber ) > 0 ):
                
                    del nodeNew.downwindNodesNumber[len ( nodeNew.downwindNodesNumber ) - 1]
                    
                nodeNew.number = len ( self.yGrids[0].yNodes )           
                nodeNew.upwindNodesNumber.append ( self.yGrids[1].yNodes[j].number )
                nodeNew.ghost = 1                                                  # NO JUNCTION                
                nodeNew.geometry = nodeNew.geometry - self.yGrids[1].yNodes[j].geometry  * self.yGrids[1].yNodes[j].dx        
                self.yGrids[0].yNodes.append ( nodeNew )  
                    
                
############################################################## 
#
# length of links is specified in input file
# here, these lengths are transfered to the nodes.
#

    def assignDx2Nodes ( self ):                     
                          
               
        avg = yMathematics.average
        
        for i in range (0, len ( self.yGrids[0].yNodes ), 1 ):   
        
            dx_up = []
            dx_down = []
            
            for j in range (0, len ( self.yGrids[0].yNodes[i].upwindNodesNumber ), 1 ): 
            
                dx_up.append ( self.yGrids[1].yNodes[self.yGrids[0].yNodes[i].upwindNodesNumber[j]].dx ) 
                
            for j in range (0, len ( self.yGrids[0].yNodes[i].downwindNodesNumber ), 1 ):     
                                                                                          
                dx_down.append ( self.yGrids[1].yNodes[self.yGrids[0].yNodes[i].downwindNodesNumber[j]].dx )                
                
        
            self.yGrids[0].yNodes[i].dx = avg ( [avg ( dx_up, 0 ), avg ( dx_down, 0 )], 0 )   
            
            
############################################################## 
#
# mass source /sink terms (e.g. for precipitation, infiltration) are assigned to nodes in input file
# while momentum source / sink terms are assigned to links
# here, source / sink terms are transfered from links to nodes 
#


    def assignLinkSourceTerms2Nodes ( self ):   # multiply source term on link with dx and assign to node
    
                       
        for i in range (0, len ( self.yGrids[0].yNodes ), 1 ):   
        
            dx_up = []                         
            dx_down = []
        
            for j in range (0, len ( self.yGrids[0].yNodes[i].upwindNodesNumber ), 1 ): 
            
                self.yGrids[0].yNodes[i].sourceTerm =  self.yGrids[0].yNodes[i].sourceTerm + self.yGrids[1].yNodes[self.yGrids[0].yNodes[i].upwindNodesNumber[j]].sourceTerm * self.yGrids[1].yNodes[self.yGrids[0].yNodes[i].upwindNodesNumber[j]].dx
               
            for j in range (0, len ( self.yGrids[0].yNodes[i].downwindNodesNumber ), 1 ):     
                                                                                          
                self.yGrids[0].yNodes[i].sourceTerm =  self.yGrids[0].yNodes[i].sourceTerm + self.yGrids[1].yNodes[self.yGrids[0].yNodes[i].downwindNodesNumber[j]].sourceTerm * self.yGrids[1].yNodes[self.yGrids[0].yNodes[i].downwindNodesNumber[j]].dx
                
                
##############################################################
#
# for output
#


    def assignFroudeNumber ( self ):
  
    
        froudeNumberMax = 0.
    
        for j in range ( 0, len ( self.yGrids[1].yNodes ), 1 ):   
    
            if ( self.yGrids[1].yNodes[j].ghost == 0 ):
                
                self.yGrids[1].yNodes[j].froudeNumber =  self.yGrids[1].yNodes[j].primaryVariable[1] / \
                math.sqrt ( yOptions.gravity * 0.5 *   \
                max( yOptions.epsilon,  abs ( self.yGrids[0].yNodes[self.yGrids[1].yNodes[j].upwindNodesNumber[0]].primaryVariable[1] + \
                self.yGrids[0].yNodes[self.yGrids[1].yNodes[j].downwindNodesNumber[0]].primaryVariable[1] ) ) )
                froudeNumberMax = max ( froudeNumberMax, self.yGrids[1].yNodes[j].froudeNumber )
            
        print ( "  Maximum Froude number: " + str ( froudeNumberMax ) + "\n" )    
        
                        
##############################################################
      
