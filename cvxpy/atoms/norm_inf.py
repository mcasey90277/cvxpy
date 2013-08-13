from atom import Atom
import cvxpy.expressions.types as types
from cvxpy.expressions.variable import Variable
from cvxpy.constraints.affine import AffEqConstraint, AffLeqConstraint
import cvxpy.utilities as u
import max
import abs

class normInf(Atom):
    """ Infinity norm max{|x|} """
    def __init__(self, x):
        super(normInf, self).__init__(x)

    def set_shape(self):
        self.validate_arguments()
        self._shape = u.Shape(1,1)

    @property
    def sign(self):
        return u.Sign.POSITIVE

    # Default curvature.
    def base_curvature(self):
        return u.Curvature.CONVEX

    def monotonicity(self):
        return [u.Monotonicity.NONMONOTONIC]

    # Verify that the argument x is a vector.
    def validate_arguments(self):
        if not self.args[0].is_vector():
            raise TypeError("The argument '%s' to normInf must resolve to a vector." 
                % self.args[0].name())

    def graph_implementation(self, var_args):
        x = var_args[0]
        return max.max(abs.abs(x)).canonicalize()