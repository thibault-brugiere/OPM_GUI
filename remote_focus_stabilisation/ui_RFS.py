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
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1082, 710)
        self.label_image_preview = QLabel(Form)
        self.label_image_preview.setObjectName(u"label_image_preview")
        self.label_image_preview.setGeometry(QRect(330, 20, 720, 540))
        self.label_image_preview.setMinimumSize(QSize(720, 540))
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush)
        brush1 = QBrush(QColor(153, 153, 153, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush1)
        self.label_image_preview.setPalette(palette)
        self.label_image_preview.setAutoFillBackground(True)
        self.label_message = QLabel(Form)
        self.label_message.setObjectName(u"label_message")
        self.label_message.setGeometry(QRect(340, 590, 47, 13))
        self.pb_stabilize = QPushButton(Form)
        self.pb_stabilize.setObjectName(u"pb_stabilize")
        self.pb_stabilize.setGeometry(QRect(20, 90, 75, 23))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_image_preview.setText("")
        self.label_message.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.pb_stabilize.setText(QCoreApplication.translate("Form", u"Stabilize", None))
    # retranslateUi

