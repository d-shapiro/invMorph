# invMorph

Some scripts for a particular project involving dlib's face pose estimation and 3DS Max's morphs.

It is assumed that face shapes from dlib are represented in a text format where each line represents a vertex e.g. `face point : x 379 y 289`, and the vertices are in the same order as in dlib

## dlibtoobj.py
Converts a face shape output by dlib to a .obj file consisting of one face, which consists of all the dlib vertices in order
  
Usage: `python dlibtoobj.py <input_file> <output_file> [limit]`
  
The optional `limit` argument ensures that the output has no more than that many vertices
  
e.g. `python dlibtoobj.py in_01.txt out.obj` or `python dlibtoobj.py in_01.txt out.obj 68`
  
## dlibTo3dsmax.py

Takes in a dlib base face, morph target faces, and desired faces, and applies the invMorph procedure to them to output a .ms maxScript.
The maxscript assumes that the base face is already loaded into 3dsmax and is set up with the morph target faces as morph targets.
Each frame in the maxscript will correspond to a desired face from the input.
In each frame, it will set the base's morph weights such that the morph produces a face that is as close as possible to that frame's desired face.

Usage: `python dlibTo3dsmax.py <base_and_morph_targets_file> <desireds_file> <out_file> [base_shape_name]`

The base_and_morph_targets_file should contain first the base face, then the morph target faces in order, with empty lines separating faces

The desireds_file should contain all desired faces, in frame order, with empty lines separating faces

The base_shape_name is what the base face is called in 3DSMax, and defaults to "BASE"

e.g. `python dlibTo3dsmax.py base_and_targets.txt frames.txt out.ms`
