from geomdl import NURBS
from geomdl import utilities
from geomdl.visualization import VisMPL

# Create a B-Spline curve
curve = NURBS.Curve()


# Set up the curve
curve.degree = 3
# Set control points (weights vector will be 1 by default)
# Use curve.ctrlptsw is if you are using homogeneous points as Pw
curve.ctrlpts = [[2, 7, 10], [3, 6, 5], [4, 8, -10], [5, 5, 15], [7, 6, 25], [8, 4, 7]]

# Set knot vector
#curve.knotvector = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]

# Set evaluation delta (controls the number of curve points)
curve.delta = 0.05

# Auto-generate knot vector
curve.knotvector = utilities.generate_knot_vector(curve.degree, len(curve.ctrlpts))

# Set evaluation delta
curve.delta = 0.01

# Plot the control point polygon and the evaluated curve
curve.vis = VisMPL.VisCurve2D()
curve.render()
