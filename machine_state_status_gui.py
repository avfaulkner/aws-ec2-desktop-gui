import os
import sys

from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import random
from machine_state_status import *




class MainWindow(QMainWindow):
   def __init__(self, parent=None):
      super(MainWindow, self).__init__(parent)
      self.setWindowTitle("machine State Status")

      # QMainWindow already comes with a layout; create a new widget to use a different one
      self.widget = QWidget(self)
      self.setCentralWidget(self.widget) 

      # Create an outer layout using new widget to contain inner layouts
      self.outerLayout = QVBoxLayout(self.widget)
      # Create a two column form layout for the label and dropdown menu
      self.topLayout = QVBoxLayout()
      # Add a label and a combobox to the form layout
      # Drop down menu
      self.comboBox = QComboBox(self)
      self.comboBox.addItems(["C2", "P5", "P6", "P7", "P8", "P9"])
      self.topLayout.addWidget(QLabel("Select an environment:")) 
      self.topLayout.addWidget(self.comboBox)
      # switch credentials
      self.comboBox.currentIndexChanged.connect(self.dropdown_item)

      self.button = QPushButton("Start")
      self.button.pressed.connect(self.start_process)
      self.topLayout.addWidget(self.button)


      # Create a layout for the graphs
      self.graphsLayout = QHBoxLayout()
      # Add the graphs to the layout
      self.graphsLayout.addWidget(Graphs())
      self.graphsLayout.addWidget(Graphs2())


      # Create layout for terminal output
      self.outputLayout = QVBoxLayout()
      self.text = QPlainTextEdit()
      self.text.setReadOnly(True)
      self.outputLayout.addWidget(self.text)
   

      # Nest the inner layouts into the outer layout
      self.outerLayout.addLayout(self.topLayout)
      self.outerLayout.addLayout(self.graphsLayout)
      self.outerLayout.addLayout(self.outputLayout)
      # Set the window's main layout
      self.setLayout(self.outerLayout)

      # menu bar
      self.bar = self.menuBar()
      self.file = self.bar.addMenu("File")
      self.file.addAction("STG account")  # switch between stg and prod accounts
      self.file.addAction("PROD account")
      self.file.addAction("China account")
      self.file.addAction("Add New Account")  # enter new credentials for new account
      self.file.addAction("Manage Accounts")  # modify credentials for an account
      self.file.addAction("Quit")
      self.file.triggered[QAction].connect(self.file_actions)

      self.help = self.bar.addMenu("Help")
      self.help.addAction("About")
      self.help.triggered[QAction].connect(self.help_actions)

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
      self.p.start("python3.8.exe", ['machine_state_status.py'])
      


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
         message = "machine State Status\n \
               This script will query AWS for EC2 instances which have the slumbering-machine=true and t_role=machine tags and are in\n \
               the running or stopped state."
         b1 = QLabel(message, dlg)
         b1.move(50, 50)
         dlg.setWindowTitle("Dialog")
         dlg.exec_()

   def dropdown_item(self, item):
      option = self.comboBox.currentText()
      message = f"export aws creds and region for {option}"
      self.message(message)


class Graphs(QWidget):
      
    # constructor
   def __init__(self, parent=None):
      super(Graphs, self).__init__(parent) 
      # a figure instance to plot on
      self.figure = plt.figure(1)  
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
      bar_graph_running("machines_running.csv")
        # refresh canvas
      self.canvas.draw()

class Graphs2(QWidget):
   def __init__(self, parent=None):
      super(Graphs2, self).__init__(parent) 
      # a figure instance to plot on
      self.figure2 = plt.figure(2)  
      # this is the Canvas Widget that
      # displays the 'figure'it takes the
      # 'figure' instance as a parameter to __init__
      self.canvas2 = FigureCanvas(self.figure2)

      # this is the Navigation widget
      # it takes the Canvas widget and a parent
      self.toolbar2 = NavigationToolbar(self.canvas2, self)

      # Just some button connected to 'plot' method
      self.button2 = QPushButton('Plot')
         
      # adding action to the button
      self.button2.clicked.connect(self.plot2) ##########################################################
      # creating a Vertical Box layout
      layout = QVBoxLayout()
         
      # adding tool bar to the layout
      layout.addWidget(self.toolbar2)
         
      # adding canvas to the layout
      layout.addWidget(self.canvas2)
         
      # adding push button to the layout
      layout.addWidget(self.button2)
         
      # setting layout to the main window
      self.setLayout(layout)

    # action called by the push button
   def plot2(self):
      bar_graph_stopped("machines_stopped.csv")
        # refresh canvas
      self.canvas2.draw()



def main():
   app = QApplication(sys.argv)  # run application
   ex = MainWindow()
   ex.show()
   sys.exit(app.exec_())  # exit application

if __name__ == "__main__":
    main()
