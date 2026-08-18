# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_alignement_O2_O3.ui'
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
    QSlider, QSpacerItem, QTextBrowser, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(442, 382)
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

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.pb_piezo_reference = QPushButton(Form)
        self.pb_piezo_reference.setObjectName(u"pb_piezo_reference")
        self.pb_piezo_reference.setCheckable(False)

        self.horizontalLayout_15.addWidget(self.pb_piezo_reference)

        self.label_piezo_referenced_icon = QLabel(Form)
        self.label_piezo_referenced_icon.setObjectName(u"label_piezo_referenced_icon")
        self.label_piezo_referenced_icon.setMinimumSize(QSize(32, 32))
        self.label_piezo_referenced_icon.setMaximumSize(QSize(32, 32))

        self.horizontalLayout_15.addWidget(self.label_piezo_referenced_icon)

        self.label_piezo_referenced = QLabel(Form)
        self.label_piezo_referenced.setObjectName(u"label_piezo_referenced")
        self.label_piezo_referenced.setMinimumSize(QSize(30, 0))

        self.horizontalLayout_15.addWidget(self.label_piezo_referenced)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_11)


        self.verticalLayout.addLayout(self.horizontalLayout_15)

        self.slider_step_size = QSlider(Form)
        self.slider_step_size.setObjectName(u"slider_step_size")
        self.slider_step_size.setMinimum(50)
        self.slider_step_size.setMaximum(2000)
        self.slider_step_size.setValue(50)
        self.slider_step_size.setSliderPosition(50)
        self.slider_step_size.setOrientation(Qt.Horizontal)

        self.verticalLayout.addWidget(self.slider_step_size)

        self.label_step_size = QLabel(Form)
        self.label_step_size.setObjectName(u"label_step_size")

        self.verticalLayout.addWidget(self.label_step_size)

        self.spinBox_step_size = QDoubleSpinBox(Form)
        self.spinBox_step_size.setObjectName(u"spinBox_step_size")
        self.spinBox_step_size.setDecimals(3)
        self.spinBox_step_size.setMinimum(0.050000000000000)
        self.spinBox_step_size.setMaximum(2.000000000000000)
        self.spinBox_step_size.setSingleStep(0.100000000000000)
        self.spinBox_step_size.setValue(0.100000000000000)

        self.verticalLayout.addWidget(self.spinBox_step_size)

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
        self.lcdNumber_Position.setDigitCount(9)
        self.lcdNumber_Position.setProperty(u"value", 0.000000000000000)

        self.horizontalLayout_5.addWidget(self.lcdNumber_Position)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.textBrowser = QTextBrowser(Form)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout.addWidget(self.textBrowser)


        self.retranslateUi(Form)

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
        self.pb_piezo_reference.setText(QCoreApplication.translate("Form", u"Reference", None))
        self.label_piezo_referenced_icon.setText("")
        self.label_piezo_referenced.setText(QCoreApplication.translate("Form", u"Done", None))
#if QT_CONFIG(tooltip)
        self.slider_step_size.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Set the step size for piezo movement in \u00b5m.</p><p>Adjust between 0.05\u00b5m  and 2\u00b5m to control the increment of each movement command</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_step_size.setText(QCoreApplication.translate("Form", u"Step size (\u00b5m)", None))
#if QT_CONFIG(tooltip)
        self.spinBox_step_size.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Set the step size for piezo movement in \u00b5m.</p><p>Adjust between 0.05\u00b5m and 2\u00b5m to control the increment of each movement command</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
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
        self.label_position.setText(QCoreApplication.translate("Form", u"Serial position (mm)", None))
#if QT_CONFIG(tooltip)
        self.lcdNumber_Position.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Displays the current position of the piezo controller</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.textBrowser.setHtml(QCoreApplication.translate("Form", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">The Piezo Controller interface for fine-tuning the focus between Objective 2 and Objective 3 of the microscope. This interface allows you to precisely adjust the position of the piezo stage to achieve optimal focus while imaging sample with the camera.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -q"
                        "t-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Elements of the Interface:</span></p>\n"
"<ol style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" font-size:8pt;\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Port Selection (ComboBox):</span></li>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 2;\"><li style=\" font-size:8pt;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Select the serial port to which the piezo controller is connected. Ensure the correct port is chosen for proper communication with the device.</li></ul>\n"
"<li style=\" font-size:8pt;\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\""
                        "><span style=\" font-weight:600;\">Connection Status (QLabel):</span></li>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 2;\"><li style=\" font-size:8pt;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Indicates whether the piezo controller is successfully connected via the selected port. A green checkmark means the device is connected, while a red cross indicates no connection.</li></ul>\n"
"<li style=\" font-size:8pt;\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Step Size (SpinBox):</span></li>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 2;\"><li style=\" font-size:8pt;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Set the step size f"
                        "or piezo movement in \u00b5m, allowing for precise adjustments.</li></ul>\n"
"<li style=\" font-size:8pt;\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Movement Control Buttons:</span></li>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 2;\"><li style=\" font-size:8pt;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Forward and Backward Arrows:</span> </li></ul>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 3;\"><li style=\" font-size:8pt;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Use these buttons to move the piezo stage in the specified direction. Each button is labeled with the direction and speed of"
                        " movement: </li></ul>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 4;\"><li style=\" font-size:8pt;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Small Step:</span> Move the piezo by one step size.</li>\n"
"<li style=\" font-size:8pt;\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Big step :</span> Move the piezoof 5 steps.</li></ul>\n"
"<li style=\" font-size:8pt;\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Current Position (QLCDNumber):</span></li></ol>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 2;\"><li style=\" font-size:8pt;\" style=\" margin-top:0px; margin-bo"
                        "ttom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Displays the current position of the piezo stage. This value updates in real-time as the piezo moves, reflecting its precise location.</li></ul></body></html>", None))
    # retranslateUi

