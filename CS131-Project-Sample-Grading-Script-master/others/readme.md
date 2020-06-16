# other scripts

## To future TAs
- Please download the .tab file (GradeBook---(upper-right-coner)--->Tabbed download) of the students' ids from MyUCLA, and name it "namelist.tab", put under this repository.
- remove the first few lines of **namelist.tab**, leaving the lines starting from students' info
- Specify the min_port and max_port (two integers) in [ports_config.py](./ports_config.py)
- Then run ```python assign_ports.py```

## To students
- After the TAs assigned the ports to you, you should see *ports_assigned.csv*
- You may read from it directly, or you can also run ```python check_my_ports.py``` with the script and *ports_assigned.csv* under the same repo.
- Please make sure that you installed [pandas](https://pandas.pydata.org/docs/getting_started/install.html#installing-pandas) before running the port-checking script.
- Once you have your port numbers, you don't need the CSV file any more, please **hard-code** the port number into your scripts.
- Please do a double-check on the port numbers before final submission. You might get a few points off if we need to correct details in your scripts for you.