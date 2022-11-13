import os
import sys

from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import random
from admin_state_status import *




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
      # switch credentials
      self.comboBox.currentIndexChanged.connect(self.dropdown_item)

      self.button = QPushButton("Start")
      self.button.pressed.connect(self.start_process)
      topLayout.addWidget(self.button)


      # Create a layout for the graphs
      graphsLayout = QHBoxLayout()


      # Add the graphs to the layout
      graphsLayout.addWidget(QMessageBox())

      # # graphsLayout.addWidget(self.toolbar)
      graphsLayout.addWidget(Graphs())


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

   # send message data to gui textbox
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
         self.message("switch to stg account")

      if q.text() == "PROD account":
         self.message("switch to prod account")

      if q.text() == "China account":
         self.message("switch to China account")

      if q.text() == "Add New Account":
         self.message("open dialogue box to add new account creds")

      if q.text() == "Manage Accounts":
         self.message("open dialogue box to modify existing account creds")

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
      message = f"export aws creds and region for {option}"
      self.message(message)

      
class Graphs(QDialog):
      
    # constructor
    def __init__(self, parent=None):
        super(Graphs, self).__init__(parent)
  
        # a figure instance to plot on
        self.figure = plt.figure()
  
        # this is the Canvas Widget that
        # displays the 'figure'it takes the
        # 'figure' instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
  
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)
  
        # Just some button connected to 'plot' method
        self.button = QPushButton('Plot')
          
        # adding action to the button
        self.button.clicked.connect(self.plot) ##########################################################
  
        # creating a Vertical Box layout
        layout = QVBoxLayout()
          
        # adding tool bar to the layout
        layout.addWidget(self.toolbar)
          
        # adding canvas to the layout
        layout.addWidget(self.canvas)
          
        # adding push button to the layout
        layout.addWidget(self.button)
          
        # setting layout to the main window
        self.setLayout(layout)
  
    # action called by the push button
    def plot(self):
          
        # random data
        data = [bar_graph_running("admins_running.csv")]
        plt.show()
      #   bar_graph_running("admins_running.csv")
  
      #   # clearing old figure
      #   self.figure.clear()
  
      #   # create an axis
      #   ax = self.figure.add_subplot(111)
  
      #   # plot data
      #   ax.plot(data, '*-')
  
        # refresh canvas
        self.canvas.draw()


def main():
   app = QApplication(sys.argv)  # run application
   ex = MainWindow()
   ex.show()
   sys.exit(app.exec_())  # exit application

if __name__ == "__main__":
    main()
