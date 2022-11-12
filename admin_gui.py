import os
import sys

from PyQt5 import QtCore, QtGui

# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

#UPDATED HERE: C:\Users\annie\OneDrive\codes

class layout(QWidget):
   def __init__(self, parent=None):
      super(MainWindow, self).__init__(parent)
      
   


class MainWindow(QMainWindow):
   def __init__(self, parent=None):
      super(MainWindow, self).__init__(parent)
      self.setWindowTitle("Admin State Status")
      self.left = 200
      self.top = 200
      self.width = 320
      self.height = 200
      self.setGeometry(self.left, self.top, self.width, self.height)
      # self.mdi = QMdiArea()
      # self.setCentralWidget(self.mdi)
      # layout = QHBoxLayout()
      # self.setLayout(layout)

      # QMainWindow already comes with a layout; create a new widget to use a different one
      self.widget = QWidget(self)
      self.setCentralWidget(self.widget) 
      # layout = QHBoxLayout(self.widget)
      # layout.addItem(QSpacerItem(139, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
      # vlay = QVBoxLayout()
      # vlay.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
      # layout.addLayout(vlay)
      # layout.addItem(QSpacerItem(139, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

      # Create an outer layout using new widget to contain inner layouts
      outerLayout = QVBoxLayout(self.widget)
      # Create a two column form layout for the label and dropdown menu
      topLayout = QFormLayout()
      # Add a label and a combobox to the form layout
      # Drop down menu
      self.comboBox = QComboBox(self)
      self.comboBox.addItems(["C2", "P5", "P6", "P7", "P8", "P9"])
      self.comboBox.currentIndexChanged.connect(self.dropdown_item)
      # vlay.addWidget(self.comboBox)
      # vlay.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
      topLayout.addRow("Select an environment:", self.comboBox)

      # Create a layout for the graphs
      graphsLayout = QHBoxLayout()

      # Add the graphs to the layout
      graphsLayout.addWidget(QMessageBox())
      graphsLayout.addWidget(QMessageBox())

      # Create layout for terminal output
      outputLayout = QVBoxLayout()
      outputLayout.addWidget(QMessageBox())

      # Nest the inner layouts into the outer layout
      outerLayout.addLayout(topLayout)
      outerLayout.addLayout(graphsLayout)
      outerLayout.addLayout(outputLayout)
      # Set the window's main layout
      self.setLayout(outerLayout)

      # menu bar
      bar = self.menuBar()
      file = bar.addMenu("File")
      file.addAction("STG account")  # switch between stg and prod accounts
      file.addAction("PROD account")
      file.addAction("China account")
      file.addAction("Add New Account")  # enter new credentials for new account
      file.addAction("Manage Accounts")  # modify credentials for an account
      file.addAction("Quit")
      file.triggered[QAction].connect(self.file_actions)

      help = bar.addMenu("Help")
      help.addAction("About")
      help.triggered[QAction].connect(self.help_actions)

   def file_actions(self, q):
      print("triggered")

      if q.text() == "STG account":
         print("switch to stg account")
         # sub = QMdiSubWindow()
         # sub.setWidget(QTextEdit())
         # sub.setWindowTitle("subwindow"+str(MainWindow.count))
         # self.mdi.addSubWindow(sub)
         # sub.show()

      if q.text() == "PROD account":
         print("switch to prod account")

      if q.text() == "China account":
         print("switch to China account")

      if q.text() == "Add New Account":
         print("open dialogue box to add new account creds")

      if q.text() == "Manage Accounts":
         print("open dialogue box to modify existing account creds")

      if q.text() == "Quit":
         print("Quit program")

   def help_actions(self, q):
      print("triggered")
      if q.text() == "About":
         dlg = QDialog()
         message = "Admin State Status\n \
               This script will query AWS for EC2 instances which have the slumbering-admin=true and t_role=Admin tags and are in\n \
               the running or stopped state."
         b1 = QLabel(message, dlg)
         b1.move(50, 50)
         dlg.setWindowTitle("Dialog")
         dlg.setWindowModality(QtCore.Qt.ApplicationModal) #dialogue cannot be bypassed; must be closed
         dlg.exec_()

   def dropdown_item(self, item):
      option = self.comboBox.currentText()
      print(f"export aws creds and region for {option}")


def main():
   app = QApplication(sys.argv)  # run application
   ex = MainWindow()
   ex.show()
   sys.exit(app.exec_())  # exit application

if __name__ == "__main__":
    main()
