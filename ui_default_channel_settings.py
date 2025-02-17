# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_default_channel_settings.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QHBoxLayout, QLCDNumber, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSlider, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(511, 780)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.lineEdit_channel_name = QLineEdit(Form)
        self.lineEdit_channel_name.setObjectName(u"lineEdit_channel_name")
        self.lineEdit_channel_name.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_12.addWidget(self.lineEdit_channel_name)

        self.comboBox_channel_name = QComboBox(Form)
        self.comboBox_channel_name.addItem("")
        self.comboBox_channel_name.addItem("")
        self.comboBox_channel_name.addItem("")
        self.comboBox_channel_name.addItem("")
        self.comboBox_channel_name.setObjectName(u"comboBox_channel_name")

        self.horizontalLayout_12.addWidget(self.comboBox_channel_name)

        self.pb_channel_save = QPushButton(Form)
        self.pb_channel_save.setObjectName(u"pb_channel_save")
        self.pb_channel_save.setEnabled(True)

        self.horizontalLayout_12.addWidget(self.pb_channel_save)

        self.pb_channel_add = QPushButton(Form)
        self.pb_channel_add.setObjectName(u"pb_channel_add")

        self.horizontalLayout_12.addWidget(self.pb_channel_add)

        self.pb_channel_remove = QPushButton(Form)
        self.pb_channel_remove.setObjectName(u"pb_channel_remove")
        self.pb_channel_remove.setEnabled(True)

        self.horizontalLayout_12.addWidget(self.pb_channel_remove)


        self.verticalLayout.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.lcdNumber_laser_405 = QLCDNumber(Form)
        self.lcdNumber_laser_405.setObjectName(u"lcdNumber_laser_405")
        palette = QPalette()
        brush = QBrush(QColor(226, 137, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Light, brush)
        brush1 = QBrush(QColor(255, 255, 255, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Base, brush1)
        brush2 = QBrush(QColor(0, 0, 0, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.Light, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Light, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.lcdNumber_laser_405.setPalette(palette)
        self.lcdNumber_laser_405.setAutoFillBackground(True)
        self.lcdNumber_laser_405.setSmallDecimalPoint(False)
        self.lcdNumber_laser_405.setProperty(u"value", 405.000000000000000)

        self.horizontalLayout_17.addWidget(self.lcdNumber_laser_405)

        self.lcdNumber_laser_488 = QLCDNumber(Form)
        self.lcdNumber_laser_488.setObjectName(u"lcdNumber_laser_488")
        palette1 = QPalette()
        brush3 = QBrush(QColor(85, 255, 255, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.Light, brush3)
        palette1.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette1.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette1.setBrush(QPalette.Inactive, QPalette.Light, brush3)
        palette1.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette1.setBrush(QPalette.Disabled, QPalette.Light, brush3)
        palette1.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette1.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.lcdNumber_laser_488.setPalette(palette1)
        self.lcdNumber_laser_488.setAutoFillBackground(True)
        self.lcdNumber_laser_488.setSmallDecimalPoint(False)
        self.lcdNumber_laser_488.setProperty(u"value", 488.000000000000000)

        self.horizontalLayout_17.addWidget(self.lcdNumber_laser_488)

        self.lcdNumber_laser_561 = QLCDNumber(Form)
        self.lcdNumber_laser_561.setObjectName(u"lcdNumber_laser_561")
        palette2 = QPalette()
        brush4 = QBrush(QColor(255, 255, 127, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette2.setBrush(QPalette.Active, QPalette.Light, brush4)
        palette2.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette2.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette2.setBrush(QPalette.Inactive, QPalette.Light, brush4)
        palette2.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette2.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette2.setBrush(QPalette.Disabled, QPalette.Light, brush4)
        palette2.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette2.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.lcdNumber_laser_561.setPalette(palette2)
        self.lcdNumber_laser_561.setAutoFillBackground(True)
        self.lcdNumber_laser_561.setSmallDecimalPoint(False)
        self.lcdNumber_laser_561.setProperty(u"value", 561.000000000000000)

        self.horizontalLayout_17.addWidget(self.lcdNumber_laser_561)

        self.lcdNumber_laser_640 = QLCDNumber(Form)
        self.lcdNumber_laser_640.setObjectName(u"lcdNumber_laser_640")
        palette3 = QPalette()
        brush5 = QBrush(QColor(255, 0, 0, 255))
        brush5.setStyle(Qt.SolidPattern)
        palette3.setBrush(QPalette.Active, QPalette.Light, brush5)
        palette3.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette3.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette3.setBrush(QPalette.Inactive, QPalette.Light, brush5)
        palette3.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette3.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette3.setBrush(QPalette.Disabled, QPalette.Light, brush5)
        palette3.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette3.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.lcdNumber_laser_640.setPalette(palette3)
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

        self.checkBox_laser_405 = QCheckBox(Form)
        self.checkBox_laser_405.setObjectName(u"checkBox_laser_405")

        self.horizontalLayout_6.addWidget(self.checkBox_laser_405)

        self.horizontalSpacer_2 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)


        self.horizontalLayout_19.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalSpacer_6 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_6)

        self.checkBox_laser_488 = QCheckBox(Form)
        self.checkBox_laser_488.setObjectName(u"checkBox_laser_488")

        self.horizontalLayout_9.addWidget(self.checkBox_laser_488)

        self.horizontalSpacer_3 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_3)


        self.horizontalLayout_19.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalSpacer_7 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_7)

        self.checkBox_laser_561 = QCheckBox(Form)
        self.checkBox_laser_561.setObjectName(u"checkBox_laser_561")

        self.horizontalLayout_10.addWidget(self.checkBox_laser_561)

        self.horizontalSpacer_4 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_4)


        self.horizontalLayout_19.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalSpacer_8 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_8)

        self.checkBox_laser_640 = QCheckBox(Form)
        self.checkBox_laser_640.setObjectName(u"checkBox_laser_640")

        self.horizontalLayout_11.addWidget(self.checkBox_laser_640)

        self.horizontalSpacer_5 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_5)


        self.horizontalLayout_19.addLayout(self.horizontalLayout_11)


        self.verticalLayout.addLayout(self.horizontalLayout_19)

        self.label_laser_power = QLabel(Form)
        self.label_laser_power.setObjectName(u"label_laser_power")
        self.label_laser_power.setAutoFillBackground(False)
        self.label_laser_power.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_laser_power)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.spinBox_laser_405 = QSpinBox(Form)
        self.spinBox_laser_405.setObjectName(u"spinBox_laser_405")
        self.spinBox_laser_405.setMaximum(100)

        self.horizontalLayout_13.addWidget(self.spinBox_laser_405)

        self.spinBox_laser_488 = QSpinBox(Form)
        self.spinBox_laser_488.setObjectName(u"spinBox_laser_488")
        self.spinBox_laser_488.setMaximum(100)

        self.horizontalLayout_13.addWidget(self.spinBox_laser_488)

        self.spinBox_laser_561 = QSpinBox(Form)
        self.spinBox_laser_561.setObjectName(u"spinBox_laser_561")
        self.spinBox_laser_561.setMaximum(100)

        self.horizontalLayout_13.addWidget(self.spinBox_laser_561)

        self.spinBox_laser_640 = QSpinBox(Form)
        self.spinBox_laser_640.setObjectName(u"spinBox_laser_640")
        self.spinBox_laser_640.setMaximum(100)

        self.horizontalLayout_13.addWidget(self.spinBox_laser_640)


        self.verticalLayout.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.slider_laser_405 = QSlider(Form)
        self.slider_laser_405.setObjectName(u"slider_laser_405")
        self.slider_laser_405.setMaximumSize(QSize(16777215, 16777215))
        self.slider_laser_405.setMaximum(100)
        self.slider_laser_405.setOrientation(Qt.Vertical)

        self.horizontalLayout_14.addWidget(self.slider_laser_405)

        self.slider_laser_488 = QSlider(Form)
        self.slider_laser_488.setObjectName(u"slider_laser_488")
        self.slider_laser_488.setMaximumSize(QSize(16777215, 16777215))
        self.slider_laser_488.setMaximum(100)
        self.slider_laser_488.setOrientation(Qt.Vertical)

        self.horizontalLayout_14.addWidget(self.slider_laser_488)

        self.slider_laser_561 = QSlider(Form)
        self.slider_laser_561.setObjectName(u"slider_laser_561")
        self.slider_laser_561.setMaximumSize(QSize(16777215, 16777215))
        self.slider_laser_561.setMaximum(100)
        self.slider_laser_561.setOrientation(Qt.Vertical)

        self.horizontalLayout_14.addWidget(self.slider_laser_561)

        self.slider_laser_640 = QSlider(Form)
        self.slider_laser_640.setObjectName(u"slider_laser_640")
        self.slider_laser_640.setMaximumSize(QSize(16777215, 16777215))
        self.slider_laser_640.setMaximum(100)
        self.slider_laser_640.setOrientation(Qt.Vertical)

        self.horizontalLayout_14.addWidget(self.slider_laser_640)


        self.verticalLayout.addLayout(self.horizontalLayout_14)

        self.label_channel_filter = QLabel(Form)
        self.label_channel_filter.setObjectName(u"label_channel_filter")
        self.label_channel_filter.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_channel_filter)

        self.comboBox_channel_filter = QComboBox(Form)
        self.comboBox_channel_filter.addItem("")
        self.comboBox_channel_filter.addItem("")
        self.comboBox_channel_filter.addItem("")
        self.comboBox_channel_filter.addItem("")
        self.comboBox_channel_filter.setObjectName(u"comboBox_channel_filter")

        self.verticalLayout.addWidget(self.comboBox_channel_filter)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.comboBox_channel_camera = QComboBox(Form)
        self.comboBox_channel_camera.addItem("")
        self.comboBox_channel_camera.setObjectName(u"comboBox_channel_camera")
        self.comboBox_channel_camera.setEnabled(False)
        self.comboBox_channel_camera.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_15.addWidget(self.comboBox_channel_camera)

        self.spinBox_channel_exposure_time = QDoubleSpinBox(Form)
        self.spinBox_channel_exposure_time.setObjectName(u"spinBox_channel_exposure_time")
        self.spinBox_channel_exposure_time.setDecimals(2)
        self.spinBox_channel_exposure_time.setMinimum(8.699999999999999)
        self.spinBox_channel_exposure_time.setMaximum(999.990000000000009)
        self.spinBox_channel_exposure_time.setValue(8.699999999999999)

        self.horizontalLayout_15.addWidget(self.spinBox_channel_exposure_time)

        self.label_channel_exposure_time = QLabel(Form)
        self.label_channel_exposure_time.setObjectName(u"label_channel_exposure_time")
        self.label_channel_exposure_time.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_15.addWidget(self.label_channel_exposure_time)


        self.verticalLayout.addLayout(self.horizontalLayout_15)

        self.label_status = QLabel(Form)
        self.label_status.setObjectName(u"label_status")
        self.label_status.setAutoFillBackground(True)

        self.verticalLayout.addWidget(self.label_status)


        self.retranslateUi(Form)
        self.spinBox_laser_405.valueChanged.connect(self.slider_laser_405.setValue)
        self.spinBox_laser_488.valueChanged.connect(self.slider_laser_488.setValue)
        self.spinBox_laser_561.valueChanged.connect(self.slider_laser_561.setValue)
        self.spinBox_laser_640.valueChanged.connect(self.slider_laser_640.setValue)
        self.slider_laser_405.valueChanged.connect(self.spinBox_laser_405.setValue)
        self.slider_laser_488.valueChanged.connect(self.spinBox_laser_488.setValue)
        self.slider_laser_561.valueChanged.connect(self.spinBox_laser_561.setValue)
        self.slider_laser_640.valueChanged.connect(self.spinBox_laser_640.setValue)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lineEdit_channel_name.setText("")
        self.comboBox_channel_name.setItemText(0, QCoreApplication.translate("Form", u"BFP", None))
        self.comboBox_channel_name.setItemText(1, QCoreApplication.translate("Form", u"GFP", None))
        self.comboBox_channel_name.setItemText(2, QCoreApplication.translate("Form", u"CY3.5", None))
        self.comboBox_channel_name.setItemText(3, QCoreApplication.translate("Form", u"TexRed", None))

        self.pb_channel_save.setText(QCoreApplication.translate("Form", u"Save", None))
        self.pb_channel_add.setText(QCoreApplication.translate("Form", u"Add", None))
        self.pb_channel_remove.setText(QCoreApplication.translate("Form", u"Remove", None))
#if QT_CONFIG(tooltip)
        self.checkBox_laser_405.setToolTip(QCoreApplication.translate("Form", u"Enable or disable the 405 nm channel for acquisition (Snoutscope protocol).", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_laser_405.setText("")
#if QT_CONFIG(tooltip)
        self.checkBox_laser_488.setToolTip(QCoreApplication.translate("Form", u"Enable or disable the 488 nm channel for acquisition (Snoutscope protocol).", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_laser_488.setText("")
#if QT_CONFIG(tooltip)
        self.checkBox_laser_561.setToolTip(QCoreApplication.translate("Form", u"Enable or disable the 561 nm channel for acquisition (Snoutscope protocol).", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_laser_561.setText("")
#if QT_CONFIG(tooltip)
        self.checkBox_laser_640.setToolTip(QCoreApplication.translate("Form", u"Enable or disable the 640 nm channel for acquisition (Snoutscope protocol).", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_laser_640.setText("")
        self.label_laser_power.setText(QCoreApplication.translate("Form", u"Laser Power (%)", None))
#if QT_CONFIG(tooltip)
        self.spinBox_laser_405.setToolTip(QCoreApplication.translate("Form", u"Set the laser power for the 405 nm channel as a percentage of its maximum output.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_laser_488.setToolTip(QCoreApplication.translate("Form", u"Set the laser power for the 488 nm channel as a percentage of its maximum output.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_laser_561.setToolTip(QCoreApplication.translate("Form", u"Set the laser power for the 561 nm channel as a percentage of its maximum output.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_laser_640.setToolTip(QCoreApplication.translate("Form", u"Set the laser power for the 640 nm channel as a percentage of its maximum output.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.slider_laser_405.setToolTip(QCoreApplication.translate("Form", u"Set the laser power for the 405 nm channel as a percentage of its maximum output.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.slider_laser_488.setToolTip(QCoreApplication.translate("Form", u"Set the laser power for the 488 nm channel as a percentage of its maximum output.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.slider_laser_561.setToolTip(QCoreApplication.translate("Form", u"Set the laser power for the 561 nm channel as a percentage of its maximum output.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.slider_laser_640.setToolTip(QCoreApplication.translate("Form", u"Set the laser power for the 640 nm channel as a percentage of its maximum output.", None))
#endif // QT_CONFIG(tooltip)
        self.label_channel_filter.setText(QCoreApplication.translate("Form", u"Filter", None))
        self.comboBox_channel_filter.setItemText(0, QCoreApplication.translate("Form", u"BFP", None))
        self.comboBox_channel_filter.setItemText(1, QCoreApplication.translate("Form", u"GFP", None))
        self.comboBox_channel_filter.setItemText(2, QCoreApplication.translate("Form", u"CY3.5", None))
        self.comboBox_channel_filter.setItemText(3, QCoreApplication.translate("Form", u"TexRed", None))

        self.comboBox_channel_camera.setItemText(0, QCoreApplication.translate("Form", u"Camera 1", None))

#if QT_CONFIG(tooltip)
        self.comboBox_channel_camera.setToolTip(QCoreApplication.translate("Form", u"Select the camera to be used for the 405 nm channel.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_channel_exposure_time.setToolTip(QCoreApplication.translate("Form", u"Set the exposure time for the 405 nm channel in milliseconds.", None))
#endif // QT_CONFIG(tooltip)
        self.label_channel_exposure_time.setText(QCoreApplication.translate("Form", u"Exposure Time (ms)", None))
        self.label_status.setText("")
    # retranslateUi

