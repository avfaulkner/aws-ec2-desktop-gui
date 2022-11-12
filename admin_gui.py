import os
import sys

from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *




class MainWindow(QMainWindow):
   def __init__(self, parent=None):
      super(MainWindow, self).__init__(parent)
      self.setWindowTitle("Admin State Status")

      # QMainWindow already comes with a layout; create a new widget to use a different one
      self.widget = QWidget(self)
      self.setCentralWidget(self.widget) 

      # Create an outer layout using new widget to contain inner layouts
      outerLayout = QVBoxLayout(self.widget)
      # Create a two column form layout for the label and dropdown menu
      topLayout = QHBoxLayout()
      # Add a label and a combobox to the form layout
      # Drop down menu
      self.comboBox = QComboBox(self)
      self.comboBox.addItems(["C2", "P5", "P6", "P7", "P8", "P9"])
      topLayout.addWidget(QLabel("Select an environment:")) 
      topLayout.addWidget(self.comboBox)
      self.button = QPushButton("Start")
      self.button.pressed.connect(self.start_process)
      topLayout.addWidget(self.button)

      # switch credentials
      self.comboBox.currentIndexChanged.connect(self.dropdown_item)


      # Create a layout for the graphs
      graphsLayout = QHBoxLayout()


      # Add the graphs to the layout
      graphsLayout.addWidget(QMessageBox())
      graphsLayout.addWidget(QMessageBox())

      # Create layout for terminal output
      outputLayout = QVBoxLayout()
      self.text = QPlainTextEdit()
      self.text.setReadOnly(True)
      outputLayout.addWidget(self.text)
   

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

   def message(self, s):
      self.text.appendPlainText(s)

   def start_process(self):
      self.message("Executing process.")
      self.p = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
      self.p.readyReadStandardOutput.connect(self.handle_stdout)
      self.p.readyReadStandardError.connect(self.handle_stderr)
      self.p.stateChanged.connect(self.handle_state)
      self.p.finished.connect(self.process_finished)  # Clean up once complete.
      self.p.start("python3.8.exe", ['admin_state_status.py'])

   def handle_stdout(self):
      data = self.p.readAllStandardOutput()
      stdout = bytes(data).decode("utf8")
      self.message(stdout)

   def handle_stderr(self):
      data = self.p.readAllStandardError()
      stderr = bytes(data).decode("utf8")
      self.message(stderr)

   def handle_state(self, state):
      states = {
         QProcess.NotRunning: 'Not running',
         QProcess.Starting: 'Starting',
         QProcess.Running: 'Running',
      }
      state_name = states[state]
      self.message(f"State changed: {state_name}")

   def process_finished(self):
      self.message("Process finished.")
      self.p = None


   def file_actions(self, q):
      print("triggered")

      if q.text() == "STG account":
         print("switch to stg account")

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
