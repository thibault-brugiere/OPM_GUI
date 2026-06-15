# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_multi_position.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QHeaderView,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1163, 654)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_serial_port = QLabel(Form)
        self.label_serial_port.setObjectName(u"label_serial_port")

        self.horizontalLayout.addWidget(self.label_serial_port)

        self.comboBox_devices = QComboBox(Form)
        self.comboBox_devices.setObjectName(u"comboBox_devices")

        self.horizontalLayout.addWidget(self.comboBox_devices)

        self.label_connection = QLabel(Form)
        self.label_connection.setObjectName(u"label_connection")
        self.label_connection.setMinimumSize(QSize(91, 18))

        self.horizontalLayout.addWidget(self.label_connection)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.pb_save = QPushButton(Form)
        self.pb_save.setObjectName(u"pb_save")

        self.horizontalLayout.addWidget(self.pb_save)

        self.pb_load = QPushButton(Form)
        self.pb_load.setObjectName(u"pb_load")

        self.horizontalLayout.addWidget(self.pb_load)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pb_add_position = QPushButton(Form)
        self.pb_add_position.setObjectName(u"pb_add_position")

        self.horizontalLayout_2.addWidget(self.pb_add_position)

        self.pb_remove_all_positions = QPushButton(Form)
        self.pb_remove_all_positions.setObjectName(u"pb_remove_all_positions")

        self.horizontalLayout_2.addWidget(self.pb_remove_all_positions)

        self.pb_sort_snake = QPushButton(Form)
        self.pb_sort_snake.setObjectName(u"pb_sort_snake")

        self.horizontalLayout_2.addWidget(self.pb_sort_snake)

        self.pb_sort_nearest = QPushButton(Form)
        self.pb_sort_nearest.setObjectName(u"pb_sort_nearest")

        self.horizontalLayout_2.addWidget(self.pb_sort_nearest)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.table_positions = QTableWidget(Form)
        if (self.table_positions.columnCount() < 10):
            self.table_positions.setColumnCount(10)
        __qtablewidgetitem = QTableWidgetItem()
        self.table_positions.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table_positions.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table_positions.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table_positions.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.table_positions.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.table_positions.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.table_positions.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.table_positions.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.table_positions.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.table_positions.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        self.table_positions.setObjectName(u"table_positions")

        self.verticalLayout.addWidget(self.table_positions)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_serial_port.setText(QCoreApplication.translate("Form", u"Serial Port", None))
#if QT_CONFIG(tooltip)
        self.comboBox_devices.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Select the serial port to which the piezo controller is connected.</p><p>Ensure the correct port is chosen for proper communication</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_connection.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Indicates whether the piezo controller is successfully connected via the selected port.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_connection.setText(QCoreApplication.translate("Form", u"Not Connected", None))
        self.pb_save.setText(QCoreApplication.translate("Form", u"save", None))
        self.pb_load.setText(QCoreApplication.translate("Form", u"Load", None))
        self.pb_add_position.setText(QCoreApplication.translate("Form", u"Add Position", None))
        self.pb_remove_all_positions.setText(QCoreApplication.translate("Form", u"Remove All", None))
        self.pb_sort_snake.setText(QCoreApplication.translate("Form", u"Snake Sort", None))
        self.pb_sort_nearest.setText(QCoreApplication.translate("Form", u"Nearest sort", None))
        ___qtablewidgetitem = self.table_positions.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"Enabled", None));
        ___qtablewidgetitem1 = self.table_positions.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"Name", None));
        ___qtablewidgetitem2 = self.table_positions.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"XPosition", None));
        ___qtablewidgetitem3 = self.table_positions.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"YPosition", None));
        ___qtablewidgetitem4 = self.table_positions.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Form", u"ZPosition", None));
        ___qtablewidgetitem5 = self.table_positions.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Form", u"Up", None));
        ___qtablewidgetitem6 = self.table_positions.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Form", u"Down", None));
        ___qtablewidgetitem7 = self.table_positions.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Form", u"Move to", None));
        ___qtablewidgetitem8 = self.table_positions.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Form", u"Reset", None));
        ___qtablewidgetitem9 = self.table_positions.horizontalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Form", u"Remove", None));
    # retranslateUi

