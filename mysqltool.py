import pymysql

class MySQLTool:
    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db


    # 连接mysql数据库
    def _GetConnect(self):
        if not self.db:
            raise (NameError, "没有设置数据库信息")
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, charset='utf8')
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur

    #创建数据库
    def SetDataBase(self,database):
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.pwd, charset='utf8')
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            try:
                cur.execute('create database '+database+' default character set utf8')
            except Exception as e:
                print(e.args,'数据库已存在')
        cur.close()


    #非查询操作
    def ExecNotQuery(self,sql):
        cur=self._GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

    # 批量插入
    def Insert(self, sql,data):
        cur = self._GetConnect()
        cur.executemany(sql,data)
        self.conn.commit()
        self.conn.close()