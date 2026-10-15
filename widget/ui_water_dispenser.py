# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_water_dispenser.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QHBoxLayout,
    QLCDNumber, QLabel, QPushButton, QSizePolicy,
    QSlider, QSpacerItem, QSpinBox, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(484, 441)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_serial_port = QLabel(Form)
        self.label_serial_port.setObjectName(u"label_serial_port")

        self.horizontalLayout.addWidget(self.label_serial_port)

        self.comboBox_devices = QComboBox(Form)
        self.comboBox_devices.setObjectName(u"comboBox_devices")

        self.horizontalLayout.addWidget(self.comboBox_devices)

        self.label_connection = QLabel(Form)
        self.label_connection.setObjectName(u"label_connection")
        self.label_connection.setMinimumSize(QSize(91, 18))

        self.horizontalLayout.addWidget(self.label_connection)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.slider_step_size = QSlider(Form)
        self.slider_step_size.setObjectName(u"slider_step_size")
        self.slider_step_size.setMinimum(10)
        self.slider_step_size.setMaximum(200)
        self.slider_step_size.setValue(50)
        self.slider_step_size.setSliderPosition(50)
        self.slider_step_size.setOrientation(Qt.Horizontal)

        self.verticalLayout.addWidget(self.slider_step_size)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_step_size = QLabel(Form)
        self.label_step_size.setObjectName(u"label_step_size")

        self.horizontalLayout_2.addWidget(self.label_step_size)

        self.spinBox_step_size = QSpinBox(Form)
        self.spinBox_step_size.setObjectName(u"spinBox_step_size")
        self.spinBox_step_size.setMinimum(10)
        self.spinBox_step_size.setMaximum(200)
        self.spinBox_step_size.setValue(100)

        self.horizontalLayout_2.addWidget(self.spinBox_step_size)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_12)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pb_move_bw10 = QPushButton(Form)
        self.pb_move_bw10.setObjectName(u"pb_move_bw10")
        self.pb_move_bw10.setMinimumSize(QSize(32, 32))

        self.horizontalLayout_3.addWidget(self.pb_move_bw10)

        self.pb_move_bw1 = QPushButton(Form)
        self.pb_move_bw1.setObjectName(u"pb_move_bw1")
        self.pb_move_bw1.setMinimumSize(QSize(32, 32))

        self.horizontalLayout_3.addWidget(self.pb_move_bw1)

        self.pb_move_fw1 = QPushButton(Form)
        self.pb_move_fw1.setObjectName(u"pb_move_fw1")
        self.pb_move_fw1.setMinimumSize(QSize(32, 32))

        self.horizontalLayout_3.addWidget(self.pb_move_fw1)

        self.pb_move_fw10 = QPushButton(Form)
        self.pb_move_fw10.setObjectName(u"pb_move_fw10")
        self.pb_move_fw10.setMinimumSize(QSize(32, 32))

        self.horizontalLayout_3.addWidget(self.pb_move_fw10)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.pb_Reload = QPushButton(Form)
        self.pb_Reload.setObjectName(u"pb_Reload")

        self.horizontalLayout_3.addWidget(self.pb_Reload)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_position = QLabel(Form)
        self.label_position.setObjectName(u"label_position")

        self.horizontalLayout_5.addWidget(self.label_position)

        self.lcdNumber_Position = QLCDNumber(Form)
        self.lcdNumber_Position.setObjectName(u"lcdNumber_Position")
        self.lcdNumber_Position.setMinimumSize(QSize(200, 30))
        self.lcdNumber_Position.setMaximumSize(QSize(16777215, 30))
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
        brush4 = QBrush(QColor(170, 170, 170, 255))
        brush4.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Mid, brush4)
        brush5 = QBrush(QColor(0, 0, 0, 255))
        brush5.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush5)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.BrightText, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush5)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush5)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush5)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Shadow, brush5)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.AlternateBase, brush1)
        brush6 = QBrush(QColor(255, 255, 220, 255))
        brush6.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipBase, brush6)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipText, brush5)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Light, brush2)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Midlight, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Dark, brush3)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Mid, brush4)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush5)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.BrightText, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush5)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush5)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush5)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Shadow, brush5)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.AlternateBase, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ToolTipBase, brush6)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ToolTipText, brush5)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush3)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Light, brush2)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Midlight, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Dark, brush3)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Mid, brush4)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush3)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.BrightText, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush3)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush5)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush5)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Shadow, brush5)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.AlternateBase, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipBase, brush6)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipText, brush5)
        self.lcdNumber_Position.setPalette(palette)
        self.lcdNumber_Position.setAutoFillBackground(True)
        self.lcdNumber_Position.setDigitCount(6)
        self.lcdNumber_Position.setProperty(u"value", 23000.000000000000000)
        self.lcdNumber_Position.setProperty(u"intValue", 23000)

        self.horizontalLayout_5.addWidget(self.lcdNumber_Position)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_speed = QLabel(Form)
        self.label_speed.setObjectName(u"label_speed")

        self.horizontalLayout_4.addWidget(self.label_speed)

        self.spinBox_speed = QDoubleSpinBox(Form)
        self.spinBox_speed.setObjectName(u"spinBox_speed")
        self.spinBox_speed.setMinimum(0.010000000000000)
        self.spinBox_speed.setMaximum(50.000000000000000)
        self.spinBox_speed.setValue(1.000000000000000)

        self.horizontalLayout_4.addWidget(self.spinBox_speed)

        self.label_moving = QLabel(Form)
        self.label_moving.setObjectName(u"label_moving")
        self.label_moving.setMinimumSize(QSize(32, 32))
        self.label_moving.setMaximumSize(QSize(32, 32))

        self.horizontalLayout_4.addWidget(self.label_moving)

        self.pb_start_stop = QPushButton(Form)
        self.pb_start_stop.setObjectName(u"pb_start_stop")
        self.pb_start_stop.setCheckable(True)

        self.horizontalLayout_4.addWidget(self.pb_start_stop)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_13)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.verticalSpacer = QSpacerItem(20, 218, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Form)
        self.slider_step_size.valueChanged.connect(self.spinBox_step_size.setValue)
        self.spinBox_step_size.valueChanged.connect(self.slider_step_size.setValue)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_serial_port.setText(QCoreApplication.translate("Form", u"Serial Port", None))
#if QT_CONFIG(tooltip)
        self.comboBox_devices.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Select the serial port to which the piezo controller is connected.</p><p>Ensure the correct port is chosen for proper communication</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_connection.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Indicates whether the piezo controller is successfully connected via the selected port.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_connection.setText(QCoreApplication.translate("Form", u"Not Connected", None))
#if QT_CONFIG(tooltip)
        self.slider_step_size.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Set the step size for piezo movement in \u00b5m.</p><p>Adjust between 0.05\u00b5m  and 2\u00b5m to control the increment of each movement command</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_step_size.setText(QCoreApplication.translate("Form", u"Step size (\u00b5l)", None))
#if QT_CONFIG(tooltip)
        self.pb_move_bw10.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Move the piezo 5 step backward</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_move_bw10.setText(QCoreApplication.translate("Form", u"<<", None))
#if QT_CONFIG(tooltip)
        self.pb_move_bw1.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Move the piezo 1 step backward.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_move_bw1.setText(QCoreApplication.translate("Form", u"<", None))
#if QT_CONFIG(tooltip)
        self.pb_move_fw1.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Move the piezo 1 step forward.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_move_fw1.setText(QCoreApplication.translate("Form", u">", None))
#if QT_CONFIG(tooltip)
        self.pb_move_fw10.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Move the piezo 10 step forward.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_move_fw10.setText(QCoreApplication.translate("Form", u">>", None))
        self.pb_Reload.setText(QCoreApplication.translate("Form", u"Reload", None))
        self.label_position.setText(QCoreApplication.translate("Form", u"Position (\u00b5l)", None))
#if QT_CONFIG(tooltip)
        self.lcdNumber_Position.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Displays the current position of the piezo controller</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_speed.setText(QCoreApplication.translate("Form", u"Speed (\u00b5l/min)", None))
        self.label_moving.setText("")
#if QT_CONFIG(tooltip)
        self.pb_start_stop.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Reference the pizeo origin, to do onece the piezo is on</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_start_stop.setText(QCoreApplication.translate("Form", u"Start/Stop", None))
    # retranslateUi

