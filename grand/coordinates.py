from .libgrand import ffi, lib

import numpy

__all__ = ('CartesianCoordinatesArray', 'CartesianPoints', 'CoordinatesArray',
    'GeodeticPoints', 'Point', 'Vector')


class Point:
    '''Generic point object

    Inheriting from this object provides the 'Point' property.
    '''
    pass


class Vector:
    '''Generic vector object

    Inheriting from this object provides the 'Vector' property.
    '''


class Coordinates(numpy.ndarray):
    '''Generic container for a coordinates object

    This object can be used as a standard 1d numpy.ndarray of size 3.
    '''

    def __new__(cls):
        '''Create a empty coordinates instance
        '''
        return super().__new__(cls, 3, dtype='f8')


class CoordinatesArray(numpy.ndarray):
    '''Generic container for an array of coordinates

    This object can be used as a standard nx3 structured numpy.ndarray.
    '''

    def __new__(cls, arg):
        '''Create a coordinates instance of a given size or from a
        compatible numpy.ndarray
        '''
        if isinstance(arg, int):
            n = arg
        elif isinstance(arg, numpy.ndarray):
            n, m = arg.shape
            assert(m == 3)
        else:
            raise TypeError(type(arg))

        return super().__new__(cls, (n, 3), dtype='f8', order='C')

    @property
    def size(self):
        return self.shape[0]


class CartesianCoordinates(Coordinates):
    '''Generic container for cartesian coordinates

    The x, y and z properties allow to manipulate the corresponding coordinates.
    '''

    def __new__(cls, x=0., y=0., z=0.):
        '''Create a Cartesian coordinates instance

        Unspecified coordinates are initialized to 0.
        '''
        obj = super().__new__(cls)
        obj[0] = x
        obj[1] = y
        obj[2] = z
        return obj

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, v):
        self[0] = v

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, v):
        self[1] = v

    @property
    def z(self):
        return self[2]

    @z.setter
    def z(self, v):
        self[2] = v


class CartesianPoint(CartesianCoordinates, Point):
    '''Cartesian coordinates of a point
    '''

    def __new__(cls, x=0., y=0., z=0.):
        '''Create a new instance from another point instance or from
        x, y, z values
        '''
        if isinstance(x, Coordinates):
            obj = super().__new__(cls)

            if isinstance(x, GeodeticPoint):
                lib.turtle_ecef_from_geodetic(
                    x.latitude, x.longitude, x.height,
                    ffi.cast('double *', obj.ctypes.data)
                )
            elif isinstance(x, CartesianCoordinates):
                obj[:] = x
            else:
                raise TypeError(type(x))

            return obj

        else:
            return super().__new__(cls, x, y, z)


class CartesianCoordinatesArray(CoordinatesArray):
    '''Generic container for an array of cartesian coordinates

    In addition to the coordinates array, the x, y and z properties allow to
    manipulate the corresponding coordinates.
    '''

    @property
    def x(self):
        return self[:,0]

    @x.setter
    def x(self, v):
        self[:,0] = v

    @property
    def y(self):
        return self[:,1]

    @y.setter
    def y(self, v):
        self[:,1] = v

    @property
    def z(self):
        return self[:,2]

    @z.setter
    def z(self, v):
        self[:,2] = v


class CartesianPoints(CartesianCoordinatesArray, Point):
    '''Array of Cartesian points coordinates
    '''

    def __new__(cls, arg):
        '''Create a new instance from another coordinates object or as
        a generic CoordinatesArray
        '''
        if isinstance(arg, CoordinatesArray):
            obj = super().__new__(cls, arg.size)

            if isinstance(arg, GeodeticPoints):
                lib.turtle_ecef_from_geodetic_v(arg.size,
                    ffi.cast('double *', arg.ctypes.data),
                    ffi.cast('double *', obj.ctypes.data)
                )
            elif isinstance(arg, CartesianCoordinatesArray):
                obj[:] = arg
            else:
                raise TypeError(type(arg))

            return obj

        else:
            return super().__new__(cls, arg)


class GeodeticPoint(Coordinates, Point):
    '''Geodetic coordinates for a point

    The latitude, longitude and height properties allow to manipulate the
    corresponding coordinates.
    '''

    def __new__(cls, latitude=0., longitude=0., height=0.):
        '''Create a new instance from another point instance or from
        latitude, longitude, height values

        In the second case, unspecified coordinates are initialised to zero.
        '''
        if isinstance(latitude, Coordinates):
            arg = latitude
            obj = super().__new__(cls)

            if isinstance(arg, CartesianPoint):
                d = ffi.cast('double *', obj.ctypes.data)
                lib.turtle_ecef_from_geodetic(
                    ffi.cast('double *', arg.ctypes.data),
                    d, d + 1, d + 2
                )
            elif isinstance(arg, GeodeticPoint):
                obj[:] = arg
            else:
                raise TypeError(type(arg))

            return obj

        else:
            obj = super().__new__(cls)
            obj[0] = latitude
            obj[1] = longitude
            obj[2] = height

            return obj

    @property
    def latitude(self):
        return self[0]

    @latitude.setter
    def latitude(self, v):
        self[0] = v

    @property
    def longitude(self):
        return self[1]

    @longitude.setter
    def longitude(self, v):
        self[1] = v

    @property
    def height(self):
        return self[2]

    @height.setter
    def height(self, v):
        self[2] = v


class GeodeticPoints(CoordinatesArray, Point):
    '''Array of geodetic coordinates

    In addition to the coordinates array, the latitude, longitude and height
    properties allow to manipulate the corresponding coordinates.
    '''

    def __new__(cls, arg):
        '''Create a new instance from another coordinates object or as
        a generic CoordinatesArray
        '''
        if isinstance(arg, CoordinatesArray):
            obj = super().__new__(cls, arg.size)

            if isinstance(arg, CartesianPoints):
                lib.turtle_ecef_to_geodetic_v(arg.size,
                    ffi.cast('double *', arg.ctypes.data),
                    ffi.cast('double *', obj.ctypes.data)
                )
            elif isinstance(arg, GeodeticPoints):
                obj[:] = arg
            else:
                raise TypeError(type(arg))

            return obj

        else:
            return super().__new__(cls, arg)

    @property
    def latitude(self):
        return self[:,0]

    @latitude.setter
    def latitude(self, v):
        self[:,0] = v

    @property
    def longitude(self):
        return self[:,1]

    @longitude.setter
    def longitude(self, v):
        self[:,1] = v

    @property
    def height(self):
        return self[:,2]

    @height.setter
    def height(self, v):
        self[:,2] = v
