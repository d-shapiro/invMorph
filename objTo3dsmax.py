import sys
from invMorph import *

def parse_obj(inp_file):
    objs = []
    obj = []
    with open(inp_file, "r") as inp:
        for line in inp:
            if line.strip().startswith("#") and "object" in line:
                if len(obj) > 0:
                    objs.append(obj)
                    obj = []
            if line.strip().startswith("v"):
                split = line.strip().split()
                if (len(split) >= 4):
                    obj.append((float(split[1]), float(split[2])))

    if len(obj) > 0:
        objs.append(obj)
    return objs


def setup_solvers(base_file):
    shapes = parse_obj(base_file)
    base_shape = shapes[0]
    targets = shapes[1:]
    return Solver(base_shape, targets), Solver2(base_shape, targets)


args = sys.argv
base_file = "targets.obj"
desireds_file = "desireds.obj"
out_file_1 = "out1.ms"
out_file_2 = "out2.ms"
if len(args) > 1:
    base_file = args[1]
if len(args) > 2:
    desireds_file = args[2]
if len(args) > 3:
    out_file_1 = args[3]
if len(args) > 4:
    out_file_2 = args[4]

solvers = setup_solvers(base_file)
solver1 = solvers[0]
solver2 = solvers[1]
# unused_inds = solver.unused_shape_inds
desired_shapes = parse_obj(desireds_file)

out = open(out_file_1, "w")

if len(desired_shapes) > 0:
    weights = solver1.solve(desired_shapes[0])
    for i in range(0, len(weights)):
        out.write("WM3_MC_SetValue$BASE.morpher " + str(i+1) + " " + str(weights[i] * 100) + "\n")

# for desired_shape in desired_shapes:
#     weights = solver.solve(desired_shape)
#     line = ",".join([str(weight) for weight in weights])
#     out.write(line)
#     out.write("\n")

out.close()

out = open(out_file_2, "w")

if len(desired_shapes) > 0:
    weights = solver2.solve(desired_shapes[0])
    for i in range(0, len(weights)):
        out.write("WM3_MC_SetValue$BASE.morpher " + str(i+1) + " " + str(weights[i] * 100) + "\n")