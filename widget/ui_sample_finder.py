# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_sample_finder.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSlider, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1430, 1042)
        self.verticalLayout_6 = QVBoxLayout(Form)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_saving = QLabel(Form)
        self.label_saving.setObjectName(u"label_saving")
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label_saving.setFont(font)
        self.label_saving.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_saving)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_data_path = QLabel(Form)
        self.label_data_path.setObjectName(u"label_data_path")
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush)
        self.label_data_path.setPalette(palette)
        self.label_data_path.setAutoFillBackground(False)
        self.label_data_path.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_data_path)

        self.pb_data_path = QPushButton(Form)
        self.pb_data_path.setObjectName(u"pb_data_path")

        self.horizontalLayout.addWidget(self.pb_data_path)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.lineEdit_exp_name = QLineEdit(Form)
        self.lineEdit_exp_name.setObjectName(u"lineEdit_exp_name")

        self.verticalLayout.addWidget(self.lineEdit_exp_name)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pb_mirror = QPushButton(Form)
        self.pb_mirror.setObjectName(u"pb_mirror")
        self.pb_mirror.setCheckable(True)
        self.pb_mirror.setChecked(False)

        self.horizontalLayout_2.addWidget(self.pb_mirror)

        self.label_mirror_icon = QLabel(Form)
        self.label_mirror_icon.setObjectName(u"label_mirror_icon")
        self.label_mirror_icon.setMinimumSize(QSize(32, 32))
        self.label_mirror_icon.setMaximumSize(QSize(32, 32))

        self.horizontalLayout_2.addWidget(self.label_mirror_icon)

        self.label_mirror = QLabel(Form)
        self.label_mirror.setObjectName(u"label_mirror")
        self.label_mirror.setMinimumSize(QSize(30, 0))

        self.horizontalLayout_2.addWidget(self.label_mirror)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pb_fluo = QPushButton(Form)
        self.pb_fluo.setObjectName(u"pb_fluo")
        self.pb_fluo.setCheckable(True)
        self.pb_fluo.setChecked(False)

        self.horizontalLayout_3.addWidget(self.pb_fluo)

        self.label_fluo_icon = QLabel(Form)
        self.label_fluo_icon.setObjectName(u"label_fluo_icon")
        self.label_fluo_icon.setMinimumSize(QSize(32, 32))
        self.label_fluo_icon.setMaximumSize(QSize(32, 32))

        self.horizontalLayout_3.addWidget(self.label_fluo_icon)

        self.label_fluo = QLabel(Form)
        self.label_fluo.setObjectName(u"label_fluo")
        self.label_fluo.setMinimumSize(QSize(30, 0))

        self.horizontalLayout_3.addWidget(self.label_fluo)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pb_transmission = QPushButton(Form)
        self.pb_transmission.setObjectName(u"pb_transmission")
        self.pb_transmission.setCheckable(True)
        self.pb_transmission.setChecked(False)

        self.horizontalLayout_4.addWidget(self.pb_transmission)

        self.label_transmission_icon = QLabel(Form)
        self.label_transmission_icon.setObjectName(u"label_transmission_icon")
        self.label_transmission_icon.setMinimumSize(QSize(32, 32))
        self.label_transmission_icon.setMaximumSize(QSize(32, 32))

        self.horizontalLayout_4.addWidget(self.label_transmission_icon)

        self.label_transmission = QLabel(Form)
        self.label_transmission.setObjectName(u"label_transmission")
        self.label_transmission.setMinimumSize(QSize(30, 0))

        self.horizontalLayout_4.addWidget(self.label_transmission)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.spinBox_channel_exposure_time = QDoubleSpinBox(Form)
        self.spinBox_channel_exposure_time.setObjectName(u"spinBox_channel_exposure_time")
        self.spinBox_channel_exposure_time.setDecimals(2)
        self.spinBox_channel_exposure_time.setMinimum(0.000000000000000)
        self.spinBox_channel_exposure_time.setMaximum(999.990000000000009)
        self.spinBox_channel_exposure_time.setValue(10.000000000000000)

        self.horizontalLayout_5.addWidget(self.spinBox_channel_exposure_time)

        self.label_channel_exposure_time = QLabel(Form)
        self.label_channel_exposure_time.setObjectName(u"label_channel_exposure_time")
        self.label_channel_exposure_time.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.label_channel_exposure_time)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.comboBox_illuminator = QComboBox(Form)
        self.comboBox_illuminator.addItem("")
        self.comboBox_illuminator.addItem("")
        self.comboBox_illuminator.addItem("")
        self.comboBox_illuminator.addItem("")
        self.comboBox_illuminator.addItem("")
        self.comboBox_illuminator.addItem("")
        self.comboBox_illuminator.setObjectName(u"comboBox_illuminator")
        self.comboBox_illuminator.setEnabled(True)
        self.comboBox_illuminator.setEditable(False)

        self.horizontalLayout_13.addWidget(self.comboBox_illuminator)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.horizontalLayout_13.addWidget(self.label)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_8)


        self.verticalLayout.addLayout(self.horizontalLayout_13)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout_14.addLayout(self.verticalLayout)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_image_preview = QLabel(Form)
        self.label_image_preview.setObjectName(u"label_image_preview")
        self.label_image_preview.setMinimumSize(QSize(1108, 592))
        self.label_image_preview.setMaximumSize(QSize(2216, 1184))
        palette1 = QPalette()
        brush1 = QBrush(QColor(150, 150, 150, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.Base, brush1)
        palette1.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Base, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        self.label_image_preview.setPalette(palette1)
        self.label_image_preview.setAutoFillBackground(True)

        self.verticalLayout_5.addWidget(self.label_image_preview)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.comboBox_LUT = QComboBox(Form)
        self.comboBox_LUT.addItem("")
        self.comboBox_LUT.addItem("")
        self.comboBox_LUT.setObjectName(u"comboBox_LUT")

        self.horizontalLayout_9.addWidget(self.comboBox_LUT)

        self.comboBox_preview_zoom = QComboBox(Form)
        self.comboBox_preview_zoom.addItem("")
        self.comboBox_preview_zoom.addItem("")
        self.comboBox_preview_zoom.addItem("")
        self.comboBox_preview_zoom.addItem("")
        self.comboBox_preview_zoom.addItem("")
        self.comboBox_preview_zoom.addItem("")
        self.comboBox_preview_zoom.setObjectName(u"comboBox_preview_zoom")

        self.horizontalLayout_9.addWidget(self.comboBox_preview_zoom)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_7)


        self.verticalLayout_4.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.slider_min_grayscale = QSlider(Form)
        self.slider_min_grayscale.setObjectName(u"slider_min_grayscale")
        self.slider_min_grayscale.setMinimum(0)
        self.slider_min_grayscale.setMaximum(4095)
        self.slider_min_grayscale.setPageStep(100)
        self.slider_min_grayscale.setValue(1)
        self.slider_min_grayscale.setOrientation(Qt.Horizontal)

        self.horizontalLayout_8.addWidget(self.slider_min_grayscale)

        self.spinBox_min_grayscale = QSpinBox(Form)
        self.spinBox_min_grayscale.setObjectName(u"spinBox_min_grayscale")
        self.spinBox_min_grayscale.setMaximum(4095)

        self.horizontalLayout_8.addWidget(self.spinBox_min_grayscale)

        self.label_min_grayscale = QLabel(Form)
        self.label_min_grayscale.setObjectName(u"label_min_grayscale")

        self.horizontalLayout_8.addWidget(self.label_min_grayscale)


        self.verticalLayout_2.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.slider_max_grayscale = QSlider(Form)
        self.slider_max_grayscale.setObjectName(u"slider_max_grayscale")
        self.slider_max_grayscale.setMaximum(4095)
        self.slider_max_grayscale.setValue(4095)
        self.slider_max_grayscale.setOrientation(Qt.Horizontal)

        self.horizontalLayout_10.addWidget(self.slider_max_grayscale)

        self.spinBox_max_grayscale = QSpinBox(Form)
        self.spinBox_max_grayscale.setObjectName(u"spinBox_max_grayscale")
        self.spinBox_max_grayscale.setMinimum(1)
        self.spinBox_max_grayscale.setMaximum(4095)
        self.spinBox_max_grayscale.setSingleStep(0)
        self.spinBox_max_grayscale.setValue(4095)

        self.horizontalLayout_10.addWidget(self.spinBox_max_grayscale)

        self.label_max_grayscale = QLabel(Form)
        self.label_max_grayscale.setObjectName(u"label_max_grayscale")

        self.horizontalLayout_10.addWidget(self.label_max_grayscale)


        self.verticalLayout_2.addLayout(self.horizontalLayout_10)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)


        self.horizontalLayout_11.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.pb_minmax_grayscale = QPushButton(Form)
        self.pb_minmax_grayscale.setObjectName(u"pb_minmax_grayscale")

        self.verticalLayout_3.addWidget(self.pb_minmax_grayscale)

        self.pb_auto_grayscale = QPushButton(Form)
        self.pb_auto_grayscale.setObjectName(u"pb_auto_grayscale")

        self.verticalLayout_3.addWidget(self.pb_auto_grayscale)

        self.pb_reset_grayscale = QPushButton(Form)
        self.pb_reset_grayscale.setObjectName(u"pb_reset_grayscale")

        self.verticalLayout_3.addWidget(self.pb_reset_grayscale)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)


        self.horizontalLayout_11.addLayout(self.verticalLayout_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.pb_preview = QPushButton(Form)
        self.pb_preview.setObjectName(u"pb_preview")
        self.pb_preview.setFont(font)

        self.horizontalLayout_7.addWidget(self.pb_preview)

        self.pb_pause_preview = QPushButton(Form)
        self.pb_pause_preview.setObjectName(u"pb_pause_preview")
        self.pb_pause_preview.setFont(font)
        self.pb_pause_preview.setCheckable(True)

        self.horizontalLayout_7.addWidget(self.pb_pause_preview)

        self.pb_stop_preview = QPushButton(Form)
        self.pb_stop_preview.setObjectName(u"pb_stop_preview")
        self.pb_stop_preview.setFont(font)

        self.horizontalLayout_7.addWidget(self.pb_stop_preview)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_5)

        self.pb_snap = QPushButton(Form)
        self.pb_snap.setObjectName(u"pb_snap")
        self.pb_snap.setFont(font)

        self.horizontalLayout_6.addWidget(self.pb_snap)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_6)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)


        self.horizontalLayout_12.addLayout(self.verticalLayout_4)

        self.label_histogram_greyvalue = QLabel(Form)
        self.label_histogram_greyvalue.setObjectName(u"label_histogram_greyvalue")
        self.label_histogram_greyvalue.setMinimumSize(QSize(600, 250))
        palette2 = QPalette()
        palette2.setBrush(QPalette.Active, QPalette.Base, brush)
        palette2.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette2.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette2.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette2.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette2.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        self.label_histogram_greyvalue.setPalette(palette2)
        self.label_histogram_greyvalue.setAutoFillBackground(True)

        self.horizontalLayout_12.addWidget(self.label_histogram_greyvalue)


        self.verticalLayout_5.addLayout(self.horizontalLayout_12)


        self.horizontalLayout_14.addLayout(self.verticalLayout_5)


        self.verticalLayout_6.addLayout(self.horizontalLayout_14)

        self.label_message = QLabel(Form)
        self.label_message.setObjectName(u"label_message")

        self.verticalLayout_6.addWidget(self.label_message)


        self.retranslateUi(Form)
        self.slider_max_grayscale.valueChanged.connect(self.spinBox_max_grayscale.setValue)
        self.spinBox_max_grayscale.valueChanged.connect(self.slider_max_grayscale.setValue)
        self.slider_min_grayscale.valueChanged.connect(self.spinBox_min_grayscale.setValue)
        self.spinBox_min_grayscale.valueChanged.connect(self.slider_min_grayscale.setValue)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_saving.setText(QCoreApplication.translate("Form", u"Saving", None))
        self.label_data_path.setText(QCoreApplication.translate("Form", u"D:/Projets_Python/OPM_GUI/Images", None))
#if QT_CONFIG(tooltip)
        self.pb_data_path.setToolTip(QCoreApplication.translate("Form", u"Select folder where the experiment will be saved", None))
#endif // QT_CONFIG(tooltip)
        self.pb_data_path.setText(QCoreApplication.translate("Form", u"...", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_exp_name.setToolTip(QCoreApplication.translate("Form", u"Set the name of the expetiment", None))
#endif // QT_CONFIG(tooltip)
        self.lineEdit_exp_name.setText(QCoreApplication.translate("Form", u"Image", None))
        self.pb_mirror.setText(QCoreApplication.translate("Form", u"Mirror", None))
        self.label_mirror_icon.setText("")
        self.label_mirror.setText(QCoreApplication.translate("Form", u"OUT", None))
        self.pb_fluo.setText(QCoreApplication.translate("Form", u"Fluorescent", None))
        self.label_fluo_icon.setText("")
        self.label_fluo.setText(QCoreApplication.translate("Form", u"OFF", None))
        self.pb_transmission.setText(QCoreApplication.translate("Form", u"Transmission", None))
        self.label_transmission_icon.setText("")
        self.label_transmission.setText(QCoreApplication.translate("Form", u"OFF", None))
#if QT_CONFIG(tooltip)
        self.spinBox_channel_exposure_time.setToolTip(QCoreApplication.translate("Form", u"Set the exposure time for the 405 nm channel in milliseconds.", None))
#endif // QT_CONFIG(tooltip)
        self.label_channel_exposure_time.setText(QCoreApplication.translate("Form", u"Exposure Time (ms)", None))
        self.comboBox_illuminator.setItemText(0, QCoreApplication.translate("Form", u"1 BFP", None))
        self.comboBox_illuminator.setItemText(1, QCoreApplication.translate("Form", u"2 GFP", None))
        self.comboBox_illuminator.setItemText(2, QCoreApplication.translate("Form", u"3 TexRed", None))
        self.comboBox_illuminator.setItemText(3, QCoreApplication.translate("Form", u"4 Cy3", None))
        self.comboBox_illuminator.setItemText(4, QCoreApplication.translate("Form", u"5 Empty", None))
        self.comboBox_illuminator.setItemText(5, QCoreApplication.translate("Form", u"6 Empty", None))

        self.label.setText(QCoreApplication.translate("Form", u"Filter position", None))
        self.label_image_preview.setText("")
        self.comboBox_LUT.setItemText(0, QCoreApplication.translate("Form", u"Grayscale", None))
        self.comboBox_LUT.setItemText(1, QCoreApplication.translate("Form", u"Saturation", None))

        self.comboBox_preview_zoom.setItemText(0, QCoreApplication.translate("Form", u"Image zoom", None))
        self.comboBox_preview_zoom.setItemText(1, QCoreApplication.translate("Form", u"2x", None))
        self.comboBox_preview_zoom.setItemText(2, QCoreApplication.translate("Form", u"1x", None))
        self.comboBox_preview_zoom.setItemText(3, QCoreApplication.translate("Form", u"1/2x", None))
        self.comboBox_preview_zoom.setItemText(4, QCoreApplication.translate("Form", u"1/3x", None))
        self.comboBox_preview_zoom.setItemText(5, QCoreApplication.translate("Form", u"1/4x", None))

#if QT_CONFIG(tooltip)
        self.slider_min_grayscale.setToolTip(QCoreApplication.translate("Form", u"Set the maximum grey value for image display.\n"
"Pixels above this value will appear white.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_min_grayscale.setToolTip(QCoreApplication.translate("Form", u"Set the minimum grey value for image display.\n"
"Pixels below this value will appear black.", None))
#endif // QT_CONFIG(tooltip)
        self.label_min_grayscale.setText(QCoreApplication.translate("Form", u"Min", None))
#if QT_CONFIG(tooltip)
        self.slider_max_grayscale.setToolTip(QCoreApplication.translate("Form", u"Set the minimum grey value for image display.\n"
"Pixels below this value will appear black.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.spinBox_max_grayscale.setToolTip(QCoreApplication.translate("Form", u"Set the maximum grey value for image display.\n"
"Pixels above this value will appear white.", None))
#endif // QT_CONFIG(tooltip)
        self.label_max_grayscale.setText(QCoreApplication.translate("Form", u"Max", None))
#if QT_CONFIG(tooltip)
        self.pb_minmax_grayscale.setToolTip(QCoreApplication.translate("Form", u"Automatically adjust the minimum and maximum grey values based on the image histogram.", None))
#endif // QT_CONFIG(tooltip)
        self.pb_minmax_grayscale.setText(QCoreApplication.translate("Form", u"Min / Max", None))
#if QT_CONFIG(tooltip)
        self.pb_auto_grayscale.setToolTip(QCoreApplication.translate("Form", u"Automatically adjust the minimum and maximum grey values based on the image histogram.", None))
#endif // QT_CONFIG(tooltip)
        self.pb_auto_grayscale.setText(QCoreApplication.translate("Form", u"Auto", None))
#if QT_CONFIG(tooltip)
        self.pb_reset_grayscale.setToolTip(QCoreApplication.translate("Form", u"Reset the minimum and maximum grey values to their default settings.", None))
#endif // QT_CONFIG(tooltip)
        self.pb_reset_grayscale.setText(QCoreApplication.translate("Form", u"Reset", None))
#if QT_CONFIG(tooltip)
        self.pb_preview.setToolTip(QCoreApplication.translate("Form", u"Start the live preview of the acquisition.", None))
#endif // QT_CONFIG(tooltip)
        self.pb_preview.setText(QCoreApplication.translate("Form", u"Preview", None))
#if QT_CONFIG(tooltip)
        self.pb_pause_preview.setToolTip(QCoreApplication.translate("Form", u"Start the live preview of the acquisition.", None))
#endif // QT_CONFIG(tooltip)
        self.pb_pause_preview.setText(QCoreApplication.translate("Form", u"Pause", None))
#if QT_CONFIG(tooltip)
        self.pb_stop_preview.setToolTip(QCoreApplication.translate("Form", u"Start the live preview of the acquisition.", None))
#endif // QT_CONFIG(tooltip)
        self.pb_stop_preview.setText(QCoreApplication.translate("Form", u"Stop", None))
#if QT_CONFIG(tooltip)
        self.pb_snap.setToolTip(QCoreApplication.translate("Form", u"Start the live preview of the acquisition.", None))
#endif // QT_CONFIG(tooltip)
        self.pb_snap.setText(QCoreApplication.translate("Form", u"Snap", None))
        self.label_histogram_greyvalue.setText("")
        self.label_message.setText("")
    # retranslateUi

