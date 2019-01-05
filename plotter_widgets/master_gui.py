from PySide2.QtWidgets import QWidget, QVBoxLayout, QGridLayout

import plotter_widgets


class MasterGUI(QWidget):
    def __init__(self, inspector):
        super().__init__()
        self.inspector = inspector
        self.inspector.add('master_gui', self)

        self.actions_menu = plotter_widgets.ActionMenu(self.inspector)
        self.file_browser = plotter_widgets.FileBrowser(self.inspector)
        self.plot_manager = plotter_widgets.PlotManager(self.inspector)

        self.layout_left = QVBoxLayout()
        self.layout_left.addWidget(self.actions_menu)
        self.layout_left.addWidget(self.file_browser)

        self.layout = QGridLayout()
        self.layout.addLayout(self.layout_left, 0, 0)
        self.layout.addWidget(self.plot_manager, 0, 1)

        self.setLayout(self.layout)
