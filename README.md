PatriciaSQL
=============

This is very simple PostgreSQL client written in PyQt (Qt GUI and Python). 

I am using Debian/Ubuntu compatible operating system + KDE Plasma as my desktop environment. I haven't tested this tool neither on other Linux distros, nor on other operating systems (OXS, Windows etc). This should work without any problems (as both Qt and Python are widely available) but some additional dependencies may be required (especially for database connectivity, or development of the app on other OS).

Requirements:
---------------

- Python
- PostgreSQL (it was tested with PosgreSQL 10 & 11)
- libqt5sql5-psql 

Development:
--------------

Apart from what is listed above, some additional libraries & tools may be needed to work (develop) this app.

1. Qt Designer (for forms design) `sudo apt install qt-creator`
2. PyQt5 dev tools: `sudo apt install pyqt5-dev-tools`
3. You may also need one of the following:
  * python3-pyqt5 (for Python 3.x)
  * python-pyqt5 (for Python 2.x)
  * python-pyqt5.qtsql
  * python-pyside2.qtsql
  * python3-pyqt5.qtsql


Todo:
------
This section should rather be entitled "would like to have", as I am not sure I will have enough time to work on these

 - [ ] .deb package
 - [ ] syntax highlighting for PgSQL statements
 - [ ] auto-complete (database names, columns...) (*)
 - [ ] storing many connection information
 - [ ] general UI improvements:
   - [ ] additional info on query execution (execution time)
   - [ ] displaying db errors on query execution
   
   * - I am afraid that this is going to be pretty tricky one

Disclaimer:
--------------
It was more of an experiment. There are couple of things I would like to improve, but working on it is pretty low in my priority list (read: there is a little chance that this tool will be maintained or developed further by me).
