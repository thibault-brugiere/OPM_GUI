# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_alignement_O2_O3.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLCDNumber,
    QLabel, QPushButton, QSizePolicy, QSlider,
    QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(442, 224)
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


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_step_size = QLabel(Form)
        self.label_step_size.setObjectName(u"label_step_size")

        self.horizontalLayout_2.addWidget(self.label_step_size)

        self.slider_step_size = QSlider(Form)
        self.slider_step_size.setObjectName(u"slider_step_size")
        self.slider_step_size.setMinimum(1)
        self.slider_step_size.setMaximum(100)
        self.slider_step_size.setValue(100)
        self.slider_step_size.setOrientation(Qt.Horizontal)

        self.horizontalLayout_2.addWidget(self.slider_step_size)

        self.spinBox_step_size = QSpinBox(Form)
        self.spinBox_step_size.setObjectName(u"spinBox_step_size")
        self.spinBox_step_size.setMinimum(1)
        self.spinBox_step_size.setMaximum(100)
        self.spinBox_step_size.setValue(100)

        self.horizontalLayout_2.addWidget(self.spinBox_step_size)


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


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pb_move_bwj2 = QPushButton(Form)
        self.pb_move_bwj2.setObjectName(u"pb_move_bwj2")
        self.pb_move_bwj2.setMinimumSize(QSize(32, 32))

        self.horizontalLayout_4.addWidget(self.pb_move_bwj2)

        self.pb_move_bwj1 = QPushButton(Form)
        self.pb_move_bwj1.setObjectName(u"pb_move_bwj1")
        self.pb_move_bwj1.setMinimumSize(QSize(32, 32))

        self.horizontalLayout_4.addWidget(self.pb_move_bwj1)

        self.pb_move_fwj1 = QPushButton(Form)
        self.pb_move_fwj1.setObjectName(u"pb_move_fwj1")
        self.pb_move_fwj1.setMinimumSize(QSize(32, 32))

        self.horizontalLayout_4.addWidget(self.pb_move_fwj1)

        self.pb_move_fwj2 = QPushButton(Form)
        self.pb_move_fwj2.setObjectName(u"pb_move_fwj2")
        self.pb_move_fwj2.setMinimumSize(QSize(32, 32))

        self.horizontalLayout_4.addWidget(self.pb_move_fwj2)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

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
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(255, 255, 255, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        brush2 = QBrush(QColor(255, 206, 57, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Light, brush2)
        palette.setBrush(QPalette.Active, QPalette.Midlight, brush1)
        brush3 = QBrush(QColor(158, 105, 0, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Dark, brush3)
        brush4 = QBrush(QColor(170, 170, 170, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Mid, brush4)
        brush5 = QBrush(QColor(0, 0, 0, 255))
        brush5.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Text, brush5)
        palette.setBrush(QPalette.Active, QPalette.BrightText, brush1)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush5)
        palette.setBrush(QPalette.Active, QPalette.Base, brush5)
        palette.setBrush(QPalette.Active, QPalette.Window, brush5)
        palette.setBrush(QPalette.Active, QPalette.Shadow, brush5)
        palette.setBrush(QPalette.Active, QPalette.AlternateBase, brush1)
        brush6 = QBrush(QColor(255, 255, 220, 255))
        brush6.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ToolTipBase, brush6)
        palette.setBrush(QPalette.Active, QPalette.ToolTipText, brush5)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Light, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.Midlight, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Dark, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.Mid, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush5)
        palette.setBrush(QPalette.Inactive, QPalette.BrightText, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush5)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush5)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush5)
        palette.setBrush(QPalette.Inactive, QPalette.Shadow, brush5)
        palette.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush6)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush5)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Light, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Midlight, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Dark, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.Mid, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.BrightText, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush5)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush5)
        palette.setBrush(QPalette.Disabled, QPalette.Shadow, brush5)
        palette.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush6)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush5)
        self.lcdNumber_Position.setPalette(palette)
        self.lcdNumber_Position.setAutoFillBackground(True)
        self.lcdNumber_Position.setDigitCount(9)
        self.lcdNumber_Position.setProperty(u"value", 0.000000000000000)

        self.horizontalLayout_5.addWidget(self.lcdNumber_Position)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.verticalSpacer = QSpacerItem(20, 16, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

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
        self.label_step_size.setText(QCoreApplication.translate("Form", u"Step size (%)", None))
#if QT_CONFIG(tooltip)
        self.slider_step_size.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Set the step size for piezo movement as a percentage of the total range.</p><p>Adjust between 21% and 100% to control the increment of each movement command</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_step_size.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Set the step size for piezo movement as a percentage of the total range.</p><p>Adjust between 21% and 100% to control the increment of each movement command</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pb_move_bw10.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Move the piezo 10 step backward.</p><p>Around 500nm to 2,5\u00b5m depending on step size</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_move_bw10.setText(QCoreApplication.translate("Form", u"<<", None))
#if QT_CONFIG(tooltip)
        self.pb_move_bw1.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Move the piezo 1 step backward.</p><p>Around 50nm to 250nm depending on step size</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_move_bw1.setText(QCoreApplication.translate("Form", u"<", None))
#if QT_CONFIG(tooltip)
        self.pb_move_fw1.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Move the piezo 1 step forward.</p><p>Around 50nm to 250nm depending on step size</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_move_fw1.setText(QCoreApplication.translate("Form", u">", None))
#if QT_CONFIG(tooltip)
        self.pb_move_fw10.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Move the piezo 10 step forward</p><p>Around 500nm to 2,5\u00b5m depending on step size</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_move_fw10.setText(QCoreApplication.translate("Form", u">>", None))
#if QT_CONFIG(tooltip)
        self.pb_move_bwj2.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Move the piezo backward with a speed around 0.25mm/s</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_move_bwj2.setText(QCoreApplication.translate("Form", u"<<<<", None))
#if QT_CONFIG(tooltip)
        self.pb_move_bwj1.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Move the piezo backward with a speed around 2.5 \u00b5m/s</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_move_bwj1.setText(QCoreApplication.translate("Form", u"<<<", None))
#if QT_CONFIG(tooltip)
        self.pb_move_fwj1.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Move the piezo forward with a speed of 50 steps/s.</p><p>Arount 2.5 ot 12 \u00b5m/s depending on step size</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_move_fwj1.setText(QCoreApplication.translate("Form", u">>>", None))
#if QT_CONFIG(tooltip)
        self.pb_move_fwj2.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Move the piezo forward with a speed around 0.25mm/s</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_move_fwj2.setText(QCoreApplication.translate("Form", u">>>>", None))
        self.label_position.setText(QCoreApplication.translate("Form", u"Serial position (mm)", None))
#if QT_CONFIG(tooltip)
        self.lcdNumber_Position.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Displays the current position of the piezo controller</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

