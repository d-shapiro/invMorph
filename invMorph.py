from invMorphSolver import *
from util import *

# This file is the main invMorph program. Given an input directory containing a base dlib face, morph target faces, and
# desired faces (that we want to create using the base and morphtargets), this program will output a MaxScript that will
# create the base and morphtarget faces in 3dsmax, set up the base's morpher with the morphtargets, and then create an
# animation. Each frame of the animation will correspond to a different desired face (going in lexicographical order of
# file names) and the morpher channel values in that frame will be set so as to morph the base shape into as close an
# approximation as possible of that frame's desired face.

# first, parse command-line parameters, if any.
args = sys.argv
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

# look through the input directory and find all of the necessary input files
base_files = get_shape_files(base_dir)
morph_files = sorted(get_shape_files(morphs_dir))
desired_files = sorted(get_shape_files(desireds_dir))

# there should be exactly one base file
assert len(base_files) == 1
assert len(morph_files) > 0
assert len(desired_files) > 0

# parse the input files into lists of (x,y) tuples
base_shape = parse_shape(base_files[0])
targets = parse_shapes(morph_files)
desired_shapes = parse_shapes(desired_files)

# setup the solver by providing it with base face shape and morph targets
solver = Solver(base_shape, targets)

# open the output file for writing our maxScript to
out = open(out_file, "w")

# write the maxScript lines that will create the base shape as an editable mesh, and call it 'BASE'
out.write(script_shape(base_shape, base_shape_name))

# these next maxScript lines setup a morpher modifier and add it to the base object
out.write("mymorpher = Morpher()\n")
out.write("mymorpher.Use_Limits = 0\n")
out.write("mymorpher.Autoload_of_targets = 1\n")
out.write("addModifier %s mymorpher\n" % base_shape_name)
out.write("\n")

# for each morph target shape, write maxScript lines that will create it as an editable mesh, and set it as a morph
# target for BASE's morpher modifier
for i in range(len(targets)):
    target_name = "TARGET_" + str(i+1)
    out.write(script_shape(targets[i], target_name))
    out.write("WM3_MC_BuildFromNode$%s.morpher %d $%s\n" % (base_shape_name, i+1, target_name))
    out.write("\n")

# now we will go through our desired shapes, and dedicate a frame of animation to each one
out.write("with animate on\n")
out.write("(\n")
for frame in range(0, len(desired_shapes)):
    des_shape = desired_shapes[frame]

    # we invoke the solver to get a list of weights that, when applied as channel values to the morpher we set up,
    # should create a face that is as close as possible to the desired one.
    weights = solver.solve(des_shape)

    # write lines of maxScript setting BASE's channel values to these weights, for the current frame only
    for i in range(0, len(weights)):
        out.write("at time %d WM3_MC_SetValue$%s.morpher %d %f\n" % (frame, base_shape_name, i+1, weights[i] * 100))

out.write(")\n")

out.close()

