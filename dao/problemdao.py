'''
+----------------------+------------------+------+-----+---------+----------------+
| Field                | Type             | Null | Key | Default | Extra          |
+----------------------+------------------+------+-----+---------+----------------+
| pid                  | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
| title                | char(255)        | NO   | MUL | NULL    |                |
| description          | longtext         | NO   |     | NULL    |                |
| input                | text             | NO   |     | NULL    |                |
| output               | text             | NO   |     | NULL    |                |
| sample_in            | text             | NO   |     | NULL    |                |
| sample_out           | text             | NO   |     | NULL    |                |
| number_of_testcase   | int(10) unsigned | NO   |     | NULL    |                |
| total_submit         | int(10) unsigned | NO   |     | NULL    |                |
| total_ac             | int(10) unsigned | NO   |     | NULL    |                |
| total_wa             | int(10) unsigned | NO   |     | NULL    |                |
| total_re             | int(10) unsigned | NO   |     | NULL    |                |
| total_ce             | int(10) unsigned | NO   |     | NULL    |                |
| total_tle            | int(10) unsigned | NO   |     | NULL    |                |
| total_mle            | int(10) unsigned | NO   |     | NULL    |                |
| total_pe             | int(10) unsigned | NO   |     | NULL    |                |
| total_ole            | int(10) unsigned | NO   |     | NULL    |                |
| total_rf             | int(10) unsigned | NO   |     | NULL    |                |
| special_judge_status | smallint(6)      | NO   |     | 0       |                |
| basic_solver_value   | int(10) unsigned | NO   |     | NULL    |                |
| ac_value             | int(10) unsigned | NO   |     | NULL    |                |
| time_limit           | int(10) unsigned | NO   |     | NULL    |                |
| case_time_limit      | int(10) unsigned | NO   |     | NULL    |                |
| memory_limit         | int(10) unsigned | NO   |     | 0       |                |
| hint                 | text             | NO   |     | NULL    |                |
| source               | text             | NO   | MUL | NULL    |                |
| author               | text             | NO   |     | NULL    |                |
| hide                 | tinyint(1)       | NO   | MUL | NULL    |                |
| vid                  | char(50)         | NO   | MUL | NULL    |                |
| vname                | char(50)         | NO   | MUL | NULL    |                |
| isvirtual            | tinyint(1)       | NO   | MUL | NULL    |                |
| vacnum               | int(11)          | NO   |     | NULL    |                |
| vtotalnum            | int(11)          | NO   |     | NULL    |                |
| ignore_noc           | tinyint(1)       | NO   |     | NULL    |                |
| vacpnum              | int(11)          | NO   |     | NULL    |                |
| vtotalpnum           | int(11)          | NO   |     | NULL    |                |
| is_interactive       | tinyint(1)       | NO   |     | NULL    |                |
+----------------------+------------------+------+-----+---------+----------------+
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

    for key in kwargs.keys():

        if key == 'voj' or key == 'vid' or key == 'title':
            continue
        else :
            kwargs[key]=UTF8StrToBase64Str(kwargs[key])

    sql = 'INSERT INTO problem (title,description,input,output,sample_in,sample_out,vname,vid,source,problem_limit) ' \
          'VALUES ("{title}","{description}","{input}","{output}","{sampleInput}","{sampleOutput}","{voj}","{vid}","{source}","{problem_limit}")'.format(**kwargs)

    cur = conn.cursor()
    print('exeSQL: ',sql)
    cur.execute(sql)

def getProblem(**kwargs):
    '''
    :param kwargs: voj vid
    :return:
    '''
    sql = 'SELECT * FROM problem WHERE vname like "{voj}" and vid like "{vid}" '.format(**kwargs)
    return sql

def main():
    pass

if __name__=='__main__':
    main()
