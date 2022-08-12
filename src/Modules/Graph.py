import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from datetime import datetime

from Controllers import GraphController

class GraphModule(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.pack(side=LEFT, fill=BOTH)

        self.master = master
        self.continueRecord = False

        # Graph Controller
        self.graph = GraphController()

        # ::Graph Capture::
        # Main LabelFrame
        self.main_lf = ttk.Labelframe(master.capture_frame, text="Graph", padding=5, bootstyle=INFO)
        self.main_lf.pack(side=LEFT, fill=BOTH, expand=YES, padx=5, pady=5)

        # Draw canvas
        self.canvas_graph = ttk.Canvas(self.main_lf, width=master.vid_mod.vid.width, height=master.vid_mod.vid.height)
        self.canvas_graph.pack(side=TOP)

        self.canvas = FigureCanvasTkAgg(self.graph.fig, self.canvas_graph)
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=YES)
        self.canvas.draw()

        # ::Graph Controller:
        # Labelframe
        self.controller_lf = ttk.Labelframe(self.main_lf, text="Controller", padding=10)
        self.controller_lf.pack(side=TOP, fill=BOTH, expand=YES, padx=5, pady=5)

        # Time interval
        self.var_time_interval = ttk.Variable(value=200)
        self.create_controller_time_interval()

        # Data limit
        self.var_data_limit = ttk.Variable(value=50)
        self.create_controller_data_limit()
        
        # Button START/STOP
        self.btn_start_stop = ttk.Button(self.controller_lf, text="START/STOP", command=self.change_state, bootstyle=SUCCESS)
        self.btn_start_stop.pack(side=RIGHT, padx=(0, 10))

        # Button RESET
        self.btn_reset = ttk.Button(self.controller_lf, text="RESET", command=lambda: self.graph.reset(self.canvas), bootstyle=DEFAULT)
        self.btn_reset.pack(side=RIGHT, padx=(10, 0))

        # ToolBar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.controller_lf)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=YES)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.update()

    def create_controller_time_interval(self):
        # Frame
        frame = ttk.Frame(self.controller_lf)
        frame.pack(side=TOP, fill=BOTH, expand=YES, pady=2, anchor=NW)
        # Lebel
        label = ttk.Label(frame, text="Time interval:")
        label.pack(side=LEFT)
        # Scale
        scale = ttk.Scale(frame, 
                            variable=self.var_time_interval, 
                            from_=1, to=5000,
                            command=self._set_time_interval)
        scale.pack(side=LEFT, fill=X, expand=YES, padx=5)
        # Entry
        self.entry_time_interval = ttk.Entry(frame, textvariable=self.var_time_interval, width=5)
        self.entry_time_interval.pack(side=LEFT, padx=(0,5))
        # Button
        btn_reset = ttk.Button(frame, text="RESET", command=self._reset_time_interval, bootstyle="default-outline")
        btn_reset.pack(side=LEFT)
        btn_set = ttk.Button(frame, text="SET", command=lambda: self._set_time_interval(None), bootstyle="success")
        btn_set.pack(side=LEFT, padx=(0,5))
    
    def _reset_time_interval(self):
        self.var_time_interval.set(200)
        self.graph.time_interval = 200
    
    def _set_time_interval(self, value):
        value = int(self.var_time_interval.get())
        if value < 1 or value > 5000:
            self.entry_time_interval.configure(bootstyle=DANGER)
            return
        self.entry_time_interval.configure(bootstyle=DEFAULT)
        self.var_time_interval.set(value)
        self.graph.time_interval = value

    def create_controller_data_limit(self):
        # Frame
        frame = ttk.Frame(self.controller_lf)
        frame.pack(side=TOP, fill=BOTH, expand=YES, pady=2, anchor=NW)
        # Lebel
        label = ttk.Label(frame, text="Data limit(10-100):")
        label.pack(side=LEFT)
        # Entry
        self.entry_data_limit = ttk.Entry(frame, textvariable=self.var_data_limit, width=5)
        self.entry_data_limit.pack(side=LEFT, padx=(5,5))
        # Button
        btn_reset = ttk.Button(frame, text="RESET", command=self._reset_data_limit, bootstyle="default-outline")
        btn_reset.pack(side=LEFT)
        btn_set = ttk.Button(frame, text="SET", command=lambda: self._set_data_limit(None), bootstyle="success")
        btn_set.pack(side=LEFT, padx=(0,5))

    def _reset_data_limit(self):
        self.var_data_limit.set(50)
        self.graph.data_limit = 50
    
    def _set_data_limit(self, value):
        value = int(self.var_data_limit.get())
        if value < 10 or value > 100:
            self.entry_data_limit.configure(bootstyle=DANGER)
            return
        self.entry_data_limit.configure(bootstyle=DEFAULT)
        self.var_data_limit.set(value)
        self.graph.data_limit = value

    def change_state(self):
        if self.continueRecord:
            self.btn_start_stop.configure(bootstyle=SUCCESS)
        else:
            self.btn_start_stop.configure(bootstyle=DANGER)

        self.continueRecord = not self.continueRecord

    def update(self):
        if not self.continueRecord:
            if not self.graph.x_data:
                self.graph.start = datetime.now()
            self.master.window.after(5, self.update)
            return

        self.graph.intensity = self.master.vid_mod.vid.intensity
        self.graph.update(self.canvas)

        self.master.window.after(self.graph.time_interval, self.update)


