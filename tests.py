from importlib import reload
import sys
import unittest

import autoqt


class TestPyQt(unittest.TestCase):
    def setUp(self):
        sys.modules['PySide2.QtCore'] = None
        reload(autoqt)

    def tearDown(self):
        sys.modules.pop('PySide2.QtCore')

    def test_uses_pyqt(self):
        """autoqt should be using PyQt5"""
        self.assertEqual(autoqt.USING, 'PyQt5')


class TestPySide(unittest.TestCase):
    def setUp(self):
        sys.modules['PyQt5.QtCore'] = None
        reload(autoqt)

    def tearDown(self):
        sys.modules.pop('PyQt5.QtCore')

    def test_uses_pyqt(self):
        """autoqt should be using PySide2"""
        self.assertEqual(autoqt.USING, 'PySide2')
