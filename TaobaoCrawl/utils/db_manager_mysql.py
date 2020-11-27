# -*- coding: utf-8 -*-
import pymysql

"""
    MySql工具类的底层操作
"""


class DbManager:
    # 构造函数
    def __init__(self, host='127.0.0.1', port=3306, user='用户名',
                 passwd='用户密码', db='taobao', charset='utf8mb4'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        self.charset = charset
        self.conn = None
        self.cur = None

    # 连接数据库
    def connectDatabase(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db,
                                        charset=self.charset)

        except:
            # logger.error("connectDatabase failed")
            print("connectDatabase failed")
            return False
        # self.cur = self.conn.cursor()
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)  # 返回字典结构
        return True

    # 关闭数据库
    def close(self):
        # 如果数据打开，则关闭；否则没有操作
        if self.conn and self.cur:
            self.cur.close()
            self.conn.close()
        return True

    # 执行数据库的sq语句,主要用来做插入操作
    def execute(self, sql, params=None, commit=False, ):
        # 连接数据库
        res = self.connectDatabase()
        if not res:
            return False
        try:
            if self.conn and self.cur:
                # 正常逻辑，执行sql，提交操作
                rowcount = self.cur.execute(sql, params)
                # print(rowcount)
                if commit:
                    self.conn.commit()
                else:
                    pass
        except:
            # logger.error("execute failed: " + sql)
            # logger.error("params: " + str(params))

            print("execute failed: " + sql)
            print("params: " + str(params))

            self.close()
            return False
        return rowcount

    # 查询所有数据
    def fetchall(self, sql, params=None):
        res = self.execute(sql, params)
        if not res:
            # logger.info("查询失败")
            return False
        self.close()
        results = self.cur.fetchall()
        # logger.info("查询成功" + str(results))
        return results

    # 查询一条数据
    def fetchone(self, sql, params=None):
        res = self.execute(sql, params)
        if not res:
            # logger.info("查询失败")
            return False
        self.close()
        result = self.cur.fetchone()
        # logger.info("查询成功" + str(result))
        return result

    # 增删改(单条数据)
    def edit(self, sql, params=None):
        res = self.execute(sql, params, True)
        if ((not res) and (res != 0)):
            # logger.info("edit操作失败")
            print(f"edit操作失败,sql={sql},params={params}")
            return False
        self.conn.commit()
        self.close()
        # logger.info("操作成功" + str(res))
        return res

    # 增删改(列表数据)
    def editList(self, sql, params_list=[]):
        for params in params_list:
            res = self.execute(sql, params, True)
            if not res:
                print(f"editList操作失败,sql={sql},params={params}")
        self.conn.commit()
        self.close()
        # logger.info("操作成功" + str(res))
        return res

    def del_data(self, sql, params=None):
        res = self.execute(sql, params, True)
        print("删除行数=" + str(res))
        self.conn.commit()
        self.close()
        # logger.info("操作成功" + str(res))
        return res
