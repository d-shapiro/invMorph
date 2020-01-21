import sys
from invMorph import *

facepoint_prefix = "face point :"
fp_prefix_len = len(facepoint_prefix)


def parse_shapes(inp_file):
    shapes = []
    shape = []
    with open(inp_file, "r") as inp:
        for line in inp:
            if line.startswith(facepoint_prefix):
                split = line[fp_prefix_len:].strip().split()
                assert len(split) == 4
                if split[0] == "y":
                    shape.append((float(split[3]), float(split[1])))
                else:
                    shape.append((float(split[1]), float(split[3])))
            else:
                if len(shape) > 0:
                    shapes.append(shape)
                    shape = []

    if len(shape) > 0:
        shapes.append(shape)
    return shapes

args = sys.argv
base_file = "base_and_targets"
desireds_file = "desireds"
out_file = "out.ms"
base_shape_name = "BASE"
if len(args) > 1:
    base_file = args[1]
if len(args) > 2:
    desireds_file = args[2]
if len(args) > 3:
    out_file = args[3]
if len(args) > 4:
    base_shape_name = args[4]

btshapes = parse_shapes(base_file)
base_shape = btshapes[0]
targets = btshapes[1:]
solver = Solver2(base_shape, targets)

desired_shapes = parse_shapes(desireds_file)

out = open(out_file, "w")

out.write("with animate on\n")
out.write("(\n")
for frame in range(0, len(desired_shapes)):
    des_shape = desired_shapes[frame]
    weights = solver.solve(des_shape)
    for i in range(0, len(weights)):
        out.write("at time " + frame + " WM3_MC_SetValue$" + base_shape_name + ".morpher " + str(i+1) + " " + str(weights[i] * 100) + "\n")

out.write(")\n")

out.close()

