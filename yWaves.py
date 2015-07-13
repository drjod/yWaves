####################################################################################
#
# yWaves by Jens-Olaf Delfs (JOD)
#
####################################################################################


import ySimulator
    

#####################################################################################
#
# yWaves main function
# generates one single instance of ySimulatorClass
# so it generates one single wave, which is specified in an input file
#


def run ( inputFile ):
    

    yWave = ySimulator.ySimulatorClass ( inputFile ) 

    yWave.run ()    
     
    del yWave
    
     
#####################################################################################
