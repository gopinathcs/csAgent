# CS Agent

## About CS Agent

CS Agent is an EL agent that extracts and loads data from databases behind a firewall for the ConverSight.ai platform.


#### Currently Supported Databases.

1. mySQL


#### Steps to run **CS Agent**

1. Click the green dropdown in the upper right corner to clone or download the repository, or click this link to download the repository directly.(https://github.com/ConverSight/csAgent/archive/refs/tags/v0.1.1.zip)
2. Change the configurations on the yaml file, it will be on the ***csAgent/config/config.yaml***
3. For example, to change the **token**, look for the key **STATIC_TOKEN** and replace the value with your token.<br>
    Change ``STATIC_TOKEN: <TOKEN>`` to ``STATIC_TOKEN: 'JWT%20ajkshdjkfhaskjdhakshdfkahsdkjfhakdshf'``
4. To get the token, please contact the ConverSight.ai team or login as an administrator and click to the Configure Dataset page.
5. To add database credentials on the yaml file, look for the database key and replace the values with yours <br>
    For example, <br>
    ``mySQL:``<br>
    &nbsp;&nbsp;&nbsp; ``host: "192.168.155.268"``<br>
    &nbsp;&nbsp;&nbsp; ``port: "1433"``<br>
    &nbsp;&nbsp;&nbsp; ``username: "test_user"``<br>
    &nbsp;&nbsp;&nbsp; ``password: "test_password"``<br>
    &nbsp;&nbsp;&nbsp; ``database: "test_db"``<br>
    &nbsp;&nbsp;&nbsp; ``timeout: 5``<br>
6. Run CS Agent with the following command once the setup is complete.
    1. python app.py 
7. If you do not already have Python installed on your machine, please see the links below for instructions on how to do so.
    1. Windows (https://www.python.org/downloads/windows/)
    2. Linux - Ubuntu (`sudo apt install python3.8`) 
    3. Mac (https://www.python.org/downloads/macos/)
8. Install the packages needed by CS Agent from the **requirements.txt** file after Python is installed. To install all of the packages, follow the steps below.
    1. ``pip install -r /path/to/requirements.txt``
    2. make sure pip is installed on your system
