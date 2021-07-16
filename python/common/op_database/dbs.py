import MySQLdb

OperrationalError = MySQLdb.OperationalError

class MySQL(object):
    def __init__(self,host,user,password,port=3306,charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.password =password
        self.charset = charset
        try:
            self.conn = MySQLdb.connect(host=self.host,port=self.port,user=self.user,password=self.password)
            self.conn.autocommit(False)
            self.conn.set_character_set(self.charset)
            self.cursor = self.conn.cursor()

        except MySQLdb.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def __del__(self):
        self.close()
        # self.cursor.close()
        # self.conn.close()

    def select_db(self,db):
        try:
            self.conn.select_db(db)
        except MySQLdb.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def query(self,sql):
        try:
            n = self.cursor.execute(sql)
            return n
        except MySQLdb.Error as e:
            print("Mysql Error:%s\nSQL:%s" %(e,sql))

    def fetchRow(self):
        result = self.cursor.fetchone()
        return result

    def fetchAll(self):
        result = self.cursor.fetchall()
        desc = self.cursor.description
        d = []
        for inv in result:
            _d = {}
            for i in range(0, len(inv)):
                _d[desc[i][0]] = str(inv[i])
                d.append(_d)
        return d

    def insert(self,table_name,data):
        columns=data.keys()
        _prefix="".join(['INSERT INTO `',table_name,'`'])
        _fields=",".join(["".join(['`',column,'`']) for column in columns])
        _values=",".join(["%s" for i in range(len(columns))])
        _sql="".join([_prefix,"(",_fields,") VALUES (",_values,")"])
        _params=[data[key] for key in columns]
        return self.cursor.execute(_sql,tuple(_params))

    def update(self, tbname, data, condition):
        _fields = []
        _prefix = "".join(['UPDATE `', tbname, '`', 'SET'])
        for key in data.keys():
            _fields.append("%s = %s" % (key, data[key]))
        _sql = "".join([_prefix, _fields, "WHERE", condition])

        return self.cursor.execute(_sql)


    def delete(self,tbname,condition):
        _prefix="".join(['DELETE FROM  `',tbname,'`','WHERE'])
        _sql="".join([_prefix,condition])
        return self.cursor.execute(_sql)

    def getLastInsertId(self):
        return self.cursor.lastrowid

    def rowcount(self):
        return self.cursor.rowcount

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__=='__main__':
    n=MySQL('127.0.0.1','root','123456',3306)
    n.select_db('test')
    tbname='map'
    a=({'id':3,'x':3,'y':3},{'id':4,'x':4,'y':4},{'id':5,'x':5,'y':5})
    for d in a:
        n.insert(tbname,d)
    n.commit()