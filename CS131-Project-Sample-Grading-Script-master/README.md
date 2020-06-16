# CS131 Project Sample Grading Script
* This is not really a grading script because you didn't see any grading
* The evaluation giving you True / False something is somewhat partial credits for each task
* This is the simplest version of the core part of the grading script, but it doesn't contain any real test case
* You may regard it as a super client (who has the power of starting a server) as well.

## [WARNING] This is NOT the real grading script
* If you pass this script with ordinary manner, then you should be fine
* Don't try to fool our grading script by hard-coding any answer inside, the real test cases are totally different
* We have **much stronger** checking points that what is listed in [evaluate.py](./evaluate.py), please do not try to fool our script by hacking the criterias.

## Recent Updates
* SEASnet has some servers where the environment e.g. path is not the same as what we've tested upon, and couldn't recognize ```lsof```. To make it work, consider trying:
```
PATH="/usr/sbin/:$PATH" python3 client_basic.py
```

## Background
- This is for [UCLA CS131 (**Programming Languages**)](http://web.cs.ucla.edu/classes/winter20/cs131/index.html) [**Project**](http://web.cs.ucla.edu/classes/winter20/cs131/hw/pr.html) (instructor: [Prof. Paul Eggert](http://web.cs.ucla.edu/classes/winter20/cs131/mail-eggert.html))
- This project is on Python, specifically aiming at the use of [asyncio](https://docs.python.org/3/library/asyncio.html) and [aiohttp](https://aiohttp.readthedocs.io/en/stable/)
- To complete the project a Google Map API Key is needed, I tried, in order to get rid of the limit you need payment information attached.

## Resource
- Thanks to previous-year TA, Wenhao's code
- Following [discussion online](https://stackoverflow.com/questions/3855127/find-and-kill-process-locking-port-3000-on-mac), to kill the process occupying port 8000 we could run: 
```shell
lsof -ti:8000 | xargs kill
```
- To find who is listening to port ```8000```:
```shell
lsof -i:8000
```
- To run a script in the background I used *nohup*
- To execute [command line within Python](https://stackoverflow.com/questions/450285/executing-command-line-programs-from-within-python):
    ```shell
    import os
    os.system('sox input.wav -b 24 output.aiff rate -v -L -b 90 48k')
    ```
- under [hint code repo](https://github.com/CS131-TA-team/UCLA_CS131_CodeHelp/tree/master/Python) I put my hint code for you to get started with this project there.

## Usage
* put your ```server.py``` and all other needed ```.py``` files under the [**sample_submission**](./sample_submission) folder
* modify the port number in ```client_basic.py``` (or keep them the same if you run on local machine --- the easiest way to test your code is to change your port number to around 800X and then test them on your local machine)
    * If you run on your local environment and see error of **ssl**, please try replacing ```aiohttp.ClientSession()``` with ```aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))```.
* could run single evaluation by
    ```shell
    python client_basic.py
    ```
* Guaranteed to work on mac and linux, not 100% sure about Windows.
* Once it works, feel free to add your own test cases in ```client_basic.SuperClient.test```
* Before final submission, remove your ```server.py```, and test whether or not your file could be successfully unzipped by:
    1. Putting your **project.tgz** file under [**sample_submission**](./sample_submission)
    2. Come back to this directory, and run ```python preprocess.py```.

## About organizing log files
You might want to have a look at [os.mkdir](https://www.tutorialspoint.com/python/os_mkdir.htm) and [os.path.exists](https://www.geeksforgeeks.org/python-os-path-exists-method/)

## What kind of submission is safe?
1. Unzip your file, by putting your file for submit (preferrably **project.tgz**) under [sample_submission](./sample_submission) folder, and then running ```python preprocess.py```.
2. After you unzip your files into the [sample_submission](./sample_submission) folder, with no extra effort required (e.g. don't need to create an empty folder manually, etc.), we can always make ```client_basic``` run (I mean if you occupy others' port then it is not guaranteed to work).

