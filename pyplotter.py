# Created by Daan Treurniet
import sys
from PySide2 import QtWidgets

import plotter_widgets
from datastore import DataStore
from inspector import Inspector

class PyPlotter():
    def __init__(self):

        self.inspector = Inspector()
        self.inspector.add('pyplotter', self)

        self.data_store = DataStore(self.inspector)

        self.app = QtWidgets.QApplication([])
        self.master_gui = plotter_widgets.MasterGUI(self.inspector)

        self.master_gui.show()
        self.inspector.get('action_menu').button_load_pressed()

        sys.exit(self.app.exec_())

if __name__ == '__main__':
    pyplotter = PyPlotter()
