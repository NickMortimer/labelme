from qtpy import QtCore
from qtpy import QtGui
from qtpy import QtWidgets


class DroneWidget(QtWidgets.QLabel):
    def __init__(self):
        super(DroneWidget, self).__init__()
        self.setValue("No Position")
        self.setToolTip("Postion")
        self.setStatusTip(self.toolTip())
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.calibration = None

    def minimumSizeHint(self):
        height = super(FovWidget, self).minimumSizeHint().height()
        fm = QtGui.QFontMetrics(self.font())
        width = fm.width(str(self.maximum()))
        return QtCore.QSize(width, height)

    def setCalibration(self,calibration,imagewidth,imageheight):
        self.calibration=calibration
    

    def from_real_world_mtx(droneeasting,dronenorthing,imagewidth,imageheight,yaw,altitude,easting,northing):

        #yaw = yaw-90
        rads = np.deg2rad(yaw)
        rotation = np.array([[np.cos(rads),-np.sin(rads),0,0],
                        [np.sin(rads),np.cos(rads),0,0],
                        [0,0,0,-altitude]])
        
        focalleninpixel=3666.666504
        pixelsize =0.0132/5472
        camera_matrix = np.array([[focalleninpixel*pixelsize,0,pixelsize*item.ImageWidth/2],
                        [0,pixelsize*focalleninpixel,pixelsize*item.ImageHeight/2],
                        [0,0,1]])
        cam = camera_matrix.dot(rotation).dot([easting-droneeasting,northing-dronenorthing,0,1])
        #print(cam)
        cam = cam/cam[-1]
        cam = cam/pixelsize

        return int(cam[0]),int(cam[1])