from subprocess import check_output


def get_number_of_lines(filename):
    return int(check_output(['wc', '-l', filename]).decode().split(' ')[0])
