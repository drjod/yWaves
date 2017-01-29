from ySimulator import ySimulator


def run(*args):
    """
    main function
    :param *args: either input file (string) or empty
    :return:
    """
    input_file = args[0] if len(args) else input('Input file: ')

    wave = ySimulator(input_file)
    wave.run()


if __name__== '__main__':
    run()
