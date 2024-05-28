In order to run this python code you need to install:

WINDOWS:
pip install requests beautifulsoup4 pymysql

LINUX:
pip3 install requests beautifulsoup4 pymysql

You also need to modify database conexion details at the end of the file:
connection = pymysql.connect(host='',
                             user='',
                             password='',
                             database='',
                             cursorclass=pymysql.cursors.DictCursor)
