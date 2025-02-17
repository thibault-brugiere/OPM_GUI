# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_Control_Microscope_Main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QComboBox,
    QDateTimeEdit, QDoubleSpinBox, QFrame, QGroupBox,
    QHBoxLayout, QLCDNumber, QLabel, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QRadioButton, QSizePolicy, QSlider, QSpacerItem,
    QSpinBox, QStatusBar, QTimeEdit, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1880, 1163)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setAnimated(True)
        MainWindow.setDockNestingEnabled(True)
        self.action_SaveConfig = QAction(MainWindow)
        self.action_SaveConfig.setObjectName(u"action_SaveConfig")
        self.action_LoadConfig = QAction(MainWindow)
        self.action_LoadConfig.setObjectName(u"action_LoadConfig")
        self.action_DAQ = QAction(MainWindow)
        self.action_DAQ.setObjectName(u"action_DAQ")
        self.action_Lasers = QAction(MainWindow)
        self.action_Lasers.setObjectName(u"action_Lasers")
        self.action_Camera = QAction(MainWindow)
        self.action_Camera.setObjectName(u"action_Camera")
        self.actionData_path = QAction(MainWindow)
        self.actionData_path.setObjectName(u"actionData_path")
        self.actionExperience_Name = QAction(MainWindow)
        self.actionExperience_Name.setObjectName(u"actionExperience_Name")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_32 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_saving = QLabel(self.centralwidget)
        self.label_saving.setObjectName(u"label_saving")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label_saving.setFont(font)
        self.label_saving.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_saving)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_data_path = QLabel(self.centralwidget)
        self.label_data_path.setObjectName(u"label_data_path")
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush)
        self.label_data_path.setPalette(palette)
        self.label_data_path.setAutoFillBackground(True)
        self.label_data_path.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_18.addWidget(self.label_data_path)

        self.pb_data_path = QPushButton(self.centralwidget)
        self.pb_data_path.setObjectName(u"pb_data_path")

        self.horizontalLayout_18.addWidget(self.pb_data_path)


        self.verticalLayout.addLayout(self.horizontalLayout_18)

        self.lineEdit_exp_name = QLineEdit(self.centralwidget)
        self.lineEdit_exp_name.setObjectName(u"lineEdit_exp_name")

        self.verticalLayout.addWidget(self.lineEdit_exp_name)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.comboBox_setup = QComboBox(self.centralwidget)
        self.comboBox_setup.addItem("")
        self.comboBox_setup.addItem("")
        self.comboBox_setup.setObjectName(u"comboBox_setup")

        self.horizontalLayout_5.addWidget(self.comboBox_setup)

        self.label_setup = QLabel(self.centralwidget)
        self.label_setup.setObjectName(u"label_setup")

        self.horizontalLayout_5.addWidget(self.label_setup)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.line_7 = QFrame(self.centralwidget)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShape(QFrame.Shape.HLine)
        self.line_7.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_7)

        self.label_camera_settings = QLabel(self.centralwidget)
        self.label_camera_settings.setObjectName(u"label_camera_settings")
        self.label_camera_settings.setFont(font)
        self.label_camera_settings.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_camera_settings)

        self.comboBox_camera = QComboBox(self.centralwidget)
        self.comboBox_camera.addItem("")
        self.comboBox_camera.setObjectName(u"comboBox_camera")
        self.comboBox_camera.setEnabled(False)

        self.verticalLayout.addWidget(self.comboBox_camera)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.spinBox_hsize = QSpinBox(self.centralwidget)
        self.spinBox_hsize.setObjectName(u"spinBox_hsize")
        self.spinBox_hsize.setMaximum(4432)
        self.spinBox_hsize.setSingleStep(4)
        self.spinBox_hsize.setValue(4432)

        self.horizontalLayout.addWidget(self.spinBox_hsize)

        self.label_hsize = QLabel(self.centralwidget)
        self.label_hsize.setObjectName(u"label_hsize")

        self.horizontalLayout.addWidget(self.label_hsize)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.spinBox_hpos = QSpinBox(self.centralwidget)
        self.spinBox_hpos.setObjectName(u"spinBox_hpos")
        self.spinBox_hpos.setMaximum(4432)
        self.spinBox_hpos.setSingleStep(4)
        self.spinBox_hpos.setValue(0)

        self.horizontalLayout_2.addWidget(self.spinBox_hpos)

        self.label_hpos = QLabel(self.centralwidget)
        self.label_hpos.setObjectName(u"label_hpos")

        self.horizontalLayout_2.addWidget(self.label_hpos)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.spinBox_vsize = QSpinBox(self.centralwidget)
        self.spinBox_vsize.setObjectName(u"spinBox_vsize")
        self.spinBox_vsize.setMaximum(2368)
        self.spinBox_vsize.setSingleStep(4)
        self.spinBox_vsize.setValue(2368)

        self.horizontalLayout_3.addWidget(self.spinBox_vsize)

        self.label_vsize = QLabel(self.centralwidget)
        self.label_vsize.setObjectName(u"label_vsize")

        self.horizontalLayout_3.addWidget(self.label_vsize)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.spinBox_vpos = QSpinBox(self.centralwidget)
        self.spinBox_vpos.setObjectName(u"spinBox_vpos")
        self.spinBox_vpos.setMaximum(2368)
        self.spinBox_vpos.setSingleStep(4)
        self.spinBox_vpos.setValue(0)

        self.horizontalLayout_4.addWidget(self.spinBox_vpos)

        self.label_vpos = QLabel(self.centralwidget)
        self.label_vpos.setObjectName(u"label_vpos")

        self.horizontalLayout_4.addWidget(self.label_vpos)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.comboBox_size_preset = QComboBox(self.centralwidget)
        self.comboBox_size_preset.addItem("")
        self.comboBox_size_preset.addItem("")
        self.comboBox_size_preset.addItem("")
        self.comboBox_size_preset.setObjectName(u"comboBox_size_preset")

        self.horizontalLayout_29.addWidget(self.comboBox_size_preset)

        self.pb_center_FOV = QPushButton(self.centralwidget)
        self.pb_center_FOV.setObjectName(u"pb_center_FOV")

        self.horizontalLayout_29.addWidget(self.pb_center_FOV)


        self.verticalLayout.addLayout(self.horizontalLayout_29)

        self.label_fov_size = QLabel(self.centralwidget)
        self.label_fov_size.setObjectName(u"label_fov_size")

        self.verticalLayout.addWidget(self.label_fov_size)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.comboBox_binning = QComboBox(self.centralwidget)
        self.comboBox_binning.addItem("")
        self.comboBox_binning.addItem("")
        self.comboBox_binning.addItem("")
        self.comboBox_binning.setObjectName(u"comboBox_binning")

        self.horizontalLayout_28.addWidget(self.comboBox_binning)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_28.addWidget(self.label)


        self.verticalLayout.addLayout(self.horizontalLayout_28)

        self.line_8 = QFrame(self.centralwidget)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setFrameShape(QFrame.Shape.HLine)
        self.line_8.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_8)

        self.label_channels_settings = QLabel(self.centralwidget)
        self.label_channels_settings.setObjectName(u"label_channels_settings")
        self.label_channels_settings.setFont(font)
        self.label_channels_settings.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_channels_settings)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.lineEdit_channel_name = QLineEdit(self.centralwidget)
        self.lineEdit_channel_name.setObjectName(u"lineEdit_channel_name")
        self.lineEdit_channel_name.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_12.addWidget(self.lineEdit_channel_name)

        self.comboBox_channel_name = QComboBox(self.centralwidget)
        self.comboBox_channel_name.addItem("")
        self.comboBox_channel_name.addItem("")
        self.comboBox_channel_name.addItem("")
        self.comboBox_channel_name.addItem("")
        self.comboBox_channel_name.setObjectName(u"comboBox_channel_name")

        self.horizontalLayout_12.addWidget(self.comboBox_channel_name)

        self.pb_channel_save = QPushButton(self.centralwidget)
        self.pb_channel_save.setObjectName(u"pb_channel_save")
        self.pb_channel_save.setEnabled(True)

        self.horizontalLayout_12.addWidget(self.pb_channel_save)

        self.pb_channel_add = QPushButton(self.centralwidget)
        self.pb_channel_add.setObjectName(u"pb_channel_add")

        self.horizontalLayout_12.addWidget(self.pb_channel_add)

        self.pb_channel_remove = QPushButton(self.centralwidget)
        self.pb_channel_remove.setObjectName(u"pb_channel_remove")
        self.pb_channel_remove.setEnabled(True)

        self.horizontalLayout_12.addWidget(self.pb_channel_remove)


        self.verticalLayout.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.lcdNumber_laser_405 = QLCDNumber(self.centralwidget)
        self.lcdNumber_laser_405.setObjectName(u"lcdNumber_laser_405")
        palette1 = QPalette()
        brush1 = QBrush(QColor(226, 137, 255, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.Light, brush1)
        palette1.setBrush(QPalette.Active, QPalette.Base, brush)
        brush2 = QBrush(QColor(0, 0, 0, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette1.setBrush(QPalette.Inactive, QPalette.Light, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette1.setBrush(QPalette.Disabled, QPalette.Light, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette1.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.lcdNumber_laser_405.setPalette(palette1)
        self.lcdNumber_laser_405.setAutoFillBackground(True)
        self.lcdNumber_laser_405.setSmallDecimalPoint(False)
        self.lcdNumber_laser_405.setProperty(u"value", 405.000000000000000)

        self.horizontalLayout_17.addWidget(self.lcdNumber_laser_405)

        self.lcdNumber_laser_488 = QLCDNumber(self.centralwidget)
        self.lcdNumber_laser_488.setObjectName(u"lcdNumber_laser_488")
        palette2 = QPalette()
        brush3 = QBrush(QColor(85, 255, 255, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette2.setBrush(QPalette.Active, QPalette.Light, brush3)
        palette2.setBrush(QPalette.Active, QPalette.Base, brush)
        palette2.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette2.setBrush(QPalette.Inactive, QPalette.Light, brush3)
        palette2.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette2.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette2.setBrush(QPalette.Disabled, QPalette.Light, brush3)
        palette2.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette2.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.lcdNumber_laser_488.setPalette(palette2)
        self.lcdNumber_laser_488.setAutoFillBackground(True)
        self.lcdNumber_laser_488.setSmallDecimalPoint(False)
        self.lcdNumber_laser_488.setProperty(u"value", 488.000000000000000)

        self.horizontalLayout_17.addWidget(self.lcdNumber_laser_488)

        self.lcdNumber_laser_561 = QLCDNumber(self.centralwidget)
        self.lcdNumber_laser_561.setObjectName(u"lcdNumber_laser_561")
        palette3 = QPalette()
        brush4 = QBrush(QColor(255, 255, 127, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette3.setBrush(QPalette.Active, QPalette.Light, brush4)
        palette3.setBrush(QPalette.Active, QPalette.Base, brush)
        palette3.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette3.setBrush(QPalette.Inactive, QPalette.Light, brush4)
        palette3.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette3.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette3.setBrush(QPalette.Disabled, QPalette.Light, brush4)
        palette3.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette3.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.lcdNumber_laser_561.setPalette(palette3)
        self.lcdNumber_laser_561.setAutoFillBackground(True)
        self.lcdNumber_laser_561.setSmallDecimalPoint(False)
        self.lcdNumber_laser_561.setProperty(u"value", 561.000000000000000)

        self.horizontalLayout_17.addWidget(self.lcdNumber_laser_561)

        self.lcdNumber_laser_640 = QLCDNumber(self.centralwidget)
        self.lcdNumber_laser_640.setObjectName(u"lcdNumber_laser_640")
        palette4 = QPalette()
        brush5 = QBrush(QColor(255, 0, 0, 255))
        brush5.setStyle(Qt.SolidPattern)
        palette4.setBrush(QPalette.Active, QPalette.Light, brush5)
        palette4.setBrush(QPalette.Active, QPalette.Base, brush)
        palette4.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette4.setBrush(QPalette.Inactive, QPalette.Light, brush5)
        palette4.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette4.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette4.setBrush(QPalette.Disabled, QPalette.Light, brush5)
        palette4.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette4.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.lcdNumber_laser_640.setPalette(palette4)
        self.lcdNumber_laser_640.setAutoFillBackground(True)
        self.lcdNumber_laser_640.setSmallDecimalPoint(False)
        self.lcdNumber_laser_640.setProperty(u"value", 640.000000000000000)

        self.horizontalLayout_17.addWidget(self.lcdNumber_laser_640)


        self.verticalLayout.addLayout(self.horizontalLayout_17)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer)

        self.checkBox_laser_405 = QCheckBox(self.centralwidget)
        self.checkBox_laser_405.setObjectName(u"checkBox_laser_405")

        self.horizontalLayout_6.addWidget(self.checkBox_laser_405)

        self.horizontalSpacer_2 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)


        self.horizontalLayout_19.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalSpacer_6 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_6)

        self.checkBox_laser_488 = QCheckBox(self.centralwidget)
        self.checkBox_laser_488.setObjectName(u"checkBox_laser_488")

        self.horizontalLayout_9.addWidget(self.checkBox_laser_488)

        self.horizontalSpacer_3 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_3)


        self.horizontalLayout_19.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalSpacer_7 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_7)

        self.checkBox_laser_561 = QCheckBox(self.centralwidget)
        self.checkBox_laser_561.setObjectName(u"checkBox_laser_561")

        self.horizontalLayout_10.addWidget(self.checkBox_laser_561)

        self.horizontalSpacer_4 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_4)


        self.horizontalLayout_19.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalSpacer_8 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_8)

        self.checkBox_laser_640 = QCheckBox(self.centralwidget)
        self.checkBox_laser_640.setObjectName(u"checkBox_laser_640")

        self.horizontalLayout_11.addWidget(self.checkBox_laser_640)

        self.horizontalSpacer_5 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_5)


        self.horizontalLayout_19.addLayout(self.horizontalLayout_11)


        self.verticalLayout.addLayout(self.horizontalLayout_19)

        self.label_laser_power = QLabel(self.centralwidget)
        self.label_laser_power.setObjectName(u"label_laser_power")
        self.label_laser_power.setAutoFillBackground(False)
        self.label_laser_power.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_laser_power)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.spinBox_laser_405 = QSpinBox(self.centralwidget)
        self.spinBox_laser_405.setObjectName(u"spinBox_laser_405")
        self.spinBox_laser_405.setMaximum(100)

        self.horizontalLayout_13.addWidget(self.spinBox_laser_405)

        self.spinBox_laser_488 = QSpinBox(self.centralwidget)
        self.spinBox_laser_488.setObjectName(u"spinBox_laser_488")
        self.spinBox_laser_488.setMaximum(100)

        self.horizontalLayout_13.addWidget(self.spinBox_laser_488)

        self.spinBox_laser_561 = QSpinBox(self.centralwidget)
        self.spinBox_laser_561.setObjectName(u"spinBox_laser_561")
        self.spinBox_laser_561.setMaximum(100)

        self.horizontalLayout_13.addWidget(self.spinBox_laser_561)

        self.spinBox_laser_640 = QSpinBox(self.centralwidget)
        self.spinBox_laser_640.setObjectName(u"spinBox_laser_640")
        self.spinBox_laser_640.setMaximum(100)

        self.horizontalLayout_13.addWidget(self.spinBox_laser_640)


        self.verticalLayout.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.slider_laser_405 = QSlider(self.centralwidget)
        self.slider_laser_405.setObjectName(u"slider_laser_405")
        self.slider_laser_405.setMaximumSize(QSize(16777215, 16777215))
        self.slider_laser_405.setMaximum(100)
        self.slider_laser_405.setOrientation(Qt.Vertical)

        self.horizontalLayout_14.addWidget(self.slider_laser_405)

        self.slider_laser_488 = QSlider(self.centralwidget)
        self.slider_laser_488.setObjectName(u"slider_laser_488")
        self.slider_laser_488.setMaximumSize(QSize(16777215, 16777215))
        self.slider_laser_488.setMaximum(100)
        self.slider_laser_488.setOrientation(Qt.Vertical)

        self.horizontalLayout_14.addWidget(self.slider_laser_488)

        self.slider_laser_561 = QSlider(self.centralwidget)
        self.slider_laser_561.setObjectName(u"slider_laser_561")
        self.slider_laser_561.setMaximumSize(QSize(16777215, 16777215))
        self.slider_laser_561.setMaximum(100)
        self.slider_laser_561.setOrientation(Qt.Vertical)

        self.horizontalLayout_14.addWidget(self.slider_laser_561)

        self.slider_laser_640 = QSlider(self.centralwidget)
        self.slider_laser_640.setObjectName(u"slider_laser_640")
        self.slider_laser_640.setMaximumSize(QSize(16777215, 16777215))
        self.slider_laser_640.setMaximum(100)
        self.slider_laser_640.setOrientation(Qt.Vertical)

        self.horizontalLayout_14.addWidget(self.slider_laser_640)


        self.verticalLayout.addLayout(self.horizontalLayout_14)

        self.label_channel_filter = QLabel(self.centralwidget)
        self.label_channel_filter.setObjectName(u"label_channel_filter")
        self.label_channel_filter.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_channel_filter)

        self.comboBox_channel_filter = QComboBox(self.centralwidget)
        self.comboBox_channel_filter.addItem("")
        self.comboBox_channel_filter.addItem("")
        self.comboBox_channel_filter.addItem("")
        self.comboBox_channel_filter.addItem("")
        self.comboBox_channel_filter.setObjectName(u"comboBox_channel_filter")

        self.verticalLayout.addWidget(self.comboBox_channel_filter)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.comboBox_channel_camera = QComboBox(self.centralwidget)
        self.comboBox_channel_camera.addItem("")
        self.comboBox_channel_camera.setObjectName(u"comboBox_channel_camera")
        self.comboBox_channel_camera.setEnabled(False)
        self.comboBox_channel_camera.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_15.addWidget(self.comboBox_channel_camera)

        self.spinBox_channel_exposure_time = QDoubleSpinBox(self.centralwidget)
        self.spinBox_channel_exposure_time.setObjectName(u"spinBox_channel_exposure_time")
        self.spinBox_channel_exposure_time.setDecimals(2)
        self.spinBox_channel_exposure_time.setMinimum(8.699999999999999)
        self.spinBox_channel_exposure_time.setMaximum(999.990000000000009)
        self.spinBox_channel_exposure_time.setValue(8.699999999999999)

        self.horizontalLayout_15.addWidget(self.spinBox_channel_exposure_time)

        self.label_channel_exposure_time = QLabel(self.centralwidget)
        self.label_channel_exposure_time.setObjectName(u"label_channel_exposure_time")
        self.label_channel_exposure_time.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_15.addWidget(self.label_channel_exposure_time)


        self.verticalLayout.addLayout(self.horizontalLayout_15)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout_32.addLayout(self.verticalLayout)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_32.addWidget(self.line)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_timelaps_settings = QLabel(self.centralwidget)
        self.label_timelaps_settings.setObjectName(u"label_timelaps_settings")
        self.label_timelaps_settings.setFont(font)
        self.label_timelaps_settings.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_timelaps_settings)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.spinBox_timepoints = QSpinBox(self.centralwidget)
        self.spinBox_timepoints.setObjectName(u"spinBox_timepoints")
        self.spinBox_timepoints.setMaximum(3600)
        self.spinBox_timepoints.setValue(10)

        self.horizontalLayout_16.addWidget(self.spinBox_timepoints)

        self.label_timepoints = QLabel(self.centralwidget)
        self.label_timepoints.setObjectName(u"label_timepoints")

        self.horizontalLayout_16.addWidget(self.label_timepoints)


        self.verticalLayout_5.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.radioButton_time_intervals = QRadioButton(self.centralwidget)
        self.buttonGroup = QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.radioButton_time_intervals)
        self.radioButton_time_intervals.setObjectName(u"radioButton_time_intervals")
        self.radioButton_time_intervals.setChecked(True)

        self.horizontalLayout_7.addWidget(self.radioButton_time_intervals)

        self.spinBox_time_interval = QDoubleSpinBox(self.centralwidget)
        self.spinBox_time_interval.setObjectName(u"spinBox_time_interval")
        self.spinBox_time_interval.setEnabled(True)
        self.spinBox_time_interval.setWrapping(False)
        self.spinBox_time_interval.setDecimals(3)
        self.spinBox_time_interval.setMinimum(0.010000000000000)
        self.spinBox_time_interval.setMaximum(3600.000000000000000)
        self.spinBox_time_interval.setValue(1.000000000000000)

        self.horizontalLayout_7.addWidget(self.spinBox_time_interval)

        self.label_time_interval = QLabel(self.centralwidget)
        self.label_time_interval.setObjectName(u"label_time_interval")

        self.horizontalLayout_7.addWidget(self.label_time_interval)


        self.verticalLayout_5.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.radioButton_total_duration = QRadioButton(self.centralwidget)
        self.buttonGroup.addButton(self.radioButton_total_duration)
        self.radioButton_total_duration.setObjectName(u"radioButton_total_duration")
        self.radioButton_total_duration.setChecked(False)

        self.horizontalLayout_8.addWidget(self.radioButton_total_duration)

        self.timeEdit_total_duration = QTimeEdit(self.centralwidget)
        self.timeEdit_total_duration.setObjectName(u"timeEdit_total_duration")
        self.timeEdit_total_duration.setEnabled(False)
        self.timeEdit_total_duration.setMaximumTime(QTime(23, 59, 59))
        self.timeEdit_total_duration.setCurrentSection(QDateTimeEdit.HourSection)
        self.timeEdit_total_duration.setTime(QTime(0, 0, 10))

        self.horizontalLayout_8.addWidget(self.timeEdit_total_duration)

        self.label_total_duration = QLabel(self.centralwidget)
        self.label_total_duration.setObjectName(u"label_total_duration")

        self.horizontalLayout_8.addWidget(self.label_total_duration)


        self.verticalLayout_5.addLayout(self.horizontalLayout_8)

        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_5.addWidget(self.line_3)

        self.label_scanner_settings = QLabel(self.centralwidget)
        self.label_scanner_settings.setObjectName(u"label_scanner_settings")
        self.label_scanner_settings.setFont(font)
        self.label_scanner_settings.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_scanner_settings)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_14)

        self.slider_scanner_position = QSlider(self.centralwidget)
        self.slider_scanner_position.setObjectName(u"slider_scanner_position")
        self.slider_scanner_position.setMinimumSize(QSize(0, 300))
        self.slider_scanner_position.setMaximumSize(QSize(16777215, 300))
        self.slider_scanner_position.setMinimum(-200)
        self.slider_scanner_position.setMaximum(200)
        self.slider_scanner_position.setOrientation(Qt.Vertical)

        self.horizontalLayout_20.addWidget(self.slider_scanner_position)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_15)


        self.verticalLayout_5.addLayout(self.horizontalLayout_20)

        self.label_scanner_position = QLabel(self.centralwidget)
        self.label_scanner_position.setObjectName(u"label_scanner_position")
        font1 = QFont()
        font1.setPointSize(8)
        font1.setBold(False)
        self.label_scanner_position.setFont(font1)
        self.label_scanner_position.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_scanner_position)

        self.spinBox_scanner_position = QSpinBox(self.centralwidget)
        self.spinBox_scanner_position.setObjectName(u"spinBox_scanner_position")
        self.spinBox_scanner_position.setMinimum(-200)
        self.spinBox_scanner_position.setMaximum(200)

        self.verticalLayout_5.addWidget(self.spinBox_scanner_position)

        self.pb_scanner_center = QPushButton(self.centralwidget)
        self.pb_scanner_center.setObjectName(u"pb_scanner_center")

        self.verticalLayout_5.addWidget(self.pb_scanner_center)

        self.label_scan_range = QLabel(self.centralwidget)
        self.label_scan_range.setObjectName(u"label_scan_range")

        self.verticalLayout_5.addWidget(self.label_scan_range)

        self.spinBox_scan_range = QDoubleSpinBox(self.centralwidget)
        self.spinBox_scan_range.setObjectName(u"spinBox_scan_range")
        self.spinBox_scan_range.setMaximum(300.000000000000000)
        self.spinBox_scan_range.setValue(20.000000000000000)

        self.verticalLayout_5.addWidget(self.spinBox_scan_range)

        self.line_4 = QFrame(self.centralwidget)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_5.addWidget(self.line_4)

        self.label_channels = QLabel(self.centralwidget)
        self.label_channels.setObjectName(u"label_channels")
        self.label_channels.setFont(font)
        self.label_channels.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_channels)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.spinBox_number_channels = QSpinBox(self.centralwidget)
        self.spinBox_number_channels.setObjectName(u"spinBox_number_channels")
        self.spinBox_number_channels.setMinimum(0)
        self.spinBox_number_channels.setMaximum(10)

        self.horizontalLayout_31.addWidget(self.spinBox_number_channels)

        self.label_number_channels = QLabel(self.centralwidget)
        self.label_number_channels.setObjectName(u"label_number_channels")
        self.label_number_channels.setAutoFillBackground(False)

        self.horizontalLayout_31.addWidget(self.label_number_channels)


        self.verticalLayout_5.addLayout(self.horizontalLayout_31)

        self.groupBox_channel_order = QGroupBox(self.centralwidget)
        self.groupBox_channel_order.setObjectName(u"groupBox_channel_order")
        self.groupBox_channel_order.setMinimumSize(QSize(0, 0))
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_channel_order)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")

        self.verticalLayout_5.addWidget(self.groupBox_channel_order)

        self.verticalSpacer_2 = QSpacerItem(20, 188, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)

        self.line_6 = QFrame(self.centralwidget)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.Shape.HLine)
        self.line_6.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_5.addWidget(self.line_6)

        self.label_volume_duration = QLabel(self.centralwidget)
        self.label_volume_duration.setObjectName(u"label_volume_duration")
        self.label_volume_duration.setAutoFillBackground(False)

        self.verticalLayout_5.addWidget(self.label_volume_duration)


        self.horizontalLayout_32.addLayout(self.verticalLayout_5)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_32.addWidget(self.line_2)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_image_preview = QLabel(self.centralwidget)
        self.label_image_preview.setObjectName(u"label_image_preview")
        self.label_image_preview.setMinimumSize(QSize(1108, 592))
        self.label_image_preview.setMaximumSize(QSize(2216, 1184))
        palette5 = QPalette()
        palette5.setBrush(QPalette.Active, QPalette.Base, brush)
        palette5.setBrush(QPalette.Active, QPalette.Window, brush)
        palette5.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette5.setBrush(QPalette.Inactive, QPalette.Window, brush)
        palette5.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette5.setBrush(QPalette.Disabled, QPalette.Window, brush)
        self.label_image_preview.setPalette(palette5)
        self.label_image_preview.setAutoFillBackground(True)

        self.verticalLayout_4.addWidget(self.label_image_preview)

        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.checkBox_show_saturation = QCheckBox(self.centralwidget)
        self.checkBox_show_saturation.setObjectName(u"checkBox_show_saturation")

        self.horizontalLayout_27.addWidget(self.checkBox_show_saturation)

        self.comboBox_preview_zoom = QComboBox(self.centralwidget)
        self.comboBox_preview_zoom.addItem("")
        self.comboBox_preview_zoom.addItem("")
        self.comboBox_preview_zoom.addItem("")
        self.comboBox_preview_zoom.addItem("")
        self.comboBox_preview_zoom.addItem("")
        self.comboBox_preview_zoom.addItem("")
        self.comboBox_preview_zoom.setObjectName(u"comboBox_preview_zoom")

        self.horizontalLayout_27.addWidget(self.comboBox_preview_zoom)


        self.verticalLayout_3.addLayout(self.horizontalLayout_27)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.slider_min_grayscale = QSlider(self.centralwidget)
        self.slider_min_grayscale.setObjectName(u"slider_min_grayscale")
        self.slider_min_grayscale.setMaximum(65534)
        self.slider_min_grayscale.setOrientation(Qt.Horizontal)

        self.horizontalLayout_21.addWidget(self.slider_min_grayscale)

        self.spinBox_min_grayscale = QSpinBox(self.centralwidget)
        self.spinBox_min_grayscale.setObjectName(u"spinBox_min_grayscale")
        self.spinBox_min_grayscale.setMaximum(65534)

        self.horizontalLayout_21.addWidget(self.spinBox_min_grayscale)

        self.label_min_grayscale = QLabel(self.centralwidget)
        self.label_min_grayscale.setObjectName(u"label_min_grayscale")

        self.horizontalLayout_21.addWidget(self.label_min_grayscale)


        self.verticalLayout_3.addLayout(self.horizontalLayout_21)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.slider_max_grayscale = QSlider(self.centralwidget)
        self.slider_max_grayscale.setObjectName(u"slider_max_grayscale")
        self.slider_max_grayscale.setMinimum(1)
        self.slider_max_grayscale.setMaximum(65535)
        self.slider_max_grayscale.setPageStep(100)
        self.slider_max_grayscale.setValue(65535)
        self.slider_max_grayscale.setOrientation(Qt.Horizontal)

        self.horizontalLayout_22.addWidget(self.slider_max_grayscale)

        self.spinBox_max_grayscale = QSpinBox(self.centralwidget)
        self.spinBox_max_grayscale.setObjectName(u"spinBox_max_grayscale")
        self.spinBox_max_grayscale.setMinimum(1)
        self.spinBox_max_grayscale.setMaximum(65535)
        self.spinBox_max_grayscale.setValue(65535)

        self.horizontalLayout_22.addWidget(self.spinBox_max_grayscale)

        self.label_max_grayscale = QLabel(self.centralwidget)
        self.label_max_grayscale.setObjectName(u"label_max_grayscale")

        self.horizontalLayout_22.addWidget(self.label_max_grayscale)


        self.verticalLayout_3.addLayout(self.horizontalLayout_22)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.pb_auto_grayscale = QPushButton(self.centralwidget)
        self.pb_auto_grayscale.setObjectName(u"pb_auto_grayscale")

        self.horizontalLayout_23.addWidget(self.pb_auto_grayscale)

        self.pb_reset_grayscale = QPushButton(self.centralwidget)
        self.pb_reset_grayscale.setObjectName(u"pb_reset_grayscale")

        self.horizontalLayout_23.addWidget(self.pb_reset_grayscale)


        self.verticalLayout_3.addLayout(self.horizontalLayout_23)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.pb_preview = QPushButton(self.centralwidget)
        self.pb_preview.setObjectName(u"pb_preview")
        self.pb_preview.setFont(font)

        self.horizontalLayout_24.addWidget(self.pb_preview)

        self.pb_pause_preview = QPushButton(self.centralwidget)
        self.pb_pause_preview.setObjectName(u"pb_pause_preview")
        self.pb_pause_preview.setFont(font)

        self.horizontalLayout_24.addWidget(self.pb_pause_preview)

        self.pb_stop_preview = QPushButton(self.centralwidget)
        self.pb_stop_preview.setObjectName(u"pb_stop_preview")
        self.pb_stop_preview.setFont(font)

        self.horizontalLayout_24.addWidget(self.pb_stop_preview)


        self.verticalLayout_3.addLayout(self.horizontalLayout_24)

        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_26.addItem(self.horizontalSpacer_12)

        self.pb_snap = QPushButton(self.centralwidget)
        self.pb_snap.setObjectName(u"pb_snap")
        self.pb_snap.setFont(font)

        self.horizontalLayout_26.addWidget(self.pb_snap)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_26.addItem(self.horizontalSpacer_13)


        self.verticalLayout_3.addLayout(self.horizontalLayout_26)


        self.horizontalLayout_30.addLayout(self.verticalLayout_3)

        self.label_histogram_greyvalue = QLabel(self.centralwidget)
        self.label_histogram_greyvalue.setObjectName(u"label_histogram_greyvalue")
        self.label_histogram_greyvalue.setMinimumSize(QSize(600, 200))
        palette6 = QPalette()
        palette6.setBrush(QPalette.Active, QPalette.Base, brush)
        palette6.setBrush(QPalette.Active, QPalette.Window, brush)
        palette6.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette6.setBrush(QPalette.Inactive, QPalette.Window, brush)
        palette6.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette6.setBrush(QPalette.Disabled, QPalette.Window, brush)
        self.label_histogram_greyvalue.setPalette(palette6)
        self.label_histogram_greyvalue.setAutoFillBackground(True)

        self.horizontalLayout_30.addWidget(self.label_histogram_greyvalue)


        self.verticalLayout_4.addLayout(self.horizontalLayout_30)

        self.line_5 = QFrame(self.centralwidget)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_4.addWidget(self.line_5)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_25.addItem(self.horizontalSpacer_9)

        self.pb_snoutscope_acquisition = QPushButton(self.centralwidget)
        self.pb_snoutscope_acquisition.setObjectName(u"pb_snoutscope_acquisition")
        self.pb_snoutscope_acquisition.setFont(font)

        self.horizontalLayout_25.addWidget(self.pb_snoutscope_acquisition)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_25.addItem(self.horizontalSpacer_10)

        self.pb_multidimensional_acquisition = QPushButton(self.centralwidget)
        self.pb_multidimensional_acquisition.setObjectName(u"pb_multidimensional_acquisition")
        self.pb_multidimensional_acquisition.setFont(font)

        self.horizontalLayout_25.addWidget(self.pb_multidimensional_acquisition)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_25.addItem(self.horizontalSpacer_11)


        self.verticalLayout_4.addLayout(self.horizontalLayout_25)


        self.horizontalLayout_32.addLayout(self.verticalLayout_4)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1880, 26))
        self.menuFichier = QMenu(self.menubar)
        self.menuFichier.setObjectName(u"menuFichier")
        self.menuSaving = QMenu(self.menuFichier)
        self.menuSaving.setObjectName(u"menuSaving")
        self.menuConfig = QMenu(self.menubar)
        self.menuConfig.setObjectName(u"menuConfig")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFichier.menuAction())
        self.menubar.addAction(self.menuConfig.menuAction())
        self.menuFichier.addAction(self.action_SaveConfig)
        self.menuFichier.addAction(self.action_LoadConfig)
        self.menuFichier.addAction(self.menuSaving.menuAction())
        self.menuSaving.addAction(self.actionData_path)
        self.menuSaving.addAction(self.actionExperience_Name)
        self.menuConfig.addAction(self.action_Camera)
        self.menuConfig.addAction(self.action_DAQ)
        self.menuConfig.addAction(self.action_Lasers)

        self.retranslateUi(MainWindow)
        self.slider_laser_405.valueChanged.connect(self.spinBox_laser_405.setValue)
        self.spinBox_laser_405.valueChanged.connect(self.slider_laser_405.setValue)
        self.slider_laser_488.valueChanged.connect(self.spinBox_laser_488.setValue)
        self.spinBox_laser_488.valueChanged.connect(self.slider_laser_488.setValue)
        self.spinBox_laser_561.valueChanged.connect(self.slider_laser_561.setValue)
        self.slider_laser_561.valueChanged.connect(self.spinBox_laser_561.setValue)
        self.slider_laser_640.valueChanged.connect(self.spinBox_laser_640.setValue)
        self.spinBox_laser_640.valueChanged.connect(self.slider_laser_640.setValue)
        self.slider_scanner_position.valueChanged.connect(self.spinBox_scanner_position.setValue)
        self.radioButton_total_duration.clicked["bool"].connect(self.spinBox_time_interval.setDisabled)
        self.radioButton_time_intervals.clicked["bool"].connect(self.timeEdit_total_duration.setDisabled)
        self.radioButton_time_intervals.clicked["bool"].connect(self.spinBox_time_interval.setEnabled)
        self.radioButton_total_duration.clicked["bool"].connect(self.timeEdit_total_duration.setEnabled)
        self.spinBox_scanner_position.valueChanged.connect(self.slider_scanner_position.setValue)
        self.spinBox_min_grayscale.valueChanged.connect(self.slider_min_grayscale.setValue)
        self.spinBox_max_grayscale.valueChanged.connect(self.slider_max_grayscale.setValue)
        self.slider_min_grayscale.valueChanged.connect(self.spinBox_min_grayscale.setValue)
        self.slider_max_grayscale.sliderMoved.connect(self.spinBox_max_grayscale.setValue)

        self.comboBox_setup.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_SaveConfig.setText(QCoreApplication.translate("MainWindow", u"Save Config", None))
        self.action_LoadConfig.setText(QCoreApplication.translate("MainWindow", u"Load Config", None))
        self.action_DAQ.setText(QCoreApplication.translate("MainWindow", u"DAQ", None))
        self.action_Lasers.setText(QCoreApplication.translate("MainWindow", u"Lasers", None))
        self.action_Camera.setText(QCoreApplication.translate("MainWindow", u"Camera", None))
        self.actionData_path.setText(QCoreApplication.translate("MainWindow", u"Data path", None))
        self.actionExperience_Name.setText(QCoreApplication.translate("MainWindow", u"Experience Name", None))
        self.label_saving.setText(QCoreApplication.translate("MainWindow", u"Saving", None))
        self.label_data_path.setText(QCoreApplication.translate("MainWindow", u"D:/Projets_Python/OPM_GUI/Images", None))
        self.pb_data_path.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.lineEdit_exp_name.setText(QCoreApplication.translate("MainWindow", u"Image", None))
        self.comboBox_setup.setItemText(0, QCoreApplication.translate("MainWindow", u"Armin", None))
        self.comboBox_setup.setItemText(1, QCoreApplication.translate("MainWindow", u"Thibault", None))

#if QT_CONFIG(tooltip)
        self.comboBox_setup.setToolTip(QCoreApplication.translate("MainWindow", u"Select the experimental setup to use: Armin's or Thibault's configuration.\n"
"This choice affects hardware settings and acquisition parameters.", None))
#endif // QT_CONFIG(tooltip)
        self.comboBox_setup.setCurrentText(QCoreApplication.translate("MainWindow", u"Thibault", None))
        self.label_setup.setText(QCoreApplication.translate("MainWindow", u"Setup", None))
        self.label_camera_settings.setText(QCoreApplication.translate("MainWindow", u"Camera Settings", None))
        self.comboBox_camera.setItemText(0, QCoreApplication.translate("MainWindow", u"Camera 1", None))

#if QT_CONFIG(tooltip)
        self.comboBox_camera.setToolTip(QCoreApplication.translate("MainWindow", u"Select the camera for which the settings below will be applied", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_hsize.setToolTip(QCoreApplication.translate("MainWindow", u"Set the number of pixels along the horizontal axis of the camera sensor.", None))
#endif // QT_CONFIG(tooltip)
        self.label_hsize.setText(QCoreApplication.translate("MainWindow", u"Pixels horizontal   ", None))
#if QT_CONFIG(tooltip)
        self.spinBox_hpos.setToolTip(QCoreApplication.translate("MainWindow", u"Adjust the horizontal position of the field of view on the camera sensor.", None))
#endif // QT_CONFIG(tooltip)
        self.label_hpos.setText(QCoreApplication.translate("MainWindow", u"Position horizontal", None))
#if QT_CONFIG(tooltip)
        self.spinBox_vsize.setToolTip(QCoreApplication.translate("MainWindow", u"Set the number of pixels along the vertical axis of the camera sensor.", None))
#endif // QT_CONFIG(tooltip)
        self.label_vsize.setText(QCoreApplication.translate("MainWindow", u"Pixels vertical       ", None))
#if QT_CONFIG(tooltip)
        self.spinBox_vpos.setToolTip(QCoreApplication.translate("MainWindow", u"Adjust the vertical position of the field of view on the camera sensor.", None))
#endif // QT_CONFIG(tooltip)
        self.label_vpos.setText(QCoreApplication.translate("MainWindow", u"Position vertical    ", None))
        self.comboBox_size_preset.setItemText(0, QCoreApplication.translate("MainWindow", u"Preset size", None))
        self.comboBox_size_preset.setItemText(1, QCoreApplication.translate("MainWindow", u"44032 x 2368", None))
        self.comboBox_size_preset.setItemText(2, QCoreApplication.translate("MainWindow", u"2048 x 2048", None))

#if QT_CONFIG(tooltip)
        self.comboBox_size_preset.setToolTip(QCoreApplication.translate("MainWindow", u"Set size of the FOV to preset values", None))
#endif // QT_CONFIG(tooltip)
        self.pb_center_FOV.setText(QCoreApplication.translate("MainWindow", u"Center FOV", None))
#if QT_CONFIG(tooltip)
        self.label_fov_size.setToolTip(QCoreApplication.translate("MainWindow", u"Display the size of the field of view in \u00b5m", None))
#endif // QT_CONFIG(tooltip)
        self.label_fov_size.setText(QCoreApplication.translate("MainWindow", u"Field of view : \u00b5m", None))
        self.comboBox_binning.setItemText(0, QCoreApplication.translate("MainWindow", u"1", None))
        self.comboBox_binning.setItemText(1, QCoreApplication.translate("MainWindow", u"2", None))
        self.comboBox_binning.setItemText(2, QCoreApplication.translate("MainWindow", u"4", None))

#if QT_CONFIG(tooltip)
        self.comboBox_binning.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Adjust the binning on the camera sensor. <span style=\" font-weight:600;\">NOTE:</span> the pixels and position, horizontal and vertical, doesn't take in account the binning</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("MainWindow", u"Binning", None))
        self.label_channels_settings.setText(QCoreApplication.translate("MainWindow", u"Channels Settings", None))
        self.lineEdit_channel_name.setText("")
        self.comboBox_channel_name.setItemText(0, QCoreApplication.translate("MainWindow", u"BFP", None))
        self.comboBox_channel_name.setItemText(1, QCoreApplication.translate("MainWindow", u"GFP", None))
        self.comboBox_channel_name.setItemText(2, QCoreApplication.translate("MainWindow", u"CY3.5", None))
        self.comboBox_channel_name.setItemText(3, QCoreApplication.translate("MainWindow", u"TexRed", None))

        self.pb_channel_save.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.pb_channel_add.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.pb_channel_remove.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
#if QT_CONFIG(tooltip)
        self.checkBox_laser_405.setToolTip(QCoreApplication.translate("MainWindow", u"Enable or disable the 405 nm channel for acquisition (Snoutscope protocol).", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_laser_405.setText("")
#if QT_CONFIG(tooltip)
        self.checkBox_laser_488.setToolTip(QCoreApplication.translate("MainWindow", u"Enable or disable the 488 nm channel for acquisition (Snoutscope protocol).", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_laser_488.setText("")
#if QT_CONFIG(tooltip)
        self.checkBox_laser_561.setToolTip(QCoreApplication.translate("MainWindow", u"Enable or disable the 561 nm channel for acquisition (Snoutscope protocol).", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_laser_561.setText("")
#if QT_CONFIG(tooltip)
        self.checkBox_laser_640.setToolTip(QCoreApplication.translate("MainWindow", u"Enable or disable the 640 nm channel for acquisition (Snoutscope protocol).", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_laser_640.setText("")
        self.label_laser_power.setText(QCoreApplication.translate("MainWindow", u"Laser Power (%)", None))
#if QT_CONFIG(tooltip)
        self.spinBox_laser_405.setToolTip(QCoreApplication.translate("MainWindow", u"Set the laser power for the 405 nm channel as a percentage of its maximum output.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_laser_488.setToolTip(QCoreApplication.translate("MainWindow", u"Set the laser power for the 488 nm channel as a percentage of its maximum output.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_laser_561.setToolTip(QCoreApplication.translate("MainWindow", u"Set the laser power for the 561 nm channel as a percentage of its maximum output.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_laser_640.setToolTip(QCoreApplication.translate("MainWindow", u"Set the laser power for the 640 nm channel as a percentage of its maximum output.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.slider_laser_405.setToolTip(QCoreApplication.translate("MainWindow", u"Set the laser power for the 405 nm channel as a percentage of its maximum output.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.slider_laser_488.setToolTip(QCoreApplication.translate("MainWindow", u"Set the laser power for the 488 nm channel as a percentage of its maximum output.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.slider_laser_561.setToolTip(QCoreApplication.translate("MainWindow", u"Set the laser power for the 561 nm channel as a percentage of its maximum output.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.slider_laser_640.setToolTip(QCoreApplication.translate("MainWindow", u"Set the laser power for the 640 nm channel as a percentage of its maximum output.", None))
#endif // QT_CONFIG(tooltip)
        self.label_channel_filter.setText(QCoreApplication.translate("MainWindow", u"Filter", None))
        self.comboBox_channel_filter.setItemText(0, QCoreApplication.translate("MainWindow", u"BFP", None))
        self.comboBox_channel_filter.setItemText(1, QCoreApplication.translate("MainWindow", u"GFP", None))
        self.comboBox_channel_filter.setItemText(2, QCoreApplication.translate("MainWindow", u"CY3.5", None))
        self.comboBox_channel_filter.setItemText(3, QCoreApplication.translate("MainWindow", u"TexRed", None))

        self.comboBox_channel_camera.setItemText(0, QCoreApplication.translate("MainWindow", u"Camera 1", None))

#if QT_CONFIG(tooltip)
        self.comboBox_channel_camera.setToolTip(QCoreApplication.translate("MainWindow", u"Select the camera to be used for the 405 nm channel.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_channel_exposure_time.setToolTip(QCoreApplication.translate("MainWindow", u"Set the exposure time for the 405 nm channel in milliseconds.", None))
#endif // QT_CONFIG(tooltip)
        self.label_channel_exposure_time.setText(QCoreApplication.translate("MainWindow", u"Exposure Time (ms)", None))
        self.label_timelaps_settings.setText(QCoreApplication.translate("MainWindow", u"Timelaps Settings", None))
#if QT_CONFIG(tooltip)
        self.spinBox_timepoints.setToolTip(QCoreApplication.translate("MainWindow", u"Set the number of timepoints in the timelapse experiment.\n"
"This value is linked to the total duration and interval.", None))
#endif // QT_CONFIG(tooltip)
        self.label_timepoints.setText(QCoreApplication.translate("MainWindow", u"Timepoints", None))
        self.radioButton_time_intervals.setText("")
#if QT_CONFIG(tooltip)
        self.spinBox_time_interval.setToolTip(QCoreApplication.translate("MainWindow", u"Set the time interval between two consecutive timepoints.\n"
"This value is linked to the total duration.", None))
#endif // QT_CONFIG(tooltip)
        self.label_time_interval.setText(QCoreApplication.translate("MainWindow", u"Time interval (s)", None))
        self.radioButton_total_duration.setText("")
        self.timeEdit_total_duration.setDisplayFormat(QCoreApplication.translate("MainWindow", u"HH:mm:ss.zzz", None))
        self.label_total_duration.setText(QCoreApplication.translate("MainWindow", u"Total duration", None))
        self.label_scanner_settings.setText(QCoreApplication.translate("MainWindow", u"Scanner Settings", None))
#if QT_CONFIG(tooltip)
        self.slider_scanner_position.setToolTip(QCoreApplication.translate("MainWindow", u"Adjust the scanner position.\n"
"Just for preview.", None))
#endif // QT_CONFIG(tooltip)
        self.label_scanner_position.setText(QCoreApplication.translate("MainWindow", u"Scanner\n"
"Position (\u00b5m)", None))
#if QT_CONFIG(tooltip)
        self.spinBox_scanner_position.setToolTip(QCoreApplication.translate("MainWindow", u"Adjust the scanner position.\n"
"Just for preview.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pb_scanner_center.setToolTip(QCoreApplication.translate("MainWindow", u"Center the scanner position (set to 0).", None))
#endif // QT_CONFIG(tooltip)
        self.pb_scanner_center.setText(QCoreApplication.translate("MainWindow", u"Center", None))
        self.label_scan_range.setText(QCoreApplication.translate("MainWindow", u"Scan Range (\u00b5m)", None))
#if QT_CONFIG(tooltip)
        self.spinBox_scan_range.setToolTip(QCoreApplication.translate("MainWindow", u"Set the scan range around the center (0 \u00b5m).\n"
"This defines the maximum displacement during scanning.", None))
#endif // QT_CONFIG(tooltip)
        self.label_channels.setText(QCoreApplication.translate("MainWindow", u"Channels", None))
        self.label_number_channels.setText(QCoreApplication.translate("MainWindow", u"Number of channels", None))
        self.groupBox_channel_order.setTitle(QCoreApplication.translate("MainWindow", u"Channels orders", None))
        self.label_volume_duration.setText(QCoreApplication.translate("MainWindow", u"Frame thickness \u00b5m\n"
"Number of frames/volumes\n"
"Estimated volume duration: 0.000 s", None))
        self.label_image_preview.setText("")
        self.checkBox_show_saturation.setText(QCoreApplication.translate("MainWindow", u"Show saturation", None))
        self.comboBox_preview_zoom.setItemText(0, QCoreApplication.translate("MainWindow", u"Image zoom", None))
        self.comboBox_preview_zoom.setItemText(1, QCoreApplication.translate("MainWindow", u"2x", None))
        self.comboBox_preview_zoom.setItemText(2, QCoreApplication.translate("MainWindow", u"1x", None))
        self.comboBox_preview_zoom.setItemText(3, QCoreApplication.translate("MainWindow", u"1/2x", None))
        self.comboBox_preview_zoom.setItemText(4, QCoreApplication.translate("MainWindow", u"1/3x", None))
        self.comboBox_preview_zoom.setItemText(5, QCoreApplication.translate("MainWindow", u"1/4x", None))

#if QT_CONFIG(tooltip)
        self.slider_min_grayscale.setToolTip(QCoreApplication.translate("MainWindow", u"Set the minimum grey value for image display.\n"
"Pixels below this value will appear black.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_min_grayscale.setToolTip(QCoreApplication.translate("MainWindow", u"Set the minimum grey value for image display.\n"
"Pixels below this value will appear black.", None))
#endif // QT_CONFIG(tooltip)
        self.label_min_grayscale.setText(QCoreApplication.translate("MainWindow", u"Min", None))
#if QT_CONFIG(tooltip)
        self.slider_max_grayscale.setToolTip(QCoreApplication.translate("MainWindow", u"Set the maximum grey value for image display.\n"
"Pixels above this value will appear white.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_max_grayscale.setToolTip(QCoreApplication.translate("MainWindow", u"Set the maximum grey value for image display.\n"
"Pixels above this value will appear white.", None))
#endif // QT_CONFIG(tooltip)
        self.label_max_grayscale.setText(QCoreApplication.translate("MainWindow", u"Max", None))
#if QT_CONFIG(tooltip)
        self.pb_auto_grayscale.setToolTip(QCoreApplication.translate("MainWindow", u"Automatically adjust the minimum and maximum grey values based on the image histogram.", None))
#endif // QT_CONFIG(tooltip)
        self.pb_auto_grayscale.setText(QCoreApplication.translate("MainWindow", u"Auto", None))
#if QT_CONFIG(tooltip)
        self.pb_reset_grayscale.setToolTip(QCoreApplication.translate("MainWindow", u"Reset the minimum and maximum grey values to their default settings.", None))
#endif // QT_CONFIG(tooltip)
        self.pb_reset_grayscale.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
#if QT_CONFIG(tooltip)
        self.pb_preview.setToolTip(QCoreApplication.translate("MainWindow", u"Start the live preview of the acquisition.", None))
#endif // QT_CONFIG(tooltip)
        self.pb_preview.setText(QCoreApplication.translate("MainWindow", u"Preview", None))
#if QT_CONFIG(tooltip)
        self.pb_pause_preview.setToolTip(QCoreApplication.translate("MainWindow", u"Start the live preview of the acquisition.", None))
#endif // QT_CONFIG(tooltip)
        self.pb_pause_preview.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
#if QT_CONFIG(tooltip)
        self.pb_stop_preview.setToolTip(QCoreApplication.translate("MainWindow", u"Start the live preview of the acquisition.", None))
#endif // QT_CONFIG(tooltip)
        self.pb_stop_preview.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
#if QT_CONFIG(tooltip)
        self.pb_snap.setToolTip(QCoreApplication.translate("MainWindow", u"Start the live preview of the acquisition.", None))
#endif // QT_CONFIG(tooltip)
        self.pb_snap.setText(QCoreApplication.translate("MainWindow", u"Snap", None))
        self.label_histogram_greyvalue.setText("")
#if QT_CONFIG(tooltip)
        self.pb_snoutscope_acquisition.setToolTip(QCoreApplication.translate("MainWindow", u"Start image acquisition using the Snoutscope program.", None))
#endif // QT_CONFIG(tooltip)
        self.pb_snoutscope_acquisition.setText(QCoreApplication.translate("MainWindow", u"Snoutscope\n"
"Acquisition", None))
#if QT_CONFIG(tooltip)
        self.pb_multidimensional_acquisition.setToolTip(QCoreApplication.translate("MainWindow", u"Start a multidimensional acquisition, including multiple channels, positions, or timepoints.", None))
#endif // QT_CONFIG(tooltip)
        self.pb_multidimensional_acquisition.setText(QCoreApplication.translate("MainWindow", u"Multidimensional\n"
"Acquisition", None))
        self.menuFichier.setTitle(QCoreApplication.translate("MainWindow", u"Fichier", None))
        self.menuSaving.setTitle(QCoreApplication.translate("MainWindow", u"Saving", None))
        self.menuConfig.setTitle(QCoreApplication.translate("MainWindow", u"Config", None))
    # retranslateUi

