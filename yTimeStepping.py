class yTimeStepping:
    """
    fixed or adaptive based on CFL-condition(and a safety factor)
    """
    def __init__(self, current, end, stepsize, adaptive, safetyfactor, factor_min, factor_max):
        self.__current = current
        self.__end = end
        self.__stepsize = stepsize
        self.__adaptive = adaptive
        self.__safetyfactor = safetyfactor
        self.__factor_min = factor_min
        self.__factor_max = factor_max

        self.__step = 1
        self.__velocity_max = 0

    @property
    def current(self):
        return self.__current

    @property
    def end(self):
        return self.__end

    @property
    def step(self):
        return self.__step

    @property
    def velocity_max(self):
        return self.__velocity_max

    @property
    def stepsize(self):
        return self.__stepsize

    @velocity_max.setter
    def velocity_max(self, value):
        self.__velocity_max = value

    def calculate_stepsize(self):
        if self.__adaptive == 1:
            factor = self.__safetyfactor /(self.__velocity_max * self.__stepsize)
            factor = max(self.__factor_min, min(factor, self.__factor_max))
            self.__stepsize *= factor
        else:
            if self.__velocity_max * self.__stepsize > 1:
                print("Warning: | sigma | > 1")

        if self.__current + self.__stepsize > self.__end:
            self.__stepsize = self.__end - self.__current 

        self.__current += self.__stepsize
        self.__step += 1

        print("  Simulation time: {}".format(self.__current))
        print("  Timestep size {}".format(self.__stepsize))

