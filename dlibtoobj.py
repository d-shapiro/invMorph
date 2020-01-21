import sys

facepoint_prefix = "face point :"
fp_prefix_len = len(facepoint_prefix)

args = sys.argv
inp_file = "in.txt"
out_file = "out.obj"
if len(args) > 1:
    inp_file = args[1]
if len(args) > 2:
    out_file = args[2]

out = open(out_file, "w")
faceline = "f "
i = 1
with open(inp_file, "r") as inp:
        for line in inp:
            split = line[fp_prefix_len:].strip().split()
            assert len(split) == 4
            out.write(str.format("v  {} {} 0.0000\n", float(split[1]), float(split[3])))
            faceline += str.format("{} ", i)
            i += 1

        out.write(faceline)
        out.write("\n")
        out.close()

