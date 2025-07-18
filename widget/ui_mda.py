# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_mda.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QProgressBar, QPushButton, QSizePolicy,
    QSlider, QSpacerItem, QSpinBox, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1007, 1156)
        self.verticalLayout_4 = QVBoxLayout(Form)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_timeline = QLabel(Form)
        self.label_timeline.setObjectName(u"label_timeline")
        self.label_timeline.setMinimumSize(QSize(640, 128))
        self.label_timeline.setMaximumSize(QSize(16777215, 128))
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        brush1 = QBrush(QColor(76, 76, 76, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        self.label_timeline.setPalette(palette)
        self.label_timeline.setAutoFillBackground(True)
        self.label_timeline.setScaledContents(True)
        self.label_timeline.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.label_timeline)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer = QSpacerItem(108, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer)

        self.slider_timeline = QSlider(Form)
        self.slider_timeline.setObjectName(u"slider_timeline")
        self.slider_timeline.setMinimum(1)
        self.slider_timeline.setMaximum(2)
        self.slider_timeline.setOrientation(Qt.Horizontal)

        self.horizontalLayout_8.addWidget(self.slider_timeline)

        self.sb_timeline = QSpinBox(Form)
        self.sb_timeline.setObjectName(u"sb_timeline")
        self.sb_timeline.setMinimum(1)
        self.sb_timeline.setMaximum(2)

        self.horizontalLayout_8.addWidget(self.sb_timeline)

        self.horizontalSpacer_2 = QSpacerItem(118, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_8)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_4.addWidget(self.line)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_mainImage = QLabel(Form)
        self.label_mainImage.setObjectName(u"label_mainImage")
        self.label_mainImage.setMinimumSize(QSize(512, 256))
        palette1 = QPalette()
        palette1.setBrush(QPalette.Active, QPalette.Base, brush)
        palette1.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette1.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        self.label_mainImage.setPalette(palette1)
        self.label_mainImage.setAutoFillBackground(True)
        self.label_mainImage.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_mainImage)

        self.label_Image_side = QLabel(Form)
        self.label_Image_side.setObjectName(u"label_Image_side")
        self.label_Image_side.setMinimumSize(QSize(128, 256))
        palette2 = QPalette()
        palette2.setBrush(QPalette.Active, QPalette.Base, brush)
        palette2.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette2.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette2.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette2.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette2.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        self.label_Image_side.setPalette(palette2)
        self.label_Image_side.setAutoFillBackground(True)
        self.label_Image_side.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_Image_side)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.cb_projection = QComboBox(Form)
        self.cb_projection.addItem("")
        self.cb_projection.addItem("")
        self.cb_projection.setObjectName(u"cb_projection")

        self.horizontalLayout_6.addWidget(self.cb_projection)

        self.cb_lut = QComboBox(Form)
        self.cb_lut.addItem("")
        self.cb_lut.setObjectName(u"cb_lut")

        self.horizontalLayout_6.addWidget(self.cb_lut)

        self.cb_image_zoom = QComboBox(Form)
        self.cb_image_zoom.addItem("")
        self.cb_image_zoom.setObjectName(u"cb_image_zoom")

        self.horizontalLayout_6.addWidget(self.cb_image_zoom)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.slider_image_channel = QSlider(Form)
        self.slider_image_channel.setObjectName(u"slider_image_channel")
        self.slider_image_channel.setOrientation(Qt.Horizontal)

        self.horizontalLayout_9.addWidget(self.slider_image_channel)

        self.cb_image_channel = QComboBox(Form)
        self.cb_image_channel.addItem("")
        self.cb_image_channel.addItem("")
        self.cb_image_channel.addItem("")
        self.cb_image_channel.addItem("")
        self.cb_image_channel.setObjectName(u"cb_image_channel")

        self.horizontalLayout_9.addWidget(self.cb_image_channel)


        self.verticalLayout_3.addLayout(self.horizontalLayout_9)

        self.line_2 = QFrame(Form)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.slider_grayscale_min = QSlider(Form)
        self.slider_grayscale_min.setObjectName(u"slider_grayscale_min")
        self.slider_grayscale_min.setMaximum(65535)
        self.slider_grayscale_min.setOrientation(Qt.Horizontal)

        self.horizontalLayout_2.addWidget(self.slider_grayscale_min)

        self.sb_grayscale_min = QSpinBox(Form)
        self.sb_grayscale_min.setObjectName(u"sb_grayscale_min")
        self.sb_grayscale_min.setMaximum(65534)

        self.horizontalLayout_2.addWidget(self.sb_grayscale_min)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.slider_grayscale_max = QSlider(Form)
        self.slider_grayscale_max.setObjectName(u"slider_grayscale_max")
        self.slider_grayscale_max.setMaximum(65535)
        self.slider_grayscale_max.setValue(65535)
        self.slider_grayscale_max.setOrientation(Qt.Horizontal)

        self.horizontalLayout_3.addWidget(self.slider_grayscale_max)

        self.sb_grayscale_max = QSpinBox(Form)
        self.sb_grayscale_max.setObjectName(u"sb_grayscale_max")
        self.sb_grayscale_max.setMinimum(1)
        self.sb_grayscale_max.setMaximum(65535)
        self.sb_grayscale_max.setValue(65535)

        self.horizontalLayout_3.addWidget(self.sb_grayscale_max)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_4.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pb_grayscale_min_max = QPushButton(Form)
        self.pb_grayscale_min_max.setObjectName(u"pb_grayscale_min_max")

        self.verticalLayout.addWidget(self.pb_grayscale_min_max)

        self.pb_grayscale_auto = QPushButton(Form)
        self.pb_grayscale_auto.setObjectName(u"pb_grayscale_auto")

        self.verticalLayout.addWidget(self.pb_grayscale_auto)

        self.pb_grayscale_reset = QPushButton(Form)
        self.pb_grayscale_reset.setObjectName(u"pb_grayscale_reset")

        self.verticalLayout.addWidget(self.pb_grayscale_reset)


        self.horizontalLayout_4.addLayout(self.verticalLayout)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.line_3 = QFrame(Form)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pb_hold = QPushButton(Form)
        self.pb_hold.setObjectName(u"pb_hold")

        self.horizontalLayout_5.addWidget(self.pb_hold)

        self.pb_pause = QPushButton(Form)
        self.pb_pause.setObjectName(u"pb_pause")

        self.horizontalLayout_5.addWidget(self.pb_pause)

        self.pb_stop = QPushButton(Form)
        self.pb_stop.setObjectName(u"pb_stop")

        self.horizontalLayout_5.addWidget(self.pb_stop)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)


        self.horizontalLayout_11.addLayout(self.verticalLayout_3)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_informations = QLabel(Form)
        self.label_informations.setObjectName(u"label_informations")
        self.label_informations.setMinimumSize(QSize(128, 128))
        self.label_informations.setAutoFillBackground(True)
        self.label_informations.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_7.addWidget(self.label_informations)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.progressBar_acquisition = QProgressBar(Form)
        self.progressBar_acquisition.setObjectName(u"progressBar_acquisition")
        self.progressBar_acquisition.setValue(24)

        self.horizontalLayout_10.addWidget(self.progressBar_acquisition)

        self.label_progress_acquisition = QLabel(Form)
        self.label_progress_acquisition.setObjectName(u"label_progress_acquisition")

        self.horizontalLayout_10.addWidget(self.label_progress_acquisition)


        self.verticalLayout_6.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.progressBar_saving = QProgressBar(Form)
        self.progressBar_saving.setObjectName(u"progressBar_saving")
        self.progressBar_saving.setValue(24)

        self.horizontalLayout_7.addWidget(self.progressBar_saving)

        self.label_progress_saving = QLabel(Form)
        self.label_progress_saving.setObjectName(u"label_progress_saving")

        self.horizontalLayout_7.addWidget(self.label_progress_saving)


        self.verticalLayout_6.addLayout(self.horizontalLayout_7)


        self.verticalLayout_7.addLayout(self.verticalLayout_6)


        self.horizontalLayout_11.addLayout(self.verticalLayout_7)


        self.verticalLayout_4.addLayout(self.horizontalLayout_11)


        self.retranslateUi(Form)
        self.slider_timeline.valueChanged.connect(self.sb_timeline.setValue)
        self.slider_grayscale_min.valueChanged.connect(self.sb_grayscale_min.setValue)
        self.slider_grayscale_max.valueChanged.connect(self.sb_grayscale_max.setValue)
        self.sb_grayscale_max.valueChanged.connect(self.slider_grayscale_max.setValue)
        self.sb_grayscale_min.valueChanged.connect(self.slider_grayscale_min.setValue)
        self.sb_timeline.valueChanged.connect(self.slider_timeline.setValue)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
#if QT_CONFIG(tooltip)
        self.label_timeline.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Preview of central slices across time.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_timeline.setText(QCoreApplication.translate("Form", u"Timeline", None))
#if QT_CONFIG(tooltip)
        self.slider_timeline.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Navigate through time to display a specific volume.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.sb_timeline.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Navigate through time to display a specific volume.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_mainImage.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Displays the latest acquired volume (center slice).</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_mainImage.setText(QCoreApplication.translate("Form", u"Image Display", None))
#if QT_CONFIG(tooltip)
        self.label_Image_side.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Shows a side projection (XZ or YZ) of the center of the volume.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_Image_side.setText(QCoreApplication.translate("Form", u"Image\n"
"Side", None))
        self.cb_projection.setItemText(0, QCoreApplication.translate("Form", u"Mean", None))
        self.cb_projection.setItemText(1, QCoreApplication.translate("Form", u"Maximum", None))

        self.cb_lut.setItemText(0, QCoreApplication.translate("Form", u"Grayscale", None))

        self.cb_image_zoom.setItemText(0, QCoreApplication.translate("Form", u"zoom", None))

#if QT_CONFIG(tooltip)
        self.cb_image_zoom.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Set zoom level for image display.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.slider_image_channel.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Select the active channel to display.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.cb_image_channel.setItemText(0, QCoreApplication.translate("Form", u"channel", None))
        self.cb_image_channel.setItemText(1, QCoreApplication.translate("Form", u"BFP", None))
        self.cb_image_channel.setItemText(2, QCoreApplication.translate("Form", u"GFP", None))
        self.cb_image_channel.setItemText(3, QCoreApplication.translate("Form", u"RFP", None))

#if QT_CONFIG(tooltip)
        self.cb_image_channel.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Select the active channel to display.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.slider_grayscale_min.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Adjust minimum grey level for image display.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.sb_grayscale_min.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Adjust minimum grey level for image display.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.slider_grayscale_max.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Adjust maximum grey level for image display.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.sb_grayscale_max.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Adjust maximum grey level for image display.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pb_grayscale_min_max.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Set grey levels to minimum and maximum of the image</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_grayscale_min_max.setText(QCoreApplication.translate("Form", u"Min / Max", None))
#if QT_CONFIG(tooltip)
        self.pb_grayscale_auto.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Automatically adjust grey levels based on image histogram.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_grayscale_auto.setText(QCoreApplication.translate("Form", u"Auto", None))
#if QT_CONFIG(tooltip)
        self.pb_grayscale_reset.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Reset grey levels to default values.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_grayscale_reset.setText(QCoreApplication.translate("Form", u"Reset", None))
#if QT_CONFIG(tooltip)
        self.pb_hold.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Freeze current image display (do not update with new volumes).</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_hold.setText(QCoreApplication.translate("Form", u"Hold", None))
#if QT_CONFIG(tooltip)
        self.pb_pause.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Pause acquisition.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_pause.setText(QCoreApplication.translate("Form", u"Pause", None))
#if QT_CONFIG(tooltip)
        self.pb_stop.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Stop acquisition safely and save current data.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_stop.setText(QCoreApplication.translate("Form", u"stop", None))
#if QT_CONFIG(tooltip)
        self.label_informations.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Displays acquisition status, elapsed time, number of volumes and images.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_informations.setText(QCoreApplication.translate("Form", u"Informations", None))
#if QT_CONFIG(tooltip)
        self.progressBar_acquisition.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Indicates image acquisition progress. Green = running, Gray = paused.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_progress_acquisition.setText(QCoreApplication.translate("Form", u"Image Acquisition", None))
#if QT_CONFIG(tooltip)
        self.progressBar_saving.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Indicates saving progress. Green = running, Gray = paused.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_progress_saving.setText(QCoreApplication.translate("Form", u"Volume Saving    ", None))
    # retranslateUi

