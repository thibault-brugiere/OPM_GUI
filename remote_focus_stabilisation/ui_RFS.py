# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_RFS.ui'
##
## Created by: Qt User Interface Compiler version 6.9.3
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLCDNumber,
    QLabel, QPushButton, QSizePolicy, QSlider,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1085, 924)
        self.horizontalLayout_13 = QHBoxLayout(Form)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.pb_laser_on = QPushButton(Form)
        self.pb_laser_on.setObjectName(u"pb_laser_on")
        self.pb_laser_on.setCheckable(True)

        self.horizontalLayout_6.addWidget(self.pb_laser_on)

        self.label_laser_icon = QLabel(Form)
        self.label_laser_icon.setObjectName(u"label_laser_icon")
        self.label_laser_icon.setMinimumSize(QSize(32, 32))
        self.label_laser_icon.setMaximumSize(QSize(32, 32))

        self.horizontalLayout_6.addWidget(self.label_laser_icon)

        self.label_laser = QLabel(Form)
        self.label_laser.setObjectName(u"label_laser")
        self.label_laser.setMinimumSize(QSize(30, 0))

        self.horizontalLayout_6.addWidget(self.label_laser)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)


        self.verticalLayout_5.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.pb_stabilize = QPushButton(Form)
        self.pb_stabilize.setObjectName(u"pb_stabilize")
        self.pb_stabilize.setCheckable(True)

        self.horizontalLayout_7.addWidget(self.pb_stabilize)

        self.label_stabilize_icon = QLabel(Form)
        self.label_stabilize_icon.setObjectName(u"label_stabilize_icon")
        self.label_stabilize_icon.setMinimumSize(QSize(32, 32))
        self.label_stabilize_icon.setMaximumSize(QSize(32, 32))

        self.horizontalLayout_7.addWidget(self.label_stabilize_icon)

        self.label_stabilize = QLabel(Form)
        self.label_stabilize.setObjectName(u"label_stabilize")
        self.label_stabilize.setMinimumSize(QSize(30, 0))

        self.horizontalLayout_7.addWidget(self.label_stabilize)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_3)


        self.verticalLayout_5.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_serial_port = QLabel(Form)
        self.label_serial_port.setObjectName(u"label_serial_port")

        self.horizontalLayout_8.addWidget(self.label_serial_port)

        self.comboBox_devices = QComboBox(Form)
        self.comboBox_devices.setObjectName(u"comboBox_devices")

        self.horizontalLayout_8.addWidget(self.comboBox_devices)

        self.label_connection = QLabel(Form)
        self.label_connection.setObjectName(u"label_connection")
        self.label_connection.setMinimumSize(QSize(91, 18))

        self.horizontalLayout_8.addWidget(self.label_connection)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_4)


        self.verticalLayout_5.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_calibrate = QLabel(Form)
        self.label_calibrate.setObjectName(u"label_calibrate")

        self.horizontalLayout_12.addWidget(self.label_calibrate)

        self.pb_calibrate = QPushButton(Form)
        self.pb_calibrate.setObjectName(u"pb_calibrate")
        self.pb_calibrate.setCheckable(True)

        self.horizontalLayout_12.addWidget(self.pb_calibrate)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_9)


        self.verticalLayout_5.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_step_size = QLabel(Form)
        self.label_step_size.setObjectName(u"label_step_size")

        self.horizontalLayout_9.addWidget(self.label_step_size)

        self.slider_step_size = QSlider(Form)
        self.slider_step_size.setObjectName(u"slider_step_size")
        self.slider_step_size.setMinimumSize(QSize(120, 0))
        self.slider_step_size.setMinimum(1)
        self.slider_step_size.setMaximum(100)
        self.slider_step_size.setValue(100)
        self.slider_step_size.setOrientation(Qt.Horizontal)

        self.horizontalLayout_9.addWidget(self.slider_step_size)

        self.sb_step_size = QSpinBox(Form)
        self.sb_step_size.setObjectName(u"sb_step_size")
        self.sb_step_size.setMinimum(1)
        self.sb_step_size.setMaximum(100)
        self.sb_step_size.setValue(100)

        self.horizontalLayout_9.addWidget(self.sb_step_size)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_5)


        self.verticalLayout_5.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_6)

        self.pb_move_bw1 = QPushButton(Form)
        self.pb_move_bw1.setObjectName(u"pb_move_bw1")
        self.pb_move_bw1.setMinimumSize(QSize(32, 32))

        self.horizontalLayout_10.addWidget(self.pb_move_bw1)

        self.pb_move_fw1 = QPushButton(Form)
        self.pb_move_fw1.setObjectName(u"pb_move_fw1")
        self.pb_move_fw1.setMinimumSize(QSize(32, 32))

        self.horizontalLayout_10.addWidget(self.pb_move_fw1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_7)


        self.verticalLayout_5.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_position = QLabel(Form)
        self.label_position.setObjectName(u"label_position")
        self.label_position.setMinimumSize(QSize(61, 16))

        self.horizontalLayout_11.addWidget(self.label_position)

        self.lcdNumber_Position = QLCDNumber(Form)
        self.lcdNumber_Position.setObjectName(u"lcdNumber_Position")
        self.lcdNumber_Position.setMinimumSize(QSize(150, 23))
        palette = QPalette()
        brush = QBrush(QColor(255, 170, 0, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        brush1 = QBrush(QColor(255, 255, 255, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush1)
        brush2 = QBrush(QColor(255, 206, 57, 255))
        brush2.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Light, brush2)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Midlight, brush1)
        brush3 = QBrush(QColor(158, 105, 0, 255))
        brush3.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Dark, brush3)
        brush4 = QBrush(QColor(0, 0, 0, 255))
        brush4.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush4)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush4)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Light, brush2)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Midlight, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Dark, brush3)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush4)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush4)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush3)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Light, brush2)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Midlight, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Dark, brush3)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush3)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush3)
        self.lcdNumber_Position.setPalette(palette)

        self.horizontalLayout_11.addWidget(self.lcdNumber_Position)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_8)


        self.verticalLayout_5.addLayout(self.horizontalLayout_11)

        self.label_message = QLabel(Form)
        self.label_message.setObjectName(u"label_message")
        self.label_message.setMinimumSize(QSize(60, 120))

        self.verticalLayout_5.addWidget(self.label_message)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_3)


        self.horizontalLayout_13.addLayout(self.verticalLayout_5)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_image_preview = QLabel(Form)
        self.label_image_preview.setObjectName(u"label_image_preview")
        self.label_image_preview.setMinimumSize(QSize(720, 540))
        palette1 = QPalette()
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush1)
        brush5 = QBrush(QColor(153, 153, 153, 255))
        brush5.setStyle(Qt.BrushStyle.SolidPattern)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush5)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush1)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush5)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush5)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush5)
        self.label_image_preview.setPalette(palette1)
        self.label_image_preview.setAutoFillBackground(True)

        self.verticalLayout_4.addWidget(self.label_image_preview)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.cb_LUT = QComboBox(Form)
        self.cb_LUT.addItem("")
        self.cb_LUT.setObjectName(u"cb_LUT")

        self.horizontalLayout_3.addWidget(self.cb_LUT)

        self.cb_preview_zoom = QComboBox(Form)
        self.cb_preview_zoom.addItem("")
        self.cb_preview_zoom.addItem("")
        self.cb_preview_zoom.addItem("")
        self.cb_preview_zoom.addItem("")
        self.cb_preview_zoom.addItem("")
        self.cb_preview_zoom.addItem("")
        self.cb_preview_zoom.setObjectName(u"cb_preview_zoom")

        self.horizontalLayout_3.addWidget(self.cb_preview_zoom)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.slider_min_grayscale = QSlider(Form)
        self.slider_min_grayscale.setObjectName(u"slider_min_grayscale")
        self.slider_min_grayscale.setMaximum(1022)
        self.slider_min_grayscale.setOrientation(Qt.Horizontal)

        self.horizontalLayout.addWidget(self.slider_min_grayscale)

        self.sb_min_grayscale = QSpinBox(Form)
        self.sb_min_grayscale.setObjectName(u"sb_min_grayscale")
        self.sb_min_grayscale.setMaximum(1022)

        self.horizontalLayout.addWidget(self.sb_min_grayscale)

        self.label_min_grayscale = QLabel(Form)
        self.label_min_grayscale.setObjectName(u"label_min_grayscale")

        self.horizontalLayout.addWidget(self.label_min_grayscale)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.slider_max_grayscale = QSlider(Form)
        self.slider_max_grayscale.setObjectName(u"slider_max_grayscale")
        self.slider_max_grayscale.setMinimum(1)
        self.slider_max_grayscale.setMaximum(1023)
        self.slider_max_grayscale.setOrientation(Qt.Horizontal)

        self.horizontalLayout_2.addWidget(self.slider_max_grayscale)

        self.sb_max_grayscale = QSpinBox(Form)
        self.sb_max_grayscale.setObjectName(u"sb_max_grayscale")
        self.sb_max_grayscale.setMinimum(1)
        self.sb_max_grayscale.setMaximum(1023)
        self.sb_max_grayscale.setValue(1023)

        self.horizontalLayout_2.addWidget(self.sb_max_grayscale)

        self.label_max_grayscale = QLabel(Form)
        self.label_max_grayscale.setObjectName(u"label_max_grayscale")

        self.horizontalLayout_2.addWidget(self.label_max_grayscale)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout_4.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pb_minmax_grayscale = QPushButton(Form)
        self.pb_minmax_grayscale.setObjectName(u"pb_minmax_grayscale")

        self.verticalLayout.addWidget(self.pb_minmax_grayscale)

        self.pb_auto_grayscale = QPushButton(Form)
        self.pb_auto_grayscale.setObjectName(u"pb_auto_grayscale")

        self.verticalLayout.addWidget(self.pb_auto_grayscale)

        self.pb_reset_grayscale = QPushButton(Form)
        self.pb_reset_grayscale.setObjectName(u"pb_reset_grayscale")

        self.verticalLayout.addWidget(self.pb_reset_grayscale)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.horizontalLayout_4.addLayout(self.verticalLayout)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)


        self.horizontalLayout_5.addLayout(self.verticalLayout_3)

        self.label_histogram_greyvalue = QLabel(Form)
        self.label_histogram_greyvalue.setObjectName(u"label_histogram_greyvalue")
        self.label_histogram_greyvalue.setMinimumSize(QSize(400, 250))
        palette2 = QPalette()
        palette2.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush1)
        brush6 = QBrush(QColor(150, 150, 150, 255))
        brush6.setStyle(Qt.BrushStyle.SolidPattern)
        palette2.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush6)
        palette2.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush1)
        palette2.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush6)
        palette2.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush6)
        palette2.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush6)
        self.label_histogram_greyvalue.setPalette(palette2)
        self.label_histogram_greyvalue.setAutoFillBackground(True)

        self.horizontalLayout_5.addWidget(self.label_histogram_greyvalue)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.label_graph = QLabel(Form)
        self.label_graph.setObjectName(u"label_graph")
        self.label_graph.setMinimumSize(QSize(720, 100))
        palette3 = QPalette()
        palette3.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush1)
        palette3.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush5)
        palette3.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush1)
        palette3.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush5)
        palette3.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush5)
        palette3.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush5)
        self.label_graph.setPalette(palette3)
        self.label_graph.setAutoFillBackground(True)

        self.verticalLayout_4.addWidget(self.label_graph)


        self.horizontalLayout_13.addLayout(self.verticalLayout_4)


        self.retranslateUi(Form)
        self.sb_min_grayscale.valueChanged.connect(self.slider_min_grayscale.setValue)
        self.slider_min_grayscale.valueChanged.connect(self.sb_min_grayscale.setValue)
        self.sb_max_grayscale.valueChanged.connect(self.slider_max_grayscale.setValue)
        self.slider_max_grayscale.valueChanged.connect(self.sb_max_grayscale.setValue)
        self.slider_step_size.valueChanged.connect(self.sb_step_size.setValue)
        self.sb_step_size.valueChanged.connect(self.slider_step_size.setValue)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pb_laser_on.setText(QCoreApplication.translate("Form", u"Laser", None))
        self.label_laser_icon.setText("")
        self.label_laser.setText(QCoreApplication.translate("Form", u"OFF", None))
        self.pb_stabilize.setText(QCoreApplication.translate("Form", u"Stabilize", None))
        self.label_stabilize_icon.setText("")
        self.label_stabilize.setText(QCoreApplication.translate("Form", u"OFF", None))
        self.label_serial_port.setText(QCoreApplication.translate("Form", u"Serial Port", None))
#if QT_CONFIG(tooltip)
        self.comboBox_devices.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Select the serial port to which the piezo controller is connected.</p><p>Ensure the correct port is chosen for proper communication</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_connection.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Indicates whether the piezo controller is successfully connected via the selected port.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_connection.setText(QCoreApplication.translate("Form", u"Not Connected", None))
        self.label_calibrate.setText(QCoreApplication.translate("Form", u"Calibrate", None))
        self.pb_calibrate.setText(QCoreApplication.translate("Form", u"calibrate", None))
        self.label_step_size.setText(QCoreApplication.translate("Form", u"Step size (%)", None))
#if QT_CONFIG(tooltip)
        self.slider_step_size.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Set the step size for piezo movement as a percentage of the total range.</p><p>Adjust between 21% and 100% to control the increment of each movement command</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.sb_step_size.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Set the step size for piezo movement as a percentage of the total range.</p><p>Adjust between 21% and 100% to control the increment of each movement command</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pb_move_bw1.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Move the piezo 1 step backward.</p><p>Around 50nm to 250nm depending on step size</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_move_bw1.setText(QCoreApplication.translate("Form", u"<", None))
#if QT_CONFIG(tooltip)
        self.pb_move_fw1.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Move the piezo 1 step forward.</p><p>Around 50nm to 250nm depending on step size</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_move_fw1.setText(QCoreApplication.translate("Form", u">", None))
        self.label_position.setText(QCoreApplication.translate("Form", u"Position (\u00b5m)", None))
        self.label_message.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.label_image_preview.setText("")
        self.cb_LUT.setItemText(0, QCoreApplication.translate("Form", u"Grayscale", None))

        self.cb_preview_zoom.setItemText(0, QCoreApplication.translate("Form", u"Image Zoom", None))
        self.cb_preview_zoom.setItemText(1, QCoreApplication.translate("Form", u"50%", None))
        self.cb_preview_zoom.setItemText(2, QCoreApplication.translate("Form", u"100%", None))
        self.cb_preview_zoom.setItemText(3, QCoreApplication.translate("Form", u"200%", None))
        self.cb_preview_zoom.setItemText(4, QCoreApplication.translate("Form", u"300%", None))
        self.cb_preview_zoom.setItemText(5, QCoreApplication.translate("Form", u"400%", None))

        self.label_min_grayscale.setText(QCoreApplication.translate("Form", u"Min", None))
        self.label_max_grayscale.setText(QCoreApplication.translate("Form", u"Max", None))
#if QT_CONFIG(tooltip)
        self.pb_minmax_grayscale.setToolTip(QCoreApplication.translate("Form", u"Automatically adjust the minimum and maximum grey values based on the image histogram.", None))
#endif // QT_CONFIG(tooltip)
        self.pb_minmax_grayscale.setText(QCoreApplication.translate("Form", u"Min / Max", None))
#if QT_CONFIG(tooltip)
        self.pb_auto_grayscale.setToolTip(QCoreApplication.translate("Form", u"Automatically adjust the minimum and maximum grey values based on the image histogram.", None))
#endif // QT_CONFIG(tooltip)
        self.pb_auto_grayscale.setText(QCoreApplication.translate("Form", u"Auto", None))
#if QT_CONFIG(tooltip)
        self.pb_reset_grayscale.setToolTip(QCoreApplication.translate("Form", u"Reset the minimum and maximum grey values to their default settings.", None))
#endif // QT_CONFIG(tooltip)
        self.pb_reset_grayscale.setText(QCoreApplication.translate("Form", u"Reset", None))
        self.label_histogram_greyvalue.setText("")
        self.label_graph.setText("")
    # retranslateUi

