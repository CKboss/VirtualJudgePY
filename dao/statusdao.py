'''
+------------+--------------+------+-----+---------+----------------+
| Field      | Type         | Null | Key | Default | Extra          |
+------------+--------------+------+-----+---------+----------------+
| runid      | int(11)      | NO   | PRI | NULL    | auto_increment |
| timesubmit | datetime     | YES  |     | NULL    |                |
| status     | varchar(100) | YES  |     | NULL    |                |
| runtime    | varchar(45)  | YES  |     | NULL    |                |
| runmemory  | varchar(45)  | YES  |     | NULL    |                |
| pid        | int(11)      | YES  | MUL | NULL    |                |
| cid        | int(11)      | YES  |     | NULL    |                |
| language   | varchar(45)  | YES  |     | NULL    |                |
| source     | text         | YES  |     | NULL    |                |
| isopen     | tinyint(1)   | YES  |     | NULL    |                |
| uid        | int(11)      | YES  |     | NULL    |                |
| username   | varchar(255) | YES  |     | NULL    |                |
| originOJ   | varchar(255) | YES  |     | NULL    |                |
| originProb | varchar(45)  | YES  |     | NULL    |                |
| realrunid  | varchar(45)  | YES  |     | NULL    |                |
| isdisplay  | tinyint(1)   | YES  |     | NULL    |                |
| ceinfo     | text         | YES  |     | NULL    |                |
+------------+--------------+------+-----+---------+----------------+
'''


