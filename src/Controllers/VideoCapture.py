from re import X
import cv2
import numpy as np

from Controllers import Controller

class VideoCaptureController(Controller):

    def __init__(self, video_source=0):
        super().__init__()
        self.time_interval = 15
        self._box_crop = 50
        self._box_draw = 100

        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.x_center = int(self.width // 2)
        self.y_center = int(self.height // 2)
        self.x_pt = self.x_center
        self.y_pt = self.y_center
    
    def __del__(self):
        """Release the video source when the object is destroyed."""
        if self.vid.isOpened():
            self.vid.release()

    @classmethod
    def Camera(cls):
        return cls(video_source=0)

    @property
    def box_crop(self):
        return self._box_crop

    @box_crop.setter
    def box_crop(self, value):
        self._box_crop = value

    @property
    def box_draw(self):
        return self._box_draw

    @box_draw.setter
    def box_draw(self, value):
        self._box_draw = value

    def _adjust_frame(self, frame):
        """Adjust frame for Nail Detection."""
        # converting to gray-scale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # crop image
        gray_frame = gray_frame[self.y_center-self.box_crop:self.y_center+self.box_crop, self.x_center-self.box_crop:self.x_center+self.box_crop]

        # resize image
        gray_frame = cv2.resize(gray_frame, (self.width, self.height), interpolation = cv2.INTER_AREA)

        # mirror image
        gray_frame = cv2.flip(gray_frame, 1)

        # draw a rectangle
        gray_frame = cv2.rectangle(gray_frame, (self.x_pt-self.box_draw, self.y_pt-self.box_draw), (self.x_pt+self.box_draw, self.y_pt+self.box_draw), (255, 255, 255), 2)

        # get intensity (white 255 -> black 0)
        self.intensity = np.average(gray_frame[self.y_pt-self.box_draw+5:self.y_pt+self.box_draw-5, self.x_pt-self.box_draw+5:self.x_pt+self.box_draw-5])

        # draw a label
        cv2.putText(gray_frame, '%.2f' % (self.intensity), (self.x_pt-self.box_draw+3, self.y_pt-self.box_draw+25), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255), 2)
        
        return gray_frame

    def get_point_positions_range(self):
        x = (self.box_draw, self.width-self.box_draw)
        y = (self.box_draw, self.height-self.box_draw)
        return (x, y)

    def get_frame(self, adjust=True):
        """Return a boolean success flag and the current frame."""
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                if adjust:
                    frame = self._adjust_frame(frame)
                    return (ret, frame)
                else:
                    return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            else:
                return (ret, None)

        else:
            return (False, None)



