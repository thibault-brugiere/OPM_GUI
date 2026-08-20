# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_autofocus_02_03.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(499, 871)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_graph = QLabel(Form)
        self.label_graph.setObjectName(u"label_graph")
        self.label_graph.setMinimumSize(QSize(400, 600))
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush)
        brush1 = QBrush(QColor(108, 108, 108, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush1)
        self.label_graph.setPalette(palette)
        self.label_graph.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.label_graph.setAutoFillBackground(True)

        self.verticalLayout.addWidget(self.label_graph)

        self.label_parameters = QLabel(Form)
        self.label_parameters.setObjectName(u"label_parameters")
        self.label_parameters.setMinimumSize(QSize(300, 80))
        palette1 = QPalette()
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush)
        palette1.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush1)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush)
        palette1.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush1)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush1)
        palette1.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush1)
        self.label_parameters.setPalette(palette1)
        self.label_parameters.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.label_parameters.setAutoFillBackground(True)

        self.verticalLayout.addWidget(self.label_parameters)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_autofocus_quality = QLabel(Form)
        self.label_autofocus_quality.setObjectName(u"label_autofocus_quality")
        self.label_autofocus_quality.setMinimumSize(QSize(121, 0))

        self.horizontalLayout.addWidget(self.label_autofocus_quality)

        self.label_autofocus_quality_icon = QLabel(Form)
        self.label_autofocus_quality_icon.setObjectName(u"label_autofocus_quality_icon")
        self.label_autofocus_quality_icon.setMinimumSize(QSize(32, 32))
        self.label_autofocus_quality_icon.setMaximumSize(QSize(32, 32))

        self.horizontalLayout.addWidget(self.label_autofocus_quality_icon)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_keet = QLabel(Form)
        self.label_keet.setObjectName(u"label_keet")
        self.label_keet.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_2.addWidget(self.label_keet)

        self.pb_yes = QPushButton(Form)
        self.pb_yes.setObjectName(u"pb_yes")

        self.horizontalLayout_2.addWidget(self.pb_yes)

        self.pb_no = QPushButton(Form)
        self.pb_no.setObjectName(u"pb_no")

        self.horizontalLayout_2.addWidget(self.pb_no)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 498, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_graph.setText(QCoreApplication.translate("Form", u"Graph", None))
        self.label_parameters.setText(QCoreApplication.translate("Form", u"Parameters", None))
        self.label_autofocus_quality.setText(QCoreApplication.translate("Form", u"Autofocus quality: Good", None))
        self.label_autofocus_quality_icon.setText("")
        self.label_keet.setText(QCoreApplication.translate("Form", u"Keep this value?", None))
        self.pb_yes.setText(QCoreApplication.translate("Form", u"Yes", None))
        self.pb_no.setText(QCoreApplication.translate("Form", u"No", None))
    # retranslateUi

