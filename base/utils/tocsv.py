import pymysql
import csv
import codecs

class to_csv(object):

    def get_conn(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='123456')
        return conn

    def query(self, cur, sql, args):
        cur.execute(sql, args)
        return cur.fetchall()

    def read_mysql_to_csv(self, filename):
        with codecs.open(filename=filename, mode='w', encoding='utf-8') as f:
            write = csv.writer(f, dialect='excel')
            conn = self.get_conn()
            cur = conn.cursor()
            sql = 'select* from easytest.base_seqprocess'
            results = self.query(cur=cur, sql=sql, args=None)
            for result in results:
                print(result)
                write.writerow(result)

if __name__ == '__main__':
    r = to_csv()
    r.read_mysql_to_csv('1.csv')