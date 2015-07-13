####################################################################################
#
# yWaves class yRead by JOD
#
####################################################################################


import yNetwork
import yNode
import yOutput
import yLaws
import os


####################################################################################


class yReadClass:


    workfile      = 'input' 
    
    yNetwork       = -1
    yTimeStepping  = -1
    yOptions       = -1
    yNumerics      = -1
    yOutputs       = []
    yLaws          = []

                                      
    def __init__ ( self, workfile, yNetwork, yTimeStepping, yOptions, yNumerics, yLaws, yOutputs ):

        
        self.workfile        = workfile
        self.yNetwork        = yNetwork     
        self.yTimeStepping   = yTimeStepping
        self.yOptions        = yOptions  
        self.yNumerics       = yNumerics
        self.yLaws           = yLaws   
        self.yOutputs        = yOutputs     
        

#####################################################################################    
                     
           
    def readFile ( self ):
    
    
        file = open ( self.workfile, 'r' ) 
        
        line = file.readline () 
        lineVariables = line.split()
        
        while ( len ( lineVariables ) == 0 or lineVariables[0] != "END" ):
            
            if ( len ( lineVariables ) == 0 ):
            
                pass            
            
            elif ( lineVariables[0] == "OPTIONS" ):
               
                self.readOptions ( file )
        
            elif ( lineVariables[0] == "NODES" ):
            
                self.readNodes ( file )
        
            elif ( lineVariables[0] == "LINKS" ):
            
                self.readLinks ( file )
                
            elif ( lineVariables[0] == "CONSTITUTIVE_LAWS" ):
            
                self.readLaws ( file )
                
            elif ( lineVariables[0] == "OUTPUTS" ):
            
                self.readOutputs ( file )    
                return
                            
            line = file.readline () 
            lineVariables = line.split()    
            
        file.closed 
               
                                        
####################################################################################
#
# activate momentum balance for Saint-Venant
# select numerical scheme (flux limiter)
# specify time stepping (fixed or adaptive)
#


    def readOptions ( self, file ):   
         
  
        lineVariables = []
        
        #momentum
        line = file.readline ()
        lineVariables = line.split()
        self.yOptions.momentum = int ( lineVariables[0] )
        
        #numerics
        line = file.readline ()
        lineVariables = line.split()
        self.yNumerics.methodNumber = int ( lineVariables[0] )
           
        # timeStepping
        line = file.readline ()
        lineVariables = line.split()
        self.yTimeStepping.current = float ( lineVariables[0] )
        self.yTimeStepping.end = float ( lineVariables[1] )
        self.yTimeStepping.dt = float ( lineVariables[2] )
        
        # adaptive
        line = file.readline ()
        lineVariables = line.split()
        self.yTimeStepping.adaptive = int ( lineVariables[0] )
        self.yTimeStepping.savetyFactor = float ( lineVariables[1] )
        self.yTimeStepping.factor_min = float ( lineVariables[2] )
        self.yTimeStepping.factor_max = float ( lineVariables[3] )
        
            
####################################################################################  
#
# collect nodes (they host scalar entities - water depth) 
# and append them as yNodes on yGrid 0 of the yNetwork 
#          


    def readNodes ( self, file ):
   
        lineVariables = []   
        line = file.readline ()  # next line
        line = file.readline () 
        lineVariables = line.split() # 0: number, 1: elevation, 2: initialWaterDepth, 3: sourceTerm, 4: boundaryCondition
        
        
        while ( len ( lineVariables ) > 0 ):

            upwindNodesNumber = []  
            downwindNodesNumber = []
                     
            #                          number                    waterDepth [new, old]                                     no ghost
            nodeNew = yNode.yNodeClass ( int ( lineVariables[0] ), [float ( lineVariables[2] ), float ( lineVariables[2] )], 0, upwindNodesNumber, downwindNodesNumber )  
            
            nodeNew.geometry = float ( lineVariables[1] ) 
            nodeNew.sourceTerm = float ( lineVariables[3] )  
            nodeNew.boundaryCondition = lineVariables[4]                        
            self.yNetwork.yGrids[0].yNodes.append ( nodeNew )
            
            line = file.readline ()
            lineVariables = line.split()  
            
                         
####################################################################################  
#
# collect links (they host vector entities - velocity) 
# and append them as yNodes on yGrid 1 of the yNetwork 
#          
# each link has an upwind and a downwind node
# specifiation in imput file states who is who 
#

    def readLinks ( self, file ):

    
        lineVariables = []   
        line = file.readline ()  # next line
        line = file.readline () 
        lineVariables = line.split() # 0: number, 1,2: nodenumbers[up, down], 3: dx, 4: conductance, 5: velocity, 6: sourceTerm, 7: boundaryCondition
        
        
        while ( len ( lineVariables ) > 0 ):
      
            upwindNodesNumber = [] 
            downwindNodesNumber = []
         
            #                          number                    velocity_dtdx [new, old]                                                                                                                       no ghost
            nodeNew = yNode.yNodeClass ( int ( lineVariables[0] ), [float ( lineVariables[5] ),float ( lineVariables[5] )], 0, upwindNodesNumber, downwindNodesNumber )      
 
            nodeNew.geometry =  ( self.yNetwork.yGrids[0].yNodes[int ( lineVariables[1] )].geometry - self.yNetwork.yGrids[0].yNodes[int ( lineVariables[2] )].geometry ) / float ( lineVariables[3] )
            if ( nodeNew.geometry < 0 ):
                print ( "Warning: Slope < 0 at link " + str( int ( lineVariables[0] ) ) )
            
            nodeNew.dx = float ( lineVariables[3] )
            nodeNew.lawNumber = int ( lineVariables[4] )                                  
            nodeNew.sourceTerm = float ( lineVariables[6] )      # multiplication with dx in network.construct ()
            nodeNew.boundaryCondition = lineVariables[7]                                                         
            nodeNew.upwindNodesNumber.append ( int ( lineVariables[1] ) )  
            nodeNew.downwindNodesNumber.append ( int ( lineVariables[2] ) )                       
            self.yNetwork.yGrids[1].yNodes.append ( nodeNew )
                    
            line = file.readline ()
            lineVariables = line.split()            
                      
        
###################################################################################### 
#
# collect constitutive equations (for yLawClass)
# and append them on the yLaws vector 
#
        
    def readLaws ( self, file ): 
    
        
        line = file.readline ()
        lineVariables = line.split()
        
        while ( len ( lineVariables ) > 0 ):
        
            lawNew = yLaws.yLawClass ( int ( lineVariables[0] ) ) 
            
            if ( lineVariables[1] == "constant" ):   # linear advection 
            
                lawNew.lawType = 0
                lawNew.values.append ( float ( lineVariables[2] ) )
                
            elif ( lineVariables[1] == "manning" ):
            
                lawNew.lawType = 1
                lawNew.values.append ( 1. / float ( lineVariables[2] ) )  #  C = 1 / n
            
            elif ( lineVariables[1] == "darcyWeissbach" ):
                                       
                lawNew.lawType = 2
                lawNew.values.append ( sqrt ( 8 * options.gravity / ( float ( lineVariables[2] ) ) )   )   #  C = (8g/f)^,5
            
            elif (lineVariables[1] == "brooksCorey"):
            
                lawNew.lawType = 3
                lawNew.values.append ( float ( lineVariables[2] ) )   
                lawNew.values.append ( ( 2 + 3 * float ( lineVariables[3] )  / ( float ( lineVariables[3] ) ) ) - 1  )    
																							#  a - 1 = ( ( 2 + 3 lambda ) / lambda ) - 1                     
            else:
            
                print ( "Error in law.read(): Law unknown" )
            
                    
            self.yLaws.append ( lawNew )    
                
            
            line = file.readline ()
            lineVariables = line.split()      
          
            
####################################################################################
#
# collect outputs (for yOutputClass)
# and append them on the yOutputs vector                          
#

    def readOutputs ( self, file ):   
   
    
        line = file.readline ()  
        gridNumber = -1
                           
        while ( line[0] != "E" ): # NOT END
    
            nodesNumber = []
            variables = []
            startTime = []        
            startValues = []   
                  
            if ( line[0] == "P" ):    # PROFILE
                              
                lineVariables = line.split() 
                
                if ( lineVariables[1] == "NODES" ): 
                    
                    gridNumber = 0
               
                elif ( lineVariables[1] == "LINKS" ):
                
                    gridNumber = 1
                      
                else:
                
                    print ("Error in readOutput: NODES or LINKS on PROFILE?")     
                 
                            
                line = file.readline ()  
                lineVariables = line.split()
                
                for i in range (0, len ( lineVariables ), 1 ):
                
                    nodesNumber.append ( int ( lineVariables[i] ) )    
            
                
                line = file.readline ()  
                lineVariables = line.split()                 
                                                             
                for i in range (0, len ( lineVariables ), 1 ):
                                                               
                    variables.append ( lineVariables[i] )        
                
                outNew = yOutput.yOutputClass ( len ( self.yOutputs ), gridNumber, nodesNumber, variables, startTime, startValues )
                self.yOutputs.append ( outNew )   
                     
                                        
            if ( line[0] == "S" ):  #SINGLE  ( for time series )
                     
                lineVariables = line.split()                                     
                                                                                 
                if ( lineVariables[1] == "NODE" ):                              
                                                                                 
                    gridNumber = 0                                     
                                                                                 
                elif ( lineVariables[1] == "LINK" ):                            
                                                                                 
                    gridNumber = 1                                      
                                                                                 
                else:                                                            
                                                                                 
                    print ("Error in readOutput: NODES / LINKS on PROFILE?")    
            
                nodesNumber.append ( int ( lineVariables[2] ) ) 
            
                line = file.readline ()                          
                lineVariables = line.split()                     
                
                startTime.append ( self.yTimeStepping.current )
                    
                                                           
                for i in range (0, len ( lineVariables ), 1 ):    
                                                                 
                    variables.append ( lineVariables[i] )                  
                    startValues.append ( self.yNetwork.yGrids[gridNumber].yNodes[nodesNumber[0]].getValue ( variables[i] ) )
                
                #seriesValues.append ( self.yNetwork.yGrids[gridNumber].yNodes[nodesNumber[0]].getValue ( variables[0] ) )
                    
                outNew = yOutput.yOutputClass ( len ( self.yOutputs ), gridNumber, nodesNumber, variables, startTime, startValues )
                self.yOutputs.append ( outNew )          
            
            line = file.readline () 

                              
##################################################################################### 








