#!/usr/bin/env python3

# Catatan
# cuma buat format .JPG dan .TIFF
# karena make library pillow silahkan install dulu
# pip install Pillow 
# kebanyakan medsos itu dah ngilangin data nya
import os
import sys
import time
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS

# buat ngasih warna
red = '\033[91m'
green = '\033[92m'
white = '\033[00m'

#animasi loading
def load_animasi():    
    kata_str = "i am not a hacker i am just tester..."
    ls_len = len(kata_str) 
    animasi = "|/-\\"
    htganim = 0
    htgwaktu = 0        
    i = 0                     
    
    while (htgwaktu != 100): 
        time.sleep(0.075)  
        kata_str_list = list(kata_str)
        x = ord(kata_str_list[i]) 
        y = 0                             
        if x != 32 and x != 46:              
            if x>90: 
                y = x-32
            else: 
                y = x + 32
            kata_str_list[i]= chr(y) 
        res =''              

        for j in range(ls_len): 

            res = res + kata_str_list[j] 
        sys.stdout.write("\r"+res + animasi[htganim]) 
        sys.stdout.flush() 
        kata_str = res 
        htganim = (htganim + 1)% 4
        i =(i + 1)% ls_len 
        htgwaktu = htgwaktu + 1

# windows
    if os.name =="nt": 
        os.system("cls") 
# linux / Mac OS 
    else:
        os.system("clear") 
if __name__ == '__main__':  
    load_animasi()


print (green+'''

           1010010        0001101
           1000100        0011100
           0110011        1001001 
           1011001        0010111
           1010100        0100100
           1110010101011100010100
           101010000HADES01011100
           1010101000111000100001
           0011100        1000000
           1001000        0100100
           1010101        1000110
           1100110        0011100
           1010001        0011111

'''+white)
print( red+"      [-] I AM NOT HACKER, I AM JUST TESTER[-]"+white)



# fungsi pembantu
def buat_url_maps(koor_gps):
    # kita extract data trus kita masukin ke fungsi ini buat Latitude.
    der_lat = convert_derajat(float(koor_gps["lat"][0]),  float(koor_gps["lat"][1]), float(koor_gps["lat"][2]), koor_gps["lat_ref"])
    # yang ini kita extract buat Longitude.
    der_lon = convert_derajat(float(koor_gps["lon"][0]),  float(koor_gps["lon"][1]), float(koor_gps["lon"][2]), koor_gps["lon_ref"])
    # kita return biar bisa di cari make google maps
    return f"https://maps.google.com/?q={der_lat},{der_lon}"


# kita convert karena longitude dan latitude  kan terdiri dari derajat/menit/detik
def convert_derajat(derajat, menit, detik, arah):
    derajat_desimal = derajat + menit / 60 + detik / 3600
    # "S" buat selatan dan "B" buat Barat
    if arah == "S" or arah == "B":
        derajat_desimal *= -1
    return derajat_desimal
        

# buat pilihan mau di tampilin kelayar atau ke file.
while True:
    pilihan = input(green+"Mau di tampilin kemana?:\n\n"+white+"1 - File\n2 - Terminal\n"+green+"Masukin pilihanmu kesini, bukan ke hati: "+white)
    start = "Engine start...\n"
    for s in start:
        sys.stdout.write(s)
        sys.stdout.flush()
        time.sleep(0.1)
    try:
        conf_pil = int(pilihan)
        if conf_pil == 1:
            # kita bikin file.baru
            sys.stdout = open("data_gambar.txt", "w")
            break
        elif conf_pil == 2:
            # Karena dia langsung menampilkan kelayar kita hanya nge-break perulangngannya.
            break
        else:
            print(red+"Lu masukin apa? .")
    except:
        print(red+"Lu masukin yang kagak valid")


# nambahin file ke folder ./images
cwd = os.getcwd()
# satuin di satu directory buat script sama folder images nya.
os.chdir(os.path.join(cwd, "images"))
# dapetin semua file yg ada di folder
files = os.listdir()

# cek ada apa kagak file di folder ./images.
if len(files) == 0:
    print(red+"kagak ada file di folder images."+white)
    exit()
# kita loop file yang ada d folder
for file in files:
    # kita tambain "try" "except" takut ada format yang g di dukung:
    try:
        # kita open gambarnya
        image = Image.open(file)
        print(f"-----------[ {file} ]-----------")
        koor_gps = {}
        # cek ada data yg bisa di ambil kagak
        if image._getexif() == None:
            print(f"{file} kagak ada data yang bisa di ambil.")
        # kalo ada kita buat dsini
        else:
            for tag, value in image._getexif().items():
                # kalo kita running trus g make TAGS.get() nanti yang ada muncul angka angka doang dan gw pengennya kalian bisa ngerti.
                tag_name = TAGS.get(tag)
                if tag_name == "GPSInfo":
                    for key, val in value.items():
                        print(f"{GPSTAGS.get(key)} - {val}")
                        # kita tambahin data latitude yang udah kita kasih di line 85
                        if GPSTAGS.get(key) == "GPSLatitude":
                            koor_gps["lat"] = val
                        # sama juga ini buat data longitude nya yg udah kita kasih di line 87
                        elif GPSTAGS.get(key) == "GPSLongitude":
                            koor_gps["lon"] = val
                        # kita tambahin data refrensi latitude yang dah kita buat di lone 85
                        elif GPSTAGS.get(key) == "GPSLatitudeRef":
                            koor_gps["lat_ref"] = val
                        # yg ini buat data refrensi Longitude  yang dah dibuat di line 87.
                        elif GPSTAGS.get(key) == "GPSLongitudeRef":
                            koor_gps["lon_ref"] = val   
                else:
                    # tampilin data yg g related
                    print(f"{tag_name} - {value}")
            # nah disini kita tampilin link koordinat map nya
            if koor_gps:
                print(buat_url_maps(koor_gps))

    except IOError:
        print("File format not supported!")

if pilihan == "1":
    sys.stdout.close()
os.chdir(cwd)
