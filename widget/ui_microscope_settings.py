# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_microscope_settings.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(840, 970)
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

        self.line_4 = QFrame(Form)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_4)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_9)

        self.label_stage = QLabel(Form)
        self.label_stage.setObjectName(u"label_stage")
        self.label_stage.setFont(font)
        self.label_stage.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_10.addWidget(self.label_stage)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_10)


        self.verticalLayout.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_stage_port = QLabel(Form)
        self.label_stage_port.setObjectName(u"label_stage_port")
        self.label_stage_port.setMinimumSize(QSize(122, 0))
        self.label_stage_port.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_20.addWidget(self.label_stage_port)

        self.lineEdit_stage_port = QLineEdit(Form)
        self.lineEdit_stage_port.setObjectName(u"lineEdit_stage_port")

        self.horizontalLayout_20.addWidget(self.lineEdit_stage_port)


        self.verticalLayout.addLayout(self.horizontalLayout_20)

        self.line_1 = QFrame(Form)
        self.line_1.setObjectName(u"line_1")
        self.line_1.setFrameShape(QFrame.Shape.HLine)
        self.line_1.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_1)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_22.addItem(self.horizontalSpacer_11)

        self.label_Preview = QLabel(Form)
        self.label_Preview.setObjectName(u"label_Preview")
        self.label_Preview.setFont(font)
        self.label_Preview.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_22.addWidget(self.label_Preview)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_22.addItem(self.horizontalSpacer_12)


        self.verticalLayout.addLayout(self.horizontalLayout_22)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.label_mirror_ser_num = QLabel(Form)
        self.label_mirror_ser_num.setObjectName(u"label_mirror_ser_num")
        self.label_mirror_ser_num.setMinimumSize(QSize(122, 0))
        self.label_mirror_ser_num.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_23.addWidget(self.label_mirror_ser_num)

        self.lineEdit_trans_mirror_ser_num = QLineEdit(Form)
        self.lineEdit_trans_mirror_ser_num.setObjectName(u"lineEdit_trans_mirror_ser_num")

        self.horizontalLayout_23.addWidget(self.lineEdit_trans_mirror_ser_num)


        self.verticalLayout.addLayout(self.horizontalLayout_23)

        self.line_5 = QFrame(Form)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_5)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_3)

        self.label_galvanometer = QLabel(Form)
        self.label_galvanometer.setObjectName(u"label_galvanometer")
        self.label_galvanometer.setFont(font)
        self.label_galvanometer.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_8.addWidget(self.label_galvanometer)

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

        self.label_lasers = QLabel(Form)
        self.label_lasers.setObjectName(u"label_lasers")
        self.label_lasers.setFont(font)
        self.label_lasers.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_9.addWidget(self.label_lasers)

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

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_OxxiusCombiner_port = QLabel(Form)
        self.label_OxxiusCombiner_port.setObjectName(u"label_OxxiusCombiner_port")
        self.label_OxxiusCombiner_port.setMinimumSize(QSize(122, 0))
        self.label_OxxiusCombiner_port.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_12.addWidget(self.label_OxxiusCombiner_port)

        self.lineEdit_OxxiusCombiner_port = QLineEdit(Form)
        self.lineEdit_OxxiusCombiner_port.setObjectName(u"lineEdit_OxxiusCombiner_port")

        self.horizontalLayout_12.addWidget(self.lineEdit_OxxiusCombiner_port)


        self.verticalLayout.addLayout(self.horizontalLayout_12)

        self.line_3 = QFrame(Form)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_3)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_7)

        self.label_filters = QLabel(Form)
        self.label_filters.setObjectName(u"label_filters")
        self.label_filters.setFont(font)
        self.label_filters.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_11.addWidget(self.label_filters)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_8)


        self.verticalLayout.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.label_Filter_port = QLabel(Form)
        self.label_Filter_port.setObjectName(u"label_Filter_port")
        self.label_Filter_port.setMinimumSize(QSize(122, 0))
        self.label_Filter_port.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_21.addWidget(self.label_Filter_port)

        self.lineEdit_Filter_port = QLineEdit(Form)
        self.lineEdit_Filter_port.setObjectName(u"lineEdit_Filter_port")

        self.horizontalLayout_21.addWidget(self.lineEdit_Filter_port)


        self.verticalLayout.addLayout(self.horizontalLayout_21)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_filter_changing_time = QLabel(Form)
        self.label_filter_changing_time.setObjectName(u"label_filter_changing_time")
        self.label_filter_changing_time.setMinimumSize(QSize(122, 0))
        self.label_filter_changing_time.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_13.addWidget(self.label_filter_changing_time)

        self.lineEdit_filter_changing_time = QLineEdit(Form)
        self.lineEdit_filter_changing_time.setObjectName(u"lineEdit_filter_changing_time")

        self.horizontalLayout_13.addWidget(self.lineEdit_filter_changing_time)


        self.verticalLayout.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_Filter1 = QLabel(Form)
        self.label_Filter1.setObjectName(u"label_Filter1")
        self.label_Filter1.setMinimumSize(QSize(122, 0))
        self.label_Filter1.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_18.addWidget(self.label_Filter1)

        self.lineEdit_Filter1 = QLineEdit(Form)
        self.lineEdit_Filter1.setObjectName(u"lineEdit_Filter1")

        self.horizontalLayout_18.addWidget(self.lineEdit_Filter1)


        self.verticalLayout.addLayout(self.horizontalLayout_18)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_Filter2 = QLabel(Form)
        self.label_Filter2.setObjectName(u"label_Filter2")
        self.label_Filter2.setMinimumSize(QSize(122, 0))
        self.label_Filter2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_16.addWidget(self.label_Filter2)

        self.lineEdit_Filter2 = QLineEdit(Form)
        self.lineEdit_Filter2.setObjectName(u"lineEdit_Filter2")

        self.horizontalLayout_16.addWidget(self.lineEdit_Filter2)


        self.verticalLayout.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.label_Filter3 = QLabel(Form)
        self.label_Filter3.setObjectName(u"label_Filter3")
        self.label_Filter3.setMinimumSize(QSize(122, 0))
        self.label_Filter3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_17.addWidget(self.label_Filter3)

        self.lineEdit_Filter3 = QLineEdit(Form)
        self.lineEdit_Filter3.setObjectName(u"lineEdit_Filter3")

        self.horizontalLayout_17.addWidget(self.lineEdit_Filter3)


        self.verticalLayout.addLayout(self.horizontalLayout_17)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_Filter4 = QLabel(Form)
        self.label_Filter4.setObjectName(u"label_Filter4")
        self.label_Filter4.setMinimumSize(QSize(122, 0))
        self.label_Filter4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_19.addWidget(self.label_Filter4)

        self.lineEdit_Filter4 = QLineEdit(Form)
        self.lineEdit_Filter4.setObjectName(u"lineEdit_Filter4")

        self.horizontalLayout_19.addWidget(self.lineEdit_Filter4)


        self.verticalLayout.addLayout(self.horizontalLayout_19)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_Filter5 = QLabel(Form)
        self.label_Filter5.setObjectName(u"label_Filter5")
        self.label_Filter5.setMinimumSize(QSize(122, 0))
        self.label_Filter5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_15.addWidget(self.label_Filter5)

        self.lineEdit_Filter5 = QLineEdit(Form)
        self.lineEdit_Filter5.setObjectName(u"lineEdit_Filter5")

        self.horizontalLayout_15.addWidget(self.lineEdit_Filter5)


        self.verticalLayout.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_Filter6 = QLabel(Form)
        self.label_Filter6.setObjectName(u"label_Filter6")
        self.label_Filter6.setMinimumSize(QSize(122, 0))
        self.label_Filter6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_14.addWidget(self.label_Filter6)

        self.lineEdit_Filter6 = QLineEdit(Form)
        self.lineEdit_Filter6.setObjectName(u"lineEdit_Filter6")

        self.horizontalLayout_14.addWidget(self.lineEdit_Filter6)


        self.verticalLayout.addLayout(self.horizontalLayout_14)

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
        self.label_stage.setText(QCoreApplication.translate("Form", u"Stage", None))
        self.label_stage_port.setText(QCoreApplication.translate("Form", u"Stage port:", None))
        self.label_Preview.setText(QCoreApplication.translate("Form", u"Preview", None))
        self.label_mirror_ser_num.setText(QCoreApplication.translate("Form", u"mirror serial number:", None))
        self.label_galvanometer.setText(QCoreApplication.translate("Form", u"Galvanometer", None))
        self.label_volts_per_um.setText(QCoreApplication.translate("Form", u"Volts per \u00b5m:", None))
        self.label_galvo_response_time.setText(QCoreApplication.translate("Form", u"Response time (ms):", None))
        self.label_galvo_flyback_time.setText(QCoreApplication.translate("Form", u"Flyback time (ms):", None))
        self.label_lasers.setText(QCoreApplication.translate("Form", u"Lasers", None))
        self.label_laser_response_time.setText(QCoreApplication.translate("Form", u"Response time (ms):", None))
        self.label_OxxiusCombiner_port.setText(QCoreApplication.translate("Form", u"Oxxius Combiner port:", None))
        self.label_filters.setText(QCoreApplication.translate("Form", u"Filters", None))
        self.label_Filter_port.setText(QCoreApplication.translate("Form", u"Filter port", None))
        self.label_filter_changing_time.setText(QCoreApplication.translate("Form", u"Changing time (ms):", None))
        self.label_Filter1.setText(QCoreApplication.translate("Form", u"Filter 1", None))
        self.label_Filter2.setText(QCoreApplication.translate("Form", u"Filter 2", None))
        self.label_Filter3.setText(QCoreApplication.translate("Form", u"Filter 3", None))
        self.label_Filter4.setText(QCoreApplication.translate("Form", u"Filter 4", None))
        self.label_Filter5.setText(QCoreApplication.translate("Form", u"Filter 5", None))
        self.label_Filter6.setText(QCoreApplication.translate("Form", u"Filter 6", None))
    # retranslateUi

