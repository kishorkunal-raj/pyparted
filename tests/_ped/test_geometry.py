#!/usr/bin/python
#
# Copyright (C) 2008  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
# Red Hat Author(s): Chris Lumens <clumens@redhat.com>
#
import _ped
import unittest
from baseclass import *

# One class per method, multiple tests per class.  For these simple methods,
# that seems like good organization.  More complicated methods may require
# multiple classes and their own test suite.
class GeometryNewTestCase(RequiresDevice):
    def runTest(self):
        # Check that not passing args to _ped.Geometry.__init__ is caught.
        self.assertRaises(TypeError, _ped.Geometry)

        # And then the correct ways of creating a _ped.Geometry.
        self.assert_(isinstance(_ped.Geometry(self._device, 0, 100), _ped.Geometry))
        self.assert_(isinstance(_ped.Geometry(self._device, 0, 100, 101), _ped.Geometry))

class GeometryGetSetTestCase(RequiresDevice):
    def setUp(self):
        RequiresDevice.setUp(self)
        self.g = _ped.Geometry(self._device, start=0, length=100)

    def runTest(self):
        # Test that passing the kwargs to __init__ works.
        self.assert_(isinstance(self.g, _ped.Geometry))
        self.assert_(self.g.start == 0)
        self.assert_(self.g.length == 100)
        self.assert_(self.g.end == 99)

        # Test that setting directly and getting with getattr works.
        self.g.start = 10
        self.g.length = 90
        self.g.end = 99

        self.assert_(getattr(self.g, "start") == 10)
        self.assert_(getattr(self.g, "length") == 90)
        self.assert_(getattr(self.g, "end") == 99)

        # Check that setting with setattr and getting directly works.
        setattr(self.g, "start", 20)
        setattr(self.g, "length", 80)
        setattr(self.g, "end", 99)

        self.assert_(self.g.start == 20)
        self.assert_(self.g.length == 80)
        self.assert_(self.g.end == 99)

        # Check that values have the right type.
        self.assertRaises(TypeError, setattr, self.g, "start", "string")

        # Check that looking for invalid attributes fails properly.
        self.assertRaises(AttributeError, getattr, self.g, "blah")

class GeometryDuplicateTestCase(RequiresDevice):
    def setUp(self):
        RequiresDevice.setUp(self)
        self.g = _ped.Geometry(self._device, start=0, length=100)

    def runTest(self):
        self.dup = self.g.duplicate()
        self.assert_(self.g.start == self.dup.start)
        self.assert_(self.g.length == self.dup.length)
        self.assert_(self.g.end == self.dup.end)

class GeometryIntersectTestCase(RequiresDevice):
    def setUp(self):
        RequiresDevice.setUp(self)
        self.g1 = _ped.Geometry(self._device, start=0, length=100)
        self.g2 = _ped.Geometry(self._device, start=0, length=100)

    def runTest(self):
       # g1 and g2 are the same, so their intersection is the same
        self.i = self.g1.intersect(self.g2)
        self.assert_(self.i.start == self.g1.start)
        self.assert_(self.i.end == self.g1.end)
        self.assert_(self.i.length == self.g1.length)

        # g2 is the second half of g1, so their intersection is the same as g2.
        self.g2.set_start(50)
        self.i = self.g1.intersect(self.g2)
        self.assert_(self.i.start == self.g2.start)
        self.assert_(self.i.end == self.g2.end)
        self.assert_(self.i.length == self.g2.length)

        # g2 only partially overlaps the end of g1, so they have a more
        # interesting intersection.
        self.g1.set_end(75)
        self.i = self.g1.intersect(self.g2)
        self.assert_(self.i.start == self.g2.start)
        self.assert_(self.i.end == self.g1.end)
        self.assert_(self.i.length == 25)

        # g1 and g2 do not overlap at all, so they have no intersection.
        self.g1.set(0, 25)
        self.g2.set(50, 100)
        self.assertRaises(ArithmeticError, self.g1.intersect, self.g2)

class GeometryDestroyTestCase(RequiresDevice):
    def setUp(self):
        RequiresDevice.setUp(self)
        self.g = _ped.Geometry(self._device, start=0, length=100)

    def runTest(self):
        self.g.destroy()
        self.assert_(hasattr(self.g, "start") == False)

class GeometrySetTestCase(RequiresDevice):
    def setUp(self):
        RequiresDevice.setUp(self)
        self.g = _ped.Geometry(self._device, start=0, length=100)

    def runTest(self):
        self.assert_(self.g.start == 0)
        self.assert_(self.g.length == 100)

        # Setting a negative for either value, or a length past the end of
        # the device should fail.
        self.assertRaises(_ped.CreateException, self.g.set, 100, -1000)
        self.assertRaises(_ped.CreateException, self.g.set, -1, 1000)
        self.assertRaises(_ped.CreateException, self.g.set, 0, 1000000000)

class GeometrySetStartTestCase(RequiresDevice):
    def setUp(self):
        RequiresDevice.setUp(self)
        self.g = _ped.Geometry(self._device, start=0, length=100)

    def runTest(self):
        self.g.set_start(10)
        self.assert_(self.g.start == 10)
        self.assert_(self.g.length == 90)
        self.assert_(self.g.end == 100)

        # Setting a negative start or the start past the end of the device
        # should fail.
        self.assertRaises(_ped.CreateException, self.set_start, -1)
        self.assertRaises(_ped.CreateException, self.set_start, 1000000000)

class GeometrySetEndTestCase(RequiresDevice):
    def setUp(self):
        RequiresDevice.setUp(self)
        self.g = _ped.Geometry(self._device, start=0, length=100)

    def runTest(self):
        self.g.set_end(50)
        self.assert_(self.g.start == 0)
        self.assert_(self.g.length == 50)
        self.assert_(self.g.end == 50)

        # Setting a negative end or the end past the end of the device or
        # before the start should fail.
        self.assertRaises(_ped.CreateException, self.set_end, -1)
        self.assertRaises(_ped.CreateException, self.set_end, 1000000000)
        self.g.set_start(10)
        self.assertRaises(_ped.CreateException, self.set_end, 50)

class GeometryTestOverlapTestCase(RequiresDevice):
    def setUp(self):
        RequiresDevice.setUp(self)
        self.g1 = _ped.Geometry(self._device, start=0, length=100)
        self.g2 = _ped.Geometry(self._device, start=50, length=100)

    def runTest(self):
        # g2 occupies the second half of g1, so they overlap.
        self.assert_(self.g1.test_overlap(self.g2) == True)

        # g2 is entirely contained within g1, so they overlap.
        self.g2.set_end(75)
        self.assert_(self.g1.test_overlap(self.g2) == True)

        # g1 goes from inside g2 to the end, so they overlap.
        self.g1.set_start(60)
        self.assert_(self.g1.test_overlap(self.g2) == True)

        # g2 exists entirely before g1, so they do not overlap.
        self.g2.set(10, 10)
        self.assert_(self.g1.test_overlap(self.g2) == False)

class GeometryTestInsideTestCase(RequiresDevice):
    def setUp(self):
        RequiresDevice.setUp(self)
        self.g1 = _ped.Geometry(self._device, start=0, length=100)
        self.g2 = _ped.Geometry(self._device, start=0, length=100)

    def runTest(self):
        # g1 and g2 are the same, so they exist inside each other.
        self.assert_(self.g1.test_inside(self.g2) == True)
        self.assert_(self.g2.test_inside(self.g1) == False)

        # g2 is entirely contained within g1, so it's inside.
        self.g2.set_end(75)
        self.assert_(self.g1.test_overlap(self.g2) == True)
        self.assert_(self.g2.test_overlap(self.g1) == False)

        # g1 goes from inside g2 to the end, it's inside.
        self.g1.set_start(60)
        self.assert_(self.g1.test_overlap(self.g2) == True)
        self.assert_(self.g2.test_overlap(self.g1) == False)

        # g2 exists entirely before g1, so they do not overlap.
        self.g2.set(10, 10)
        self.assert_(self.g1.test_overlap(self.g2) == False)
        self.assert_(self.g2.test_overlap(self.g1) == False)

class GeometryTestEqualTestCase(RequiresDevice):
    def setUp(self):
        RequiresDevice.setUp(self)
        self.g1 = _ped.Geometry(self._device, start=0, length=100)
        self.g2 = _ped.Geometry(self._device, start=0, length=100)

    def runTest(self):
        # g1 and g2 have the same start and end.
        self.assert_(self.g1.test_equal(self.g2) == True)

        # g1 and g2 have the same end, but different starts.
        self.g2.set_start(5)
        self.assert_(self.g1.test_equal(self.g2) == False)

        # g1 and g2 have the same start, but different ends.
        self.g2.set_start(5)
        self.g2.set_end(50)
        self.assert_(self.g1.test_equal(self.g2) == False)

class GeometryTestSectorInsideTestCase(unittest.TestCase):
    def runTest(self):
        # TODO
        pass

class GeometryReadTestCase(unittest.TestCase):
    def runTest(self):
        # TODO
        pass

class GeometrySyncTestCase(unittest.TestCase):
    def runTest(self):
        # TODO
        pass

class GeometrySyncFastTestCase(unittest.TestCase):
    def runTest(self):
        # TODO
        pass

class GeometryWriteTestCase(unittest.TestCase):
    def runTest(self):
        # TODO
        pass

class GeometryCheckTestCase(unittest.TestCase):
    def runTest(self):
        # TODO
        pass

class GeometryMapTestCase(unittest.TestCase):
    def runTest(self):
        # TODO
        pass

# And then a suite to hold all the test cases for this module.
def suite():
    suite = unittest.TestSuite()
    suite.addTest(GeometryNewTestCase())
    suite.addTest(GeometryGetSetTestCase())
    suite.addTest(GeometryDuplicateTestCase())
    suite.addTest(GeometryIntersectTestCase())
    suite.addTest(GeometryDestroyTestCase())
    suite.addTest(GeometrySetTestCase())
    suite.addTest(GeometrySetStartTestCase())
    suite.addTest(GeometrySetEndTestCase())
    suite.addTest(GeometryTestOverlapTestCase())
    suite.addTest(GeometryTestInsideTestCase())
    suite.addTest(GeometryTestEqualTestCase())
    suite.addTest(GeometryTestSectorInsideTestCase())
    suite.addTest(GeometryReadTestCase())
    suite.addTest(GeometrySyncTestCase())
    suite.addTest(GeometrySyncFastTestCase())
    suite.addTest(GeometryWriteTestCase())
    suite.addTest(GeometryCheckTestCase())
    suite.addTest(GeometryMapTestCase())
    return suite

s = suite()
unittest.TextTestRunner(verbosity=2).run(s)