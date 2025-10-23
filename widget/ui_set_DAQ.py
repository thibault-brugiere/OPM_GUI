# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_set_DAQ.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(630, 1183)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_vol_trig = QLabel(Form)
        self.label_vol_trig.setObjectName(u"label_vol_trig")
        self.label_vol_trig.setMinimumSize(QSize(100, 0))
        self.label_vol_trig.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_9.addWidget(self.label_vol_trig)

        self.lineEdit_vol_trig = QLineEdit(Form)
        self.lineEdit_vol_trig.setObjectName(u"lineEdit_vol_trig")

        self.horizontalLayout_9.addWidget(self.lineEdit_vol_trig)

        self.label_vol_trig_out = QLabel(Form)
        self.label_vol_trig_out.setObjectName(u"label_vol_trig_out")
        self.label_vol_trig_out.setMinimumSize(QSize(180, 0))

        self.horizontalLayout_9.addWidget(self.label_vol_trig_out)


        self.verticalLayout.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_vol_trig_outputt = QLabel(Form)
        self.label_vol_trig_outputt.setObjectName(u"label_vol_trig_outputt")
        self.label_vol_trig_outputt.setMinimumSize(QSize(100, 0))
        self.label_vol_trig_outputt.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_10.addWidget(self.label_vol_trig_outputt)

        self.lineEdit_vol_trig_outputt = QLineEdit(Form)
        self.lineEdit_vol_trig_outputt.setObjectName(u"lineEdit_vol_trig_outputt")

        self.horizontalLayout_10.addWidget(self.lineEdit_vol_trig_outputt)

        self.label_vol_trig_outputt_out = QLabel(Form)
        self.label_vol_trig_outputt_out.setObjectName(u"label_vol_trig_outputt_out")
        self.label_vol_trig_outputt_out.setMinimumSize(QSize(180, 0))

        self.horizontalLayout_10.addWidget(self.label_vol_trig_outputt_out)


        self.verticalLayout.addLayout(self.horizontalLayout_10)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_galvo = QLabel(Form)
        self.label_galvo.setObjectName(u"label_galvo")
        self.label_galvo.setMinimumSize(QSize(100, 0))
        self.label_galvo.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_galvo)

        self.lineEdit_galvo = QLineEdit(Form)
        self.lineEdit_galvo.setObjectName(u"lineEdit_galvo")

        self.horizontalLayout.addWidget(self.lineEdit_galvo)

        self.label_galvo_out = QLabel(Form)
        self.label_galvo_out.setObjectName(u"label_galvo_out")
        self.label_galvo_out.setMinimumSize(QSize(180, 0))

        self.horizontalLayout.addWidget(self.label_galvo_out)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_camera1 = QLabel(Form)
        self.label_camera1.setObjectName(u"label_camera1")
        self.label_camera1.setMinimumSize(QSize(100, 0))
        self.label_camera1.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label_camera1)

        self.lineEdit_camera1 = QLineEdit(Form)
        self.lineEdit_camera1.setObjectName(u"lineEdit_camera1")

        self.horizontalLayout_2.addWidget(self.lineEdit_camera1)

        self.label_camera1_out = QLabel(Form)
        self.label_camera1_out.setObjectName(u"label_camera1_out")
        self.label_camera1_out.setMinimumSize(QSize(180, 0))

        self.horizontalLayout_2.addWidget(self.label_camera1_out)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_camera2 = QLabel(Form)
        self.label_camera2.setObjectName(u"label_camera2")
        self.label_camera2.setMinimumSize(QSize(100, 0))
        self.label_camera2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label_camera2)

        self.lineEdit_camera2 = QLineEdit(Form)
        self.lineEdit_camera2.setObjectName(u"lineEdit_camera2")

        self.horizontalLayout_3.addWidget(self.lineEdit_camera2)

        self.label_camera2_out = QLabel(Form)
        self.label_camera2_out.setObjectName(u"label_camera2_out")
        self.label_camera2_out.setMinimumSize(QSize(180, 0))

        self.horizontalLayout_3.addWidget(self.label_camera2_out)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_filter_wheel_1 = QLabel(Form)
        self.label_filter_wheel_1.setObjectName(u"label_filter_wheel_1")
        self.label_filter_wheel_1.setMinimumSize(QSize(100, 0))
        self.label_filter_wheel_1.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_11.addWidget(self.label_filter_wheel_1)

        self.lineEdit_filter_wheel_1 = QLineEdit(Form)
        self.lineEdit_filter_wheel_1.setObjectName(u"lineEdit_filter_wheel_1")

        self.horizontalLayout_11.addWidget(self.lineEdit_filter_wheel_1)

        self.label_camera2_out_2 = QLabel(Form)
        self.label_camera2_out_2.setObjectName(u"label_camera2_out_2")
        self.label_camera2_out_2.setMinimumSize(QSize(180, 0))

        self.horizontalLayout_11.addWidget(self.label_camera2_out_2)


        self.verticalLayout.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_filter_wheel_2 = QLabel(Form)
        self.label_filter_wheel_2.setObjectName(u"label_filter_wheel_2")
        self.label_filter_wheel_2.setMinimumSize(QSize(100, 0))
        self.label_filter_wheel_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_12.addWidget(self.label_filter_wheel_2)

        self.lineEdit_filter_wheel_2 = QLineEdit(Form)
        self.lineEdit_filter_wheel_2.setObjectName(u"lineEdit_filter_wheel_2")

        self.horizontalLayout_12.addWidget(self.lineEdit_filter_wheel_2)

        self.label_camera2_out_3 = QLabel(Form)
        self.label_camera2_out_3.setObjectName(u"label_camera2_out_3")
        self.label_camera2_out_3.setMinimumSize(QSize(180, 0))

        self.horizontalLayout_12.addWidget(self.label_camera2_out_3)


        self.verticalLayout.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_laser_blanking = QLabel(Form)
        self.label_laser_blanking.setObjectName(u"label_laser_blanking")
        self.label_laser_blanking.setMinimumSize(QSize(100, 0))
        self.label_laser_blanking.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_8.addWidget(self.label_laser_blanking)

        self.lineEdit_laser_blanking = QLineEdit(Form)
        self.lineEdit_laser_blanking.setObjectName(u"lineEdit_laser_blanking")

        self.horizontalLayout_8.addWidget(self.lineEdit_laser_blanking)

        self.label_laser_blanking_out = QLabel(Form)
        self.label_laser_blanking_out.setObjectName(u"label_laser_blanking_out")
        self.label_laser_blanking_out.setMinimumSize(QSize(180, 0))

        self.horizontalLayout_8.addWidget(self.label_laser_blanking_out)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_7)

        self.label_lasers_analog = QLabel(Form)
        self.label_lasers_analog.setObjectName(u"label_lasers_analog")
        font = QFont()
        font.setBold(True)
        self.label_lasers_analog.setFont(font)
        self.label_lasers_analog.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_13.addWidget(self.label_lasers_analog)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_8)


        self.verticalLayout.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_laser_405 = QLabel(Form)
        self.label_laser_405.setObjectName(u"label_laser_405")
        self.label_laser_405.setMinimumSize(QSize(100, 0))
        self.label_laser_405.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_laser_405)

        self.lineEdit_laser_ao_405 = QLineEdit(Form)
        self.lineEdit_laser_ao_405.setObjectName(u"lineEdit_laser_ao_405")

        self.horizontalLayout_4.addWidget(self.lineEdit_laser_ao_405)

        self.label_laser_405_out = QLabel(Form)
        self.label_laser_405_out.setObjectName(u"label_laser_405_out")
        self.label_laser_405_out.setMinimumSize(QSize(180, 0))

        self.horizontalLayout_4.addWidget(self.label_laser_405_out)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_laser_488 = QLabel(Form)
        self.label_laser_488.setObjectName(u"label_laser_488")
        self.label_laser_488.setMinimumSize(QSize(100, 0))
        self.label_laser_488.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.label_laser_488)

        self.lineEdit_laser_ao_488 = QLineEdit(Form)
        self.lineEdit_laser_ao_488.setObjectName(u"lineEdit_laser_ao_488")

        self.horizontalLayout_5.addWidget(self.lineEdit_laser_ao_488)

        self.label_laser_488_out = QLabel(Form)
        self.label_laser_488_out.setObjectName(u"label_laser_488_out")
        self.label_laser_488_out.setMinimumSize(QSize(180, 0))

        self.horizontalLayout_5.addWidget(self.label_laser_488_out)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_laser_561 = QLabel(Form)
        self.label_laser_561.setObjectName(u"label_laser_561")
        self.label_laser_561.setMinimumSize(QSize(100, 0))
        self.label_laser_561.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.label_laser_561)

        self.lineEdit_laser_ao_561 = QLineEdit(Form)
        self.lineEdit_laser_ao_561.setObjectName(u"lineEdit_laser_ao_561")

        self.horizontalLayout_6.addWidget(self.lineEdit_laser_ao_561)

        self.label_laser_561_out = QLabel(Form)
        self.label_laser_561_out.setObjectName(u"label_laser_561_out")
        self.label_laser_561_out.setMinimumSize(QSize(180, 0))

        self.horizontalLayout_6.addWidget(self.label_laser_561_out)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_laser_640 = QLabel(Form)
        self.label_laser_640.setObjectName(u"label_laser_640")
        self.label_laser_640.setMinimumSize(QSize(100, 0))
        self.label_laser_640.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_7.addWidget(self.label_laser_640)

        self.lineEdit_laser_ao_640 = QLineEdit(Form)
        self.lineEdit_laser_ao_640.setObjectName(u"lineEdit_laser_ao_640")

        self.horizontalLayout_7.addWidget(self.lineEdit_laser_ao_640)

        self.label_laser_640_out = QLabel(Form)
        self.label_laser_640_out.setObjectName(u"label_laser_640_out")
        self.label_laser_640_out.setMinimumSize(QSize(180, 0))

        self.horizontalLayout_7.addWidget(self.label_laser_640_out)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_9)

        self.label_lasers_digital = QLabel(Form)
        self.label_lasers_digital.setObjectName(u"label_lasers_digital")
        self.label_lasers_digital.setFont(font)
        self.label_lasers_digital.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_14.addWidget(self.label_lasers_digital)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_10)


        self.verticalLayout.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_laser_406 = QLabel(Form)
        self.label_laser_406.setObjectName(u"label_laser_406")
        self.label_laser_406.setMinimumSize(QSize(100, 0))
        self.label_laser_406.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_16.addWidget(self.label_laser_406)

        self.lineEdit_laser_do_405 = QLineEdit(Form)
        self.lineEdit_laser_do_405.setObjectName(u"lineEdit_laser_do_405")

        self.horizontalLayout_16.addWidget(self.lineEdit_laser_do_405)

        self.label_laser_405_out_2 = QLabel(Form)
        self.label_laser_405_out_2.setObjectName(u"label_laser_405_out_2")
        self.label_laser_405_out_2.setMinimumSize(QSize(180, 0))

        self.horizontalLayout_16.addWidget(self.label_laser_405_out_2)


        self.verticalLayout.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_laser_489 = QLabel(Form)
        self.label_laser_489.setObjectName(u"label_laser_489")
        self.label_laser_489.setMinimumSize(QSize(100, 0))
        self.label_laser_489.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_15.addWidget(self.label_laser_489)

        self.lineEdit_laser_do_488 = QLineEdit(Form)
        self.lineEdit_laser_do_488.setObjectName(u"lineEdit_laser_do_488")

        self.horizontalLayout_15.addWidget(self.lineEdit_laser_do_488)

        self.label_laser_488_out_2 = QLabel(Form)
        self.label_laser_488_out_2.setObjectName(u"label_laser_488_out_2")
        self.label_laser_488_out_2.setMinimumSize(QSize(180, 0))

        self.horizontalLayout_15.addWidget(self.label_laser_488_out_2)


        self.verticalLayout.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.label_laser_562 = QLabel(Form)
        self.label_laser_562.setObjectName(u"label_laser_562")
        self.label_laser_562.setMinimumSize(QSize(100, 0))
        self.label_laser_562.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_17.addWidget(self.label_laser_562)

        self.lineEdit_laser_do_561 = QLineEdit(Form)
        self.lineEdit_laser_do_561.setObjectName(u"lineEdit_laser_do_561")

        self.horizontalLayout_17.addWidget(self.lineEdit_laser_do_561)

        self.label_laser_561_out_2 = QLabel(Form)
        self.label_laser_561_out_2.setObjectName(u"label_laser_561_out_2")
        self.label_laser_561_out_2.setMinimumSize(QSize(180, 0))

        self.horizontalLayout_17.addWidget(self.label_laser_561_out_2)


        self.verticalLayout.addLayout(self.horizontalLayout_17)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_laser_641 = QLabel(Form)
        self.label_laser_641.setObjectName(u"label_laser_641")
        self.label_laser_641.setMinimumSize(QSize(100, 0))
        self.label_laser_641.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_18.addWidget(self.label_laser_641)

        self.lineEdit_laser_do_640 = QLineEdit(Form)
        self.lineEdit_laser_do_640.setObjectName(u"lineEdit_laser_do_640")

        self.horizontalLayout_18.addWidget(self.lineEdit_laser_do_640)

        self.label_laser_640_out_2 = QLabel(Form)
        self.label_laser_640_out_2.setObjectName(u"label_laser_640_out_2")
        self.label_laser_640_out_2.setMinimumSize(QSize(180, 0))

        self.horizontalLayout_18.addWidget(self.label_laser_640_out_2)


        self.verticalLayout.addLayout(self.horizontalLayout_18)

        self.verticalSpacer = QSpacerItem(20, 658, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_vol_trig.setText(QCoreApplication.translate("Form", u"Volume trigger", None))
        self.lineEdit_vol_trig.setText("")
        self.label_vol_trig_out.setText(QCoreApplication.translate("Form", u"ctr", None))
        self.label_vol_trig_outputt.setText(QCoreApplication.translate("Form", u"Vol. trig. outputt", None))
        self.label_vol_trig_outputt_out.setText(QCoreApplication.translate("Form", u"PFI", None))
        self.label_galvo.setText(QCoreApplication.translate("Form", u"Galvo", None))
        self.label_galvo_out.setText(QCoreApplication.translate("Form", u"ao", None))
        self.label_camera1.setText(QCoreApplication.translate("Form", u"Camera 1", None))
        self.label_camera1_out.setText(QCoreApplication.translate("Form", u"digital out", None))
        self.label_camera2.setText(QCoreApplication.translate("Form", u"Camera 2", None))
        self.label_camera2_out.setText(QCoreApplication.translate("Form", u"digital out (optionnal)", None))
        self.label_filter_wheel_1.setText(QCoreApplication.translate("Form", u"Filter wheel 1", None))
        self.label_camera2_out_2.setText(QCoreApplication.translate("Form", u"digital out (optionnal)", None))
        self.label_filter_wheel_2.setText(QCoreApplication.translate("Form", u"Filter wheel 2", None))
        self.label_camera2_out_3.setText(QCoreApplication.translate("Form", u"digital out (optionnal)", None))
        self.label_laser_blanking.setText(QCoreApplication.translate("Form", u"laser blanking", None))
        self.label_laser_blanking_out.setText(QCoreApplication.translate("Form", u"digital out", None))
        self.label_lasers_analog.setText(QCoreApplication.translate("Form", u"Lasers analog out", None))
        self.label_laser_405.setText(QCoreApplication.translate("Form", u"405", None))
        self.label_laser_405_out.setText(QCoreApplication.translate("Form", u"ao (None if not connected)", None))
        self.label_laser_488.setText(QCoreApplication.translate("Form", u"488", None))
        self.label_laser_488_out.setText(QCoreApplication.translate("Form", u"ao (None if not connected)", None))
        self.label_laser_561.setText(QCoreApplication.translate("Form", u"561", None))
        self.label_laser_561_out.setText(QCoreApplication.translate("Form", u"ao (None if not connected)", None))
        self.label_laser_640.setText(QCoreApplication.translate("Form", u"640", None))
        self.label_laser_640_out.setText(QCoreApplication.translate("Form", u"ao (None if not connected)", None))
        self.label_lasers_digital.setText(QCoreApplication.translate("Form", u"Lasers digital out", None))
        self.label_laser_406.setText(QCoreApplication.translate("Form", u"405", None))
        self.label_laser_405_out_2.setText(QCoreApplication.translate("Form", u"ao (None if not connected)", None))
        self.label_laser_489.setText(QCoreApplication.translate("Form", u"488", None))
        self.label_laser_488_out_2.setText(QCoreApplication.translate("Form", u"ao (None if not connected)", None))
        self.label_laser_562.setText(QCoreApplication.translate("Form", u"561", None))
        self.label_laser_561_out_2.setText(QCoreApplication.translate("Form", u"ao (None if not connected)", None))
        self.label_laser_641.setText(QCoreApplication.translate("Form", u"640", None))
        self.label_laser_640_out_2.setText(QCoreApplication.translate("Form", u"ao (None if not connected)", None))
    # retranslateUi

