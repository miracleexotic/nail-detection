class Controller:
    
    def __init__(self):
        self._intensity = 0
        self._time_interval = 1000

    @property
    def intensity(self):
        return self._intensity

    @intensity.setter
    def intensity(self, value):
        self._intensity = value

    @property
    def time_interval(self):
        return self._time_interval

    @time_interval.setter
    def time_interval(self, value):
        self._time_interval = value