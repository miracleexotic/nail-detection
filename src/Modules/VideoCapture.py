import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import PIL.Image, PIL.ImageTk

from Controllers import VideoCaptureController

class VideoCaptureModule(ttk.Frame):

    def __init__(self, master, video_source=0):
        super().__init__(master)
        self.pack(side=LEFT, fill=BOTH)

        self.master = master
        self.video_source = video_source

        # VideoCapture Controller
        self.vid = VideoCaptureController.Camera()
        self.x, self.y = self.vid.get_point_positions_range()

        # ::Camera Capture::
        # Main LabelFrame
        self.main_lf = ttk.Labelframe(master.capture_frame, text="Camera", width=self.vid.width, height=self.vid.height, padding=5, bootstyle=INFO)
        self.main_lf.pack(side=LEFT, fill=BOTH, expand=YES, padx=5, pady=5)
        # Upper Frame
        self.camera_upper_frame = ttk.Frame(self.main_lf)
        self.camera_upper_frame.pack(side=TOP, fill=X, expand=YES)
        # Draw canvas
        self.canvas_vid = ttk.Canvas(self.camera_upper_frame, width=self.vid.width, height=self.vid.height)
        self.canvas_vid.pack(side=LEFT, expand=YES, padx=5)
        # Vertical
        self.var_pos_vertical = ttk.Variable(value=self.vid.y_pt)
        self.create_controller_pos_vertical()
        # Lower Frame
        self.camera_lower_frame = ttk.Frame(self.main_lf)
        self.camera_lower_frame.pack(side=TOP, fill=X, expand=YES)
        # Horizontal
        self.var_pos_horizontal = ttk.Variable(value=self.vid.x_pt)
        self.create_controller_pos_horizontal()
        # Button RESET
        self.pos_btn_reset = ttk.Button(self.camera_lower_frame, text="RESET", command=self._pos_reset, bootstyle="default-outline")
        self.pos_btn_reset.pack(side=LEFT)

        # ::Camera Controller::
        # Controller Frame
        self.controller_frame = ttk.Frame(self.main_lf)
        self.controller_frame.pack(side=TOP, fill=X, expand=YES)
        # Labelframe
        self.controller_lf = ttk.Labelframe(self.controller_frame, text="Controller", padding=10)
        self.controller_lf.pack(side=BOTTOM, fill=BOTH, expand=YES, padx=5, pady=5)

        # Time interval
        self.var_time_interval = ttk.Variable(value=self.vid.time_interval)
        self.create_controller_time_interval()

        # Zoom
        self.var_box_crop = ttk.Variable(value=self.vid.box_crop)
        self.create_controller_box_crop()

        # Box size
        self.var_box_draw = ttk.Variable(value=self.vid.box_draw)
        self.create_controller_box_draw()

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.update()
    
    def create_controller_pos_vertical(self):
        # Frame
        frame = ttk.Frame(self.camera_upper_frame)
        frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=2, pady=2)
        # Scale
        self.scale_pos_vertical = ttk.Scale(frame, 
                            variable=self.var_pos_vertical, 
                            from_=self.y[0], to=self.y[1],
                            command=self._set_pos_vertical,
                            orient=VERTICAL)
        self.scale_pos_vertical.pack(side=TOP, fill=Y, expand=YES, padx=5, pady=5)
        # Entry
        label_pos_vertical = ttk.Entry(frame, textvariable=self.var_pos_vertical, width=5)
        label_pos_vertical.pack(side=TOP, padx=(0,5))
    
    def _set_pos_vertical(self, value):
        value = int(self.var_pos_vertical.get())
        self.var_pos_vertical.set(value)
        self.vid.y_pt = value

    def create_controller_pos_horizontal(self):
        # Frame
        frame = ttk.Frame(self.camera_lower_frame)
        frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=2, pady=5)
        # Scale
        self.scale_pos_horizontal = ttk.Scale(frame, 
                            variable=self.var_pos_horizontal, 
                            from_=self.x[0], to=self.x[1],
                            command=self._set_pos_horizontal,
                            orient=HORIZONTAL)
        self.scale_pos_horizontal.pack(side=LEFT, fill=X, expand=YES, padx=5)
        # Entry
        label_pos_horizontal = ttk.Entry(frame, textvariable=self.var_pos_horizontal, width=5)
        label_pos_horizontal.pack(side=LEFT, padx=(0,5))
    
    def _set_pos_horizontal(self, value):
        value = int(self.var_pos_horizontal.get())
        self.var_pos_horizontal.set(value)
        self.vid.x_pt = value

    def _pos_reset(self):
        self.vid.x_pt = self.vid.x_center
        self.var_pos_horizontal.set(self.vid.x_pt)
        self.vid.y_pt = self.vid.y_center
        self.var_pos_vertical.set(self.vid.y_pt)

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
        self.var_time_interval.set(15)
        self.vid.time_interval = 15
    
    def _set_time_interval(self, value):
        value = int(self.var_time_interval.get())
        if value < 1 or value > 5000:
            self.entry_time_interval.configure(bootstyle=DANGER)
            return
        self.entry_time_interval.configure(bootstyle=DEFAULT)
        self.var_time_interval.set(value)
        self.vid.time_interval = value

    def create_controller_box_crop(self):
        # Frame
        frame = ttk.Frame(self.controller_lf)
        frame.pack(side=TOP, fill=BOTH, expand=YES, pady=2, anchor=NW)
        # Lebel
        label = ttk.Label(frame, text="Zoom:")
        label.pack(side=LEFT, padx=(0, 45))
        # Scale
        scale = ttk.Scale(frame, 
                            variable=self.var_box_crop, 
                            from_=1, to=100,
                            command=self._set_box_crop)
        scale.pack(side=LEFT, fill=X, expand=YES, padx=5)
        # Entry
        self.entry_box_crop = ttk.Entry(frame, textvariable=self.var_box_crop, width=5)
        self.entry_box_crop.pack(side=LEFT, padx=(0,5))
        # Button
        btn_reset = ttk.Button(frame, text="RESET", command=self._reset_box_crop, bootstyle="default-outline")
        btn_reset.pack(side=LEFT)
        btn_set = ttk.Button(frame, text="SET", command=lambda: self._set_box_crop(None), bootstyle="success")
        btn_set.pack(side=LEFT, padx=(0,5))

    def _reset_box_crop(self):
        self.var_box_crop.set(50)
        self.vid.box_crop = 50
    
    def _set_box_crop(self, value):
        value = int(self.var_box_crop.get())
        if value < 1 or value > 100:
            self.entry_box_crop.configure(bootstyle=DANGER)
            return
        self.entry_box_crop.configure(bootstyle=DEFAULT)
        self.var_box_crop.set(value)
        self.vid.box_crop = 101 - value

    def create_controller_box_draw(self):
        # Frame
        frame = ttk.Frame(self.controller_lf)
        frame.pack(side=TOP, fill=BOTH, expand=YES, pady=2, anchor=NW)
        # Lebel
        label = ttk.Label(frame, text="Box size:")
        label.pack(side=LEFT)
        # Scale
        scale = ttk.Scale(frame, 
                            variable=self.var_box_draw, 
                            from_=10, to=min(self.vid.x_center, self.vid.y_center),
                            command=self._set_box_draw)
        scale.pack(side=LEFT, fill=X, expand=YES, padx=5)
        # Entry
        self.entry_box_draw = ttk.Entry(frame, textvariable=self.var_box_draw, width=5)
        self.entry_box_draw.pack(side=LEFT, padx=(0,5))
        # Button
        btn_reset = ttk.Button(frame, text="RESET", command=self._reset_box_draw, bootstyle="default-outline")
        btn_reset.pack(side=LEFT)
        btn_set = ttk.Button(frame, text="SET", command=lambda: self._set_box_draw(None), bootstyle="success")
        btn_set.pack(side=LEFT, padx=(0,5))
    
    def _new_position_range(self):
        self.x, self.y = self.vid.get_point_positions_range()
        self.scale_pos_vertical.configure(from_=self.y[0], to=self.y[1])
        self.scale_pos_vertical.pack(side=TOP, fill=Y, expand=YES, padx=5, pady=5)
        self.scale_pos_horizontal.configure(from_=self.x[0], to=self.x[1])
        self.scale_pos_horizontal.pack(side=LEFT, fill=X, expand=YES, padx=5)

    def _check_pos_box(self, box_size):
        if self.vid.x_pt < box_size:
            self.vid.x_pt = box_size
        elif self.vid.x_pt > self.vid.width-box_size:
            self.vid.x_pt = self.vid.width-box_size
        
        if self.vid.y_pt < box_size:
            self.vid.y_pt = box_size
        elif self.vid.y_pt > self.vid.height-box_size:
            self.vid.y_pt = self.vid.height-box_size

    def _reset_box_draw(self):
        self.var_box_draw.set(100)
        self.vid.box_draw = 100
        self._new_position_range()
    
    def _set_box_draw(self, value):
        value = int(self.var_box_draw.get())
        if value < 10 or value > min(self.vid.x_center, self.vid.y_center):
            self.entry_box_draw.configure(bootstyle=DANGER)
            return
        self.entry_box_draw.configure(bootstyle=DEFAULT)
        self.var_box_draw.set(value)
        self._check_pos_box(value)
        self.vid.box_draw = value
        self._new_position_range()

    def update(self):
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas_vid.create_image(0, 0, image=self.photo, anchor=NW)

        self.master.window.after(self.vid.time_interval, self.update)

