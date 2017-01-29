class yConnector:
    """
    Connector is node on grid 0 and link on grid 1
    hosts primary / secondary variable, froude number, flux
    source term / boundary condition
    ghost connectors on 1D domain boundaries
    """
    __primary_variable_slope = float()
    __velocity_centered = float()

    __froude_number = float()
    __flux = float()  # massFlux, momentumFlux_timestepsizelength

    def __init__(self, _id, geometry, primary_variable, ghost,
                 source_term, boundary_condition, immediate_connectors_id, length, law_id):
        self.__id = _id
        self.__geometry = geometry
        self.__primary_variable = primary_variable  # [old, new], grid1: waterdepth, grid2: velocity
        self.__ghost = ghost
        self.__source_term = source_term
        self.__boundary_condition = boundary_condition
        self.__immediate_connectors_id = immediate_connectors_id
        self.__length = length
        self.__law_id = law_id  # only used for links (grid 1)

        # if connectorNew.geometry < 0:
        #    print("Warning: Slope < 0 at link " + str(int(linevariables[0])))

    @property
    def id(self):
        return self.__id

    @property
    def geometry(self):
        return self.__geometry

    @property
    def immediate_connectors_id(self):
        return self.__immediate_connectors_id

    @property
    def ghost(self):
        return self.__ghost

    @property
    def source_term(self):
        return self.__source_term

    @property
    def boundary_condition(self):
        return self.__boundary_condition

    @property
    def primary_variable(self):
        return self.__primary_variable

    @property
    def flux(self):
        return self.__flux

    @property
    def length(self):
        return self.__length

    @property
    def froude_number(self):
        return self.__froude_number

    @property
    def law_id(self):
        return self.__law_id

    @id.setter
    def id(self, value):
        self.__id = value

    @flux.setter
    def flux(self, value):
        self.__flux = value

    @froude_number.setter
    def froude_number(self, value):
        self.__froude_number = value

    @length.setter
    def length(self, value):
        self.__length = value

    @immediate_connectors_id.setter
    def immediate_connectors_id(self, value):
        self.__immediate_connectors_id = value

    @ghost.setter
    def ghost(self, value):
        self.__ghost = value

    @geometry.setter
    def geometry(self, value):
        self.__geometry = value

    @source_term.setter
    def source_term(self, value):
        self.__source_term = value

    def get_variable_value(self, variable):
        """
        for output
        :param variable:
        :return:
        """
        if variable == "waterDepth" or variable == "velocity":
            return self.__primary_variable[1]
        elif variable == "flux":
            return self.__flux
        elif variable == "froudeNumber":
            return self.__froude_number
        else:
            print("Error in printResults: Variable not known")
            return None
