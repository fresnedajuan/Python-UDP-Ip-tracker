from geolite2 import geolite2
import socket, subprocess 


cmd = r"C:\Program Files\Wireshark\tshark.exe -i10 -fudp"
print("UDP Scanner based on Geolite2")
print("-----------------------------")

process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
my_ip = socket.gethostbyname(socket.gethostname())
print("This is my IP: "+my_ip)
reader = geolite2.reader()
info = geolite2.get_info()
start = 1
def get_ip_location(ip):
    location = reader.get(ip)
    #print(location)
    try:
        country = location["country"]["names"]["en"]
    except:
        country = "Unknown"

    try:
        subdivision = location["subdivisions"][0]["names"]["en"]
    except:
        subdivision = "Unknown"    

    try:
        city = location["city"]["names"]["en"]
    except:
        city = "Unknown"
    
    return country, subdivision, city


for line in iter(process.stdout.readline, b""):
    columns = str(line).split(" ")
    #print(line)
    if "UDP" in columns:
        src_ip = columns[columns.index("UDP") - 1]

        if src_ip == my_ip:
            continue

        try:

            country, sub, city = get_ip_location(src_ip)
            if start == 1:
                countryP = country
                subP = sub
                cityP = city
                start = 2
            if (countryP != country and subP != sub and cityP != city and city != "Mountain View"):
                countryP = country
                subP = sub
                cityP = city
                print("----------------------------------------------")
                print(">>> " + country + ", " + sub + ", " + city + "   IP: " + src_ip)
                #print(reader.get(src_ip))
                real_ip = socket.gethostbyname(src_ip)
                country, sub, city = get_ip_location(real_ip)
                print("> " + country + ", " + sub + ", " + city)
        except:
                print("Not found   IP: "+ src_ip)