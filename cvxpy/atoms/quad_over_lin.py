from atom import Atom
import cvxpy.expressions.types as types
from cvxpy.expressions.variable import Variable
from cvxpy.constraints.second_order import SOC
from cvxpy.constraints.affine import AffEqConstraint, AffLeqConstraint
import cvxpy.utilities as u
import cvxpy.interface.matrix_utilities as intf
import vstack

class quad_over_lin(Atom):
    """ x'*x/y """
    def __init__(self, x, y):
        super(quad_over_lin, self).__init__(x, y)

    # The shape is the common width and the sum of the heights.
    def set_shape(self):
        self.validate_arguments()
        self._shape = u.Shape(1,1)

    @property
    def sign(self):
        return u.Sign.POSITIVE

    # Default curvature.
    def base_curvature(self):
        return u.Curvature.CONVEX

    def monotonicity(self): # TODO what would make sense?
        return [u.Monotonicity.NONMONOTONIC, u.Monotonicity.DECREASING]

    # Any argument size is valid.
    def validate_arguments(self):
        if not self.args[0].is_vector():
            raise TypeError("The first argument to quad_over_lin must be a vector.")
        elif not self.args[1].is_scalar():
            raise TypeError("The seconde argument to quad_over_lin must be a scalar.")

    def graph_implementation(self, var_args):
        v = Variable(*self.size)
        x = var_args[0]
        y = var_args[1]

        constraints = SOC(y + v, vstack.vstack(y - v, 2*x)).canonicalize()[1]
        constraints += [AffLeqConstraint(0, y)]
        return (v, constraints)