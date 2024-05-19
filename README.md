# backporting_tool
A small, efficient Python-based solution for backporting changes from the recently updated C file to the old one.
Wraps diff and patch command line utilities for backporting changes.

# Requirements
- Ubuntu 20.04 or higher
- Python 3.8 or higher
- Command line utility: diff 3.7 or higher
- Command line utility: patch 2.7.6 or higher

it only uses the python standard library so the requirements.txt file is empty.

# Installation

- Make sure diff command line utility is on latest version: 
```
sudo apt install diffutils
```
- Make sure patch command line utility is on latest version: 
```
sudo apt install patch
```
- Clone current github repo: 
```
git clone https://github.com/dexters1/backporting_tool.git
```
- Make sure necessary permissions are given to the script inside github repo: 
```
chmod +x backporting_tool.py
```
- Run the script with proper arguments, example: 
```
./backporting_tool.py -b "/tmp/examples/e27c4470/before/kernel-4.18.0-477.27.1.el8_8w2bb4pco"
-a "/tmp/examples/e27c4470/after/kernel-4.18.0-513.5.1.el8_9dxsabows"
-t "/tmp/examples/e27c4470/target/sch_api.cd10e7n9d"
```
