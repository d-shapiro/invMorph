import numpy as np
from scipy.linalg import lu


def shape_to_vector(shape_vertices):
    coords = [coord for vert in shape_vertices for coord in vert]
    return np.transpose(np.array([coords]))


def shape_v_to_morph(base_shape_v, shape_v):
    return shape_v - base_shape_v


def dot(v1, v2):
    return np.dot(v1.T, v2)[0][0]


def proj_cofficient(v1, v2):
    return dot(v2, v1) / dot(v1, v1)


def gram_schmidt(xs):
    vs = []
    for i in range(len(xs)):
        x_i = xs[i]
        v_i = x_i
        for v in vs:
            v_i = v_i - (proj_cofficient(x_i, v) * v)
        vs.append(v_i)
    return vs


class Solver:
    def __init__(self, base_shape, target_shapes):
        self.base_v = shape_to_vector(base_shape)
        assert len(self.base_v) % 2 == 0
        # self.vert_count = len(self.base_v) / 3
        self.morph_vs = [shape_v_to_morph(self.base_v, shape_to_vector(shape)) for shape in target_shapes]
        for m_v in self.morph_vs:
            assert len(m_v) == len(self.base_v)
        self.A = np.hstack(self.morph_vs)

    def solve(self, desired_shape, verbose=False):
        y_v = shape_v_to_morph(self.base_v, shape_to_vector(desired_shape))
        assert len(y_v) == len(self.base_v)

        if verbose:
            print(self.A)

        # Now solve Ax = y_v, to try to express y_v as a linear combination of the basis_vs
        soln = np.linalg.lstsq(self.A, y_v)

        x_v = soln[0]

        if verbose:
            print("solution 2 error: ")
            print(soln[1])
            print("solution 2 rank of A: ")
            print(soln[2])
            print("solution 2 singulars: ")
            print(soln[3])

            # print(self.A)

        return x_v.flatten()


# class Solver:
#     def __init__(self, base_shape, target_shapes):
#         self.base_v = shape_to_vector(base_shape)
#         assert len(self.base_v) % 2 == 0
#         # self.vert_count = len(self.base_v) / 3
#         self.morph_vs = [shape_v_to_morph(self.base_v, shape_to_vector(shape)) for shape in target_shapes]
#         for m_v in self.morph_vs:
#             assert len(m_v) == len(self.base_v)
#         A = np.hstack(self.morph_vs)
#
#         # find pivot columns of A (these form a basis for span(morph_vs))
#         U = lu(A)[2]
#
#         self.lin_indep_columns = [np.flatnonzero(U[i, :])[0] for i in range(U.shape[0]) if len(np.flatnonzero(U[i, :])) > 0]
#         basis_vs = [self.morph_vs[i] for i in range(0, len(self.morph_vs)) if i in self.lin_indep_columns]
#         self.basis_matrix = np.hstack(basis_vs)
#
#         # might want to notify user that certain shapes weren't used
#         self.unused_shape_inds = [i for i in range(0, len(self.morph_vs)) if i not in self.lin_indep_columns]
#
#         # do the Gram-Schmidt process on basis_vs to find an orthogonal basis for span(morph_vs)
#         self.orth_basis_vs = gram_schmidt(basis_vs)
#
#     def solve(self, desired_shape):
#         y_v = shape_v_to_morph(self.base_v, shape_to_vector(desired_shape))
#         assert len(y_v) == len(self.base_v)
#
#         if dot(y_v, y_v) == 0:
#             y_hat = y_v
#         else:
#             # (orthogonal decomposition theorem) find projection of y_v onto span(morph_vs)
#             coeffs = [proj_cofficient(y_v, u_v) for u_v in self.orth_basis_vs]
#
#             y_hat = sum([coeffs[i] * self.orth_basis_vs[i] for i in range(len(coeffs))])
#
#         # Now solve Ax = y_hat (with A = self.basis_matrix), to express y_hat as a linear combination of the basis_vs
#         soln = np.linalg.lstsq(self.basis_matrix, y_hat)
#
#         x_v = soln[0]
#
#         print("solution 1 error: ")
#         print(soln[1])
#         print("solution 1 rank of A: ")
#         print(soln[2])
#         print("solution 1 singulars: ")
#         print(soln[3])
#
#         # print(self.basis_matrix)
#
#         # Finish by aligning with the original set of vectors, filling in 0 as the coefficient for superfluous inputs
#
#         complete_xs = []
#         j = 0
#         for i in range(len(self.morph_vs)):
#             if j < len(self.lin_indep_columns) and self.lin_indep_columns[j] == i:
#                 complete_xs.append(x_v[j][0])
#                 j += 1
#             else:
#                 complete_xs.append(0.0)
#
#         return complete_xs


