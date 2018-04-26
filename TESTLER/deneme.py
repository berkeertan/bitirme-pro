import MySQLdb
db = MySQLdb.connect(host= "127.0.0.1", user = "root", passwd = "", db= "deustaj", use_unicode=True, charset="utf8")
cursor = db.cursor()
cursor.execute("UPDATE f_basvurular SET f_basvuru_kod_onay = 1 WHERE id = 15")
db.commit()
