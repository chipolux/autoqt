from importlib import reload
from unittest import mock
import sys
import unittest

from PySide2.QtCore import Signal
from PyQt5.QtCore import pyqtSignal

import autoqt


class TestAutoQt:
    def test_default_getter(self):
        """ensure default getter returns value"""

        class Obj(autoqt.AutoObject):
            signal = self.sig()
            i = autoqt.AutoProp(int, 'signal', '_i')
            s = autoqt.AutoProp(str, 'signal', '_s')

            def __init__(self, parent=None):
                super().__init__(parent)
                self._i = 10
                self._s = 'stuff'

        obj = Obj()
        self.assertEqual(obj.i, 10)
        self.assertEqual(obj.s, 'stuff')

    def test_default_setter(self):
        """ensure default setter sets value"""

        class Obj(autoqt.AutoObject):
            signal = self.sig()
            i = autoqt.AutoProp(int, 'signal', '_i', write=True)
            s = autoqt.AutoProp(str, 'signal', '_s', write=True)

            def __init__(self, parent=None):
                super().__init__(parent)
                self._i = 10
                self._s = 'stuff'

        obj = Obj()
        obj.i = 11
        self.assertEqual(obj._i, 11)
        obj.s = 'other'
        self.assertEqual(obj._s, 'other')

    def test_default_setter_emits(self):
        """ensure default setter emits signal"""

        class Obj(autoqt.AutoObject):
            iChanged = self.sig()
            sChanged = self.sig()
            i = autoqt.AutoProp(int, 'iChanged', '_i', write=True)
            s = autoqt.AutoProp(str, 'sChanged', '_s', write=True)

            def __init__(self, parent=None):
                super().__init__(parent)
                self._i = 10
                self._s = 'stuff'

        obj = Obj()
        obj.iChanged = mock.Mock()
        obj.sChanged = mock.Mock()
        obj.i = 11
        obj.iChanged.emit.assert_called()
        obj.s = 'other'
        obj.sChanged.emit.assert_called()

    def test_write_no_setter(self):
        """should throw AttributeError when writing without setter"""

        class Obj(autoqt.AutoObject):
            signal = self.sig()
            i = autoqt.AutoProp(int, 'signal', '_i')
            s = autoqt.AutoProp(str, 'signal', '_s')

            def __init__(self, parent=None):
                super().__init__(parent)
                self._i = 10
                self._s = 'stuff'

        obj = Obj()
        with self.assertRaises(AttributeError):
            obj.i = 11
        with self.assertRaises(AttributeError):
            obj.s = 'other'

    def test_write_wrong_type(self):
        """should throw TypeError when writing an invalid type"""

        class Obj(autoqt.AutoObject):
            signal = self.sig()
            i = autoqt.AutoProp(int, 'signal', '_i', write=True)
            s = autoqt.AutoProp(str, 'signal', '_s', write=True)

            def __init__(self, parent=None):
                super().__init__(parent)
                self._i = 10
                self._s = 'stuff'

        obj = Obj()
        with self.assertRaises(TypeError):
            obj.i = 'other'
        with self.assertRaises(TypeError):
            obj.s = 11

    def test_read_without_attr(self):
        """should throw AttributeError when reading property without an attr"""

        class Obj(autoqt.AutoObject):
            signal = self.sig()
            s = autoqt.AutoProp(str, 'signal')

        obj = Obj()
        with self.assertRaises(AttributeError):
            obj.s


class TestPyQt(unittest.TestCase, TestAutoQt):
    def setUp(self):
        # start pre-empting PySide2 imports
        sys.modules['PySide2.QtCore'] = None
        reload(autoqt)
        self.sig = pyqtSignal

    def tearDown(self):
        # stop pre-empting PySide2 imports
        sys.modules.pop('PySide2.QtCore')

    def test_uses_pyqt(self):
        """autoqt should be using PyQt5"""
        self.assertEqual(autoqt.USING, 'PyQt5')


class TestPySide(unittest.TestCase, TestAutoQt):
    def setUp(self):
        # start pre-empting PyQt5 imports
        sys.modules['PyQt5.QtCore'] = None
        reload(autoqt)
        self.sig = Signal

    def tearDown(self):
        # stop pre-empting PyQt5 imports
        sys.modules.pop('PyQt5.QtCore')

    def test_uses_pyqt(self):
        """autoqt should be using PySide2"""
        self.assertEqual(autoqt.USING, 'PySide2')
