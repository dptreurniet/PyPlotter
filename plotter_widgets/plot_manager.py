from PySide2.QtWidgets import QWidget, QGridLayout, QLayoutItem
from PySide2.QtCharts import QtCharts
from PySide2.QtCore import QPointF
from PySide2.QtGui import QPainter

from plotter_pop_ups import PlotLayoutDialog

class PlotManager(QWidget):
    def __init__(self, inspector):
        super().__init__()
        self.inspector = inspector
        self.inspector.add('plot_manager', self)

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.plot_windows = []
        self.set_plot_layout(dim=[1, 1])

    def set_plot_layout(self, dim=None):
        if not dim:
            dialog = PlotLayoutDialog()
            if dialog.exec():
                dim = dialog.get_new_layout()

        new_n_plot_windows = dim[0]*dim[1]
        if new_n_plot_windows > len(self.plot_windows):
            for i in range(new_n_plot_windows - len(self.plot_windows)):
                self.plot_windows.append(PlotWindow(self.inspector))
        else:
            self.plot_windows = self.plot_windows[:new_n_plot_windows]

        # Clear current layout
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        count = 0
        for row in range(dim[1]):
            for col in range(dim[0]):
                self.layout.addWidget(self.plot_windows[count], row, col)
                count += 1

    def plot(self, datasets):
        self.plot_windows[0].clear()
        self.plot_windows[0].add_datasets(datasets)
        self.plot_windows[0].plot_line()


class PlotWindow(QtCharts.QChartView):
    def __init__(self, inspector):
        super().__init__()

        self.inspector = inspector
        self.chart = QtCharts.QChart()
        self.setChart(self.chart)

        #self.setRenderHint(QPainter.Antialiasing)

        self.datasets = []

    def clear(self):
        self.datasets = []
        self.chart.removeAllSeries()
        self.chart.createDefaultAxes()

    def add_datasets(self, datasets):
        if type(datasets) == list:
            for dataset in datasets:
                self.datasets.append(dataset)
        else:
            self.datasets.append(datasets)

    def plot_line(self):
        titles = []
        for dataset in self.datasets:
            # Generate and add serie to chart
            point_list = [QPointF(dataset.xData[i], dataset.yData[i]) for i in range(len(dataset.xData))]
            series = QtCharts.QLineSeries()
            series.append(point_list)
            self.chart.addSeries(series)

            # Set axis labels
            self.chart.createDefaultAxes()
            self.chart.axisX().setTitleText('%s [%s]' % (dataset.xQuantity, dataset.xUnit))
            if len(self.datasets) < 2:
                self.chart.axisY().setTitleText('%s [%s]' % (dataset.yQuantity, dataset.yUnit))

            # Add title to list for title generation later
            titles.append(dataset.title)

        self.chart.setTitle(self.__generate_title(titles))


    def __generate_title(self, titles):
        complete_title = ''
        for index, title in enumerate(titles):
            complete_title += title
            if len(titles) > 1 and index < len(titles)-1:
                complete_title += ', '
        return complete_title
