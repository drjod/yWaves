from yNetwork import yNetwork
from yConnector import yConnector
from yOutput import yOutput
from yLaws import yLaw
from yNumerics import yNumerics
from yTimeStepping import yTimeStepping
from yOptions import gravity

           
def read_inputfile(filename):
    numerics = None
    timemarching = None
    laws = []
    outputs = []
    network = yNetwork()

    try:
        file = open(filename, 'r')
    except Exception as err:
        print(err)
        return None, None, None, None, None

    line = file.readline()
    line_variables = line.split()

    while not line_variables or line_variables[0] != "END":
        if not line_variables:
            pass
        elif line_variables[0] == "OPTIONS":
            numerics, timemarching = read_options(file)
        elif line_variables[0] == "NODES":
            read_nodes(file, network)
        elif line_variables[0] == "LINKS":
            read_links(file, network)
        elif line_variables[0] == "CONSTITUTIVE_LAWS":
            laws = read_laws(file)
        elif line_variables[0] == "OUTPUTS":
            outputs = read_outputs(file, timemarching, network)
            break

        line = file.readline()
        line_variables = line.split()

    file.close()

    return numerics, timemarching, network, laws, outputs


def read_options(file):
    """
    activate momentum balance for Saint-Venant
    select numerical scheme(flux limiter)
    specify time stepping(fixed or adaptive)
    :param file:
    :return:
    """

    line_variables = list()
    # momentum
    line = file.readline()
    line_variables = line.split()
    momentum_flac = int(line_variables[0])
    # numerics
    line = file.readline()
    line_variables = line.split()
    numerics = yNumerics(int(line_variables[0]), momentum_flac)
    # timemarching
    line = file.readline()
    line_variables = line.split()
    current, end, stepsize = float(line_variables[0]), float(line_variables[1]), float(line_variables[2])
    # adaptive
    line = file.readline()
    line_variables = line.split()
    timemarching = yTimeStepping(current, end, stepsize,
                                 int(line_variables[0]),  # adaptive
                                 float(line_variables[1]),  # safetyfactor
                                 float(line_variables[2]),  # factor_min
                                 float(line_variables[3]))  # factor_max

    return numerics, timemarching


def read_nodes(file, network):
    """
    collect nodes from file
    nodes host scalar entities - water depth
    :param file:
    :param network:
    :return:
    """
    line = file.readline()  # next line
    line = file.readline()
    line_variables = line.split()
    # 0: number, 1: elevation, 2: initialWaterDepth, 3: source_term, 4: boundary_condition

    while line_variables:

        # 0: number, 1: elevation, 2: initialWaterDepth, 3: source_term, 4: boundary_condition
        connector = yConnector(int(line_variables[0]),  # id
                                float(line_variables[1]),  # geometry (elevation)
                                [float(line_variables[2]), float(line_variables[2])],  # waterDepth [new, old]
                                0,  # no ghost
                                float(line_variables[3]),  # source term
                                line_variables[4],  # boundary condition (string)
                                [[], []],  # immediate connectors id [upwind, downwind]
                                0,  # length assigned later (None causes crash)
                                None)  # law_id

        network.grids[0].connectors.append(connector)

        line = file.readline()
        line_variables = line.split()


def read_links(file, network):
    """
    collect links from file
    vectors host vector entities - velocity
    :param file:
    :param network:
    :return:
    """
    line = file.readline()  # next line
    line = file.readline()
    line_variables = line.split()
    # 0: number, 1,2: connectors_is[up, down], 3: length, 4: conductance,
    # 5: velocity, 6: source_term, 7: boundary_condition

    while line_variables:
        connector = yConnector(int(line_variables[0]),  # id
                                (network.grids[0].connectors[int(line_variables[1])].geometry  # geometry (slope)
                                - network.grids[0].connectors[int(line_variables[2])].geometry)
                               / float(line_variables[3]),
                                [float(line_variables[5]),float(line_variables[5])],  # velocity_[new, old]
                                0,  # no ghost
                                float(line_variables[6]),  # source term - multiplication with length in construct()
                                line_variables[7],  # boundary condition (string)
                                # immediate connectors id [upwind, downwind]
                                [[int(line_variables[1])], [int(line_variables[2])]],
                                float(line_variables[3]),  # length
                                int(line_variables[4]))  # law_id

        network.grids[1].connectors.append(connector)

        line = file.readline()
        line_variables = line.split()


def read_laws(file):
    """
    collect constitutive equations(for yLaw)
    and append them on the yLaws vector
    :param file:
    :return:
    """
    laws = list()

    line = file.readline()
    line_variables = line.split()

    while line_variables:
        if line_variables[1] == "constant":  # linear advection
            law_type = 0
            law_values = [float(line_variables[2])]
        elif line_variables[1] == "manning":
            law_type = 1
            law_values = [1. / float(line_variables[2])]  # C = 1 / n
        elif line_variables[1] == "darcyWeissbach":
            law_type = 2
            law_values = [8 * gravity / float(line_variables[2])]  # C =(8g/f)^0.5
        elif line_variables[1] == "brooksCorey":
            law_type = 3
            law_values = [float(line_variables[2]),  # a - 1 =((2 + 3 lambda) / lambda) - 1
                          2 + 3 * float(line_variables[3]) / float(line_variables[3])]
        else:
            print("Error in law.read(): Law unknown")
            law_type = None
            law_values = [None]

        law = yLaw(int(line_variables[0]),  # law_id
                   law_type, law_values)

        laws.append(law)

        line = file.readline()
        line_variables = line.split()

    return laws


def read_outputs(file, timemarching, network):
    """
    collect outputs(for yOutput)
    and append them on the yOutputs vector
    :param file
    :param timemarching: (class yTimestepping)
    :param network: (class yNetwork)
    :return:
    """
    outputs = list()

    line = file.readline()
    grid_id = None

    while line[0] != "E":  # NOT END
        if line[0] == "P":    # PROFILE
            line_variables = line.split()
            if line_variables[1] == "NODES":
                grid_id = 0
            elif line_variables[1] == "LINKS":
                grid_id = 1
            else:
                print("Error in readOutput: NODES or LINKS on PROFILE?")
                grid_id = None

            line = file.readline()
            line_variables = line.split()

            connectors_id = [int(variable) for variable in line_variables]

            line = file.readline()
            line_variables = line.split()

            variables = [variable for variable in line_variables]

            out = yOutput(len(outputs), grid_id, connectors_id, variables, [], [])
            outputs.append(out)

        if line[0] == "S":  # SINGLE(for time series)
            line_variables = line.split()

            if line_variables[1] == "NODE":
                grid_id = 0
            elif line_variables[1] == "LINK":
                grid_id = 1
            else:
                print("Error in readOutput: NODES / LINKS on PROFILE?")

            connectors_id.append(int(line_variables[2]))

            line = file.readline()
            line_variables = line.split()

            variables = [variable for variable in line_variables]
            initial_values = [network.grids[grid_id].connectors[connectors_id[0]].get_variable_value(variable)
                              for variable in line_variables]

            out = yOutput(len(outputs), grid_id, connectors_id, variables, [timemarching.current], initial_values)
            outputs.append(out)

        line = file.readline()

    return outputs
