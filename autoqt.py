# -*- coding: utf_8 -*-
from functools import partial

try:
    from PySide2.QtCore import QObject, Property
    USING = 'PySide2'
except Exception:
    from PyQt5.QtCore import QObject, pyqtProperty as Property
    USING = 'PyQt5'


VERSION = '0.0.6'


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


def _setter(self, value, attr, sig, typ):
    """Template for AutoProp fset function."""
    if not isinstance(typ, str) and not isinstance(value, typ):
        raise TypeError('{} is not {}'.format(value, typ))
    if getdeepr(self, attr) != value:
        setdeepr(self, attr, value)
        getdeepr(self, sig).emit()


class AutoProp:
    """
    Automatic property for AutoObject
    Generates fget and fset functions to simplify basic property access.

    Use in place of pyqtProperty or Property when you just need to read/write
    an instance attribute without doing anything special.

    You can use the @propName.getter and setter decorators just like you would
    with a Python or PyQt property to customize them if you need to.

    fget and fset arguments work the same as on pyqtProperty/Property as well.

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
            _setter, attr=self.attr, sig=self.signal_name, typ=type_signature
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
    convert all AutoProp attributes into Qt properties.
    """
    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(**kwargs)
        # transform AutoProp instances into Qt properties
        for attr in dir(cls):
            try:
                prop = getdeepr(cls, attr)
            except AttributeError:
                continue
            if not isinstance(prop, AutoProp):
                continue
            prop_kwargs = {'notify': getdeepr(cls, prop.signal_name)}
            if prop.fget:
                prop_kwargs['fget'] = prop.fget
            if prop.write:
                prop_kwargs['fset'] = prop.fset
            setattr(
                cls, attr, Property(prop.type_signature, **prop_kwargs)
            )
