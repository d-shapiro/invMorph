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
    return np.dot(v2, v1) / np.dot(v1, v1)


def gram_schmidt(xs):
    vs = []
    for i in range(len(xs)):
        x_i = xs[i]
        v_i = x_i
        for v in vs:
            v_i = v_i - (proj_cofficient(x_i, v) * v)
        vs.append(v_i)
    return vs

    # can just use QR factoriztion?
    # Q, R = np.linalg.qr(np.hstack(xs))
    # return np.hsplit(Q, Q.shape[1])


class Solver:
    def __init__(self, base_shape, target_shapes):
        self.base_v = shape_to_vector(base_shape)
        assert len(self.base_v) % 3 == 0
        # self.vert_count = len(self.base_v) / 3
        self.morph_vs = [shape_v_to_morph(self.base_v, shape_to_vector(shape)) for shape in target_shapes]
        for m_v in self.morph_vs:
            assert len(m_v) == len(self.base_v)
        A = np.hstack(self.morph_vs)

        # find pivot columns of A (these form a basis for span(morph_vs))
        U = lu(A)[2]
        self.lin_indep_columns = [np.flatnonzero(U[i, :])[0] for i in range(U.shape[0])]
        basis_vs = [self.morph_vs[i] for i in range(0, len(self.morph_vs)) if i in self.lin_indep_columns]
        self.basis_matrix = np.hstack(basis_vs)

        # might want to notify user that certain shapes weren't used
        unused_shape_inds = [i for i in range(0, len(self.morph_vs)) if i not in self.lin_indep_columns]

        # do the Gram-Schmidt process on basis_vs to find an orthogonal basis for span(morph_vs)
        self.orth_basis_vs = gram_schmidt(basis_vs)

    def solve(self, desired_shape):
        y_v = shape_v_to_morph(self.base_v, shape_to_vector(desired_shape))
        assert len(y_v) == len(self.base_v)

        # (orthogonal decomposition theorem) find projection of y_v onto span(morph_vs)
        coeffs = [proj_cofficient(y_v, u_v) for u_v in self.orth_basis_vs]

        y_hat = sum([coeffs[i] * self.orth_basis_vs[i] for i in range(len(coeffs))])

        # Now solve Ax = y_hat (with A = self.basis_matrix), to express y_hat as a linear compbination of the basis_vs
        x_v = np.linalg.solve(self.basis_matrix, y_hat)

        # Finish by aligning with the original set of vectors, filling in 0 as the coefficient for superfluous inputs

        complete_xs = []
        j = 0
        for i in range(len(self.morph_vs)):
            if j < len(self.lin_indep_columns) and self.lin_indep_columns[j] == i:
                complete_xs.append(x_v[j])
                j += 1
            else:
                complete_xs.append(0)

        return complete_xs



