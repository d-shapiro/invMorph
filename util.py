import sys
import os
#from invMorphSolver import *

facepoint_prefix = "face point :"
fp_prefix_len = len(facepoint_prefix)


# returns a list of the filepaths of all .txt files in the given directory
def get_shape_files(shapes_dir):
    (_, _, filenames) = os.walk(shapes_dir).next()
    txtfiles = [shapes_dir + "/" + f for f in filenames if f.endswith(".txt")]
    return txtfiles


# reads a .txt file containing dlib face points and parses it into a list of (x,y) tuples
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


# takes a list of file paths and calls parse_shape on each one, outputs a list of lists of (x,y) tuples
def parse_shapes(inp_files):
    shapes = []
    for inp_file in inp_files:
        shapes.append(parse_shape(inp_file))
    return shapes


# given a list of (x,y) tuples representing a dlib face, and a name, returns a MaxScript snippet that will create that
# dlib face as a 3DSMax editable mesh object with the given name
def script_shape(shape, var_name):
    script = "vert_array = #()\nface_array = #()\n"
    vert_count = len(shape)
    for i in range(vert_count):
        vert = shape[i]
        script += "append vert_array [%f,%f,0]\n" % (vert[0], vert[1])
        if i > 0 and i % 2 == 0:
            script += "append face_array [%d,%d,%d]\n" % (i-1, i, i+1)
    if vert_count % 2 == 0:
        script += "append face_array [%d,%d,%d]\n" % (vert_count - 1, vert_count, 1)
    script += "%s = mesh vertices:vert_array faces:face_array\n" % var_name
    script += '%s.name = "%s"\n' % (var_name, var_name)
    return script
