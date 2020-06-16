# Note
- Contents in this folder are what you could submit latter.
- Supposed to be at least a **server.py** in here.
- Note: please avoid using txt / json files as configuration files, if you really want a configuration file, try to make it config.py

## Test your file format

Please follow the following steps before you submit your file.
1. Remove **server.py** and **report.pdf** from this folder.
2. Put your **project.tgz** file under this folder.
3. Go to the upper-level directory (```cd ..```) and then run:
```shell
python preprocess.py
```
4. If it tells you something wrong, please rezip your file, until there's no warning.
5. Test your code by running
```shell
python client_basic.py
```