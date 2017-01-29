import math


class yLaw:                                                                                     
    """
    implemented are resistance to flow relationships by Manning and Dary Weisbach,
    constant velocity for linear advection and
    Brooks-Corey for infiltration simulation with a kinematic wave
    keywords in input file are constant, manning, darcyWeissbach, brooksCorey
    """
    def __init__(self, id, _type, values):
        self.__id = id
        self.__type = _type  # 0: constant, 1: manning, 2: darcyWeisbach, 3: brooksCorey(for infiltration)
        self.__values = values  # list
        
    def calculate_celerity(self, slope, statevariable):
        if self.__type == 0:      # constant
            return self.__values[0]  
        elif self.__type == 1:    # manning
            return self.__values[0] * math.sqrt(slope) * pow(abs(statevariable), 0.6666667)
        elif self.__type == 2:    # darcyWeisbach
            return self.__values[0] * math.sqrt(slope) * math.sqrt(abs(statevariable))   
        elif self.__type == 3:   # brooksCorey
            return self.__values[0] * pow(abs(statevariable), self.__values[1])
        else:
            print("Error in laws.clerity(): Law unknown")    
            return None

                
# 

