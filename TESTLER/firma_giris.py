from selenium import webdriver

import colorama 
from colorama import Fore, Back, Style

import datetime
import time

colorama.init()

def cprint(color, text):
    print(color + text)

class firma_giris:
   
    def __init__(self, driver, url,dizi):
       self.driver = driver
       self.url = url
       self.driver.get(self.url)

       self.degerler = dizi 
       self.el_id = self.driver.find_element_by_id(self.degerler["username"])
       self.el_pas = self.driver.find_element_by_id(self.degerler["pass"])
       self.sb_btn = self.driver.find_element_by_id(self.degerler["submit_button"])
      
    def basarili(self, u_name, u_pass):
        for i in range(len(u_name)):               
            self.el_id.clear()
            self.el_pas.clear()

            self.el_id.send_keys(u_name[i])
            self.el_pas.send_keys(u_pass[i])
            
            self.sb_btn.click()
            
            result = None

            try:
                self.check = self.driver.find_element_by_class_name(self.degerler["deger"]).is_displayed()
                result = True
            except:
                result = False 
            
            if result:
                date_t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open("LOGS/log-firma.txt", "a") as file:
                    file.write(" " + "\n")   
                    file.write(str(date_t))
                    file.write(" " + "\n")
                    file.write("Basarili test: Basarili")
                    file.write(" " + "\n")  
                cprint(Fore.GREEN, "Giriş Başarılı")
            else:
                cprint(Fore.RED, "Giriş Başarısız")
                time.sleep(0.5)
                
    def basarisiz(self,u_name,u_pass):
        for i in range(len(u_name)):               
            self.el_id.clear()
            self.el_pas.clear()

            self.el_id.send_keys(u_name[i])
            self.el_pas.send_keys(u_pass[i])
            self.sb_btn.click()        

            try:
                self.check = self.driver.find_element_class_name(self.degerler["deger"]).is_displayed()
                result = True
            except:
                result = False 
                
            if result:
                cprint(Fore.GREEN, "Giriş Başarılı")
            else:
                date_t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open("LOGS/log-firma.txt", "a") as file:
                    file.write(" " + "\n")   
                    file.write(str(date_t))
                    file.write(" " + "\n")
                    file.write("Basarisiz test: Basarisiz")
                    file.write(" " + "\n")  
                cprint(Fore.RED, "Giriş Başarısız")
                time.sleep(0.5)

driver = webdriver.Chrome("C:\\Users\\BERKE\\Downloads\\chromedriver.exe")
firma_giris = firma_giris(driver, "http://localhost:8080/firma-giris", {"username": "username", "pass": "pass", "deger": "dropdown-toggle", "submit_button": "submit_button"})

print(Fore.BLUE + "Başarısız test için 1, başarılı test için 2") 
test = int(input(" "))
print(" ")

if test == 1:
    print(Fore.YELLOW + "Çalıştırılan test: " + "firma_giris, basarisiz_test")
    print("")
    firma_giris.basarisiz(["20167070", "12345", "1379248"], ["5656", "6565", "35653235"])

if test == 2:
    print(Fore.YELLOW + "Çalıştırılan test: " + "firma_giris, basarili_test") 
    firma_giris.basarili(["vestel"], ["123456"])
   
