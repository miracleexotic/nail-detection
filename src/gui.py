import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from Modules import (
    VideoCaptureModule, 
    GraphModule
)

class NailDectection(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, padding=(10, 10))
        self.pack(fill=BOTH, expand=YES)
        
        self.window = master

        # ::Capture::
        self.capture_frame = ttk.Frame(self)
        self.capture_frame.pack(side=TOP, fill=X, expand=YES)

        # VideoCapture
        self.vid_mod = VideoCaptureModule(self)

        # Graph
        self.graph_mod = GraphModule(self)

        # ::Controller::
        self.controller_lf = ttk.Labelframe(self, text="Main Controller", padding=10)
        self.controller_lf.pack(side=TOP, fill=BOTH, expand=YES)

        # TODO - Hardware Controller


        self.window.protocol("WM_DELETE_WINDOW", self.onClose)

    def onClose(self):
        self.window.quit()

        
if __name__ == '__main__':
    # Create a window and pass it to the Application object
    app = ttk.Window("Nail Detection")
    NailDectection(app)
    app.mainloop()


