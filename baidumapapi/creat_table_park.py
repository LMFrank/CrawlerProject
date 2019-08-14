import pymysql

db = pymysql.connect('localhost', 'root', 'password', 'baidumap')
cursor = db.cursor()

sql = """CREATE TABLE park (
         id INT NOT NULL AUTO_INCREMENT,
         city VARCHAR(200) NOT NULL,
         park VARCHAR(200) NOT NULL,
         location_lat FLOAT,
         location_lng FLOAT,
         address VARCHAR(200),
         street_id VARCHAR(200),
         uid VARCHAR(200),
         telephone VARCHAR(200),
         detail INT,
         tag VARCHAR(200),
         detail_url VARCHAR(800),
         type VARCHAR(200),
         price VARCHAR(200),
         overall_rating FLOAT,
         image_num INT,
         comment_num INT,
         key_words VARCHAR(800),
         shop_hours VARCHAR(800),
         alias VARCHAR(800),
         scope_type VARCHAR(200),
         scope_grade VARCHAR(200),
         created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
         PRIMARY KEY (id)
);"""

cursor.execute(sql)
db.commit()
db.close()