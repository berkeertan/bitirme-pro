# Gerekli importları bu kısımda yapıyoruz 
from selenium import webdriver
import MySQLdb
import hashlib
from hashlib import md5
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import colorama 
from colorama import Fore, Back, Style

import datetime 
import time

# Textlerden renkli çıktı alabilmek için coloromayı init edip fonksiyon içinde tanımladık
colorama.init()
def cprint(color, text):
    print(color + text)

class e_mail:

    def __init__(self, driver, url, dizi):
        self.degerler = dizi 
        self.driver = driver 
        self.url = url 
        self.driver.get(self.url)
        self.e_mail = self.driver.find_element_by_id(self.degerler["mail"])

    def basarili(self, mail, firma_isim, firma_giris_adi, firma_sifre_a, firma_sifre_b):
        db = MySQLdb.connect(host= "127.0.0.1", user = "root", passwd = "", db= "deustaj", use_unicode=True, charset="utf8")
        cursor = db.cursor()
        cursor_update = db.cursor()
        cursor_firma_count = db.cursor()
        firma_after_insert = db.cursor()
        cursor_firma_count.execute("SELECT * FROM firmalar")

        self.app_btn = self.driver.find_element_by_id("f_basvuru_btn")
        self.e_mail.send_keys(mail)
        self.app_btn.click()
        self.driver.find_element_by_class_name("btn-success").click()
        time.sleep(5)

        cursor.execute("SELECT f_basvuru_url FROM f_basvurular ORDER BY id DESC LIMIT 1")
        result = cursor.fetchall()

        for row in result:
            cursor_update.execute("UPDATE f_basvurular SET f_basvuru_kod_onay = 1 WHERE f_basvuru_url = '%s'" % (row[0]))
            db.commit()
            self.driver.get("http://localhost:100/firma-kayit$url=" + row[0])
            break

        self.dizi = {"firma_isim_2": "firma_isim", "firma_giris_adi_2": "firma_giris_adi", "firma_sifre_a_2": "firma_sifre_a", "firma_sifre_b_2": "firma_sifre_b", "f_basvuru_tamamla_btn": "f_basvuru_tamamla_btn"}
        self.f_ad = self.driver.find_element_by_id(self.dizi["firma_isim_2"])
        self.k_ad = self.driver.find_element_by_id(self.dizi["firma_giris_adi_2"])
        self.pw = self.driver.find_element_by_id(self.dizi["firma_sifre_a_2"])
        self.pw_con = self.driver.find_element_by_id(self.dizi["firma_sifre_b_2"])
        self.submit_btn = self.driver.find_element_by_id(self.dizi["f_basvuru_tamamla_btn"])

        for i in range(len(firma_isim)):
            self.f_ad.send_keys(firma_isim[i])
            self.k_ad.send_keys(firma_giris_adi[i])
            self.pw.send_keys(firma_sifre_a[i])
            self.pw_con.send_keys(firma_sifre_b[i])
            self.submit_btn.click()
            
            time.sleep(3)
            firma_after_insert.execute("SELECT * FROM firmalar")
        
            if firma_after_insert.rowcount > cursor_firma_count.rowcount:
                d = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open("LOGS/firma-email-hesap.txt", "a") as file:
                    file.write(" " + "\n")   
                    file.write(str(d))
                    file.write(" " + "\n")
                    file.write("Yapılan test: Başarılı firma kayıt testi")
                    file.write(" " + "\n")
                    file.write("Beklenen sonuç: Başarılı")
                    file.write(" " + "\n")
                    file.write("Alınan sonuç: Başarılı")
                    file.write(" " + "\n\n")
                cprint(Fore.GREEN, "Basarili")
                                   
            else:
                cprint(Fore.RED, "Basarisiz")

    def basarisiz(self, mail_2, firma_isim, firma_giris_adi, firma_sifre_a, firma_sifre_b):
        db = MySQLdb.connect(host= "127.0.0.1", user = "root", passwd = "", db= "deustaj", use_unicode=True, charset="utf8")
        cursor = db.cursor()
        cursor_update = db.cursor()
        cursor_firma_count = db.cursor()
        firma_after_insert = db.cursor()
        cursor_firma_count.execute("SELECT * FROM firmalar")

        self.app_btn = self.driver.find_element_by_id("f_basvuru_btn")

        for i in range(len(mail_2)):
            self.e_mail.clear()
            self.e_mail.send_keys(mail_2[i])
            time.sleep(2)
            self.app_btn.click()
            self.disp_ul = self.driver.find_element_by_id("f_basvuru_w").is_displayed()
                
            if self.disp_ul:
                d = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open("LOGS/firma-email-hesap", "a") as file:
                    file.write(" " + "\n")   
                    file.write(str(d))
                    file.write(" " + "\n")
                    file.write("Yapılan test: Başarısız firma kayıt testi")
                    file.write(" " + "\n")
                    file.write("Beklenen sonuç: Başarısız")
                    file.write(" " + "\n")
                    file.write("Alınan sonuç: Başarısız")
                    file.write(" " + "\n\n")
                cprint(Fore.RED, "Basarisiz")
            else:
                    self.driver.find_element_by_class_name("btn-success").click()
            time.sleep(5)

        cursor.execute("SELECT f_basvuru_url FROM f_basvurular ORDER BY id DESC LIMIT 1")
        result = cursor.fetchall()

        for row in result:
            cursor_update.execute("UPDATE f_basvurular SET f_basvuru_kod_onay = 1 WHERE f_basvuru_url = '%s'" % (row[0]))
            db.commit()
            self.driver.get("http://localhost:100/firma-kayit$url=" + row[0])
            break

        self.dizi = {"firma_isim_2": "firma_isim", "firma_giris_adi_2": "firma_giris_adi", "firma_sifre_a_2": "firma_sifre_a", "firma_sifre_b_2": "firma_sifre_b", "f_basvuru_tamamla_btn": "f_basvuru_tamamla_btn"}
        self.f_ad = self.driver.find_element_by_id(self.dizi["firma_isim_2"])
        self.k_ad = self.driver.find_element_by_id(self.dizi["firma_giris_adi_2"])
        self.pw = self.driver.find_element_by_id(self.dizi["firma_sifre_a_2"])
        self.pw_con = self.driver.find_element_by_id(self.dizi["firma_sifre_b_2"])
        self.submit_btn = self.driver.find_element_by_id(self.dizi["f_basvuru_tamamla_btn"])

        for i in range(len(firma_isim)):
            self.k_ad.clear()
            self.f_ad.clear()
            self.pw_con.clear()
            self.pw.clear()
            self.f_ad.send_keys(firma_isim[i])
            self.k_ad.send_keys(firma_giris_adi[i])
            self.pw.send_keys(firma_sifre_a[i])
            self.pw_con.send_keys(firma_sifre_b[i])
            self.submit_btn.click()
            
            time.sleep(3)
            firma_after_insert.execute("SELECT * FROM firmalar")
        
            if firma_after_insert.rowcount > cursor_firma_count.rowcount:           
                cprint(Fore.GREEN, "Basarili")
                                   
            else:
                d = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open("LOGS/firma-email-hesap", "a") as file:
                    file.write(" " + "\n")   
                    file.write(str(d))
                    file.write(" " + "\n")
                    file.write("Yapılan test: Başarısız firma kayıt testi")
                    file.write(" " + "\n")
                    file.write("Beklenen sonuç: Başarısız")
                    file.write(" " + "\n")
                    file.write("Alınan sonuç: Başarısız")
                    file.write(" " + "\n\n")
                cprint(Fore.RED, "Basarisiz")
            
        
driver = webdriver.Chrome("C:\\Users\\BERKE\\Downloads\\chromedriver.exe")
e_mail = e_mail(driver, "http://localhost:100/firma-basvuru",{"mail": "f_basvuru_mail"})

print(Fore.YELLOW + "Başarısız test için 1, başarılı test için 2") 
test = int(input())
print(" ")

# 1'e basılırsa yapılacak işlemler 
if test == 1:
    print(Fore.YELLOW + "Çalıştırılan test: " + "Firma kayıt, basarisiz_test")
    print("")
    # Firma_giris sınıfının içindeki basarisiz define degerleri gönderiyoruz 
    e_mail.basarisiz(["berke", "berke@gmail.com"], ["berke","ertan"], ["ertan", ""], ["123456", "12345"], ["5662", "1235"])

# 2'ye basılırsa yapılacak işlemler 
if test == 2:
    print(Fore.YELLOW + "Çalıştırılan test: " + "Firma kayıt, basarili_test") 
    # Firma_giris sınıfının içindeki basarili define degerleri gönderiyoruz 
    e_mail.basarili(["berke@gmail.com"],["berke"], ["berke"], ["123456788"], ["123456788"])


