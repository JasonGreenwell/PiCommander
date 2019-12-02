import paramiko
import time
import threading


class PiCommander:

    def __init__(self, number_of_Pi):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.stdin, self.stdout, self.stderr = (0, 0, 0)
        self.count = number_of_Pi
        self.hosts = []

    def connect(self, hosts=[], username='', password=''):
        self.hosts = hosts
        for host in hosts:
            try:
                self.ssh.connect(hostname=host, username=username, password=password)
            except paramiko.BadAuthenticationType as bad_auth_type:
                # TODO: Log and do something
                pass
            except paramiko.AuthenticationException as authentication_exception:
                # TODO: Log and do something
                pass
            except paramiko.SSHException as ssh_exception:
                # TODO: Log and do something
                pass
            except TimeoutError as timeout_error:
                # TODO: Log and do something
                pass
            finally:
                # TODO: Do something regardless?  Maybe log the error
                pass

    def command(self, command):

        for host in self.hosts:
            self.stdin, self.stdout, self.stderr = self.ssh.exec_command(command)
            print(f"Host: {host}")
            if self.stderr:
                for _ in self.stderr:
                    print(f"Command Unsuccessful: {_.strip()}")
            elif not self.stderr:
                print("Command Successful")
                time.sleep(3)

            for _ in self.stdout.readlines():
                print(_.strip())


Pi0 = PiCommander(1)

Pi0.connect(['192.168.75.66', '192.168.75.67'], 'pi', 'VG30dett')
Pi0.command('ls')