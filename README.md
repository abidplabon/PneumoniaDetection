# PneumoniaDetection
For running the project download the code from github in zip format
Unzip the files
Install required packages and files
    -go to root of project directory
    -Create a virtual environment using "python3 -m venv /path/to/new/virtual/environment"
    -now activate the virtualenvironment then
    -write "pip install -r requirements.txt" in command prompt (Separately install pillow and keras_preprocessing to avoid unexpected errors)
Install database
    - go to project root directory
    - run following command on console/terminal
        -python3
        -from app import db
        -db.create_all()
        -exit()
Now run the final app using "Flask run"


##Default-username=mohammed
##Default-password=123456789
