import socket
import sqlite3

class PiScanner:

    def __init__(self):
        self.pi_list = []

    def scan_network(self, range_start=1, range_end=255):
        ip_list = []
        my_ip = socket.gethostbyname(socket.gethostname())
        ip_split = my_ip.split(".")

        if range_start < 1:
            range_start = 1

        if range_end > 255:
            range_end = 255

        for i in range(range_start, range_end+1):
            base_ip = ip_split[0] + '.' + ip_split[1] + '.' + ip_split[2] + '.' + str(i)
            ip_list.append(base_ip)

        self.scan_by_ip(ip_list)

    def scan_by_hostname(self, hostnames=[]):
        for host in hostnames:
            try:
                host_ip = socket.gethostbyname(host)
                self.verify_ssh(host_ip)
            except socket.gaierror as error:
                print(f"Could not connect to {host}")

    def scan_by_ip(self, ip_list=[]):

        for ip in ip_list:
            self.verify_ssh(ip)

    def verify_ssh(self, address):
        socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)

        result = socket_obj.connect_ex((address, 22))  # address and port in the tuple format
        if result == 0:
            print(f"Connection to {address} on port 22 successful")
            self.pi_list.append(address)
        else:
            print(f"No connection to {address} on port 22 ")

        socket_obj.close()

    def save_to_db(self):
        try:
            db = sqlite3.connect("picommander.SQLITE3")
        except Exception as e:
            print(e)

        cur = db.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS ip(address)")

        for ip in self.pi_list:
            cur.execute(f"INSERT INTO ip VALUES ('{ip}')")

        db.commit()
        db.close()

