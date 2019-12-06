import paramiko
import datetime
from PiScanner import PiScanner

class PiControl:

    def __init__(self):
        self.now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.stdin, self.stdout, self.stderr = (0, 0, 0)
        self.hosts = []
        self.username = ''
        self.password = ''
        self.connection_tries = 2

    def connect(self, hosts=[], username='', password=''):
        self.hosts = hosts
        self.username = username
        self.password = password
        for host in hosts:
            try:
                self.ssh.connect(hostname=host, username=self.username, password=self.password)
                self.log(f"INFO [{host}]: Connection Successful")
            except paramiko.BadAuthenticationType as bad_auth_type:
                # TODO: Log and do something
                self.log(f"ERROR [{host}]: {bad_auth_type}")
            except paramiko.AuthenticationException as authentication_exception:
                # TODO: Log and do something
                self.log(f"ERROR [{host}]: {authentication_exception}")
            except paramiko.SSHException as ssh_exception:
                # TODO: Log and do something
                self.log(f"ERROR [{host}]: {ssh_exception}")
            except paramiko.ssh_exception.NoValidConnectionsError as no_valid_connection:
                self.log(f"ERROR [{host}]: {no_valid_connection}")
            except TimeoutError as timeout_error:
                # TODO: Log and do something
                self.log(f"ERROR [{host}]: {timeout_error}")
                self.hosts.pop(self.hosts.index(f"{host}"))

    def command(self, command):
        for host in self.hosts:
            self.stdin, self.stdout, self.stderr = self.ssh.exec_command(command)
            error = self.stderr.readlines()
            if error:
                print(f"Command {command} to host {host} unsuccessul")
                for _ in error:
                    print(_.strip())
            else:
                print("*" * 20)
                print(f"Command {command} to host {host} successful")
                print("*" * 20)
                for _ in self.stdout.readlines():
                    print(f"{_.strip()}")
                print("*" * 20)

    def log(self, text):
        # CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
        with open('log.log', 'a') as file:
            file.write(f"{self.now} {text}\n")

    def main(self):
        pass


scanner = PiScanner()
scanner.scan_network(65, 66)
print(scanner.pi_list)
scanner.save_to_db()
print("-"*60)
Pi0 = PiControl()
Pi0.connect(scanner.pi_list, 'pi', 'VG30dett')
Pi0.command('cd Documents && sudo mkdir py')
