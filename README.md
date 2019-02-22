# autoqt
[![PyPI](https://badge.fury.io/py/autoqt.svg)](https://badge.fury.io/py/autoqt)

A simple single file module that makes setting up basic Qt properties a little
bit nicer without restricting you.

This is very useful if you have QObjects with many readonly properties and a
few special setters or state modifying slots.

Example:
```
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from autoqt import AutoObject, AutoProp


class SomeObject(AutoObject):
    valuesChanged = pyqtSignal()

    aNumber = AutoProp(int, 'valuesChanged', '_aNumber')
    otherNumber = AutoProp(float, 'valuesChanged', '_otherNumber')
    aString = AutoProp(str, 'valuesChanged', '_aString', write=True)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._aNumber = 10
        self._otherNumber = 20
        self._aString = 'spam'

    @pyqtSlot()
    def incrementNumber(self):
        self._aNumber += 1
        self.valuesChanged.emit()

    @otherNumber.setter
    def otherNumber(self, value):
        self._otherNumber = value + 2
        self.valuesChanged.emit()


x = SomeObject()

print(x.aNumber)  # 10
x.aNumber = 10  # throws AttributeError, readonly property
x.incrementNumber()  # valuesChanged is emitted
print(x.aNumber)  # 11

print(x.otherNumber)  # 20
x.otherNumber = 40  #  otherNumber.setter called, valuesChanged is emitted
print(x.otherNumber)  # 42

print(x.aString)  # 'spam'
x.aString = 'ham'  # valuesChanged is emitted, writable property
print(x.aString)  # 'ham'
```
