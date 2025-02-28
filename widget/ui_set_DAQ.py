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
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(642, 731)
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

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_laser_405 = QLabel(Form)
        self.label_laser_405.setObjectName(u"label_laser_405")
        self.label_laser_405.setMinimumSize(QSize(100, 0))
        self.label_laser_405.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_laser_405)

        self.lineEdit_laser_405 = QLineEdit(Form)
        self.lineEdit_laser_405.setObjectName(u"lineEdit_laser_405")

        self.horizontalLayout_4.addWidget(self.lineEdit_laser_405)

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

        self.lineEdit_laser_488 = QLineEdit(Form)
        self.lineEdit_laser_488.setObjectName(u"lineEdit_laser_488")

        self.horizontalLayout_5.addWidget(self.lineEdit_laser_488)

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

        self.lineEdit_laser_561 = QLineEdit(Form)
        self.lineEdit_laser_561.setObjectName(u"lineEdit_laser_561")

        self.horizontalLayout_6.addWidget(self.lineEdit_laser_561)

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

        self.lineEdit_laser_640 = QLineEdit(Form)
        self.lineEdit_laser_640.setObjectName(u"lineEdit_laser_640")

        self.horizontalLayout_7.addWidget(self.lineEdit_laser_640)

        self.label_laser_640_out = QLabel(Form)
        self.label_laser_640_out.setObjectName(u"label_laser_640_out")
        self.label_laser_640_out.setMinimumSize(QSize(180, 0))

        self.horizontalLayout_7.addWidget(self.label_laser_640_out)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

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
        self.label_laser_405.setText(QCoreApplication.translate("Form", u"405", None))
        self.label_laser_405_out.setText(QCoreApplication.translate("Form", u"ao (None if not connected)", None))
        self.label_laser_488.setText(QCoreApplication.translate("Form", u"488", None))
        self.label_laser_488_out.setText(QCoreApplication.translate("Form", u"ao (None if not connected)", None))
        self.label_laser_561.setText(QCoreApplication.translate("Form", u"561", None))
        self.label_laser_561_out.setText(QCoreApplication.translate("Form", u"ao (None if not connected)", None))
        self.label_laser_640.setText(QCoreApplication.translate("Form", u"640", None))
        self.label_laser_640_out.setText(QCoreApplication.translate("Form", u"ao (None if not connected)", None))
        self.label_laser_blanking.setText(QCoreApplication.translate("Form", u"laser blanking", None))
        self.label_laser_blanking_out.setText(QCoreApplication.translate("Form", u"digital out", None))
    # retranslateUi

