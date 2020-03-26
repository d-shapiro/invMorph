import sys
import os
from invMorph import *

facepoint_prefix = "face point :"
fp_prefix_len = len(facepoint_prefix)


def get_shape_files(shapes_dir):
    (_, _, filenames) = os.walk(shapes_dir).next()
    txtfiles = [shapes_dir + "/" + f for f in filenames if f.endswith(".txt")]
    return txtfiles


def parse_shape(inp_file):
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
    return shape

def parse_shapes(inp_files):
    shapes = []
    for inp_file in inp_files:
        shapes.append(parse_shape(inp_file))
    return shapes

args = sys.argv
# base_file = "base_and_targets"
# desireds_file = "desireds"
input_dir = "input"
out_file = "out.ms"
base_shape_name = "BASE"
if len(args) > 1:
    input_dir = args[1]
if len(args) > 2:
    out_file = args[2]
if len(args) > 3:
    base_shape_name = args[3]

base_dir = input_dir + "/base"
morphs_dir = input_dir + "/morphset"
desireds_dir = input_dir + "/desired"

base_files = get_shape_files(base_dir)
morph_files = sorted(get_shape_files(morphs_dir))
desired_files = sorted(get_shape_files(desireds_dir))

assert len(base_files) == 1
assert len(morph_files) > 0
assert len(desired_files) > 0

base_shape = parse_shape(base_files[0])
targets = parse_shapes(morph_files)
solver = Solver2(base_shape, targets)

desired_shapes = parse_shapes(desired_files)

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

