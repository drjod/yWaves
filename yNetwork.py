from yGrid import yGrid
from yMathematics import average, invert
from math import sqrt
from copy import deepcopy
from yOptions import averaging, gravity, epsilon


class yNetwork:
    """
    hosts grid and partner grid
    """
    def __init__(self):
        self.__grids = [yGrid(0),  # connectors
                        yGrid(1)]  # links

        self.__grids[0].partnergrid = self.__grids[1]   # each grid has partner grid
        self.__grids[1].partnergrid = self.__grids[0]

    @property
    def grids(self):
        return self.__grids

    def construct(self):
        """
        complete network after having nodes and links from input files
        :return:
        """
        self.connect_connectors_to_links()
        self.add_connector_ghosts()
        self.assign_length_to_connectors()
        self.assign_source_terms_from_link_to_connectors()

    def connect_connectors_to_links(self):
        """
        assign to connectors hosted on grids[0] all connected links from grids[1]
        :return:
        """
        for i in range(len(self.__grids[1].connectors)):
            for k in [0,1]:  # 0: upwind, 1: downwind
                for j in range(len(self.__grids[1].connectors[i].immediate_connectors_id[k])):
                    self.__grids[0].connectors[
                        self.__grids[1].connectors[i].immediate_connectors_id[k][j]].immediate_connectors_id[
                        invert(k)].append(self.__grids[1].connectors[i].id)

    def add_connector_ghosts(self):
        """
        for 1D domain boundaries
        :return:
        """
        for i in [1,0]:  # 1: links, 0: connectors
            for j in range(len(self.__grids[invert(i)].connectors)):
                for k in [0,1]:  # 0; upwind, 1; downwind
                    if not self.__grids[invert(i)].connectors[j].immediate_connectors_id[k]:  # no upwindLinks
                        # new link is downwind link of a connector
                        self.__grids[invert(i)].connectors[j].immediate_connectors_id[k].append(
                            len(self.__grids[i].connectors))
                        connector = deepcopy(
                            self.__grids[i].connectors[
                                self.__grids[invert(i)].connectors[j].immediate_connectors_id[invert(k)][0]])

                        connector.immediate_connectors_id = [[], []]  # delete elements
                        connector.id = len(self.__grids[i].connectors)
                        connector.immediate_connectors_id[invert(k)].append(self.__grids[invert(i)].connectors[j].id)
                        connector.ghost = 1
                        if i:  # only for links
                            connector.geometry += self.__grids[1].connectors[j].geometry * \
                                                  self.__grids[1].connectors[j].length
                        self.__grids[i].connectors.append(connector)

    def assign_length_to_connectors(self):
        """
        length of links is specified in input file
        here, these lengths are transfered to the connectors.
        :return:
        """
        for i in range(0, len(self.__grids[0].connectors), 1):
            lengths = [[], []]  # 0: upwind, 1: downwind(

            for k in [0, 1]:  # 0; upwind, 1; downwind
                    for j in range(len(self.__grids[0].connectors[i].immediate_connectors_id[k])):
                        lengths[k].append(self.__grids[1].connectors[
                                             self.__grids[0].connectors[i].immediate_connectors_id[k][j]].length)

            self.__grids[0].connectors[i].length = average(lengths, averaging)

    def assign_source_terms_from_link_to_connectors(self):
        """
        multiply source term on link with length and assign to connector
        mass source /sink terms(e.g. for precipitation, infiltration) are assigned to connectors in input file
        while momentum source / sink terms are assigned to links
        here, source / sink terms are transfered from links to connectors
        :return:
        """
        for i in range(len(self.__grids[0].connectors)):
            for k in [0, 1]:  # 0; upwind, 1; downwind
                for j in range(len(self.__grids[0].connectors[i].immediate_connectors_id[k])):
                    self.__grids[0].connectors[i].source_term += \
                        self.__grids[1].connectors[
                            self.__grids[0].connectors[i].immediate_connectors_id[k][j]].source_term * \
                        self.__grids[1].connectors[self.__grids[0].connectors[i].immediate_connectors_id[k][j]].length

    def assign_froude_number(self):
        """
        for output
        :return:
        """
        froude_number_max = 0.
    
        for j in range(len(self.__grids[1].connectors)):
            if self.__grids[1].connectors[j].ghost == 0:
                self.__grids[1].connectors[j].froude_number = self.__grids[1].connectors[j].primary_variable[1] / \
                sqrt(gravity * 0.5 * max(epsilon, abs(
                    self.__grids[0].connectors[
                        self.__grids[1].connectors[j].immediate_connectors_id[0][0]].primary_variable[1] +
                    self.__grids[0].connectors[
                        self.__grids[1].connectors[j].immediate_connectors_id[1][0]].primary_variable[1])))
                froude_number_max = max(froude_number_max, self.__grids[1].connectors[j].froude_number)
            
        print("  Maximum Froude number: {}\n".format(froude_number_max))
