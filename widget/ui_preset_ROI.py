# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_preset_ROI.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpinBox, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(333, 246)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.comboBox_size_preset = QComboBox(Form)
        self.comboBox_size_preset.addItem("")
        self.comboBox_size_preset.addItem("")
        self.comboBox_size_preset.addItem("")
        self.comboBox_size_preset.setObjectName(u"comboBox_size_preset")

        self.horizontalLayout_5.addWidget(self.comboBox_size_preset)

        self.pb_remove_ROI = QPushButton(Form)
        self.pb_remove_ROI.setObjectName(u"pb_remove_ROI")

        self.horizontalLayout_5.addWidget(self.pb_remove_ROI)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.spinBox_hsize = QSpinBox(Form)
        self.spinBox_hsize.setObjectName(u"spinBox_hsize")
        self.spinBox_hsize.setMaximum(4432)
        self.spinBox_hsize.setSingleStep(4)
        self.spinBox_hsize.setValue(4432)

        self.horizontalLayout.addWidget(self.spinBox_hsize)

        self.label_hsize = QLabel(Form)
        self.label_hsize.setObjectName(u"label_hsize")

        self.horizontalLayout.addWidget(self.label_hsize)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.spinBox_hpos = QSpinBox(Form)
        self.spinBox_hpos.setObjectName(u"spinBox_hpos")
        self.spinBox_hpos.setMaximum(4432)
        self.spinBox_hpos.setSingleStep(4)
        self.spinBox_hpos.setValue(0)

        self.horizontalLayout_2.addWidget(self.spinBox_hpos)

        self.label_hpos = QLabel(Form)
        self.label_hpos.setObjectName(u"label_hpos")

        self.horizontalLayout_2.addWidget(self.label_hpos)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.spinBox_vsize = QSpinBox(Form)
        self.spinBox_vsize.setObjectName(u"spinBox_vsize")
        self.spinBox_vsize.setMaximum(2368)
        self.spinBox_vsize.setSingleStep(4)
        self.spinBox_vsize.setValue(2368)

        self.horizontalLayout_3.addWidget(self.spinBox_vsize)

        self.label_vsize = QLabel(Form)
        self.label_vsize.setObjectName(u"label_vsize")

        self.horizontalLayout_3.addWidget(self.label_vsize)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.spinBox_vpos = QSpinBox(Form)
        self.spinBox_vpos.setObjectName(u"spinBox_vpos")
        self.spinBox_vpos.setMaximum(2368)
        self.spinBox_vpos.setSingleStep(4)
        self.spinBox_vpos.setValue(0)

        self.horizontalLayout_4.addWidget(self.spinBox_vpos)

        self.label_vpos = QLabel(Form)
        self.label_vpos.setObjectName(u"label_vpos")

        self.horizontalLayout_4.addWidget(self.label_vpos)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.pb_center_FOV = QPushButton(Form)
        self.pb_center_FOV.setObjectName(u"pb_center_FOV")

        self.verticalLayout.addWidget(self.pb_center_FOV)

        self.pb_add_ROI = QPushButton(Form)
        self.pb_add_ROI.setObjectName(u"pb_add_ROI")

        self.verticalLayout.addWidget(self.pb_add_ROI)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.comboBox_size_preset.setItemText(0, QCoreApplication.translate("Form", u"Preset size", None))
        self.comboBox_size_preset.setItemText(1, QCoreApplication.translate("Form", u"44032 - 0 x 2368 - 0", None))
        self.comboBox_size_preset.setItemText(2, QCoreApplication.translate("Form", u"2048 - 1192 x 2048 - 160", None))

#if QT_CONFIG(tooltip)
        self.comboBox_size_preset.setToolTip(QCoreApplication.translate("Form", u"Set size of the FOV to preset values", None))
#endif // QT_CONFIG(tooltip)
        self.pb_remove_ROI.setText(QCoreApplication.translate("Form", u"Remove", None))
#if QT_CONFIG(tooltip)
        self.spinBox_hsize.setToolTip(QCoreApplication.translate("Form", u"Set the number of pixels along the horizontal axis of the camera sensor.", None))
#endif // QT_CONFIG(tooltip)
        self.label_hsize.setText(QCoreApplication.translate("Form", u"Pixels horizontal   ", None))
#if QT_CONFIG(tooltip)
        self.spinBox_hpos.setToolTip(QCoreApplication.translate("Form", u"Adjust the horizontal position of the field of view on the camera sensor.", None))
#endif // QT_CONFIG(tooltip)
        self.label_hpos.setText(QCoreApplication.translate("Form", u"Position horizontal", None))
#if QT_CONFIG(tooltip)
        self.spinBox_vsize.setToolTip(QCoreApplication.translate("Form", u"Set the number of pixels along the vertical axis of the camera sensor.", None))
#endif // QT_CONFIG(tooltip)
        self.label_vsize.setText(QCoreApplication.translate("Form", u"Pixels vertical       ", None))
#if QT_CONFIG(tooltip)
        self.spinBox_vpos.setToolTip(QCoreApplication.translate("Form", u"Adjust the vertical position of the field of view on the camera sensor.", None))
#endif // QT_CONFIG(tooltip)
        self.label_vpos.setText(QCoreApplication.translate("Form", u"Position vertical    ", None))
        self.pb_center_FOV.setText(QCoreApplication.translate("Form", u"Center FOV", None))
        self.pb_add_ROI.setText(QCoreApplication.translate("Form", u"Add", None))
    # retranslateUi

