from PySide2.QtWidgets import QVBoxLayout, QGroupBox, QPushButton, QGridLayout

class ActionMenu(QGroupBox):
    def __init__(self, inspector):
        super().__init__()

        self.inspector = inspector
        self.inspector.add('action_menu', self)

        self.setTitle('Actions')

        self.button_load = QPushButton('Load', self)
        self.button_load.clicked.connect(self.button_load_pressed)

        self.button_unload = QPushButton('Unload', self)
        self.button_unload.clicked.connect(self.button_unload_pressed)

        self.button_1plot = QPushButton('1 Plot', self)
        self.button_1plot.clicked.connect(self.button_1plot_pressed)

        self.button_setLayout = QPushButton('Set layout', self)
        self.button_setLayout.clicked.connect(self.button_setLayout_pressed)

        self.layout = QGridLayout()
        self.layout.addWidget(self.button_load, 0, 0)
        self.layout.addWidget(self.button_unload, 0, 1)
        self.layout.addWidget(self.button_1plot, 1, 0)
        self.layout.addWidget(self.button_setLayout, 1, 1)

        self.setLayout(self.layout)

    def button_load_pressed(self):
        self.inspector.get('datastore').load_file('data/INTCANLOG2-20180818T153331-IDLE-HV-FC.mat')

    def button_unload_pressed(self):
        self.inspector.get('datastore').unload_file('data/INTCANLOG2-20180818T153331-IDLE-HV-FC.mat')

    def button_1plot_pressed(self):
        selection = self.inspector.get('tree_view').get_selection()
        self.inspector.get('plot_manager').plot(selection)

    def button_setLayout_pressed(self):
        self.inspector.get('plot_manager').set_plot_layout()
