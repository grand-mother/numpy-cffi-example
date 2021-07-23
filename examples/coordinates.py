from grand.coordinates import CartesianPoint, CartesianPoints, GeodeticPoint,  \
                              GeodeticPoints
import numpy


# A nx3 numpy array can be viewed as a coordinates type.
array = numpy.ones((2, 3))
points = array.view(CartesianPoints)

# Note that this is equivalent to a cast. I.e. array and points refer to the
# same data. See e.g. below.
assert(points.x[0] == 1)
points.z = (0, 2)
assert(array[1,2] == 2)

# New coordinates data are created with the constructor syntax. The constructor
# takes a single argument that can be:
#
# 1. An `int` specifying the size of the coordinates. The data are created empty
#    i.e. with random values.
#
# 2. An nx3 numpy ndarray. The data of the array are copied.
#
# 3. An other coordinates object. The data are copied and converted to the
#    new parametrization if needed, e.g. from Cartesian to geodetic.
#
# Note that in all three cases a new data array is created, I.e. not a
# reference.
#
# The example below creates an empty array of 10 geodetic points and sets its
# data to equal values. Then a new array of cartesian points is created from
# the latter.
geodetic = GeodeticPoints(10)
geodetic.latitude = 45
geodetic.longitude = 3
geodetic.height = 0

cartesian = CartesianPoints(geodetic)
print(cartesian.x[0]) # <= this is the corresponding ECEF x coordinates

# Note if a coordinates object is viewed as another coordinates object then
# the data are not converted. Thus, this is usually wrong.
cartesian = geodetic.view(CartesianPoints)
print(cartesian.x[0]) # <= this is still the latitude


# Similar operations are available for scalar coordinates instances. Though,
# whenever possible it is more efficient CPU wise to deal with coordinates
# packed as arrays.

# A 1d numpy.ndarray of size 3 can be viewed as a scalar coordinates object.
array = numpy.ones(3)
point = array.view(CartesianPoint)

# Note that as previously array and point refer to the same data. See e.g.
# below.
assert(point.x == 1)
point.z = 2
assert(array[2] == 2)

# New scalar coordinates are created with the constructor syntax. The
# constructor has two syntaxes.
#
# 1. Zero to three arguments are provided specifing the coordinates values.
#    Unspecified coordinates are initialised to 0.
#
# 2. A coordinates object is provided as single argument. The data are copied
#    and converted if needed.
#
# The example below creates an geodetic point and converts it to Cartesian
# (ECEF) coordinates.
geodetic = GeodeticPoint(45, 3, 0)
cartesian = CartesianPoint(geodetic)
print(cartesian.x)
