from util import *

# This file is a simple program that take an input directory containing dlib faces (as individual .txt files), and
# outputs a maxScript that will create those faces in 3DSMax as editable meshes. The main purpose of this is sanity
# checking the "desired" faces that are being input into the invMorph program.

args = sys.argv
input_dir = "input/desired"
out_file = "out_2.ms"
if len(args) > 1:
    input_dir = args[1]
if len(args) > 2:
    out_file = args[2]

shape_files = sorted(get_shape_files(input_dir))
shapes = parse_shapes(shape_files)

out = open(out_file, "w")
for i in range(len(shapes)):
    out.write(script_shape(shapes[i], shape_files[i].split("/")[-1][:-4]))
    out.write("\n")

out.close()
