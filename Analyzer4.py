import sys
import os
import shutil
import time
import inspect
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import psutil
import gc

parentdirectorypath = "D:\\Messdaten\\2019_03_ESI_FeBpy\\20190321_MnAcac_Python\\MnAA_test"



##  Note:
##      for creating the .exe file the encoding of the files seem to play a big role.
##      The .dat files seem to want to be encoded the following way: ' encoding="cp1252" ' when opening the file.
##
##


    ######  datalengthlimit         cut read mass spectrum after channel x // peaks at higher channels will be lost! But good for stability
    ######
    ######  thresholdfactor         height the channel to be accepted as a positive "peak" channel
    ######  minbroadnessofpeak      average of x neighboring channels need to have thresholdfactor*threshold to be accepted as "abovethreshold"-"channel"
    ######  peakbroadnesstolerance  channels closer together than x channels, will be attributed to the same peaknumber




    ######  Quantum Yield and Energy of GoAsPhotodiode for normalization

GaAsPhotodiode = [[1.9589, 2.0667, 2.2143, 2.48, 3.1, 4.1333, 4.83, 5.15, 5.35, 5.6, 5.75, 5.97, 6.19, 6.37, 6.55, 6.79, 7.05, 7.24, 7.45, 7.73, 8.0, 8.32, 8.63, 8.79, 9.04, 9.91, 10.19, 10.49, 10.74, 12.04, 13.43, 13.93, 14.72, 15.36, 16.14, 16.44, 16.75, 17.38, 17.7, 18.08, 18.37, 18.71, 19.37, 19.77, 20.51, 21.28, 22.33, 22.87, 23.77, 24.66, 26.01, 26.99, 27.54, 29.65, 31.33, 33.11, 34.99, 36.98, 39.44, 41.893, 42.179, 42.469, 42.765, 43.061, 43.359, 43.665, 43.976, 44.292, 44.607, 44.922, 45.25, 45.594, 45.926, 46.27, 46.615, 47.336, 47.699, 48.063, 48.436, 48.827, 49.209, 49.609, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 170.0, 180.0, 190.0, 200.0, 210.0, 220.0, 230.0, 240.0, 250.0, 260.0, 270.0, 280.0, 290.0, 300.0, 310.0, 320.0, 330.0, 340.0, 350.0, 360.0, 370.0, 380.0, 390.0, 400.0, 410.0, 420.0, 430.0, 440.0, 450.0, 460.0, 470.0, 480.0, 490.0, 500.0, 510.0, 520.0, 530.0, 540.0, 550.0, 560.0, 570.0, 580.0, 590.0, 600.0, 610.0, 620.0, 630.0, 640.0, 650.0, 660.0, 670.0, 680.0, 690.0, 700.0, 710.0, 720.0, 730.0, 740.0, 750.0, 760.0, 770.0, 780.0, 790.0, 800.0, 810.0, 820.0, 830.0, 840.0, 850.0, 860.0, 870.0, 880.0, 890.0, 900.0, 910.0, 920.0, 930.0, 940.0, 950.0, 960.0, 970.0, 980.0, 990.0, 1000.0, 1010.0, 1020.0, 1030.0, 1040.0, 1050.0, 1060.0, 1070.0, 1080.0, 1090.0, 1100.0, 1110.0, 1120.0, 1130.0, 1140.0, 1150.0, 1160.0, 1170.0, 1180.0, 1190.0, 1200.0, 1210.0, 1220.0, 1230.0, 1240.0, 1250.0, 1260.0, 1270.0, 1280.0, 1290.0, 1300.0, 1310.0, 1320.0, 1330.0, 1340.0, 1350.0, 1360.0, 1370.0, 1380.0, 1390.0, 1400.0, 1410.0, 1420.0, 1430.0, 1440.0, 1450.0, 1460.0, 1470.0, 1480.0, 1490.0, 1500.0, 1510.0, 1520.0, 1530.0, 1540.0, 1550.0, 1560.0, 1570.0, 1580.0, 1590.0, 1600.0, 1610.0, 1620.0, 1630.0, 1640.0, 1650.0, 1660.0, 1670.0, 1680.0, 1690.0, 1700.0, 1710.0, 1720.0, 1730.0, 1740.0, 1750.0, 1760.0, 1770.0, 1780.0, 1790.0, 1800.0, 1810.0, 1820.0, 1830.0, 1840.0, 1850.0, 1860.0, 1870.0, 1880.0, 1890.0, 1900.0, 1910.0, 1920.0, 1930.0, 1940.0, 1950.0, 1960.0, 1970.0, 1980.0, 1990.0, 2000.0, 2010.0, 2020.0, 2030.0, 2040.0, 2050.0, 2060.0, 2070.0, 2080.0, 2090.0, 2100.0, 2110.0, 2120.0, 2130.0, 2140.0, 2150.0, 2160.0, 2170.0, 2180.0, 2190.0, 2200.0, 2210.0, 2220.0, 2230.0, 2240.0, 2250.0, 2260.0, 2270.0, 2280.0, 2290.0, 2300.0, 2310.0, 2320.0, 2330.0, 2340.0, 2350.0, 2360.0, 2370.0, 2380.0, 2390.0, 2400.0, 2410.0, 2420.0, 2430.0, 2440.0, 2450.0, 2460.0, 2470.0, 2480.0, 2490.0, 2500.0, 2510.0, 2520.0, 2530.0, 2540.0, 2550.0, 2560.0, 2570.0, 2580.0, 2590.0, 2600.0, 2610.0, 2620.0, 2630.0, 2640.0, 2650.0, 2660.0, 2670.0, 2680.0, 2690.0, 2700.0, 2710.0, 2720.0, 2730.0, 2740.0, 2750.0, 2760.0, 2770.0, 2780.0, 2790.0, 2800.0, 2810.0, 2820.0, 2830.0, 2840.0, 2850.0, 2860.0, 2870.0, 2880.0, 2890.0, 2900.0, 2910.0, 2920.0, 2930.0, 2940.0, 2950.0, 2960.0, 2970.0, 2980.0, 2990.0, 3000.0, 3010.0, 3020.0, 3030.0, 3040.0, 3050.0, 3060.0, 3070.0, 3080.0, 3090.0, 3100.0, 3110.0, 3120.0, 3130.0, 3140.0, 3150.0, 3160.0, 3170.0, 3180.0, 3190.0, 3200.0, 3210.0, 3220.0, 3230.0, 3240.0, 3250.0, 3260.0, 3270.0, 3280.0, 3290.0, 3300.0, 3310.0, 3320.0, 3330.0, 3340.0, 3350.0, 3360.0, 3370.0, 3380.0, 3390.0, 3400.0, 3410.0, 3420.0, 3430.0, 3440.0, 3450.0, 3460.0, 3470.0, 3480.0, 3490.0, 3500.0, 3510.0, 3520.0, 3530.0, 3540.0, 3550.0, 3560.0, 3570.0, 3580.0, 3590.0, 3600.0, 3610.0, 3620.0, 3630.0, 3640.0, 3650.0, 3660.0, 3670.0, 3680.0, 3690.0, 3700.0, 3710.0, 3720.0, 3730.0, 3740.0, 3750.0, 3760.0, 3770.0, 3780.0, 3790.0, 3800.0, 3810.0, 3820.0, 3830.0, 3840.0, 3850.0, 3860.0, 3870.0, 3880.0, 3890.0, 3900.0, 3910.0, 3920.0, 3930.0, 3940.0, 3950.0, 3960.0, 3970.0, 3980.0, 3990.0, 4000.0], [0.40561, 0.46567, 0.45848, 0.42288, 0.28318, 0.20137, 0.20949, 0.15712, 0.16077, 0.17295, 0.18148, 0.19975, 0.21436, 0.23142, 0.23994, 0.23872, 0.2436, 0.2436, 0.24238, 0.23507, 0.22654, 0.22654, 0.22654, 0.22776, 0.23994, 0.26674, 0.27892, 0.28257, 0.28257, 0.40681, 0.53469, 0.5554, 0.5554, 0.53469, 0.53469, 0.60777, 0.66624, 0.74419, 0.77098, 0.81483, 0.84528, 0.87695, 0.87329, 0.84528, 0.75758, 0.70399, 0.74419, 0.75758, 0.96099, 0.99631, 1.13272, 1.2399, 1.28619, 1.2399, 1.31055, 1.51639, 1.82088, 2.10711, 2.4384, 3.03082, 3.04373, 3.05847, 3.06955, 3.08721, 3.11072, 3.14068, 3.17235, 3.20645, 3.2598, 3.29123, 3.31461, 3.38343, 3.4358, 3.49256, 3.55882, 3.63957, 3.66819, 3.71642, 3.74261, 3.79851, 3.84626, 3.88, 3.91799, 4.91916, 6.85152, 9.29896, 11.7156, 13.3585, 16.8096, 20.1064, 22.2701, 24.4271, 26.5776, 28.1, 29.5056, 30.7708, 31.9357, 33.0854, 34.2003, 35.5263, 36.908, 38.2753, 39.6284, 40.9677, 42.2935, 43.6743, 45.2091, 46.7426, 48.2746, 49.8149, 51.3558, 52.8952, 54.4327, 55.9682, 57.5014, 59.032, 60.5596, 62.2672, 64.1738, 66.0788, 67.9814, 69.881, 71.7767, 73.7087, 75.6457, 77.5753, 79.4967, 81.4091, 83.3119, 85.1882, 87.1211, 89.1068, 91.0769, 93.0178, 94.9194, 96.5809, 98.1406, 99.6849, 101.213, 102.725, 104.221, 105.794, 107.614, 109.408, 111.176, 112.916, 114.63, 116.324, 117.937, 119.468, 120.977, 122.462, 123.924, 125.363, 126.778, 128.224, 129.729, 131.205, 132.65, 134.066, 135.451, 136.807, 138.133, 139.426, 140.688, 141.921, 143.123, 144.296, 145.439, 146.553, 147.637, 148.693, 149.719, 150.716, 151.685, 152.624, 153.535, 154.418, 155.273, 156.15, 157.01, 157.845, 158.661, 159.454, 160.221, 160.964, 161.682, 162.376, 163.047, 205.539, 207.239, 208.918, 215.058, 216.912, 218.75, 220.573, 222.381, 224.176, 225.955, 227.717, 229.463, 231.192, 232.904, 234.6, 236.278, 237.939, 239.582, 241.209, 245.998, 247.525, 253.932, 255.798, 257.652, 261.031, 262.85, 264.65, 266.432, 268.194, 269.938, 271.661, 273.365, 275.048, 276.711, 278.353, 279.974, 281.573, 283.204, 284.93, 286.645, 288.347, 291.858, 293.492, 295.109, 296.709, 298.29, 299.854, 301.4, 302.928, 304.438, 305.93, 307.403, 308.858, 310.294, 311.712, 313.11, 314.49, 315.851, 317.193, 318.516, 319.82, 321.105, 322.37, 323.763, 325.14, 326.504, 327.852, 329.186, 330.504, 331.809, 333.098, 334.373, 335.632, 336.878, 338.108, 339.324, 340.525, 341.712, 342.884, 344.041, 345.184, 346.313, 347.427, 348.526, 349.611, 350.682, 351.739, 352.781, 353.809, 354.813, 355.805, 356.781, 357.744, 358.675, 359.586, 360.482, 361.365, 362.232, 363.086, 363.926, 364.751, 365.563, 366.36, 375.561, 376.178, 376.889, 377.75, 378.597, 379.431, 380.239, 380.67, 380.727, 379.926, 378.502, 377.482, 377.29, 377.511, 377.88, 378.384, 378.911, 378.993, 378.396, 377.548, 377.094, 377.256, 377.466, 377.818, 378.287, 378.674, 378.828, 379.275, 379.961, 380.476, 380.871, 381.314, 381.857, 382.339, 382.748, 383.195, 383.704, 384.175, 384.579, 384.971, 385.353, 385.8, 386.33, 386.815, 387.195, 387.563, 387.919, 388.299, 388.762, 389.244, 389.552, 389.693, 389.858, 390.096, 390.359, 390.616, 390.845, 391.094, 391.309, 391.39, 390.961, 390.112, 390.302, 390.573, 390.832, 391.08, 391.317, 391.544, 391.759, 391.964, 392.159, 392.343, 392.517, 392.68, 392.834, 392.977, 393.11, 393.233, 393.347, 393.451, 393.545, 393.63, 393.705, 393.771, 393.808, 393.821, 393.818, 393.805, 393.784, 393.754, 393.714, 393.667, 393.61, 393.545, 393.471, 393.389, 393.3, 393.201, 393.095, 392.981, 391.526, 391.407, 391.282, 391.147, 391.005, 390.856, 390.699, 390.535, 390.364, 390.185, 389.999, 389.806, 389.606, 389.4, 389.187, 388.967, 388.74, 388.506, 388.267, 388.02, 387.768, 387.51, 387.246, 386.974, 386.697, 386.415, 386.126, 385.832, 384.376, 384.083, 383.784, 383.48, 383.17, 382.855, 382.534, 382.208, 381.876, 381.539, 381.2, 380.852, 380.501, 380.145, 379.784, 379.418, 379.048, 378.672, 378.293, 377.91, 377.521, 377.129, 376.732, 376.331, 375.926, 375.516, 375.103, 374.667, 374.222, 373.773, 373.321, 372.865, 372.405, 371.943, 371.477, 371.006, 370.534, 370.057, 369.577, 369.095, 368.609, 368.12, 367.627, 367.132, 366.635, 366.134, 365.63, 365.124, 364.616, 364.104, 363.59, 363.073, 362.554, 362.034, 361.509, 360.983, 360.454, 359.923]]

class Logfile():
    def writelog(self, transportstring):
        with open('D:\\_analyzerlogfile.txt', 'a') as logfile:
            logfile.write(time.strftime("%d.%m.%Y %H:%M:%S") + '\t' +  str(psutil.virtual_memory())  + '\t' +transportstring + '\n')

class Fenster(QWidget):
    def __init__(self):
        super().__init__()
        self.initMe()

    def initMe(self):

        width = 1000
        height = 500
        self.setGeometry(300, 100, width, height)
        self.setWindowTitle('My First GUI')


        self.exitbutton = QPushButton('Exit', self)
        self.exitbutton.move(width-170, height-70)
        self.exitbutton.setFixedSize(150, 50)
        self.exitbutton.clicked.connect(self.beenden)

        self.labelfolderline = QLabel("Path to the single (_001, _002, _003, ...) data-folders", self)
        self.labelfolderline.move(50, 35)

        self.folderline = QLineEdit(parentdirectorypath, self)
        self.folderline.move(50, 50)
        self.folderline.setFixedSize(700, 30)
        folderlinefont = self.folderline.font()
        folderlinefont.setPointSize(12)
        self.folderline.setFont(folderlinefont)

        self.labelprogressbarfolder = QLabel("Progress: read files", self)
        self.labelprogressbarfolder.move(50, 350)

        self.progressbarfolder = QProgressBar(self)
        self.progressbarfolder.setGeometry(150, 350, 300, 20)

        self.labelprogressbaroverall = QLabel("Progress: overall", self)
        self.labelprogressbaroverall.move(50, 400)

        self.progressbaroverall = QProgressBar(self)
        self.progressbaroverall.setGeometry(150, 400, 300, 20)

        self.checkfoldersbutton = QPushButton('Check if Folders have "_Untergrund.dat" File', self)
        self.checkfoldersbutton.setStyleSheet("background-color: rgb(255, 204, 102)")
        self.checkfoldersbutton.move(250, 100)
        self.checkfoldersbutton.clicked.connect(self.checkfolders)

        self.deleteundergroundfolders = QPushButton('Delete Folders who do not have "_Untergrund.dat" File', self)
        self.deleteundergroundfolders.move(250, 150)
        self.deleteundergroundfolders.setStyleSheet("background-color: rgb(255, 153, 153)")

        self.deleteundergroundfolders.clicked.connect(self.deleteundergroundfoldersmethod)

        self.deleteoutputfolderbutton = QPushButton('Delete Output Folders', self)
        self.deleteoutputfolderbutton.move(250, 250)
        self.deleteoutputfolderbutton.setStyleSheet("background-color: rgb(102, 153, 255)")
        self.deleteoutputfolderbutton.clicked.connect(self.deleteoutputfolder)

        self.analysisbutton = QPushButton('Do Analysis', self)
        self.analysisbutton.move(50, 100)
        self.analysisbutton.setFixedSize(150, 50)
        self.analysisbutton.setStyleSheet("background-color: rgb(51, 204, 51)")

        self.analysisbutton.clicked.connect(self.dotheanalysis)

        global settingsareaheight
        settingsareaheight = 100

        #
        #
        #           Ini-File Settings Area
        #
        #

        #read standard setting-values from inifile.txt

        setofdata = self.readfrominifile()

        [thresholdfactor, datalengthlimit, minbroadnessofpeak, peakbroadnesstolerance,
         masscalib1time, masscalib1mass, masscalib2time, masscalib2mass,
         untergrundchannelfirst, untergrundchannellast] = setofdata

        print('setofdata after inifile-read at line:', inspect.currentframe().f_lineno, setofdata)
        #inspect.getframeinfo(currentframe()).lineno


        self.labelreadthreshold = QLabel("Peak sensitivity / Threshold Factor", self)
        self.labelreadthreshold.setToolTip('Factor of the found threshold\n\n'
                                           '1 is roughly upper level of noise\n'
                                           'The higher, the less sensitive\n'
                                           'usual values between 1.25 (sensitive) and 4 (coarse)')
        self.labelreadthreshold.move(700, settingsareaheight)

        self.linerreadthreshold = QLineEdit(str(thresholdfactor), self)
        self.linerreadthreshold.move(620, settingsareaheight - 3)
        self.linerreadthreshold.setFixedSize(60, 20)




        self.labelreadlastchannel = QLabel("Cutoff Channel / Limit", self)
        self.labelreadlastchannel.setToolTip('Channels (x-axis of Mass Spec)\n\n'
                                             'Channels above this number will not be taken into account')
        self.labelreadlastchannel.move(700, settingsareaheight + 40)

        self.linereadlastchannel = QLineEdit(str(datalengthlimit), self)
        self.linereadlastchannel.move(620, settingsareaheight + 40 - 3)
        self.linereadlastchannel.setFixedSize(60, 20)



        self.labelbroadnessofpeak = QLabel("Is Channel x a peak?: Channel x-Axis-averaging", self)
        self.labelbroadnessofpeak.setToolTip('When checking if the Peak is above threshold\n'
                                             'the script will average the x next channels on left/right\n'
                                             'and check whether the average is above threshold\n\n'
                                             'this will discriminate single spikes')
        self.labelbroadnessofpeak.move(700, settingsareaheight + 80)

        self.linebroadnessofpeak = QLineEdit(str(minbroadnessofpeak), self)
        self.linebroadnessofpeak.move(620, settingsareaheight + 80 - 3)
        self.linebroadnessofpeak.setFixedSize(60, 20)



        self.labelpeakbroadnesstolerance = QLabel("Is Channel x a peak?: Tolerate dipped Channels", self)
        self.labelpeakbroadnesstolerance.setToolTip('If the intensity for one channel drops below the threshold\n'
                                                    'how many channels have to pass before a next "peak number" is assigned,'
                                                    'important if a broad peak has a drop which should not cause the beginning of a new peak number')
        self.labelpeakbroadnesstolerance.move(700, settingsareaheight + 120)

        self.linepeakbroadnesstolerance = QLineEdit(str(peakbroadnesstolerance), self)
        self.linepeakbroadnesstolerance.move(620, settingsareaheight + 120 - 3)
        self.linepeakbroadnesstolerance.setFixedSize(60, 20)

        #
        #
        #           Mass Calibration Area
        #
        #

        self.labelMasscalib = QLabel(self)
        self.labelMasscalib.setText('Mass Calibration')
        self.labelMasscalib.move(620, settingsareaheight + 170)

        self.labelfragment1 = QLabel(self)
        self.labelfragment1.setText('Fragment 1')
        self.labelfragment1.move(620, settingsareaheight + 200)

        self.labelfragment2 = QLabel(self)
        self.labelfragment2.setText('Fragment 2')
        self.labelfragment2.move(620, settingsareaheight + 230)

        self.labelMass = QLabel(self)
        self.labelMass.setText('Mass [amu/z]')
        self.labelMass.move(730, settingsareaheight + 170)

        self.labelTime = QLabel(self)
        self.labelTime.setText('Time Of Flight [E-5 sec]')
        self.labelTime.move(820, settingsareaheight + 170)


        self.lineeditmasscalib1mass = QLineEdit(str(masscalib1mass), self)
        self.lineeditmasscalib1mass.move(730, settingsareaheight + 200 - 3)
        self.lineeditmasscalib1mass.setFixedSize(45, 20)

        self.lineeditmasscalib1time = QLineEdit(str(masscalib1time), self)
        self.lineeditmasscalib1time.move(820, settingsareaheight + 200 - 3)
        self.lineeditmasscalib1time.setFixedSize(60, 20)

        self.lineeditmasscalib2mass = QLineEdit(str(masscalib2mass), self)
        self.lineeditmasscalib2mass.move(730, settingsareaheight + 230 - 3)
        self.lineeditmasscalib2mass.setFixedSize(45, 20)

        self.lineeditmasscalib2time = QLineEdit(str(masscalib2time), self)
        self.lineeditmasscalib2time.move(820, settingsareaheight + 230 - 3)
        self.lineeditmasscalib2time.setFixedSize(60, 20)

        #
        #
        #           Untergrund Substraction Channels Area
        #
        #

        self.labeluntergrundsubstraction1 = QLabel(self)
        self.labeluntergrundsubstraction1.setText('Untergrund lower boundary Channel Nr.')
        self.labeluntergrundsubstraction1.move(620, settingsareaheight + 270)

        self.labeluntergrundsubstraction2 = QLabel(self)
        self.labeluntergrundsubstraction2.setText('Untergrund upper boundary Channel Nr.')
        self.labeluntergrundsubstraction2.move(620, settingsareaheight + 300)

        self.lineedituntergrundsubstraction1 = QLineEdit(str(untergrundchannelfirst), self)
        self.lineedituntergrundsubstraction1.move(820, settingsareaheight + 270 - 3)
        self.lineedituntergrundsubstraction1.setFixedSize(100, 20)

        self.lineedituntergrundsubstraction2 = QLineEdit(str(untergrundchannellast), self)
        self.lineedituntergrundsubstraction2.move(820, settingsareaheight + 300 - 3)
        self.lineedituntergrundsubstraction2.setFixedSize(100, 20)

        #
        #       When the analysis is done, the label will appear
        #       at this point, the text is still empty, but already has its place


        self.finishedevent = QLabel(self)
        self.finishedevent.setFixedSize(450, 40)
        self.finishedevent.move(250, 450)



        #self.finishedevent.setFont(self.finishedevent.font().setPointSize(14))

        #folderlinefont = self.folderline.font()
        #folderlinefont.setPointSize(12)
        #self.folderline.setFont(folderlinefont)


        # the global "globali" var is used to only trigger the paint event once
        global globali
        globali = 0




        self.show()


    #                   draw vertical / horizontal separation line in GUI
    #                   the global "globali" var is used to only trigger the paint event once
    #                   otherwise every "mouse over" event will trigger the paint event again...

    def paintEvent(self, event):
        global globali
        global settingsareaheight

        if globali == 0:
            self.painter = QPainter(self)
            self.pen = QPen(Qt.gray, 2)
            self.painter.setPen(self.pen)
            self.painter.drawLine(580, settingsareaheight, 580, settingsareaheight + 350)
            self.painter.drawLine(600, settingsareaheight + 160, 960, settingsareaheight + 160)
            self.painter.drawLine(600, settingsareaheight + 260, 960, settingsareaheight + 260)
            self.painter.end()
            print('performed paint event')
            globali = globali + 1


    def beenden(self):
        QCoreApplication.instance().quit()

    def deleteoutputfolder(self):
        print('20190325_1602test')
        directorytoworkin = str(self.folderline.text())

        for folder in os.listdir(directorytoworkin):
            if folder.startswith('_output'):
                #print('output folder detected and deleted:', folder)
                shutil.rmtree(directorytoworkin + '\\' + folder)

    def deleteundergroundfoldersmethod(self):
        directorytoworkin = str(self.folderline.text())
        alluntergrundfilespresent = 0
        for folder in os.listdir(directorytoworkin):
            workingdirectorypath = str(directorytoworkin + '\\' + folder)
            datafoldername = str(workingdirectorypath.split('\\')[-1])
            untergrundfilename = workingdirectorypath + '\\' + datafoldername + '_Untergrund.dat'
            if not os.path.isfile(untergrundfilename):
                print('no _Untergrund.dat file in folder:\t', workingdirectorypath, 'deleting...')
                shutil.rmtree(workingdirectorypath)
                alluntergrundfilespresent = alluntergrundfilespresent + 1
        print('Number of deleted folders:', alluntergrundfilespresent)

    #
    #
    #                       readout of inifile.txt
    #
    #

    def readfrominifile(self):
        try:
            with open('inifile.txt', 'r') as inifile:
                inifilecontent = inifile.readlines()
        except FileNotFoundError:
            print('inifile not found')
            with open('D:\\_analyzerlogfile.txt', 'a') as logfile:
                logfile.write(time.strftime("%d.%m.%Y %H:%M:%S") +  str(psutil.virtual_memory())  + '\t' +
                              '\tinifile.txt not found in analyzer.exe/.py folder. Used default values\n\n')
            inifilecontent = []

        #default values if inifile-readout does not work:
        datalengthlimit, thresholdfactor, minbroadnessofpeak, peakbroadnesstolerance = 100000, 1.5, 11, 5
        masscalib1time, masscalib1mass, masscalib2time, masscalib2mass = 2.397, 55.0, 2.12, 43.0
        untergrundchannelfirst, untergrundchannellast = 10000, 30000


        #check if values in inifile are more specified
        for line in inifilecontent:
            if line.startswith('datalengthlimit = '):
                try:
                    wordsinline = line.replace(' ', '').replace('\n', '').split('=')
                    datalengthlimit = int(wordsinline[-1])
                except ValueError:
                    Logfile.writelog(Logfile, 'datalengthlimit inifile valueError\n')
                    pass
            if line.startswith('thresholdfactor = '):
                try:
                    wordsinline = line.replace(' ', '').replace('\n', '').split('=')
                    thresholdfactor = float(wordsinline[-1])
                except ValueError:
                    Logfile.writelog(Logfile, 'thresholdfactor inifile valueError\n')
                    pass
            if line.startswith('minbroadnessofpeak = '):
                try:
                    wordsinline = line.replace(' ', '').replace('\n', '').split('=')
                    minbroadnessofpeak = int(wordsinline[-1])
                except ValueError:
                    Logfile.writelog(Logfile, 'minbroadnessofpeak inifile valueError\n')
                    pass
            if line.startswith('peakbroadnesstolerance = '):
                try:
                    wordsinline = line.replace(' ', '').replace('\n', '').split('=')
                    peakbroadnesstolerance = int(wordsinline[-1])
                except ValueError:
                    Logfile.writelog(Logfile, 'peakbroadnesstolerance inifile valueError\n')
                    pass

            if line.startswith('masscalib1time = '):
                try:
                    wordsinline = line.replace(' ', '').replace('\n', '').split('=')
                    masscalib1time = float(wordsinline[-1])
                except ValueError:
                    Logfile.writelog(Logfile, 'masscalib1time inifile valueError\n')
                    pass
            if line.startswith('masscalib1mass = '):
                try:
                    wordsinline = line.replace(' ', '').replace('\n', '').split('=')
                    masscalib1mass = float(wordsinline[-1])
                except ValueError:
                    Logfile.writelog(Logfile, 'masscalib1mass inifile valueError\n')
                    pass
            if line.startswith('masscalib2time = '):
                try:
                    wordsinline = line.replace(' ', '').replace('\n', '').split('=')
                    masscalib2time = float(wordsinline[-1])
                except ValueError:
                    Logfile.writelog(Logfile, 'masscalib2time inifile valueError\n')
                    pass
            if line.startswith('masscalib2mass = '):
                try:
                    wordsinline = line.replace(' ', '').replace('\n', '').split('=')
                    masscalib2mass = float(wordsinline[-1])
                except ValueError:
                    Logfile.writelog(Logfile, 'masscalib2mass inifile valueError\n')
                    pass
            if line.startswith('untergrundchannelfirst = '):
                try:
                    wordsinline = line.replace(' ', '').replace('\n', '').split('=')
                    untergrundchannelfirst = int(wordsinline[-1])
                except ValueError:
                    Logfile.writelog(Logfile, 'untergrundchannelfirst inifile valueError\n')
                    pass
            if line.startswith('untergrundchannellast = '):
                try:
                    wordsinline = line.replace(' ', '').replace('\n', '').split('=')
                    untergrundchannellast = int(wordsinline[-1])
                except ValueError:
                    Logfile.writelog(Logfile, 'untergrundchannellast inifile valueError\n')
                    pass


        # here we have read out a lot of data from the ini file
        # we will now pack it all in the setofdata LIST and return it to the program
        # this is just done to not blow up the "returning" brackets

        setofdata = [thresholdfactor, datalengthlimit, minbroadnessofpeak, peakbroadnesstolerance,
                     masscalib1time, masscalib1mass, masscalib2time, masscalib2mass,
                     untergrundchannelfirst, untergrundchannellast]

        return setofdata
        #except NameError:
        #    return 100001, 2, 11, 5

    #
    #
    #               When Analysis Button is clicked
    #
    #

    def readfrominputfields(self):

        datalengthlimit = int(self.linereadlastchannel.text())
        thresholdfactor = float(self.linerreadthreshold.text())
        minbroadnessofpeak = int(self.linebroadnessofpeak.text())
        peakbroadnesstolerance = int(self.linepeakbroadnesstolerance.text())
        masscalib1mass = float(self.lineeditmasscalib1mass.text())
        masscalib1time = float(self.lineeditmasscalib1time.text())
        masscalib2mass = float(self.lineeditmasscalib2mass.text())
        masscalib2time = float(self.lineeditmasscalib2time.text())


        untergrundlowerboundary = int(self.lineedituntergrundsubstraction1.text())
        untergrundupperboundary = int(self.lineedituntergrundsubstraction2.text())

        setofdata = [datalengthlimit, thresholdfactor, minbroadnessofpeak, peakbroadnesstolerance,
                     masscalib1mass, masscalib1time, masscalib2mass, masscalib2time,
                     untergrundlowerboundary, untergrundupperboundary]

        return setofdata


    def dotheanalysis(self):

        self.finishedevent.setText('the Program is running and might freeze and not respond\n nevertheless it will continue working, if there\'s a problem, it will just crash \nand you will never see it again (unless you fix the problem and start it again)')

        #doanalysis.setworkfolder(self)
        parentdirectorypath = str(self.folderline.text())



        settingpackage = self.readfrominputfields()

        print('settingpackage1:', settingpackage)
        #print(setofdata)
        #self.finishedevent = QLabel("FINISHED", self)


        time.sleep(0.1)
        #self.update()

        self.progressbaroverall.setValue(0)



        allfolders = []
        for folder in os.listdir(parentdirectorypath):
            allfolders.append(folder)

        for folder in allfolders:
            workingdirectorypath = str(parentdirectorypath + '\\' + folder)
            datafoldername = str(workingdirectorypath.split('\\')[-1])
            analysisfolderpath = str(workingdirectorypath.replace(datafoldername, '_output_' + datafoldername))
            print(workingdirectorypath)

            Doanalysis.dosomething(Doanalysis, workingdirectorypath, datafoldername, analysisfolderpath, self.progressbarfolder, settingpackage)

            self.progressbaroverall.setValue((allfolders.index(folder) + 1) / allfolders.__len__() * 100)

        self.finishedeventprocedure()

    def finishedeventprocedure(self):
        finishedeventfont = self.finishedevent.font()
        finishedeventfont.setPointSize(20)
        self.finishedevent.setFont(finishedeventfont)

        self.finishedevent.setText('FiiiINISHED!!!!')

    def checkfolders(self):
        directorytoworkin = str(self.folderline.text())
        alluntergrundfilespresent = 0
        for folder in os.listdir(directorytoworkin):
            workingdirectorypath = str(directorytoworkin + '\\' + folder)
            datafoldername = str(workingdirectorypath.split('\\')[-1])
            untergrundfilename = workingdirectorypath + '\\' + datafoldername + '_Untergrund.dat'
            if not os.path.isfile(untergrundfilename):
                print('no _Untergrund.dat file in folder:\t', workingdirectorypath)
                alluntergrundfilespresent = alluntergrundfilespresent + 1
        print('Number of errors:', alluntergrundfilespresent)

#class Doanalysis(object):
class Doanalysis(QThread):


    def createanalysisfolder(self, workingdirectorypath, datafoldername, analysisfolderpath):
        print('Creating analysis folder...')

        # go to the data folder, find the folder above it,
        # check if an analysis folder is there, if yes delete it,
        # and create an analysis folder
        print(workingdirectorypath)
        os.chdir(workingdirectorypath)
        if os.path.exists(analysisfolderpath):
            shutil.rmtree(analysisfolderpath)
            print('deleting old Analysis folder... [wait for 0.5 seconds]')
            time.sleep(0.5)
        os.mkdir(analysisfolderpath)

    def readmonofile(self, workingdirectorypath, datafoldername, analysisfolderpath):
        os.chdir(workingdirectorypath)


        with open(datafoldername+'_Mono.txt', 'r', encoding="cp1252") as file:
            content = []
            for line in file:
                if line == '# LEGEND\n':
                    for i in range(26):
                        file.readline()
                    content = file.readlines()
            monofilecontent = []
            i = 0
            for elementline in content:
                monofilecontent.append([])
                for elementdata in elementline.split('\t'):
                    monofilecontent[i].append(elementdata)
                i = i + 1

        return monofilecontent

    def readbackground(self, workingdirectorypath, datafoldername, analysisfolderpath):

        with open('D:\\_analyzerlogfile.txt', 'a') as logfile:
            logfile.write(
                time.strftime("%d.%m.%Y %H:%M:%S")+ '\t' +  str(psutil.virtual_memory())   +'\t\tin readbackground next step: chdir\t\n')

        os.chdir(workingdirectorypath)

        with open('D:\\_analyzerlogfile.txt', 'a') as logfile:
            logfile.write(
                time.strftime("%d.%m.%Y %H:%M:%S") + '\t'+  str(psutil.virtual_memory()) +'\t\tin readbackground next step: create emptylist bgdata\t\n')

        backgrounddata = []

        with open('D:\\_analyzerlogfile.txt', 'a') as logfile:
            logfile.write(
                time.strftime("%d.%m.%Y %H:%M:%S")+ '\t' +  str(psutil.virtual_memory())  +'\t\tin readbackground next step: read _Untergrund.dat\t\n')
        print('test_201904091146_1')
        print(datafoldername)
        with open(datafoldername+'_Untergrund.dat', 'r', encoding="cp1252") as file:
            for line in file:
                if not line.startswith('#'):
                    backgrounddata.append(line.replace('\n', ""))

        with open('D:\\_analyzerlogfile.txt', 'a') as logfile:
            logfile.write(
                time.strftime("%d.%m.%Y %H:%M:%S") + '\t'+  str(psutil.virtual_memory())   +'\t\tin readbackground next step: return bgdata\t\n')

        return backgrounddata


    def readrawdatav2(self, backgrounddata, workingdirectorypath, datafoldername, analysisfolderpath, progressbarfolder, datalengthlimit):
        filelist = []
        bgsubstrdatalist = []
        summedmassspec = []
        for file in os.listdir(workingdirectorypath):
            filelist.append(file)
        for element in range(1, filelist.__len__()-1):
            bgsubstrdatalist.append([])

            with open(datafoldername+'_'+str(element).zfill(3)+'.dat', 'r', encoding="cp1252") as file:
                print('open file: ', datafoldername+'_'+str(element).zfill(3)+'.dat of insgesamt', filelist.__len__()-2)
                print('readrawdatav2, element:', element, '\t\ttotal number of files:', filelist.__len__()-2)
                progressbarfolder.setValue(element / (filelist.__len__()-2) * 100)



                i = 0
                j = 0

                for line in file:

                    #print('File Nr.:', element, 'from:', filelist.__len__()-2, '/// line:', i)
                    i = i+1
                    if not line.startswith('#'):
                        bgsubstracteddatapoint = (int(line.replace('\n', "")) - int(backgrounddata[j]))
                        bgsubstrdatalist[element-1].append(str(bgsubstracteddatapoint))
                        if element == 1:
                            summedmassspec.append(0)
                        summedmassspec[j] = summedmassspec[j] + bgsubstracteddatapoint
                        j = j + 1
                    if i > datalengthlimit:
                        break
                    ################################################################################################
                    ####################################### this one up here has to be deleted // it is a Abbruchbedingung if a mass spec file is longer than x channels
                    ################################################################################################

        return bgsubstrdatalist, summedmassspec



    def backgroundsubstraction(self, rawdatalist, backgrounddata):
        bglist = []
        for scannumbers in range(rawdatalist.__len__()):
            bglist.append([])
            for datapoints in range(rawdatalist[0].__len__()):
                bglist[scannumbers].append(int(rawdatalist[scannumbers][datapoints]) - int(backgrounddata[datapoints]))
        return bglist

    def sumupformassspec(self, bgsubstracted):
        summedmassspec = []
        for scannumbers in range(bgsubstracted.__len__()):
            for datapoints in range(bgsubstracted[0].__len__()):
                if scannumbers == 0:
                    summedmassspec.append(int(0))
                summedmassspec[datapoints] = summedmassspec[datapoints] + bgsubstracted[scannumbers][datapoints]
        return summedmassspec

    def plotmassspec(self, summedmassspec, threshold, plotselectedpeakchannel, plotselectedpeaksummedmassspec):
        plt.plot(summedmassspec)
        #plt.plot([i for i in range(summedmassspec.__len__())], threshold)
        plt.plot([0, summedmassspec.__len__()], [threshold, threshold], linestyle='--')
        plt.scatter(plotselectedpeakchannel, plotselectedpeaksummedmassspec, color="red")
        plt.show()

    def detectthreshold(self, summedmassspec, thresholdfactor):
        xkoordinaten = []
        laenge = summedmassspec.__len__()
        for i in range(laenge):
            xkoordinaten.append(i)
        #print('xkoordinaten:', xkoordinaten)
        #print('laenge laenge:', laenge, laenge)
        m, b = np.polyfit(xkoordinaten[round(laenge*0.1):round(laenge*0.9)], sorted(summedmassspec)[round(laenge*0.1):round(laenge*0.9)], 1)
        #print('m, b', m, b)
        x = np.linspace(0, laenge, 1000)
        threshold = (laenge*m+b)*thresholdfactor
        #print('threshold:', threshold)
        #plt.plot(sorted(summedmassspec))
        #plt.plot(x, m*x+b)
        #plt.show()
        return round(threshold)

    def findpeakpositions(self, summedmassspec, threshold, minbroadnessofpeak):
        goodchannels = []
        goodmsintensity = []
        for i in range(summedmassspec.__len__()):
            if summedmassspec[i] > threshold:
                checktotheright = summedmassspec[i]
                checktotheleft = summedmassspec[i]
                for j in range(1, minbroadnessofpeak):
                    if i-j > 0 and i+j < summedmassspec.__len__():
                        checktotheright = checktotheright + summedmassspec[i+j]
                        checktotheleft = checktotheleft + summedmassspec[i-j]
                if checktotheright > threshold*minbroadnessofpeak or checktotheleft > threshold*minbroadnessofpeak:
                    #print(i)
                    goodchannels.append(i)
                    goodmsintensity.append(summedmassspec[i])
        #plt.scatter(goodchannels, goodmsintensity, color="red")
        return goodchannels

    def definepeaknumber(self, summedmassspec, peakchannels, peakbroadnesstolerance):
        peaknumberchannels = []
        peaknumberchannels.append([])
        j = 0
        for i in range(peakchannels.__len__()-2):
            if not peakchannels[i+1] > ( peakchannels[i] + peakbroadnesstolerance ) and peakchannels[i] > 18000:        #check whether the peaks are at least x channels broad, if yes: assign a peak count
                peaknumberchannels[j].append(peakchannels[i])
                #print(j, peakchannels[i])
            else:                                                       #and if the end of the peak is detected, allow a new peak
                j = j + 1
                peaknumberchannels.append([])
                #print('increased j by 1')
        while True:     # remove all empty lists from our "channels above threshold"
            try:
                peaknumberchannels.remove([])
            except ValueError:
                break
        #print(peaknumberchannels)
        peaknumberchannelstemp = peaknumberchannels
        #print('we have a total amount of peaks: ',peaknumberchannels.__len__())
        for k in range(peaknumberchannelstemp.__len__()-1, 0, -1):
            #print('checking peak:', k, 'with channels:', peaknumberchannelstemp[k])
            if not peaknumberchannelstemp[k].__len__() > 10:
                #print('delete: peak:', k, 'with channels:', peaknumberchannelstemp[k])
                del peaknumberchannels[k]
        #print(peaknumberchannels)
        #print('we have now a total amount of peaks: ',peaknumberchannels.__len__())
        plotselectedpeakchannel = []
        plotselectedpeaksummedmassspec = []
        for j in range(peaknumberchannels.__len__()):
            for i in range(peaknumberchannels[j].__len__()):
                #print(j, peaknumberchannels[j][i])
                plotselectedpeakchannel.append(peaknumberchannels[j][i])
                plotselectedpeaksummedmassspec.append(summedmassspec[peaknumberchannels[j][i]])

        return peaknumberchannels, plotselectedpeakchannel, plotselectedpeaksummedmassspec

    def calculatespectrum(self, peaknumberchannels, bgsubstrdatalist, untergrundboundaries):
        #print(bgsubstrdatalist)

        untergrundlowerboundary, untergrundupperboundary = untergrundboundaries

        spectrum = []
        for peaknr in range(peaknumberchannels.__len__()):
            spectrum.append([])
        for energy in range(bgsubstrdatalist.__len__()):




            #       now we do the untergrund substraction
            #       therefor we add up the bgsubstrdatalist in the range of background low to high
            #       then divide it by it's width (high - low)
            #       and scale it to the width of the peak

            summeduntergrund = 0
            for untergrundchannel in range(untergrundlowerboundary, untergrundupperboundary + 1):
                summeduntergrund = summeduntergrund + int(bgsubstrdatalist[energy][untergrundchannel])
            aufsummierteruntergrundaverage = summeduntergrund / (untergrundupperboundary - untergrundlowerboundary + 1)


            #print('\n')
            #print('# summed up Untergrund:', summeduntergrund,
            #      '\n# averaged over Nr. of Untergrund channels:', aufsummierteruntergrundaverage)
            #print('\n')



            for peaknr in range(peaknumberchannels.__len__()):
                tempspec = 0
                for channel in peaknumberchannels[peaknr]:
                    #print(bgsubstrdatalist[0][channel], end=" ")
                    tempspec = tempspec + int(bgsubstrdatalist[energy][channel])


                # here we take the "per channel averaged Untergrund" from outside the loop and multiply it by the
                # specific peak-width we have here inside this loop

                aufsummierteruntergrundscaledtopeak = aufsummierteruntergrundaverage * (
                        peaknumberchannels[peaknr][-1] - peaknumberchannels[peaknr][0] + 1)



                spectrum[peaknr].append(tempspec - aufsummierteruntergrundscaledtopeak)
                #print('energy:\t', energy, '\t\ttempspec intensity:\t', tempspec)
                #print('summeduntergrund:\t\t', summeduntergrund)
                #print('untergrundchannelwidth:\t\t', (untergrundupperboundary - untergrundlowerboundary))
                #print('aufsummierteruntergrundaverage:\t\t', aufsummierteruntergrundaverage)
                #print('width of analyzed peak:\t\t', (peaknumberchannels[peaknr][-1] - peaknumberchannels[peaknr][0]))
                #print('aufsummierteruntergrundscaledtopeak:\t\t', aufsummierteruntergrundscaledtopeak)
                #print()



                #print('\n\nThe sum of this is:', spectrum[peaknr], '\n')
        #print('spektrum ist: ', spectrum)

        return spectrum

    def plotspectrum(self, spectrum):
        for i in range(spectrum.__len__()):
            plt.plot(spectrum[i])
            #plt.legend(i)
        plt.show()

    def normalizespectrum(self, spectrum, monofilecontent):
        #get photocurrent
        photocurrent = []
        photonenergy = []
        photonflux = []
        #print(monofilecontent)
        for line in range(monofilecontent.__len__()):
            photocurrent.append(float(monofilecontent[line][5]))
            photonenergy.append(float(monofilecontent[line][3]))
        #print('photocurrent:', photocurrent)
        for i in range(photocurrent.__len__()):
            j = 0
            while photonenergy[i] > GaAsPhotodiode[0][j]:
                j = j + 1
            upperlimit = GaAsPhotodiode[0][j]
            lowerlimit = GaAsPhotodiode[0][j-1]
            ratio = (photonenergy[i]-lowerlimit)/(upperlimit-lowerlimit)

            quantenausbeute = GaAsPhotodiode[1][j-1] + ratio * (GaAsPhotodiode[1][j] - GaAsPhotodiode[1][j-1])
            photonflux.append(photocurrent[i]/(quantenausbeute*1.602e-19))
            #print(photonenergy[i], lowerlimit, ratio, quantenausbeute, photonflux[i], sep="\t\t")

        #print(photonflux)
        photonfluxnorm = []
        average = 0
        for k in range(photonflux.__len__()):
            average = average + photonflux[k]
        average = average / photonflux.__len__()
        #print('average is:', average)
        for i in range(photonflux.__len__()):
            photonfluxnorm.append(photonflux[i]/average)
            #print(photonflux[i], photonfluxnorm[i], sep="\t\t")
            #print(photonenergy[i], photocurrent[i])

        normalizedspectrum = []
        for peak in range(spectrum.__len__()):
            normalizedspectrum.append([])
            for i in range(spectrum[peak].__len__()):
                normalizedspectrum[peak].append(spectrum[peak][i] / photonfluxnorm[i])
                #print(photonfluxnorm[i], spectrum[peak][i], normalizedspectrum[peak][i], normalizedspectrum[peak][i]/spectrum[peak][i], sep ="\t\t")


        return normalizedspectrum

    def domasscalibration(self, currentmasschannels, masscalibparameters):

        middlechannel = (currentmasschannels[0] + currentmasschannels[-1]) / 2
        flighttime = middlechannel * 1 / 2 * 10 ** -9

        calibratedmass = masscalibparameters[0] * flighttime ** 2 + flighttime * masscalibparameters[1] + masscalibparameters[2]
        calibratedmass = str(round(calibratedmass, 2)).replace('.', 'p')
        return calibratedmass

    def exportmassspecandspectrum(self, summedmassspec, threshold, plotselectedpeakchannel, plotselectedpeaksummedmassspec, spectrum, monofilecontent, workingdirectorypath, datafoldername, analysisfolderpath, peaknumberchannels, masscalibparameters, untergrundboundaries):

        if spectrum.__len__() == 0:
            with open('_ERROOOR.txt', 'a') as file:
                file.write('there is an empty list of sprectra. probably no peaks were found (decrease sensitivity?)\n')
        else:
            os.chdir(analysisfolderpath)




            untergrundlowerboundary, untergrundupperboundary = untergrundboundaries

            os.mkdir('data_export')
            os.chdir('data_export')

            with open('D:\\_analyzerlogfile.txt', 'a') as logfile:
                logfile.write(
                    time.strftime("%d.%m.%Y %H:%M:%S")+ '\t'  +  str(psutil.virtual_memory())  + '\t\tin export next step: export spectra for all peaks\t\n')

            for peak in range(spectrum.__len__()):
                calibratedmass = self.domasscalibration(self, peaknumberchannels[peak], masscalibparameters)
                with open(datafoldername + '_m' + calibratedmass + '.txt', 'a') as file:
                    print(datafoldername + '_m' + calibratedmass + '.txt')
                    #print(spectrum[peak])
                    file.write(datafoldername + '_m' + calibratedmass + '_Energie'+ '\t' + datafoldername + '_m' + calibratedmass + '_Normiert' + '\n')
                    for datapoint in range(spectrum[peak].__len__()):
                        file.write(str(monofilecontent[datapoint][3]) + '\t' + str(spectrum[peak][datapoint]) + '\n')

            os.chdir('..')
            os.mkdir('massspec_export')
            os.chdir('massspec_export')


            with open('D:\\_analyzerlogfile.txt', 'a') as logfile:
                logfile.write(
                    time.strftime("%d.%m.%Y %H:%M:%S") + '\t' +  str(psutil.virtual_memory())   +'\t\tin export next step: export MS overall sum\t\n')


            #create a SUM MS file and write the MS Intensities into it //  no channels
            with open(datafoldername + '_massspec_sum.txt', 'a') as file:
                file.write(datafoldername + 'MS_SUM_Normiert\n')
                for channel in range(summedmassspec.__len__()):
                    file.write(str(summedmassspec[channel]) + '\n')


            with open('D:\\_analyzerlogfile.txt', 'a') as logfile:
                logfile.write(
                    time.strftime("%d.%m.%Y %H:%M:%S") + '\t' +  str(psutil.virtual_memory())  +'\t\tin export next step: export global channel list, which peaks contribute\t\n')


            # create MASS SPEC txt file for the channels
            with open(datafoldername + '_channelsforlines.txt', 'a') as file:
                #file.write(datafoldername + 'MS_SUM_Normiert\n')
                for channel in range(plotselectedpeakchannel.__len__()):
                    file.write(str(plotselectedpeakchannel[channel]) + '\n')


            with open('D:\\_analyzerlogfile.txt', 'a') as logfile:
                logfile.write(
                    time.strftime("%d.%m.%Y %H:%M:%S") + '\t' +  str(psutil.virtual_memory())  +'\t\tin export next step: create channel list for individual peaks\t\n')


            # create MASS SPEC txt file for individual peaks
            #i = 0
            for peak in range(peaknumberchannels.__len__()):
                #print('line nr.:', inspect.currentframe().f_lineno)
                calibratedmass = self.domasscalibration(self, peaknumberchannels[peak], masscalibparameters)
                #print('line nr.:', inspect.currentframe().f_lineno)

                with open(datafoldername + '_m' + calibratedmass + '_channels.txt', 'a') as file:
                    #print('line nr.:', inspect.currentframe().f_lineno)

                    for channel in range(peaknumberchannels[peak].__len__()):
                        #print('line nr.:', inspect.currentframe().f_lineno)

                        file.write(str(plotselectedpeakchannel[channel])+'\n')
                        #print('line nr.:', inspect.currentframe().f_lineno)

                        #i = i + 1



            os.chdir('..')

            with open('D:\\_analyzerlogfile.txt', 'a') as logfile:
                logfile.write(
                    time.strftime("%d.%m.%Y %H:%M:%S") + '\t' +  str(psutil.virtual_memory()) + '\t\tin export next step: read the photonenergy out of mono file\t\n')

            photonenergy = []
            for monofileline in monofilecontent:
                photonenergy.append(float(monofileline[3]))

            with open('D:\\_analyzerlogfile.txt', 'a') as logfile:
                logfile.write(
                    time.strftime(
                        "%d.%m.%Y %H:%M:%S") + '\t' +  str(psutil.virtual_memory())  + '\t\tin export next step: plot image: all spectra in one\t\n')

                    ######### Plot all Spectra in one image

            plt.figure(figsize=(7, 4))
            plt.figure.max_open_warning: 40
            for i in range(spectrum.__len__()):
                plt.plot(photonenergy[0:spectrum[i].__len__()], spectrum[i])
                plt.title('Spectra for peaks from Scannr: ' + datafoldername)
                calibratedmass = self.domasscalibration(self, peaknumberchannels[i], masscalibparameters)
                plt.annotate(s=calibratedmass, xy=(photonenergy[spectrum[i].index(max(spectrum[i]))-1], max(spectrum[i])))
            plt.savefig(datafoldername + '_allspectra' + '.png')
            plt.clf()
            plt.close()
            gc.collect()



            with open('D:\\_analyzerlogfile.txt', 'a') as logfile:
                logfile.write(
                    time.strftime("%d.%m.%Y %H:%M:%S") + '\t' +  str(psutil.virtual_memory())   + '\t\tin export next step: plot image: one spectrum for each peak\t\n')

                                                                            ######### Plot one image for each peak

            for i in range(spectrum.__len__()):
                plt.figure(figsize=(7, 4))
                j = str(i).zfill(3)
                plt.plot(photonenergy[0:spectrum[i].__len__()], spectrum[i])
                #plt.title(str(datafoldername + '_peak' + j + '.txt'))
                calibratedmass = self.domasscalibration(self, peaknumberchannels[i], masscalibparameters)
                plt.title(datafoldername + '_m' + calibratedmass + '.txt')
                plt.savefig(datafoldername + '_m' + calibratedmass + '.png')
                plt.clf()
                plt.close()
                gc.collect()

            with open('D:\\_analyzerlogfile.txt', 'a') as logfile:
                logfile.write(
                    time.strftime(
                        "%d.%m.%Y %H:%M:%S") + '\t' +  str(psutil.virtual_memory())  + '\t\tin export next step: plot MS image: big overview\t\n')

                    ######### General Overview over summed Massspec

        try:
            plt.figure(figsize=(60, 10))
            plt.plot(summedmassspec, color='grey', linewidth=0.2)
            #plt.plot([i for i in range(summedmassspec.__len__())], threshold)
            plt.plot([0, summedmassspec.__len__()], [threshold, threshold], linestyle='--')

            plt.plot([untergrundlowerboundary, untergrundlowerboundary], [min(summedmassspec[untergrundlowerboundary:untergrundupperboundary]), max(summedmassspec[untergrundlowerboundary:untergrundupperboundary])], color="red", linestyle='--')
            plt.plot([untergrundupperboundary, untergrundupperboundary], [min(summedmassspec[untergrundlowerboundary:untergrundupperboundary]), max(summedmassspec[untergrundlowerboundary:untergrundupperboundary])], color="red", linestyle='--')

            #plt.scatter(plotselectedpeakchannel, plotselectedpeaksummedmassspec, color="red")
            for peak in range(peaknumberchannels.__len__()):
                tempmassspec = []
                for channel in peaknumberchannels[peak]:
                    tempmassspec.append(summedmassspec[channel])
                plt.fill_between(peaknumberchannels[peak], tempmassspec, alpha=0.7)

                calibratedmass = self.domasscalibration(self, peaknumberchannels[peak], masscalibparameters)

                plt.annotate(s=str(calibratedmass), xy=(peaknumberchannels[peak][0]-100, max(tempmassspec)*0.9))

            plt.savefig('__summedmassspec.png', dpi=100)
            plt.clf()
            plt.close()
            gc.collect()
        except:
            with open('___ERROR.txt', 'a') as file:
                file.write('couldn\'t print overview mass spec\n')
            try:
                plt.figure(figsize=(30, 8))
                plt.plot(summedmassspec, color='grey', linewidth=0.2)
                # plt.plot([i for i in range(summedmassspec.__len__())], threshold)
                plt.plot([0, summedmassspec.__len__()], [threshold, threshold], linestyle='--')

                plt.plot([untergrundlowerboundary, untergrundlowerboundary],
                         [min(summedmassspec[untergrundlowerboundary:untergrundupperboundary]),
                          max(summedmassspec[untergrundlowerboundary:untergrundupperboundary])], color="red",
                         linestyle='--')
                plt.plot([untergrundupperboundary, untergrundupperboundary],
                         [min(summedmassspec[untergrundlowerboundary:untergrundupperboundary]),
                          max(summedmassspec[untergrundlowerboundary:untergrundupperboundary])], color="red",
                         linestyle='--')

                # plt.scatter(plotselectedpeakchannel, plotselectedpeaksummedmassspec, color="red")
                for peak in range(peaknumberchannels.__len__()):
                    tempmassspec = []
                    for channel in peaknumberchannels[peak]:
                        tempmassspec.append(summedmassspec[channel])
                    plt.fill_between(peaknumberchannels[peak], tempmassspec, alpha=0.7)

                    calibratedmass = self.domasscalibration(self, peaknumberchannels[peak], masscalibparameters)

                    plt.annotate(s=str(calibratedmass),
                                 xy=(peaknumberchannels[peak][0] - 100, max(tempmassspec) * 0.9))

                plt.savefig('__summedmassspec_coarse.png', dpi=50)
                plt.clf()
                plt.close()
                gc.collect()
            except:
                with open('___ERROR.txt', 'a') as file:
                    file.write('couldn\'t print low res overview mass spec\n')

        with open('D:\\_analyzerlogfile.txt', 'a') as logfile:
            logfile.write(
                time.strftime(
                    "%d.%m.%Y %H:%M:%S") + '\t' +  str(psutil.virtual_memory())  + '\t\tin export next step: plot MS image: range of selected peaks\t\n')

                                                    ######### PEAK Identification // range limited to selected peaks
        try:
            plt.figure(figsize=(60, 10))
            lowerboundary = min(plotselectedpeakchannel)-1000
            upperboundary = max(plotselectedpeakchannel)+1000
            plt.plot([i for i in range(lowerboundary,upperboundary)], summedmassspec[lowerboundary:upperboundary], color='grey', linewidth=0.2)
            # plt.plot([i for i in range(summedmassspec.__len__())], threshold)
            plt.plot([lowerboundary, upperboundary], [threshold, threshold], linestyle='--')
            # plt.scatter(plotselectedpeakchannel, plotselectedpeaksummedmassspec, color="red")
            for peak in range(peaknumberchannels.__len__()):
                tempmassspec = []
                for channel in peaknumberchannels[peak]:
                    tempmassspec.append(summedmassspec[channel])
                plt.fill_between(peaknumberchannels[peak], tempmassspec, alpha=0.3)

                calibratedmass = self.domasscalibration(self, peaknumberchannels[peak], masscalibparameters)

                plt.annotate(s=str(calibratedmass), xy=(peaknumberchannels[peak][0] - 40, max(tempmassspec) * 0.9))

                # plt.fill(tempmassspec, threshold[peaknumberchannels[peak][0]:peaknumberchannels[peak][-1]])
                # plt.plot(peaknumberchannels[peak], tempmassspec, linewidth=0.1)

            # print(plotselectedpeakchannel)
            # print(plotselectedpeaksummedmassspec)
            # plt.show()
            plt.savefig('_massspec_peak_identification.png', dpi=100)
            plt.clf()
            plt.close()
            gc.collect()
        except:
            with open('___ERROR.txt', 'a') as file:
                file.write('couldn\'t print detailed mass spec\n')
            try:
                plt.figure(figsize=(30, 8))
                lowerboundary = min(plotselectedpeakchannel) - 1000
                upperboundary = max(plotselectedpeakchannel) + 1000
                plt.plot([i for i in range(lowerboundary, upperboundary)], summedmassspec[lowerboundary:upperboundary],
                         color='grey', linewidth=0.2)
                # plt.plot([i for i in range(summedmassspec.__len__())], threshold)
                plt.plot([lowerboundary, upperboundary], [threshold, threshold], linestyle='--')
                # plt.scatter(plotselectedpeakchannel, plotselectedpeaksummedmassspec, color="red")
                for peak in range(peaknumberchannels.__len__()):
                    tempmassspec = []
                    for channel in peaknumberchannels[peak]:
                        tempmassspec.append(summedmassspec[channel])
                    plt.fill_between(peaknumberchannels[peak], tempmassspec, alpha=0.3)

                    calibratedmass = self.domasscalibration(self, peaknumberchannels[peak], masscalibparameters)

                    plt.annotate(s=str(calibratedmass), xy=(peaknumberchannels[peak][0] - 40, max(tempmassspec) * 0.9))

                    # plt.fill(tempmassspec, threshold[peaknumberchannels[peak][0]:peaknumberchannels[peak][-1]])
                    # plt.plot(peaknumberchannels[peak], tempmassspec, linewidth=0.1)

                # print(plotselectedpeakchannel)
                # print(plotselectedpeaksummedmassspec)
                # plt.show()
                plt.savefig('_massspec_peak_identification_coarse.png', dpi=50)
                plt.clf()
                plt.close()
                gc.collect()
            except:
                with open('___ERROR.txt', 'a') as file:
                    file.write('couldn\'t print low res detailed mass spec\n')


        #
        #                                                   export here the Untergrund Area of the Mass Spec
        #
        #

        print('writing log before Untergrund')

        with open('D:\\_analyzerlogfile.txt', 'a') as logfile:
            logfile.write(
                time.strftime(
                    "%d.%m.%Y %H:%M:%S") + '\t' +  str(psutil.virtual_memory())   + '\t\tin export next step: plot MS image: range of Untergrund\t\n')


        print('wrote log before Untergrund, going to Untergrund')

        try:
            print('close plot, if there is one')

            print('closed plot, if there was one.\t\t create figure')

            plt.figure(figsize=(60, 10))

            print('assign boundaries')

            lowerboundary = untergrundlowerboundary - 4000

            print('assigned lower boundary')

            upperboundary = untergrundupperboundary + 4000

            print('assigned upper boundary')

            print('lowerboundary:', lowerboundary)
            print('upperboundary:', upperboundary)
            print('untergrundlowerboundary:', untergrundlowerboundary)
            print('untergrundupperboundary:', untergrundupperboundary)

            print('plot Untergrund:\t\t next: plot mass spec in background')

            plt.plot([i for i in range(lowerboundary, upperboundary)], summedmassspec[lowerboundary:upperboundary],
                     color='grey', linewidth=0.2)

            print('plot Untergrund:\t\t next: plot threshold line')

            plt.plot([lowerboundary, upperboundary], [threshold, threshold], linestyle='--')

            print('plot Untergrund:\t\t next: plot lower boundary line')

            plt.plot([untergrundlowerboundary, untergrundlowerboundary], [min(summedmassspec[untergrundlowerboundary:untergrundupperboundary]), max(summedmassspec[untergrundlowerboundary:untergrundupperboundary])], color="red", linestyle='--')

            print('plot Untergrund:\t\t next: plot upper boundary line')

            plt.plot([untergrundupperboundary, untergrundupperboundary], [min(summedmassspec[untergrundlowerboundary:untergrundupperboundary]), max(summedmassspec[untergrundlowerboundary:untergrundupperboundary])], color="red", linestyle='--')

            print('plot Untergrund:\t\t next: save image as png')

            plt.savefig('_massspec_Untergrund_area.png', dpi=100)

            print('plot Untergrund:\t\t next: close plot')

            plt.clf()
            plt.close()
            gc.collect()
        except:
            with open('___ERROR.txt', 'a') as file:
                file.write('couldn\'t print mass spec with Untergrund Area\n')
            try:
                plt.figure(figsize=(30, 8))
                lowerboundary = untergrundlowerboundary - 4000
                upperboundary = untergrundupperboundary + 4000
                plt.plot([i for i in range(lowerboundary, upperboundary)], summedmassspec[lowerboundary:upperboundary],
                         color='grey', linewidth=0.2)

                plt.plot([lowerboundary, upperboundary], [threshold, threshold], linestyle='--')
                plt.plot([untergrundlowerboundary, untergrundlowerboundary],
                         [min(summedmassspec[untergrundlowerboundary:untergrundupperboundary]),
                          max(summedmassspec[untergrundlowerboundary:untergrundupperboundary])], color="red",
                         linestyle='--')
                plt.plot([untergrundupperboundary, untergrundupperboundary],
                         [min(summedmassspec[untergrundlowerboundary:untergrundupperboundary]),
                          max(summedmassspec[untergrundlowerboundary:untergrundupperboundary])], color="red",
                         linestyle='--')

                plt.savefig('_massspec_Untergrund_area_coarse.png', dpi=50)
                plt.clf()
                plt.close()
                gc.collect()
            except:
                with open('___ERROR.txt', 'a') as file:
                    file.write('couldn\'t print low res mass spec with Untergrund Area\n')
            #plt.legend(i)

        #os.chdir('..')





    def transformchannelsinmass(self, masscalibvalues):
        [masscalib1mass, masscalib1time, masscalib2mass, masscalib2time] = masscalibvalues

        x = [0, masscalib1time*0.00001, masscalib2time*0.00001]
        y = [0, masscalib1mass, masscalib2mass]

        masscalibfitparameters = np.polyfit(x, y, 2)

        print('masscalibfit parameters:', masscalibfitparameters)

        print('masscalibfit parameter 1:', masscalibfitparameters[0])
        print('masscalibfit parameter 2:', masscalibfitparameters[1])
        print('masscalibfit parameter 3:', masscalibfitparameters[2])

        #
        #   here we calculate the dependence between the Sampling Rate (i.e. 2 Gigasamples (GS) per Second
        #   thus, one Sample (i.e. one Channel) has the length of 1/2 nanosecond
        #

        testchannelnr = 42000
        testchanneltime = testchannelnr * 1 / 2 * 10**-9

        print('testchannelnr 42 000 is at time:', testchanneltime, 'seconds')

        print('mass for channel >>', testchannelnr, '<< is:',
              masscalibfitparameters[0] * testchanneltime ** 2 +
              masscalibfitparameters[1] * testchanneltime +
              masscalibfitparameters[2])

        return [masscalibfitparameters[0], masscalibfitparameters[1], masscalibfitparameters[2]]

    def dosomething(self, workingdirectorypath, datafoldername, analysisfolderpath, progressbarfolder, settingpackage):


        [datalengthlimit, thresholdfactor, minbroadnessofpeak, peakbroadnesstolerance,
         masscalib1mass, masscalib1time, masscalib2mass, masscalib2time,
         untergrundlowerboundary, untergrundupperboundary] = settingpackage

        masscalibvalues = [masscalib1mass, masscalib1time, masscalib2mass, masscalib2time]
        untergrundboundaries = [untergrundlowerboundary, untergrundupperboundary]

        print('settingpackage2:', settingpackage)

        Logfile.writelog(Logfile, 'start working in folder: ' + analysisfolderpath + '\\' + datafoldername)

        Logfile.writelog(Logfile, 'analysis button pressed,\tnext step: createanalysis folder')

        self.createanalysisfolder(self, workingdirectorypath, datafoldername, analysisfolderpath)

        Logfile.writelog(Logfile, 'analysis folder created,\tnext step: read monofilecontent')

        monofilecontent = self.readmonofile(self, workingdirectorypath, datafoldername, analysisfolderpath)

        Logfile.writelog(Logfile, 'monofilecontent read,\tnext step: read backgroundfile')

        backgrounddata = self.readbackground(self, workingdirectorypath, datafoldername, analysisfolderpath)

        Logfile.writelog(Logfile, 'bg data read,\tnext step: big read data v2 procedure')

        bgsubstrdatalist, summedmassspec = self.readrawdatav2(self, backgrounddata, workingdirectorypath, datafoldername, analysisfolderpath, progressbarfolder, datalengthlimit)
        print('############################## Length of summedmassspec:', summedmassspec.__len__())

        Logfile.writelog(Logfile, 'readrawdatav2 success,\tnext step: calc threshold')

        threshold = self.detectthreshold(self, summedmassspec, thresholdfactor)

        Logfile.writelog(Logfile, 'threshold success,\tnext step: find peak channels')

        peakchannels = self.findpeakpositions(self, summedmassspec, threshold, minbroadnessofpeak)

        Logfile.writelog(Logfile, 'peak channels found,\tnext step: count as peak numbers')

        peaknumberchannels, plotselectedpeakchannel, plotselectedpeaksummedmassspec = self.definepeaknumber(self, summedmassspec, peakchannels, peakbroadnesstolerance)

        Logfile.writelog(Logfile, 'peak numbers assigned,\tnext step: calculate raw spectra')

        spectrum = self.calculatespectrum(self, peaknumberchannels, bgsubstrdatalist, untergrundboundaries)

        Logfile.writelog(Logfile, 'raw spectrum calculated,\tnext step: normalized with photon flux')

        normalizedspectrum = self.normalizespectrum(self, spectrum, monofilecontent)

        Logfile.writelog(Logfile, 'success spectra-normalization,\tnext step: export everything')

        masscalibparameters = self.transformchannelsinmass(self, masscalibvalues)

        print(masscalibparameters)

        self.exportmassspecandspectrum(self, summedmassspec, threshold, plotselectedpeakchannel, plotselectedpeaksummedmassspec, normalizedspectrum, monofilecontent, workingdirectorypath, datafoldername, analysisfolderpath, peaknumberchannels, masscalibparameters, untergrundboundaries)

        Logfile.writelog(Logfile, 'everything exported,\tfinished \n\n')


        print('\ndid stuff...')
        del spectrum, normalizedspectrum, peaknumberchannels, plotselectedpeakchannel, plotselectedpeaksummedmassspec, peakchannels, threshold, bgsubstrdatalist, summedmassspec, backgrounddata, monofilecontent






def main():
    with open('D:\\_analyzerlogfile.txt', 'w') as logfile:
        logfile.write(time.strftime("%d.%m.%Y %H:%M:%S") +  str(psutil.virtual_memory())  + '\t' + '\n\n########################\ninitialize program\n######################\n\n')
    app = QApplication(sys.argv)
    w = Fenster()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
