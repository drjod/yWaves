from yMathematics import average
from yOptions import averaging

class yGrid:
    """
    each yGrid has partnergrid
    yGrid hosts yConnectors for primary variables
    while partnergridhosts yConnectors for secondary variables
    in case mass balance
    yGrid primary_variable is scalar entity(water depth)
    yGrid primarySecondaryble is vector entity(velocity, we are in 1D, so also scalar)
    in case momentum balance this turns(yGrid becomes partnergridand vice Versa)
    """
    __id = None
    __slope = None
    __partnergrid = None

    def __init__(self, _id):
        self.__id = _id
        self.__connectors = list()

    @property
    def connectors(self):
        return self.__connectors

    @property
    def partnergrid(self):
        return self.__partnergrid

    @partnergrid.setter
    def partnergrid(self, value):
        self.__partnergrid = value

    def assign_boundary_conditions(self):     
        for i in range(0, len(self.__connectors), 1):                                                                                                                                                                                                                                                          
            if self.__connectors[i].ghost == 0:
                if self.__connectors[i].boundary_condition == "NOFLOW":
                    self.__partnergrid.connectors[self.__connectors[i].immediate_connectors_id[0][0]].flux = 0
                elif self.__connectors[i].boundary_condition != "NO":   # than value
                    self.__connectors[i].primary_variable[0] = self.__connectors[i].primary_variable[1] = \
                        float(self.__connectors[i].boundary_condition)

    def assign_centered_primary_variable(self, connector_id, timing):
        primvars = [[],[]]  # 0: up, 1: down

        for k in [0, 1]:  # 0: up, 1: down
            for j in range(len(self.__connectors[connector_id].immediate_connectors_id[k])):
                primvars[k].append(self.__partnergrid.connectors[self.__connectors[
                    connector_id].immediate_connectors_id[k][j]].primary_variable[timing])

        return average(primvars, averaging)

    def update_primary_variables(self):
        connectorgrid_flac = 0

        if len(self.__connectors) > len(self.__partnergrid.connectors):  # NodesGrid (else LinksGrid)
            connectorgrid_flac = 1

        for i in range(len(self.__connectors)):   # update values on connectors
            if self.__connectors[i].ghost == 1:
                if connectorgrid_flac:
                    upwindnodes_id = len(self.__connectors[i].immediate_connectors_id[0])
                else:
                    upwindnodes_id = len(self.__partnergrid.connectors[self.__connectors[i].immediate_connectors_id[
                        0][0]].immediate_connectors_id[0])

                if upwindnodes_id > 0:  # NO JUNCTION
                    self.__connectors[i].primary_variable[0] = self.__connectors[i].primary_variable[1] = \
                    self.__connectors[self.__partnergrid.connectors[self.__connectors[i].immediate_connectors_id[
                        0][0]].immediate_connectors_id[0][0]].primary_variable[1]
                else:
                    self.__connectors[i].primary_variable[0] = self.__connectors[i].primary_variable[1] = \
                    self.__connectors[self.__partnergrid.connectors[self.__connectors[i].immediate_connectors_id[
                        1][0]].immediate_connectors_id[1][0]].primary_variable[1]
            else:
                self.__connectors[i].primary_variable[0] = self.__connectors[i].primary_variable[1] 
               
                              

