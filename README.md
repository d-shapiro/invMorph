# invMorph

Some scripts for a particular project involving dlib's face pose estimation and 3DS Max's morphs.

It is assumed that face shapes from dlib are represented in a text format where each line represents a vertex e.g. `face point : x 379 y 289`, and the vertices are in the same order as in dlib

## invMorph.py

The main program. Takes in a dlib base face, morph target faces, and desired faces, and applies the invMorph procedure to them to output a .ms maxScript.
The maxscript will first create the base and morphtarget faces in 3dsmax and set up the base's morpher with the morphtargets. Then it will create an animation, where each frame will correspond to a desired face from the input.
In each frame, it will set the base's morph weights (channel values) such that the morph produces a face that is as close as possible to that frame's desired face.

Usage: `python dlibTo3dsmax.py [input_directory] [out_file]`

The `input_directory` defaults to `input` and should contain directories named `base`, `morphset`, and `desired`. 

`input_directory/base` should contain exactly one .txt file, representing the base face.
`input_directory/morphset` should contain .txt files representing the morph target faces. The order of the resulting morph targets in 3dsMax will correspond to the lexicographic order of these files.
`input_directory/desired` should contain .txt files representing the desired faces. Their order in the resulting animation will correspond to the lexicographic order of these files.

The `out_file` defaults to `out.ms` and is the path to the output script.

### e.g.
   `python invMorph.py`

or `python invMorph.py local/path/to/input`

or `python invMorph.py C:\Users\You\absolute\path\to\input C:\Users\You\absolute\path\to\output.ms` 

etc.

## facePointsToMeshes.py

Takes an input directory containing dlib faces (as individual .txt files), and outputs a maxScript that will create those faces in 3DSMax as editable meshes. The main purpose of this is sanity checking the "desired" faces that are being input into the invMorph program.

Usage: `python facePointsToMeshes.py [input_directory] [out_file]`

The `input_directory` defaults to `input/desired` and should contain .txt files representing the faces that you want to import into 3dsMax.

The `out_file` defaults to `out_2.ms` and is the path to the output script.

### e.g. 
   `python facePointsToMeshes.py`

or `python facePointsToMeshes.py C:\Users\You\Desktop\some_faces somefacesAsMeshes.ms`

etc.
