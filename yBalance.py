from yNumerics import calculate_flux
from yOptions import gravity


class yBalance:
    """
    operator splitting
    advection, pressure, source term steps
    (upwinded) Saint-Venant source terms for friction and gravity still missing
    """
    def __init__(self, network, balance_type):
        self.__balance_type = balance_type
          
        if balance_type == 0:   # mass
            self.__grids = [network.grids[0],  # for scalars (water depth)
                            network.grids[1]]  # for vectors (velocity)

        elif balance_type == 1:  # momentum
            self.__grids = [network.grids[1],  # switch grid (and primary variable)
                            network.grids[0]]
        else:
            print("Error: Balance type must be 0 or 1")
            self.__grids = [None, None]

    def advance_time_step(self, timemarching, laws, numerics):
        self.prepare_calculation(timemarching, laws, numerics)
        self.calculate(timemarching)

    def prepare_calculation(self, timemarching, laws, numerics):
        for i in range(len(self.__grids[0].connectors)):
            numerics.assign_primary_variable_slope(self.__grids, i)
        for j in range(len(self.__grids[1].connectors)):
            numerics.assign_velocity(self.__grids, j, timemarching, laws, self.__balance_type)

        if self.__balance_type == 0:
            timemarching.calculate_stepsize()     

        for j in range(len(self.__grids[1].connectors)):
            if not self.__grids[1].connectors[j].ghost or self.__balance_type == 0:
                calculate_flux(self.__grids, j, timemarching, self.__balance_type)

        self.__grids[0].assign_boundary_conditions()

    def calculate(self, timemarching):
        for i in range(len(self.__grids[0].connectors)):
            if not self.__grids[0].connectors[i].ghost and self.__grids[0].connectors[i].boundary_condition == "NO" or \
                            self.__grids[0].connectors[i].boundary_condition == "NOFLOW":
                self.do_advection_step(i, timemarching)
                self.do_pressure_step(i, timemarching)
                self.assign_source_terms(i, timemarching)

    def do_advection_step(self, connector_id, timemarching):
        sum_flux = 0     

        for k in [0, 1]:  # 0: up, 1: down
            for j in range(len(self.__grids[0].connectors[connector_id].immediate_connectors_id[k])):
                sum_flux += (-1) ** k * self.__grids[1].connectors[self.__grids[0].connectors[
                    connector_id].immediate_connectors_id[k][j]].flux / self.__grids[1].connectors[
                    self.__grids[0].connectors[connector_id].immediate_connectors_id[k][j]].length

        if self.__balance_type == 0:  # mass
            self.__grids[0].connectors[connector_id].primary_variable[1] = \
                self.__grids[0].connectors[connector_id].primary_variable[0] + sum_flux * timemarching.stepsize
        else:  # momentum
            self.__grids[0].connectors[connector_id].primary_variable[1] = \
                (self.__grids[0].connectors[connector_id].primary_variable[0] *
                 self.__grids[0].assign_centered_primary_variable(connector_id, 0) + sum_flux * timemarching.stepsize) \
                / self.__grids[0].assign_centered_primary_variable(connector_id, 1)

    def do_pressure_step(self, connector_id, timemarching):
        if self.__balance_type == 1:  # momentum
            self.__grids[0].connectors[connector_id].primary_variable[1] += \
                gravity * (self.__grids[1].connectors[self.__grids[0].connectors[
                    connector_id].immediate_connectors_id[0][0]].primary_variable[1] +
                           self.__grids[1].connectors[self.__grids[0].connectors[
                               connector_id].immediate_connectors_id[0][0]].geometry -
                           self.__grids[1].connectors[self.__grids[0].connectors[
                                connector_id].immediate_connectors_id[1][0]].primary_variable[1] -
                           self.__grids[1].connectors[self.__grids[0].connectors[
                                connector_id].immediate_connectors_id[1][0]].geometry) * \
                timemarching.stepsize / self.__grids[0].connectors[connector_id].length

    def assign_source_terms(self, connector_id, timemarching):
        if self.__balance_type == 0:  # mass
            self.__grids[0].connectors[connector_id].primary_variable[1] += \
                self.__grids[0].connectors[connector_id].source_term * timemarching.stepsize
        else:  # momentum
            pass
