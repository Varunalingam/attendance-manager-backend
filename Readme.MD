# Attendance Manager Backend

backend repository for the attendance manager android application


### How to Setup
#### Prerequisites
1. Install Python3 and pip
2. Install MySQL `apt-get install mysqlclient-core-8.0`
3. Install Virtualenv `apt-get install virtualenv`
4. Install [`mysqlclient`](https://pypi.org/project/mysqlclient/) prerequisites :
    * You may need to install the Python and MySQL development headers and libraries like so:
        ```
        sudo apt-get install python-dev default-libmysqlclient-dev
        ```
    * If you are using python3 then you need to install python3-dev using the following command :
        ```
        sudo apt-get install python3-dev
        ```
    * Install from PyPI:
        ```
        pip3 install mysqlclient
        ```
#### Installation
1. Clone the repository - `git clone <remote-url>`
2. Go to the project directory - `cd <cloned-repo>`
3. Set up the environment :
    * Create virtual environment files - `virtualenv -p python3 venv`
    * Activate virtual environment - `source venv/bin/activate`
4. Install dependencies - `pip3 install -r requirements.txt`
5. Create a database - `attendance_manager_database`
6. Create a mysql user and update '.env' with necessary database details
7. Make migrations - `python3 manage.py makemigrations`
8. Run migrations - `python3 manage.py migrate`
9. Run Seeders - `/scripts/refresh_db.sh`
10. Start server - `python3 manage.py runserver`