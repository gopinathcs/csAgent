# CS Agent

## About CS Agent

This agent will fetch queries from ConverSight.ai platform based on the token supplied and connect to corresponding database to fetch data then convert to parquet file and upload to agent engine.

#### Currently handling the following databases

1. mySQL


#### Steps to run **CS Agent**

1. Clone the repository
2. Change the configurations on the yaml file, it will be on the ***csAgent/config/config.yaml***
3. For example, to change the **token**, look for the key **STATIC_TOKEN** and replace the value with your token.
4. Once the configuration is set, run CS Agent by the following command
    1. python app.py 
5. If you don't have python installed on your system, please check the below links on how to install python
    1. Windows (https://www.python.org/downloads/windows/)
    2. Linux - Ubuntu (`sudo apt install python3.8`) 
    3. Mac (https://www.python.org/downloads/macos/)
