class yNumerics:
    def __init__(self, method_id, momentum_flac):
        self.__method_id = method_id
        self.__momentum_flac = momentum_flac
        # 0: upwind, 1: LaxWendroff, 2: BeamWarming, 3: Fromm, 4: VanLeer, 5: minmod

    @property
    def momentum_flac(self):
        return self.__momentum_flac

    def assign_primary_variable_slope(self, grids, connector_id):
        grids[0].connectors[connector_id].primary_variable_slope = 0
     
        # NO JUNCTION
        if self.__method_id == 0:  # upwind
            pass
        elif self.__method_id == 1:  # laxWendroff
            if grids[0].connectors[connector_id].immediate_connectors_id[1]:
                if grids[1].connectors[grids[0].connectors[
                              connector_id].immediate_connectors_id[1][0]].immediate_connectors_id[1]:
                    down_down = grids[0].connectors[grids[1].connectors[grids[0].connectors[
                        connector_id].immediate_connectors_id[1][0]].immediate_connectors_id[1][0]].primary_variable[0]
                    grids[0].connectors[connector_id].primary_variable_slope = down_down - grids[0].connectors[
                        connector_id].primary_variable[0]
        elif self.__method_id == 2:  # beamWarming
            if grids[0].connectors[connector_id].immediate_connectors_id[0]:
                if grids[1].connectors[grids[0].connectors[
                              connector_id].immediate_connectors_id[0][0]].immediate_connectors_id[0]:
                    up_up = grids[0].connectors[grids[1].connectors[grids[0].connectors[
                        connector_id].immediate_connectors_id[0][0]].immediate_connectors_id[0][0]].primary_variable[0]
                    grids[0].connectors[connector_id].primary_variable_slope = \
                        grids[0].connectors[connector_id].primary_variable[0] - up_up
        elif self.__method_id == 3:  # Fromm
            if grids[0].connectors[connector_id].immediate_connectors_id[0]:
                if grids[1].connectors[grids[0].connectors[
                              connector_id].immediate_connectors_id[0][0]].immediate_connectors_id[0]:
                    up_up = grids[0].connectors[grids[1].connectors[grids[0].connectors[
                        connector_id].immediate_connectors_id[0][0]].immediate_connectors_id[0][0]].primary_variable[0]
                    if grids[0].connectors[connector_id].immediate_connectors_id[1]:
                        if grids[1].connectors[grids[0].connectors[connector_id].immediate_connectors_id[
                                      1][0]].immediate_connectors_id[1]:
                            down_down = grids[0].connectors[grids[1].connectors[grids[0].connectors[
                                connector_id].immediate_connectors_id[1][0]].immediate_connectors_id[
                                1][0]].primary_variable[0]
                            grids[0].connectors[connector_id].primary_variable_slope = 0.5 * (down_down - up_up)
        elif self.__method_id == 4:  # vanLeer
            if grids[0].connectors[connector_id].immediate_connectors_id[0]:
                if grids[1].connectors[grids[0].connectors[
                               connector_id].immediate_connectors_id[0][0]].immediate_connectors_id[0]:
                    up_up = grids[0].connectors[grids[1].connectors[grids[0].connectors[
                        connector_id].immediate_connectors_id[0][0]].immediate_connectors_id[0][0]].primary_variable[0]
       
                    if grids[0].connectors[connector_id].immediate_connectors_id[1]:
                        if grids[1].connectors[grids[0].connectors[
                                      connector_id].immediate_connectors_id[1][0]].immediate_connectors_id[1]:
                            down_down = grids[0].connectors[grids[1].connectors[grids[0].connectors[
                                connector_id].immediate_connectors_id[1][0]].immediate_connectors_id[
                                1][0]].primary_variable[0]
                            grids[0].connectors[connector_id].primary_variable_slope = \
                                calculate_vanLeer_limiter(grids[0], connector_id, up_up, down_down)
        elif self.__method_id == 5:  # minmod
            if grids[0].connectors[connector_id].immediate_connectors_id[0]:
                if grids[1].connectors[grids[0].connectors[
                              connector_id].immediate_connectors_id[0][0]].immediate_connectors_id[0]:
                    up_up = grids[0].connectors[grids[1].connectors[grids[0].connectors[
                        connector_id].immediate_connectors_id[0][0]].immediate_connectors_id[0][0]].primary_variable[0]
       
                    if grids[0].connectors[connector_id].immediate_connectors_id[1]:
                        if grids[1].connectors[grids[0].connectors[
                                      connector_id].immediate_connectors_id[1][0]].immediate_connectors_id[1]:
                            down_down = grids[0].connectors[grids[1].connectors[grids[0].connectors[
                                connector_id].immediate_connectors_id[1][0]].immediate_connectors_id[
                                1][0]].primary_variable[0]
                            grids[0].connectors[connector_id].primary_variable_slope = \
                                calculate_minmod_limiter(grids[0], connector_id, up_up, down_down)
        else:
            print("Error in waterDepthSlope calculation: Numerical method not defined !!!")

    def assign_velocity(self, grids, connector_id, timemarching, laws, balance_type):
        if balance_type == 0:  # mass
            if self.__momentum_flac:  # Saint-Venant
                pass  # velocity calculated in momentum balance
            else:
                grids[1].connectors[connector_id].primary_variable[0] = \
                    grids[1].connectors[connector_id].primary_variable[1] = \
                    laws[grids[1].connectors[connector_id].law_id].calculate_celerity(
                        grids[1].connectors[connector_id].geometry, grids[1].assign_centered_primary_variable(
                            connector_id, 0))
                # for timemarching
            if abs(grids[1].connectors[connector_id].primary_variable[0] / grids[1].connectors[connector_id].length) \
                    > timemarching.velocity_max:
                timemarching.velocity_max = abs(grids[1].connectors[connector_id].primary_variable[0])
        else:  # momentum
            grids[1].connectors[connector_id].velocity_centered = \
                grids[1].assign_centered_primary_variable(connector_id, 0)  # for flux


def calculate_flux(grids, connector_id, timemarching, balance_type):
    if balance_type == 0:  # mass
        velocity = grids[1].connectors[connector_id].primary_variable[0]
    else:
        velocity = grids[1].connectors[connector_id].velocity_centered  # NO  JUNCTION

    if velocity > 0:
        # NO JUNCTION
        primvar_advection = grids[0].connectors[grids[1].connectors[connector_id].immediate_connectors_id[
            0][0]].primary_variable[0] + 0.5 * (1 - velocity * timemarching.stepsize /
                                                grids[1].connectors[connector_id].length) * \
            grids[0].connectors[grids[1].connectors[connector_id].immediate_connectors_id[0][0]].primary_variable_slope
    else:
        primvar_advection = grids[0].connectors[grids[1].connectors[connector_id].immediate_connectors_id[
            1][0]].primary_variable[0] - 0.5 * (1 + velocity * timemarching.stepsize /
                                                grids[1].connectors[connector_id].length) * \
            grids[0].connectors[grids[1].connectors[connector_id].immediate_connectors_id[1][0]].primary_variable_slope

    if balance_type == 0:  # mass
        grids[1].connectors[connector_id].flux = primvar_advection * velocity
    else:  # momentum
        #  NO  JUNCTION
        grids[1].connectors[connector_id].flux = primvar_advection * 0.5 * (
            grids[0].connectors[grids[1].connectors[connector_id].immediate_connectors_id[0][0]].flux -
            grids[0].connectors[grids[1].connectors[connector_id].immediate_connectors_id[1][0]].flux)


def calculate_vanLeer_limiter(grid, connector_id, up_up, down_down):
    hlp = (down_down - grid.connectors[connector_id].primary_variable[0]) * \
         (grid.connectors[connector_id].primary_variable[0] - up_up)

    return 2 * hlp / (down_down - up_up) if hlp > 0 else 0


def calculate_minmod_limiter(grid, connector_id, up_up, down_down):
    a = grid.connectors[connector_id].primary_variable[0] - up_up
    b = down_down - grid.connectors[connector_id].primary_variable[0]
     
    if a * b > 0:
        return a if abs(a) < abs(b) else b
    else:
        return 0    