##############################################################
#
# yWaves yMathematics by JOD
#
##############################################################


def average (vector, averageType):
									#   averageType 0: arithmetic, 1: geometric

    value = 0
    sum = 0
    
    if ( len ( vector ) == 0 ):
    
        return 0
        
    
    if ( averageType == 0 ):
    
        for i in range ( 0, len ( vector ), 1 ):
        
            sum = sum + vector[i]
        
        
        value = sum / len ( vector )
    
    elif ( averageType == 1 ):
    
        if ( len ( vector ) == 1 ):
    
            value = vector[0]
        
        elif ( len ( vector ) == 2 ):
        
            value = 2 * vector[0] * vector[1] / ( vector[0] + vector[1] )
    
        else:
            print ( "Error in average calculation" )
            value = 0
    
    else:
    
        print ( "Error: Average type not given" )    
                                                                                                             
    return value
	
	
##############################################################	
