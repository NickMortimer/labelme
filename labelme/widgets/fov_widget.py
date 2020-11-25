from qtpy import QtCore
from qtpy import QtGui
from qtpy import QtWidgets


class FovWidget(QtWidgets.QSpinBox):
    def __init__(self, value=1,numberOfViews=6):
        super(FovWidget, self).__init__()
        self.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.setRange(1, numberOfViews*numberOfViews)
        self.setSuffix(f" of {numberOfViews*numberOfViews}")
        self.setValue(value)
        self.setToolTip("Fov Number")
        self.setStatusTip(self.toolTip())
        self.setAlignment(QtCore.Qt.AlignCenter)

    def minimumSizeHint(self):
        height = super(FovWidget, self).minimumSizeHint().height()
        fm = QtGui.QFontMetrics(self.font())
        width = fm.width(str(self.maximum()))
        return QtCore.QSize(width, height)