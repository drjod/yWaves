import math
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


class yOutput:
    """
    dynamically updated graphs - plot_results()
    or _ids on shell - write_results()
    supports time series and profiles 
    """

    def __init__(self, _id, grid_id, connectors_id, variables, seriesTimes, seriesValues):
        self.__id = _id
        self.__grid_id = grid_id
        self.__connectors_id = connectors_id
        self.__variables = variables
        self.series_times = seriesTimes
        self.series_values = seriesValues
               
        plt.ion()

    @property
    def connectors_id(self):
        return self.__connectors_id

    def plot_profiles(self, network, timemarching, gs):
        plt.subplot(gs[self.__id, 0])
        if self.__id == 0:
            plt.title("Simulation time: {} s".format(timemarching.current))
                  
        if self.__grid_id == 0:
            plt.xlabel("Node id")
        elif self.__grid_id == 1:
            plt.xlabel("Link id")
        else:
            print("Error in plot Results: Grid not known")

        for i in range(len(self.__variables)):
            values = []
            plt.ylabel(self.__variables[i])
            for ii in range(len(self.__connectors_id)):
                values.append(network.grids[self.__grid_id].connectors[self.__connectors_id[ii]].get_variable_value(
                    self.__variables[i]))
                                     
            linecolor = select_linecolor(self.__variables[i])
            plt.plot(self.__connectors_id, values, color=linecolor, linewidth=2.5, linestyle="-")

    def plot_timeseries(self, network, timemarching, gs):
        plt.subplot(gs[self.__id, 0])
        plt.xlabel("Time")
        
        if self.__grid_id == 0:
            plt.title("Node " + str(self.__connectors_id[0]))
        else:
            plt.title("Link " + str(self.__connectors_id[0]))  

        self.series_times.append(timemarching.current)

        for i in range(len(self.__variables)):
            self.series_values.append(
                network.grids[self.__grid_id].connectors[self.__connectors_id[0]].get_variable_value(
                    self.__variables[i]))
            output_values = list()

            for j in range(0, len(self.series_values), 1):
                if math.fmod(j, len(self.__variables)) == i:
                    output_values.append(self.series_values[j])
                                    
            plt.ylabel(self.__variables[i])
            linecolor = select_linecolor(self.__variables[i])
            plt.plot(self.series_times, output_values, color=linecolor, linewidth=2.5, linestyle="-")


def plot_results(outputs, network, timemarching):
    
    gs = gridspec.GridSpec(len(outputs), 1)
    gs.update(left=.18, right=.95, hspace=1.)
  
    for i in range(len(outputs)):
        if len(outputs[i].connectors_id) != 1:
            outputs[i].plot_profiles(network, timemarching, gs)
        else:
            outputs[i].plot_timeseries(network, timemarching, gs)

    # plt.draw()
    plt.show()
    if timemarching.step > 0:
        input('Press any key')
        plt.clf()
    
    if timemarching.current >= timemarching.end:
        input("Simulation finished")
         

def write_results(network, timemarching):
    """
    screen output
    :param network: (class yNetwork)
    :param timemarching: (class yTimestepping)
    :return:
    """
    print("Simulation time: {}".format(timemarching.current))
    print("Water depths:")
       
    for i in range(len(network.grids[0].connectors)):
        if network.grids[0].connectors[i].ghost == 0:
            print("{}: {}".format(i, network.grids[0].connectors[i].primary_variable[1]))
    
    print("Velocities:")    
    for j in range(len(network.grids[1].connectors)):
        if network.grids[1].connectors[j].ghost == 0:
            print("{}: {}".format(j, network.grids[0].connectors[j].primary_variable[1]))


def select_linecolor(variable):
    """

    :param variable: (string)
    :return:
    """
    if variable == "waterDepth":
        return str("blue")
    elif variable == "velocity":
        return str("red")               
    elif variable == "flux":
        return str("green")
    elif variable == "froudeNumber":
        return str("orange")
    else:   
        print("Error in select_linecolor: Variable not known")  
