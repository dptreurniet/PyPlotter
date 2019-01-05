from PySide2.QtWidgets import QDialog, QLineEdit, QLabel, QPushButton, QFormLayout, QDialogButtonBox
from PySide2.QtGui import QIntValidator


class PlotLayoutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setModal(True)

        self.label_columns = QLabel('Columns:', self)
        self.input_columns = QLineEdit(self)
        self.input_columns.textChanged.connect(self.input_changed)
        self.input_columns.setValidator(QIntValidator(1, 10, self))

        self.label_rows = QLabel('Rows:', self)
        self.input_rows = QLineEdit(self)
        self.input_rows.textChanged.connect(self.input_changed)
        self.input_rows.setValidator(QIntValidator(1, 10, self))

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QFormLayout()
        self.layout.addRow(self.label_columns, self.input_columns)
        self.layout.addRow(self.label_rows, self.input_rows)
        self.layout.addRow(self.buttonBox)

        self.setLayout(self.layout)

    def get_new_layout(self):
        return [int(self.input_columns.text()), int(self.input_rows.text())]

    def input_changed(self):
        if self.input_columns.hasAcceptableInput() and self.input_rows.hasAcceptableInput():
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)


