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
                    obj.append((split[1], split[2], split[3]))

    if len(obj) > 0:
        objs.append(obj)
    return objs

def setup_solver(base_file):
    shapes = parse_obj(base_file)
    base_shape = shapes[0]
    targets = shapes[1:]
    return Solver(base_shape, targets)


args = sys.argv
base_file = "targets.obj"
desireds_file = "desireds.obj"
out_file = "out.csv"
if len(args) > 1:
    base_file = args[1]
if len(args) > 2:
    desireds_file = args[2]
if len(args) > 3:
    out_file = args[3]

solver = setup_solver(base_file)
unused_inds = solver.unused_shape_inds
desired_shapes = parse_obj(desireds_file)

out = open(out_file, "w")

for desired_shape in desired_shapes:
    weights = solver.solve(desired_shape)
    line = ",".join([str(weight) for weight in weights])
    out.write(line)
    out.write("\n")

out.close()