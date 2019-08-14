import pymysql

db = pymysql.connect('localhost', 'root', 'password', 'baidumap')
cursor = db.cursor()

sql = """CREATE TABLE city (
    id INT NOT NULL AUTO_INCREMENT,
    city VARCHAR(200) NOT NULL,
    park VARCHAR(200) NOT NULL,
    location_lat FLOAT,
    location_lng FLOAT,
    address VARCHAR(200),
    street_id VARCHAR(200),
    uid VARCHAR(200),
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);"""

cursor.execute(sql)
db.commit
db.close()