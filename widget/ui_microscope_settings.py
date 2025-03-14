# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_microscope_settings.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(358, 608)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer)

        self.label_vgalvanometer_2 = QLabel(Form)
        self.label_vgalvanometer_2.setObjectName(u"label_vgalvanometer_2")
        font = QFont()
        font.setBold(True)
        self.label_vgalvanometer_2.setFont(font)
        self.label_vgalvanometer_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_7.addWidget(self.label_vgalvanometer_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_tilt_angle = QLabel(Form)
        self.label_tilt_angle.setObjectName(u"label_tilt_angle")
        self.label_tilt_angle.setMinimumSize(QSize(122, 0))
        self.label_tilt_angle.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_tilt_angle)

        self.lineEdit_tilt_angle = QLineEdit(Form)
        self.lineEdit_tilt_angle.setObjectName(u"lineEdit_tilt_angle")

        self.horizontalLayout.addWidget(self.lineEdit_tilt_angle)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_mag_total = QLabel(Form)
        self.label_mag_total.setObjectName(u"label_mag_total")
        self.label_mag_total.setMinimumSize(QSize(122, 0))
        self.label_mag_total.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label_mag_total)

        self.lineEdit_mag_total = QLineEdit(Form)
        self.lineEdit_mag_total.setObjectName(u"lineEdit_mag_total")

        self.horizontalLayout_2.addWidget(self.lineEdit_mag_total)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.line_1 = QFrame(Form)
        self.line_1.setObjectName(u"line_1")
        self.line_1.setFrameShape(QFrame.Shape.HLine)
        self.line_1.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_3)

        self.label_vgalvanometer = QLabel(Form)
        self.label_vgalvanometer.setObjectName(u"label_vgalvanometer")
        self.label_vgalvanometer.setFont(font)
        self.label_vgalvanometer.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_8.addWidget(self.label_vgalvanometer)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_volts_per_um = QLabel(Form)
        self.label_volts_per_um.setObjectName(u"label_volts_per_um")
        self.label_volts_per_um.setMinimumSize(QSize(122, 0))
        self.label_volts_per_um.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label_volts_per_um)

        self.lineEdit_volts_per_um = QLineEdit(Form)
        self.lineEdit_volts_per_um.setObjectName(u"lineEdit_volts_per_um")

        self.horizontalLayout_3.addWidget(self.lineEdit_volts_per_um)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_galvo_response_time = QLabel(Form)
        self.label_galvo_response_time.setObjectName(u"label_galvo_response_time")
        self.label_galvo_response_time.setMinimumSize(QSize(122, 0))
        self.label_galvo_response_time.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_galvo_response_time)

        self.lineEdit_galvo_response_time = QLineEdit(Form)
        self.lineEdit_galvo_response_time.setObjectName(u"lineEdit_galvo_response_time")

        self.horizontalLayout_4.addWidget(self.lineEdit_galvo_response_time)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_galvo_flyback_time = QLabel(Form)
        self.label_galvo_flyback_time.setObjectName(u"label_galvo_flyback_time")
        self.label_galvo_flyback_time.setMinimumSize(QSize(122, 0))
        self.label_galvo_flyback_time.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.label_galvo_flyback_time)

        self.lineEdit_galvo_flyback_time = QLineEdit(Form)
        self.lineEdit_galvo_flyback_time.setObjectName(u"lineEdit_galvo_flyback_time")

        self.horizontalLayout_5.addWidget(self.lineEdit_galvo_flyback_time)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.line_2 = QFrame(Form)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_5)

        self.label_volts_per_um_3 = QLabel(Form)
        self.label_volts_per_um_3.setObjectName(u"label_volts_per_um_3")
        self.label_volts_per_um_3.setFont(font)
        self.label_volts_per_um_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_9.addWidget(self.label_volts_per_um_3)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_6)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_laser_response_time = QLabel(Form)
        self.label_laser_response_time.setObjectName(u"label_laser_response_time")
        self.label_laser_response_time.setMinimumSize(QSize(122, 0))
        self.label_laser_response_time.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.label_laser_response_time)

        self.lineEdit_laser_response_time = QLineEdit(Form)
        self.lineEdit_laser_response_time.setObjectName(u"lineEdit_laser_response_time")

        self.horizontalLayout_6.addWidget(self.lineEdit_laser_response_time)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.verticalSpacer = QSpacerItem(20, 290, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_vgalvanometer_2.setText(QCoreApplication.translate("Form", u"Microscope", None))
        self.label_tilt_angle.setText(QCoreApplication.translate("Form", u"Tilt Angle:", None))
        self.label_mag_total.setText(QCoreApplication.translate("Form", u"Mag Total:", None))
        self.label_vgalvanometer.setText(QCoreApplication.translate("Form", u"Galvanometer", None))
        self.label_volts_per_um.setText(QCoreApplication.translate("Form", u"Volts per \u00b5m:", None))
        self.label_galvo_response_time.setText(QCoreApplication.translate("Form", u"Response time (ms):", None))
        self.label_galvo_flyback_time.setText(QCoreApplication.translate("Form", u"Response time (ms):", None))
        self.label_volts_per_um_3.setText(QCoreApplication.translate("Form", u"Lasers", None))
        self.label_laser_response_time.setText(QCoreApplication.translate("Form", u"Response time (ms):", None))
    # retranslateUi

