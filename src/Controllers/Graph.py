from matplotlib import pyplot as plt
from datetime import datetime

from Controllers import Controller

class GraphController(Controller):

    def __init__(self):
        super().__init__()
        self.time_interval = 200
        self.start = datetime.now()
        self._data_limit = 50

        self.fig = plt.Figure(figsize=(6, 3.8), dpi=100)
        self.fig.subplots_adjust(left=0.093, right=0.975, bottom=0.12, top=0.975)
        self.ax = self.fig.add_subplot(111)
        self.config()

        self.x_data, self.y_data = [], []

    @property
    def data_limit(self):
        return self._data_limit

    @data_limit.setter
    def data_limit(self, value):
        self._data_limit = value

    def reset(self, canvas):
        self.start = datetime.now()
        self.x_data.clear()
        self.y_data.clear()
        self.ax.cla()
        self.config()
        self.ax.plot(self.x_data, self.y_data)
        canvas.draw()

    def config(self):
        self.ax.set_ylim(0, 255)
        self.ax.set_xlabel("time(ms)")
        self.ax.set_ylabel("intensity")
        self.ax.grid()

    def update(self, canvas):
        if len(self.x_data) > self.data_limit:
            self.x_data = self.x_data[len(self.x_data) - self.data_limit:]
            self.y_data = self.y_data[len(self.y_data) - self.data_limit:]

        self.x_data.append((datetime.now()-self.start).total_seconds() * 1000)
        self.y_data.append(self.intensity)

        self.ax.cla()
        self.config()
        self.ax.plot(self.x_data, self.y_data)
        canvas.draw()


