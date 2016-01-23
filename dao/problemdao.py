'''
mysql> desc problem;
+-------------+---------------+------+-----+---------+----------------+
| Field       | Type          | Null | Key | Default | Extra          |
+-------------+---------------+------+-----+---------+----------------+
| pid         | int(11)       | NO   | PRI | NULL    | auto_increment |
| title       | varchar(255)  | YES  |     | NULL    |                |
| source      | varchar(255)  | YES  |     | NULL    |                |
| url         | varchar(1024) | YES  |     | NULL    |                |
| originOJ    | varchar(255)  | YES  |     | NULL    |                |
| originProb  | varchar(45)   | YES  |     | NULL    |                |
| memorylimit | varchar(45)   | YES  |     | NULL    |                |
| timelimit   | varchar(45)   | YES  |     | NULL    |                |
+-------------+---------------+------+-----+---------+----------------+

mysql> desc problemdetail;
+--------------+--------------+------+-----+---------+----------------+
| Field        | Type         | Null | Key | Default | Extra          |
+--------------+--------------+------+-----+---------+----------------+
| did          | int(11)      | NO   | PRI | NULL    | auto_increment |
| pid          | int(11)      | YES  | MUL | NULL    |                |
| description  | text         | YES  |     | NULL    |                |
| input        | text         | YES  |     | NULL    |                |
| output       | text         | YES  |     | NULL    |                |
| sampleinput  | text         | YES  |     | NULL    |                |
| sampleoutput | text         | YES  |     | NULL    |                |
| hint         | text         | YES  |     | NULL    |                |
| author       | varchar(255) | YES  |     | NULL    |                |
| source       | varchar(255) | YES  |     | NULL    |                |
| updateTime   | datetime     | YES  |     | NULL    |                |
+--------------+--------------+------+-----+---------+----------------+
'''

from tools.encode import Base64StrToUTF8Str,UTF8StrToBase64Str
from tools.dbcore import conn

pdata = dict (
    title = None,
    description = None,
    input = None,
    output = None,
    sampleInput = None,
    sampleOutput = None,
    vid = None,
    voj = None,
    source = None,
    author = None,
    problem_limit = None,
)


def InsertProblem(**kwargs):
    pass

def main():
    pass

if __name__=='__main__':
    main()
