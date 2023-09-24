# Form implementation generated from reading ui file 'demo1.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

from PySide6 import QtCore, QtGui, QtWidgets
import PySide6.QtGui
from PySide6.QtWidgets import QMessageBox
import Components
import os

class View(QtWidgets.QMainWindow):
    def __init__(self, Model):
        super().__init__()
        self.sched = Components.Scheduler()
        self.model = Model
        self = self
        self.setObjectName("self")
        self.resize(698, 390)
        pixmap = QtGui.QPixmap(os.path.dirname(__file__)+"\icon.ico")
        icon = QtGui.QIcon(pixmap)
        self.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(parent=self)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabs = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabs.setObjectName("tabs")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_1)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.add_btn = QtWidgets.QPushButton(parent=self.tab_1)
        self.add_btn.setObjectName("add_btn")
        self.gridLayout_2.addWidget(self.add_btn, 0, 1, 1, 1)

        self.rmv_btn = QtWidgets.QPushButton(parent=self.tab_1)
        self.rmv_btn.setObjectName("rmv_btn")
        self.gridLayout_2.addWidget(self.rmv_btn, 0, 2, 1, 1)

        self.clr_btn = QtWidgets.QPushButton(parent=self.tab_1)
        self.clr_btn.setObjectName("clr_btn")
        self.gridLayout_2.addWidget(self.clr_btn, 0, 3, 1, 1)

        self.save_btn = QtWidgets.QPushButton(parent=self.tab_1)
        self.save_btn.setObjectName("save_btn")
        self.gridLayout_2.addWidget(self.save_btn, 0, 4, 1, 1)

        self.task_list = QtWidgets.QListWidget(parent=self.tab_1)
        self.task_list.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.task_list.setObjectName("task_list")
        self.gridLayout_2.addWidget(self.task_list, 1, 0, 1, 5)
        self.task_list.setStyleSheet("""
            QListWidget::item:hover {
                background-color:rgba(0,0,0,0.05)
            }
        """)
        self.task_edit = QtWidgets.QLineEdit(parent=self.tab_1)
        self.task_edit.setObjectName("task_edit")
        self.gridLayout_2.addWidget(self.task_edit, 0, 0, 1, 1)
        self.tabs.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.comboBox = Components.CheckableComboBox(parent=self.tab_2)
        self.comboBox.setObjectName("comboBox")

        self.gridLayout_3.addWidget(self.comboBox, 0, 0, 1, 2)
        self.set_btn = QtWidgets.QPushButton(parent=self.tab_2)
        self.set_btn.setObjectName("set_btn")
        self.gridLayout_3.addWidget(self.set_btn, 0, 2, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(0, 0, parent=self.tab_2)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        
        self.gridLayout_3.addWidget(self.tableWidget, 1, 0, 1, 3)
        self.tabs.addTab(self.tab_2, "")
        self.horizontalLayout.addWidget(self.tabs)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 698, 22))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)
    
    def start_scheduler(self, hour, minute):
        self.sched.start(hour, minute)

    def set_data(self, data):
        # print('data:',data)
        for t in data:
            self.add_task_recorder(t,data[t])
    
    def msg_window(self, title='', content='', *, warning=False):
        type = QMessageBox.Warning if warning else QMessageBox.Information
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setIcon(type)
        msg.setText(content)
        msg.exec()
    
    def confirm_window(self, title='', content='', parent=None, *, warning=False):
        type = QMessageBox.Warning if warning else QMessageBox.Information
        msg = QMessageBox()
        # msg.setWindowTitle(title)
        msg.setIcon(type)
        ret = msg.question(parent, title, content)
        if ret == QMessageBox.No:
            return

    def get_new_task_name(self):
        return self.task_edit.text()

    def add_task_recorder(self, task, step=0):
        self.task_edit.clear()
        item = QtWidgets.QListWidgetItem()
        recorder = Components.taskRecorder(self)
        recorder.set_step(step)
        recorder.btn.clicked.connect(lambda:self.start_stop(recorder))
        recorder.renameTask.connect(lambda:self.rename_task(recorder))
        recorder.set_name(str(task))
        self.task_list.addItem(item)
        self.task_list.setItemWidget(item, recorder)
    
    def rename_task(self, recorder):
        print('hi')
        old = recorder.get_name()
        new, ok = QtWidgets.QInputDialog.getText(self, 'Rename', 'New name：')
        if not (ok and new and (new not in self.model.steps)):
            return
        self.model.rename_task(old, new)
        recorder.set_name(new)        
    
    def remove_task(self):
        selected = self.task_list.currentRow()
        if selected < 0:
            self.msg_window("Unselected", "Select one task", True)
            return
        self.confirm_window("Remove?", "This will remove all records of the task", parent=self.tab_2)
        remove = self.task_list.itemWidget(self.task_list.item(selected)).get_name()
        self.task_list.takeItem(selected)
        return remove
    
    def clear_tasks(self):
        self.confirm_window("Clear?", "This will remove all records from the database", self.tab_2)
        self.task_list.clear()
    
    def start_stop(self, recorder):
        if not recorder.timer.isActive():
            recorder.btn.setText('stop')
            recorder.timer.start(1000)
        else:
            recorder.btn.setText('start')
            recorder.timer.stop()
            self.model.update_step(recorder.get_name(), recorder.get_step())
            self.update_ratio()
    
    def update_ratio(self):
        print('self.model', type(self.model))
        max_step = self.model.get_max_step()
        if max_step is None:
            return
        for i in range(self.task_list.count()):
            t = self.task_list.itemWidget(self.task_list.item(i))
            if max_step == 0:
                t.progress.setValue(0)
            else:
                t.progress.setValue(int(100*(float(t.step)/max_step)))

    def update_tasks(self, tasks):
        task_names = [task[1] for task in tasks]
        self.comboBox.clear()
        self.comboBox.addItems(task_names)
    
    def combobox_load_tasks(self, tasks):
        self.comboBox.clear()
        self.comboBox.addItems(tasks)
    
    def get_combobox_selected(self):
        return self.comboBox.currentData()
    
    def show_records(self, tasks, table_data, perc_data, date_total):
        self.tableWidget.setColumnCount(len(tasks)+2)
        self.tableWidget.setRowCount(0)
        if table_data.shape[1] < 10:
            self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        delegate = Components.ProgressDelegate(self.tableWidget)
        for c in range(0, table_data.shape[1]+1):
            self.tableWidget.setItemDelegateForColumn(c+1, delegate)
        self.tableWidget.setHorizontalHeaderLabels(['Date']+tasks+['Total'])
        for r in range(table_data.shape[0]):
            self.tableWidget.insertRow(self.tableWidget.rowCount())
            date_val = QtWidgets.QTableWidgetItem(list(date_total.keys())[r])
            self.tableWidget.setItem(r, 0, date_val)
            for c in range(0, table_data.shape[1]):
                progress = QtWidgets.QTableWidgetItem()
                progress.setData(QtCore.Qt.UserRole+1000, perc_data[r][c])
                m, s = divmod(int(table_data[r][c]), 60)
                h, m = divmod(m, 60)
                progress.setToolTip(f'{h:02d}:{m:02d}:{s:02d}')
                self.tableWidget.setItem(r, c+1, progress)
        
    def reset_table(self):
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

    def saved(self):
        self.msg_window("Succeed", "Records saved into database")
    
    def date_change(self):
        stopped = []
        for i in range(self.task_list.count()):
            recorder = self.task_list.itemWidget(self.task_list.item(i))
            if recorder.timer.isActive():
                recorder.timer.stop()
                self.model.update_step(recorder.get_name(), recorder.get_step())
                stopped.append(recorder.label.text())
            recorder.set_step(0)
            # print(recorder.label.text()+' cleaned')
            # print(recorder.duration.text())
        self.update_ratio()
        # self.task_list.clear()
        return stopped
    
    def date_changed(self, stopped):
        for i in range(self.task_list.count()):
            recorder = self.task_list.itemWidget(self.task_list.item(i))
            if recorder.label.text() in stopped:
                recorder.btn.setText('stop')
                recorder.timer.start(1000)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "TaskMonitor"))
        self.add_btn.setText(_translate("self", "Add"))
        self.clr_btn.setText(_translate("self", "Clear"))
        self.rmv_btn.setText(_translate("self", "Remove"))
        self.save_btn.setText(_translate("self", "Save"))
        self.set_btn.setText(_translate("self", "Set"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_1), _translate("self", "Today"))
        self.tabs.setTabText(self.tabs.indexOf(self.tab_2), _translate("self", "Across days"))

    def attach2controller(self, controller):
        self.add_btn.clicked.connect(controller.add_task)
        self.clr_btn.clicked.connect(controller.clear_tasks)
        self.rmv_btn.clicked.connect(controller.remove_task)
        self.save_btn.clicked.connect(controller.save_records)
        self.set_btn.clicked.connect(controller.show_records)
        self.comboBox.popupAboutToBeShown.connect(controller.load_combobox)
        self.sched.dateChanges.connect(controller.date_change)
    
    def closeEvent(self, event):
        msg = QMessageBox()
        msg.addButton(QMessageBox.Yes)
        msg.addButton(QMessageBox.No)
        msg.addButton(QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        msg.button(QMessageBox.Cancel).setVisible(False)
        msg.setWindowTitle("Save?")
        msg.setIcon(QMessageBox.Question)
        msg.setText("You want to save?")
        reply = msg.exec()
        
        if reply == QMessageBox.Yes:
            self.model.save_records()
            event.accept()
        elif reply == QMessageBox.No:
            event.accept()
        else:
            event.ignore()
            return
        super(View, self).closeEvent(event)
        