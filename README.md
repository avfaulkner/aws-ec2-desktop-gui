# AWS EC2 Desktop Tool

This application allow the user to view information about specific instances via a desktop application.

## Tools
- PyQt5
- Python3.8
 

## Instructions
To run this script locally, please run: 
- pip install pandas matplotlib datetime boto3 pytz jupyter
- export region=(your desired region)
- export AWS_PROFILE=(your aws profile name)

<b>To view the graphs: </b>  
If running in wsl using vscode, `pip install jupyter` to view graph in interactive window, then 
right click the file or on the page containing the code if the file is open and select "Run current file in interactive window".

If running the script in a terminal:
- install xming (X11 for Windows, needed to view graphs from wsl terminal also) from sourcefourge or VcXsrv (xserver).
- sudo apt-get install python3.8-tk
- export DISPLAY=localhost:0.0 (can add to .bashrc to make permanent)
