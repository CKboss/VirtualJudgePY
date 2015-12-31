
def checkUserSQL(username,passowrd):
    sql = 'select count(*) from user WHERE username = "%s" and password = "%s" '%(username,passowrd)
    return sql

def addUserSQL(**d):
    sql = 'INSERT INTO user (uid, username, nickname, password, email, school, total_submit, total_ac, register_time, last_login_time, photo, total_value, lock_status, isroot, ipaddr, local_ac)' \
          'VALUES (1,d[username],d[nicname],d[password],d[email],d[school],0,0,' ',' ',null,0,0,0,0,0)'
