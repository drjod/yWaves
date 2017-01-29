from yBalance import yBalance
from yRead import read_inputfile
from yOutput import plot_results, write_results
from yOptions import epsilon


class ySimulator:
    def __init__(self, filename):
        self.__filename = filename

        self.__balances = list()
        self.__laws = list()
        self.__outputs = list()

        self.__network = None
        self.__timemarching = None
        self.__numerics = None

    def run(self):
        if self.do_prae_calculation():
            return 1
        self.do_calculation()
        self.do_post_calculation()
        return 0

    def do_prae_calculation(self):
        """
        read input, construct network
        states which grid hosts connectors(can be connected to many links)
        and which grid hosts links(always connected to 2 connectors)
        (via yNetwork connect_connectors_to_links() called by construct())
        :return:
        """
        self.__numerics, self.__timemarching, self.__network, \
            self.__laws, self.__outputs = read_inputfile(self.__filename)

        if self.__numerics is None:
            return 1  # error when tried opening input file

        self.__balances.append(yBalance(self.__network, 0))  # mass
        self.__balances.append(yBalance(self.__network, 1))  # momentum

        self.__network.construct()

    def do_calculation(self):
        """
        advance through time steps
        :return:
        """
        while self.__timemarching.current < self.__timemarching.end - epsilon:
            print("#######################################################\n")
            print("Timestep: {}\n".format(self.__timemarching.step))
            # mass
            self.__balances[0].advance_time_step(self.__timemarching, self.__laws, self.__numerics)
            if self.__numerics.momentum_flac:
                self.__balances[1].advance_time_step(self.__timemarching, self.__laws, self.__numerics)
            self.update()

            write_results(self.__network, self.__timemarching)
            plot_results(self.__outputs, self.__network, self.__timemarching)

    def do_post_calculation(self):
        pass

    def update(self):

        self.__timemarching.maxVelocity = epsilon

        self.__network.grids[0].update_primary_variables()
        self.__network.grids[1].update_primary_variables()

        self.__network.assign_froude_number()
