import json
import redis
import pymysql

def main():
    # 指定redis数据库信息
    rediscli = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, password=199524)
    # 指定mysql数据库
    db = pymysql.connect('localhost', 'root', '199524', 'fangtianxia')

    while True:
        # FIFO模式为 blpop，LIFO模式为 brpop，获取键值
        source, data = rediscli.blpop(["fang:items"])
        item = json.loads(data)

        try:
            # 使用cursor()方法获取操作游标
            cur = db.cursor()
            # 使用execute方法执行SQL INSERT语句
            if 'district' in item:
                insert_sql = """insert into fangtianxia.newhouse(province, city, name, house_type, area, address, 
                            district, sale, price, detail_url)
                            Values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
                cur.execute(insert_sql, (
                    item['province'], item['city'], item['name'], item['house_type'], item['area'], item['address'],
                    item['district'], item['sale'], item['price'], item['detail_url']))
            elif 'floor' in item:
                insert_sql = """insert into fangtianxia.esfhouse(province, city, name, house_type, area, floor, 
                            orientation, year, address, total_price, unit_price, detail_url)
                            Values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
                cur.execute(insert_sql, (
                    item['province'], item['city'], item['name'], item['house_type'], item['area'], item['floor'],
                    item['orientation'], item['year'], item['address'], item['total_price'], item['unit_price'], item['detail_url']))
            # 提交sql事务
            db.commit()
            # 关闭本次操作
            cur.close()
            print("inserted %s" % item['name'])
        except pymysql.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

if __name__ == '__main__':
    main()