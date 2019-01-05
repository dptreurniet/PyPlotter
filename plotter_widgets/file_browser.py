from PySide2.QtWidgets import QVBoxLayout, QLineEdit, QGroupBox
from plotter_widgets.tree_view import TreeView

class FileBrowser(QGroupBox):
    def __init__(self, inspector):
        super().__init__()

        self.inspector = inspector
        self.inspector.add('file_browser', self)

        self.setTitle('Dataset Browser')

        self.setMaximumWidth(400)

        self.filter_textbox = QLineEdit()
        self.filter_textbox.textChanged.connect(self.filter_changed)
        self.filter_textbox.returnPressed.connect(self.filter_return_pressed)

        self.tree_view = TreeView(self.inspector)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.filter_textbox)
        self.layout.addWidget(self.tree_view)

        self.setLayout(self.layout)

    def filter_changed(self):
        self.update_tree()

    def filter_return_pressed(self):
        self.tree_view.get_selection()
        self.tree_view.expand_all()

    def update_tree(self):
        self.tree_view.update(filter = self.filter_textbox.text())
