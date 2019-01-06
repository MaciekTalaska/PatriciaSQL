PatriciaSQL
=============

This is very simple PostgreSQL client written in PyQt (Qt GUI and Python). 

I am using Debian/Ubuntu compatible operating system + KDE Plasma as my desktop environment. I haven't tested this tool neither on other Linux distros, nor on other operating systems (OXS, Windows etc). This should work without any problems (as both Qt and Python are widely available) but some additional dependencies may be required (especially for database connectivity, or development of the app on other OS).

Requirements:
---------------

- Python (either 2.7x or 3.x)
- PostgreSQL (it was tested with PosgreSQL 10 & 11)
- libqt5sql5-psql 

Development:
--------------

Apart from what is listed above, some additional libraries & tools may be needed, in case you want to to work on this app.

1. Qt Designer (for forms design) `sudo apt install qt-creator`
2. PyQt5 dev tools: `sudo apt install pyqt5-dev-tools`
3. You may also need one of the following:
   For Python3:
  * python3-pyqt5
  * python3-pyqt5.qtsql
   For Python 2.7.x:
  * python-pyqt5
  * python-pyqt5.qtsql

In case something doesn't work, try installing:
  * python-pyside2.qtsql
  or
  * python3-pyside2.qtsql

Todo:
------
This section should rather be entitled "would like to have", as I am not sure I will have enough time to work on all of these:

 - [ ] .deb package
 - [x] syntax highlighting for PgSQL statements
 - [ ] store connection information in human readable format (now it is saved using pickle)
 - [ ] auto-complete (database names, columns...):
    - [ ] keywords autocomplete
    - [ ] words used autocomplete
    - [ ] database names, table names, column names... (*)
 - [ ] storing many connection information
 - [ ] execute only highlighted text (execute one of many queries)
 - [ ] shortcut for 'execute as explain'
 - [ ] general UI improvements:
   - [ ] additional info on query execution (execution time)
   - [ ] displaying db errors on query execution
   
* - I am afraid that this is going to be pretty tricky one

Disclaimer:
--------------
It was more of an experiment. I have no plans at the moment to make it a "full blown" tool. It should stay simple (and hopefully - fast). There are couple of things I would like to improve (listed in TODO section), but working on it is not very high on my priority list (read: it may happen any moment that I stop working on it).
