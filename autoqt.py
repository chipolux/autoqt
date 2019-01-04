# -*- coding: utf_8 -*-
from functools import partial

from PyQt5.QtCore import QObject, pyqtProperty


VERSION = '0.0.5'


def getdeepr(obj, name):
    """Function to get deeper attributes, replaces getattr."""
    names = name.split('.')
    for name in names[:-1]:
        obj = getattr(obj, name)
    return getattr(obj, names[-1])


def setdeepr(obj, name, value):
    """Function to set deeper attributes, replaces setattr."""
    names = name.split('.')
    for name in names[:-1]:
        obj = getattr(obj, name)
    return setattr(obj, names[-1], value)


def _getter(self, attr):
    """Template for AutoProp fget function."""
    return getdeepr(self, attr)


def _setter(self, value, attr, signal):
    """Template for AutoProp fset function."""
    if getdeepr(self, attr) != value:
        setdeepr(self, attr, value)
        getdeepr(self, signal).emit()


class AutoProp:
    """
    Automatic pyqtProperty for AutoObject
    Generates fget and fset functions to simplify basic property access.

    Use in place of pyqtProperty when you just need to read/write an instance
    attribute without doing anything special.

    You can use the @propName.getter and setter decorators just like you would
    with a Python or PyQt property to customize them if you need to.

    fget and fset arguments work the same as on pyqtProperty as well.

    The attr argument can also contain a kind of 'object path' with
    levels/layers separated by dots. For example: attr='thing.other.stuff'
    will getattr down through the 'thing' and 'other' objects to return the
    value of 'stuff'.
    """
    def __init__(self, type_signature, signal_name, attr=None, write=False,
                 fget=None, fset=None):
        self.type_signature = type_signature
        self.signal_name = signal_name
        self.attr = attr
        self.write = write
        self.fget = fget or partial(_getter, attr=self.attr)
        self.fset = fset or partial(
            _setter, attr=self.attr, signal=self.signal_name
        )

    def getter(self, func):
        self.fget = func
        return self

    def setter(self, func):
        self.fset = func
        self.write = True
        return self


class AutoObject(QObject):
    """
    Automatic QObject
    A wrapper for QObject that uses the Python 3.6 __init_subclass__ method to
    convert all AutoProp attributes into pyqtProperties.
    """
    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(**kwargs)
        # transform AutoProp instances into pyqtProperties
        for attr in dir(cls):
            try:
                prop = getdeepr(cls, attr)
            except AttributeError:
                continue
            if not isinstance(prop, AutoProp):
                continue
            prop_kwargs = {
                'notify': getdeepr(cls, prop.signal_name),
                'fget': prop.fget if prop.fget else None,
                'fset': prop.fset if prop.write else None,
            }
            setattr(
                cls, attr, pyqtProperty(prop.type_signature, **prop_kwargs)
            )
