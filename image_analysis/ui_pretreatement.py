# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_pretreatement.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
    QProgressBar, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(673, 515)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pb_select_folder = QPushButton(Form)
        self.pb_select_folder.setObjectName(u"pb_select_folder")
        self.pb_select_folder.setMinimumSize(QSize(100, 32))

        self.horizontalLayout.addWidget(self.pb_select_folder)

        self.pb_detect_files = QPushButton(Form)
        self.pb_detect_files.setObjectName(u"pb_detect_files")
        self.pb_detect_files.setMinimumSize(QSize(100, 32))

        self.horizontalLayout.addWidget(self.pb_detect_files)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label_folder = QLabel(Form)
        self.label_folder.setObjectName(u"label_folder")

        self.verticalLayout.addWidget(self.label_folder)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pb_start_MDAdeskew = QPushButton(Form)
        self.pb_start_MDAdeskew.setObjectName(u"pb_start_MDAdeskew")
        self.pb_start_MDAdeskew.setMinimumSize(QSize(75, 48))

        self.horizontalLayout_2.addWidget(self.pb_start_MDAdeskew)

        self.label_spacer = QLabel(Form)
        self.label_spacer.setObjectName(u"label_spacer")
        self.label_spacer.setMinimumSize(QSize(32, 48))
        self.label_spacer.setMaximumSize(QSize(32, 16777215))

        self.horizontalLayout_2.addWidget(self.label_spacer)

        self.pb_start_LS3deskew = QPushButton(Form)
        self.pb_start_LS3deskew.setObjectName(u"pb_start_LS3deskew")
        self.pb_start_LS3deskew.setMinimumSize(QSize(75, 48))

        self.horizontalLayout_2.addWidget(self.pb_start_LS3deskew)

        self.label_spacer_2 = QLabel(Form)
        self.label_spacer_2.setObjectName(u"label_spacer_2")
        self.label_spacer_2.setMinimumSize(QSize(32, 48))
        self.label_spacer_2.setMaximumSize(QSize(32, 16777215))

        self.horizontalLayout_2.addWidget(self.label_spacer_2)

        self.pb_ZARRconvert = QPushButton(Form)
        self.pb_ZARRconvert.setObjectName(u"pb_ZARRconvert")
        self.pb_ZARRconvert.setMinimumSize(QSize(75, 48))

        self.horizontalLayout_2.addWidget(self.pb_ZARRconvert)

        self.pb_start_LS3deskew_ZARR = QPushButton(Form)
        self.pb_start_LS3deskew_ZARR.setObjectName(u"pb_start_LS3deskew_ZARR")
        self.pb_start_LS3deskew_ZARR.setMinimumSize(QSize(75, 48))

        self.horizontalLayout_2.addWidget(self.pb_start_LS3deskew_ZARR)

        self.pb_TIFFconvert = QPushButton(Form)
        self.pb_TIFFconvert.setObjectName(u"pb_TIFFconvert")
        self.pb_TIFFconvert.setMinimumSize(QSize(75, 48))

        self.horizontalLayout_2.addWidget(self.pb_TIFFconvert)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.cb_only_deskew = QCheckBox(Form)
        self.cb_only_deskew.setObjectName(u"cb_only_deskew")
        self.cb_only_deskew.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_3.addWidget(self.cb_only_deskew)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_7)

        self.cb_try_no_ZARR = QCheckBox(Form)
        self.cb_try_no_ZARR.setObjectName(u"cb_try_no_ZARR")
        self.cb_try_no_ZARR.setMinimumSize(QSize(100, 0))
        self.cb_try_no_ZARR.setChecked(False)

        self.horizontalLayout_3.addWidget(self.cb_try_no_ZARR)

        self.cb_delete_zarr = QCheckBox(Form)
        self.cb_delete_zarr.setObjectName(u"cb_delete_zarr")
        self.cb_delete_zarr.setMinimumSize(QSize(100, 0))
        self.cb_delete_zarr.setChecked(False)

        self.horizontalLayout_3.addWidget(self.cb_delete_zarr)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_8)

        self.sb_max_z = QSpinBox(Form)
        self.sb_max_z.setObjectName(u"sb_max_z")
        self.sb_max_z.setMinimum(50)
        self.sb_max_z.setMaximum(999)
        self.sb_max_z.setValue(200)

        self.horizontalLayout_3.addWidget(self.sb_max_z)

        self.label_lax_z = QLabel(Form)
        self.label_lax_z.setObjectName(u"label_lax_z")

        self.horizontalLayout_3.addWidget(self.label_lax_z)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_5)

        self.pb_stop = QPushButton(Form)
        self.pb_stop.setObjectName(u"pb_stop")
        self.pb_stop.setMinimumSize(QSize(64, 32))

        self.horizontalLayout_4.addWidget(self.pb_stop)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_6)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.label_parameters = QLabel(Form)
        self.label_parameters.setObjectName(u"label_parameters")
        self.label_parameters.setMinimumSize(QSize(128, 64))

        self.verticalLayout.addWidget(self.label_parameters)

        self.progressBar_folder = QProgressBar(Form)
        self.progressBar_folder.setObjectName(u"progressBar_folder")
        self.progressBar_folder.setMinimumSize(QSize(256, 0))
        self.progressBar_folder.setValue(24)

        self.verticalLayout.addWidget(self.progressBar_folder)

        self.progressBar_actual_step = QProgressBar(Form)
        self.progressBar_actual_step.setObjectName(u"progressBar_actual_step")
        self.progressBar_actual_step.setMinimumSize(QSize(256, 0))
        self.progressBar_actual_step.setValue(24)

        self.verticalLayout.addWidget(self.progressBar_actual_step)

        self.verticalSpacer = QSpacerItem(20, 187, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
#if QT_CONFIG(tooltip)
        self.pb_select_folder.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Select the folder where data will be processed</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_select_folder.setText(QCoreApplication.translate("Form", u"Select folder", None))
#if QT_CONFIG(tooltip)
        self.pb_detect_files.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Automatically detect files to process in the selected folder</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_detect_files.setText(QCoreApplication.translate("Form", u"Detect files", None))
        self.label_folder.setText(QCoreApplication.translate("Form", u"folder", None))
#if QT_CONFIG(tooltip)
        self.pb_start_MDAdeskew.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Process images if an MDA experiment is detected</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_start_MDAdeskew.setText(QCoreApplication.translate("Form", u"MDA\n"
"deskewing", None))
        self.label_spacer.setText("")
#if QT_CONFIG(tooltip)
        self.pb_start_LS3deskew.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Entirely process images if an LS3 experiment is detected</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_start_LS3deskew.setText(QCoreApplication.translate("Form", u"LS3\n"
"deskewing", None))
        self.label_spacer_2.setText("")
#if QT_CONFIG(tooltip)
        self.pb_ZARRconvert.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Convert TIFF images to Zarr format</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_ZARRconvert.setText(QCoreApplication.translate("Form", u"ZARR\n"
"conversion", None))
#if QT_CONFIG(tooltip)
        self.pb_start_LS3deskew_ZARR.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Apply deskewing to Zarr images</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_start_LS3deskew_ZARR.setText(QCoreApplication.translate("Form", u"Deskewing", None))
#if QT_CONFIG(tooltip)
        self.pb_TIFFconvert.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Convert processed Zarr images to TIFF</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_TIFFconvert.setText(QCoreApplication.translate("Form", u"TIFF\n"
"conversion", None))
#if QT_CONFIG(tooltip)
        self.cb_only_deskew.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Apply deskewing only (skip rotation step)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.cb_only_deskew.setText(QCoreApplication.translate("Form", u"Only deskew", None))
#if QT_CONFIG(tooltip)
        self.cb_try_no_ZARR.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Skip Zarr conversion for small datasets (faster processing)</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.cb_try_no_ZARR.setText(QCoreApplication.translate("Form", u"skip zarr conversion", None))
#if QT_CONFIG(tooltip)
        self.cb_delete_zarr.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Delete intermediate Zarr files after processing</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.cb_delete_zarr.setText(QCoreApplication.translate("Form", u"delete zarr", None))
#if QT_CONFIG(tooltip)
        self.sb_max_z.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Maximum number of Z planes per output TIFF file</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_lax_z.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Maximum number of Z planes per output TIFF file</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_lax_z.setText(QCoreApplication.translate("Form", u"Maximum z planes", None))
#if QT_CONFIG(tooltip)
        self.pb_stop.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Stop the current process</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pb_stop.setText(QCoreApplication.translate("Form", u"STOP", None))
        self.label_parameters.setText(QCoreApplication.translate("Form", u"MDA detected", None))
    # retranslateUi

