# -*- coding: utf_8 -*-
from functools import partial

from PyQt5.QtCore import QObject, pyqtProperty


VERSION = '0.0.3'


def _getter(self, attr):
    """Template for AutoProp fget function."""
    return getattr(self, attr)


def _setter(self, value, attr, signal):
    """Template for AutoProp fset function."""
    if getattr(self, attr) != value:
        setattr(self, attr, value)
        getattr(self, signal).emit()


class AutoProp:
    """
    Automatic pyqtProperty for AutoObject
    Generates fget and fset functions to simplify basic property access.

    Use in place of pyqtProperty when you just need to read/write an instance
    attribute without doing anything special.

    You can use the @propName.getter and setter decorators just like you would
    with a Python or PyQt property to customize them if you need to.
    """
    def __init__(self, type_signature, signal_name, attr, write=False):
        self.type_signature = type_signature
        self.signal_name = signal_name
        self.attr = attr
        self.write = write
        self.fget = partial(_getter, attr=self.attr)
        self.fset = partial(_setter, attr=self.attr, signal=self.signal_name)

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
                prop = getattr(cls, attr)
            except AttributeError:
                continue
            if not isinstance(prop, AutoProp):
                continue
            prop_kwargs = {
                'notify': getattr(cls, prop.signal_name),
                'fget': prop.fget,
                'fset': prop.fset if prop.write else None,
            }
            setattr(
                cls, attr, pyqtProperty(prop.type_signature, **prop_kwargs)
            )
