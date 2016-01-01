'''
+----------------+------------------+------+-----+---------+----------------+
| Field          | Type             | Null | Key | Default | Extra          |
+----------------+------------------+------+-----+---------+----------------+
| runid          | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
| pid            | int(10) unsigned | NO   | MUL | NULL    |                |
| result         | varchar(100)     | YES  | MUL | NULL    |                |
| memory_used    | int(11)          | YES  |     | NULL    |                |
| time_used      | int(11)          | YES  |     | NULL    |                |
| time_submit    | datetime         | YES  | MUL | NULL    |                |
| contest_belong | int(10) unsigned | NO   | MUL | NULL    |                |
| username       | varchar(255)     | YES  | MUL | NULL    |                |
| source         | mediumtext       | YES  |     | NULL    |                |
| language       | int(10) unsigned | NO   | MUL | NULL    |                |
| ce_info        | text             | YES  |     | NULL    |                |
| ipaddr         | varchar(255)     | YES  |     | NULL    |                |
| isshared       | tinyint(1)       | NO   | MUL | NULL    |                |
| jnum           | smallint(6)      | NO   |     | NULL    |                |
+----------------+------------------+------+-----+---------+----------------+
'''


