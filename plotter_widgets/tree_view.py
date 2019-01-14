from PySide2.QtWidgets import QTreeView, QAbstractItemView
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtCore import Qt

import re

class TreeView(QTreeView):
    def __init__(self, inspector):
        super().__init__()
        self.inspector = inspector
        self.inspector.add('tree_view', self)

        # Set selection mode so multiple datasets can be selected
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # Hide header
        self.setHeaderHidden(True)

        # Create and set model to view
        self.model = TreeModel(self.inspector)
        self.model.update()
        self.setModel(self.model)

        # Create selection model
        self.selectionModel = self.selectionModel()
        self.selectionModel.setModel(self.model)

    def update(self, filter = None):
        # Update tree to show datastore content with optional regex filter
        self.model.update(selection_reg = filter)

    def expand_all(self):
        # Expand tree to show all items
        self.expandAll()

    def get_selection(self):
        selection = []
        for index in self.selectionModel.selectedIndexes():
            for dataset in self.__flatten(self.model.itemFromIndex(index).get_datasets()):
                selection.append(dataset)
        return selection

    def __flatten(self, lis):
        """Given a list, possibly nested to any level, return it flattened."""
        new_lis = []
        for item in lis:
            if type(item) == type([]):
                new_lis.extend(self.__flatten(item))
            else:
                new_lis.append(item)
        return new_lis

class TreeModel(QStandardItemModel):
    def __init__(self, inspector):
        super().__init__()
        self.inspector = inspector
        self.datastore = self.inspector.get('datastore')

    def update(self, selection_reg=None):
        # Empty the model to start fresh
        self.clear()

        # Get loaded files from datastore
        files = self.datastore.get_all_files()

        # Iterate over files in datastore and build model
        for key, file in files.items():
            # Add filename to model
            parentItem = self.invisibleRootItem()
            item_file = TreeItem(file.get_filename())
            parentItem.appendRow(item_file)

            # Get list of dataset titles in file
            dataset_titles = file.get_names()

            # If a selection regex is given, filter all datasets with it
            if selection_reg:
                reg = re.compile(r'.*{}.*'.format(selection_reg), re.IGNORECASE)
                dataset_titles = list(filter(reg.match, dataset_titles))

            # Create dict to keep track of a dataset has been added to the tree
            dataset_added = {key: False for key in dataset_titles}
            # Create list to keep track of added subsystems
            subsystem_added = []

            # Find all systems in the file and sort them
            dataset_systems = list(set([title.split('-')[0].strip() for title in dataset_titles]))
            dataset_systems = sorted(dataset_systems, key=str.lower)

            # Add systems to the model
            for system in dataset_systems:
                # Select file item to start building model for this file
                parentItem = item_file

                # Create an item for this system and make it the root
                item_system = TreeItem(system)
                parentItem.append_child(item_system)

                # Get all datasets that belong to this system
                reg = re.compile(re.escape(system) + r'.*')
                system_datasets = list(filter(reg.match, dataset_titles))

                # Iterate over all datasets belonging to this system
                for dataset in system_datasets:
                    # Select system item as parentItem
                    parentItem = item_system

                    # Look for subsystems with 2 words in common
                    subsystem = ' '.join(dataset.split()[:4])
                    reg = re.compile(re.escape(subsystem))
                    subsystem_datasets = sorted(list(filter(reg.match, dataset_titles)), key=str.lower)

                    # Only if subsystem has more than 3 datasets, it is grouped in a subsystem-folder
                    if len(subsystem_datasets) > 3 and subsystem not in subsystem_added:
                        # Add this subsystem to the list to prevent adding it again
                        subsystem_added.append(' '.join(dataset.split()[:4]))

                        # Add this subsystem to the model
                        item_subsystem = TreeItem(' '.join(subsystem.split()[2:4]))
                        parentItem.append_child(item_subsystem)

                        # Add all datasets that belong to the subsytem to the model
                        parentItem = item_subsystem
                        for subsytem_dataset in subsystem_datasets:
                            item_label = ' '.join(subsytem_dataset.split()[4:])
                            item_dataset = TreeItem(item_label, dataset=file.get_dataset_by_name(subsytem_dataset))
                            parentItem.append_child(item_dataset)
                            dataset_added[subsytem_dataset] = True

                    # Remove already-added datasets from the list to avoid double entries
                    dataset_titles = [title for title in dataset_titles if dataset_added[title] == False]

                    # Select system item as parentItem
                    parentItem = item_system

                    # Look for subsystems with 1 words in common
                    subsystem = ' '.join(dataset.split()[:3])
                    reg = re.compile(re.escape(subsystem))
                    subsystem_datasets = sorted(list(filter(reg.match, dataset_titles)), key=str.lower)

                    # Only if subsystem has more than 4 datasets, it is grouped in a subsystem-folder
                    if len(subsystem_datasets) > 3 and subsystem not in subsystem_added:
                        # Add this subsystem to the list to prevent adding it again
                        subsystem_added.append(' '.join(dataset.split()[:3]))

                        # Add this subsystem to the model
                        item_subsystem = TreeItem(' '.join(subsystem.split()[2:3]))
                        parentItem.append_child(item_subsystem)

                        # Add all datasets that belong to the subsytem to the model
                        parentItem = item_subsystem
                        for subsytem_dataset in subsystem_datasets:
                            item_label = ' '.join(subsytem_dataset.split()[3:])
                            item_dataset = TreeItem(item_label, dataset=file.get_dataset_by_name(subsytem_dataset))
                            parentItem.append_child(item_dataset)
                            dataset_added[subsytem_dataset] = True

                # Get remaining datasets and add them
                dataset_titles = [title for title in dataset_titles if dataset_added[title] == False]
                parentItem = item_system
                for system_dataset in system_datasets:
                    if dataset_added[system_dataset] == False:
                        item_label = ' '.join(system_dataset.split()[2:])
                        item_dataset = TreeItem(item_label, dataset=file.get_dataset_by_name(system_dataset))
                        parentItem.append_child(item_dataset)


class TreeItem(QStandardItem):
    def __init__(self, label, dataset=None):
        super().__init__(label)
        if dataset:
            self.dataset = dataset
            self.type = 'dataset'
        else:
            self.type = 'system'
            self.children = []

        # Make item non-editable
        self.setEditable(False)

    def append_child(self, item):
        self.appendRow(item)
        self.children.append(item)

    def get_type(self): return self.type

    def get_datasets(self):
        datasets = []
        if self.type == 'dataset':
            datasets.append(self.dataset)
        else:
            for child in self.children:
                datasets.append(child.get_datasets())
        return datasets

