from PySide2.QtWidgets import QDialog, QPushButton, QVBoxLayout, QHBoxLayout, QDialogButtonBox, QFileDialog, QListWidget, QGroupBox


class LoadFileDialog(QDialog):
    def __init__(self, inspector):
        super().__init__()
        self.inspector = inspector
        self.setWindowTitle('Load')

        self.selected_files = []
        self.selected_datasets = {}

        self.setModal(True)

        # Files
        self.lv_files = QListWidget()
        self.lv_files.itemSelectionChanged.connect(self.lv_file_selection_changed)

        self.bt_remove_file = QPushButton("Remove")
        self.bt_remove_file.setEnabled(False)
        self.bt_remove_file.clicked.connect(self.bt_remove_file_pressed)

        self.layout_lv_files = QVBoxLayout()
        self.layout_lv_files.addWidget(self.lv_files)
        self.layout_lv_files.addWidget(self.bt_remove_file)

        # Datasets

        self.lv_datasets_load = QListWidget()
        self.lv_datasets_ignore = QListWidget()

        self.layout_lv_datasets = QHBoxLayout()
        self.layout_lv_datasets.addWidget(self.lv_datasets_load)
        self.layout_lv_datasets.addWidget(self.lv_datasets_ignore)

        self.gb_files = QGroupBox()
        self.gb_files.setTitle('Files')
        self.gb_files.setLayout(self.layout_lv_files)

        self.gb_datasets = QGroupBox()
        self.gb_datasets.setTitle('Datasets')
        self.gb_datasets.setLayout(self.layout_lv_datasets)

        self.layout_gb = QHBoxLayout()
        self.layout_gb.addWidget(self.gb_files)
        self.layout_gb.addWidget(self.gb_datasets)

        # Buttons
        self.bt_choose = QPushButton('Choose files')
        self.bt_choose.clicked.connect(self.bt_choose_pressed)
        self.bt_load = QPushButton('Ok')
        self.bt_load.clicked.connect(self.bt_load_pressed)
        self.bt_load.setEnabled(False)
        self.bt_cancel = QPushButton('Cancel')
        self.bt_cancel.clicked.connect(self.bt_cancel_pressed)

        self.bt_box = QDialogButtonBox()
        self.bt_box.addButton(self.bt_choose, QDialogButtonBox.ActionRole)
        self.bt_box.addButton(self.bt_load, QDialogButtonBox.AcceptRole)
        self.bt_box.addButton(self.bt_cancel, QDialogButtonBox.RejectRole)

        self.layout_main = QVBoxLayout()
        self.layout_main.addLayout(self.layout_gb)
        self.layout_main.addWidget(self.bt_box)

        self.setLayout(self.layout_main)

    def update_button(self):
        self.lv_files.clear()
        for name in self.selected_files:
            name = name.split('/')[-1]
            self.lv_files.addItem(name)

        if len(self.selected_files) > 0:
            self.bt_load.setEnabled(True)

    def bt_load_pressed(self):
        pass

    def bt_cancel_pressed(self):
        print('rejected')

    def bt_choose_pressed(self):
        file_dialog = QFileDialog(self, "Load file")
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        if file_dialog.exec():
            print(file_dialog.selectedFiles())
            for name in file_dialog.selectedFiles():
                if name not in self.selected_files:
                    self.selected_files.append(name)
        self.update_button()

    def bt_remove_file_pressed(self):
        print('remove')

    def lv_file_selection_changed(self):
        if len(self.lv_files.selectedItems()) > 0:
            self.bt_remove_file.setEnabled(True)
        else:
            self.bt_remove_file.setEnabled(False)