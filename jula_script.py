import jula, sys

unit = int(sys.argv[1])
if unit > 15:
        raise Exception("arg 1 must be less than 16")

command = int(sys.argv[2])

jula.send(unit, command)


