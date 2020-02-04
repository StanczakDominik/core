# cython: language_level=3

# Copyright 2016-2018 Euratom
# Copyright 2016-2018 United Kingdom Atomic Energy Authority
# Copyright 2016-2018 Centro de Investigaciones Energéticas, Medioambientales y Tecnológicas
#
# Licensed under the EUPL, Version 1.1 or – as soon they will be approved by the
# European Commission - subsequent versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at:
#
# https://joinup.ec.europa.eu/software/page/eupl5
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the Licence is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied.
#
# See the Licence for the specific language governing permissions and limitations
# under the Licence.


from raysect.core.math.vector cimport new_vector3d, Vector3D
from raysect.core.math.function cimport autowrap_function3d


cdef class VectorFunction3D:
    """
    Cython optimised class for representing an arbitrary 3D vector function.

    Returns a Vector3D for a given 3D coordinate.

    Using __call__() in cython is slow. This class provides an overloadable
    cython cdef evaluate() method which has much less overhead than a python
    function call.

    For use in cython code only, this class cannot be extended via python.

    To create a new function object, inherit this class and implement the
    evaluate() method. The new function object can then be used with any code
    that accepts a function object.
    """

    cdef Vector3D evaluate(self, double x, double y, double z):

        raise NotImplementedError("The evaluate() method has not been implemented.")

    def __call__(self, double x, double y, double z):

        return self.evaluate(x, y, z)


cdef class ConstantVector3D(VectorFunction3D):
    """Constant 3D real vector function.

    Inherits from Function3D, implements `__call__(x, y, z)`.

    .. code-block:: pycon

       >>> from raysect.core.math import Vector3D
       >>> from cherab.core.math import ConstantVector3D
       >>>
       >>> f3 = ConstantVector3D(Vector3D(0.5, 0.5, 0.5))
       >>>
       >>> f3(1, 1, 6)
       Vector3D(0.5, 0.5, 0.5)
       >>> f3(-1, 7e6, -1e999)
       Vector3D(0.5, 0.5, 0.5)
    """

    def __init__(self, Vector3D value not None):
        self.value = value

    cdef Vector3D evaluate(self, double x, double y, double z):
        return self.value


cdef class PythonVectorFunction3D(VectorFunction3D):
    """
    Wraps a python callable object with a VectorFunction3D object.

    This class allows a python object to interact with cython code that requires
    a VectorFunction3D object. The python object must implement __call__()
    expecting three arguments and return a Vector3D object.

    This class is intended to be used to transparently wrap python objects that
    are passed via constructors or methods into cython optimised code. It is not
    intended that the users should need to directly interact with these wrapping
    objects. Constructors and methods expecting a VectorFunction3D object should
    be designed to accept a generic python object and then test that object to
    determine if it is an instance of VectorFunction3D. If the object is not a
    VectorFunction3D object it should be wrapped using this class for internal
    use.

    See also: autowrap_vectorfunction3d()

    :param object function: the 3d vector function object to wrap.

    .. code-block:: pycon

       >>> from raysect.core import Vector3D
       >>> from cherab.core.math import PythonVectorFunction3D
       >>>
       >>> def vectorfunction3d(x, y, z):
       >>>     return Vector3D(1, 0, 0)
       >>>
       >>> fv3 = PythonVectorFunction3D(vectorfunction3d)
       >>> fv3(0, 1, 3.5)
       Vector3D(1.0, 0.0, 0.0)
    """

    def __init__(self, object function):

        self.function = function

    cdef Vector3D evaluate(self, double x, double y, double z):

        return self.function(x, y, z)


cdef VectorFunction3D autowrap_vectorfunction3d(object function):
    """
    Automatically wraps the supplied python object in a PythonVectorFunction3D
    object.

    If this function is passed a valid VectorFunction3D object, then the
    VectorFunction3D object is simply returned without wrapping.

    If this function is passed a Vector3D, a ConstantVector3D object is
    returned.

    This convenience function is provided to simplify the handling of
    VectorFunction3D and python callable objects in constructors, functions and
    setters.
    """

    if isinstance(function, VectorFunction3D):
        return <VectorFunction3D> function
    if isinstance(function, Vector3D):
        return ConstantVector3D(function)
    return PythonVectorFunction3D(function)


cdef class ScalarToVectorFunction3D(VectorFunction3D):
    """
    Combines three Function3D objects to produce a VectorFunction3D.

    The three Function3D objects correspond to the x, y and z components of the
    resulting vector object.

    :param Function3D x_function: the Vx(x, y, z) 3d function.
    :param Function3D y_function: the Vy(x, y, z) 3d function.
    :param Function3D z_function: the Vz(x, y, z) 3d function.

    .. code-block:: pycon

       >>> from cherab.core.math import Constant3D
       >>> from cherab.core.math.function import ScalarToVectorFunction3D
       >>>
       >>> vx = Constant3D(1)
       >>> vy = Constant3D(2)
       >>> vz = Constant3D(3)
       >>>
       >>> fv = ScalarToVectorFunction3D(vx, vy, vz)
       >>> fv(3.5, 6.2, -2.2)
       Vector3D(1.0, 2.0, 3.0)
    """

    def __init__(self, object x_function, object y_function, object z_function):

        super().__init__()
        self._x = autowrap_function3d(x_function)
        self._y = autowrap_function3d(y_function)
        self._z = autowrap_function3d(z_function)

    cdef Vector3D evaluate(self, double x, double y, double z):

        return new_vector3d(self._x.evaluate(x, y, z),
                            self._y.evaluate(x, y, z),
                            self._z.evaluate(x, y, z))

