import subprocess
import requests

class ssh:

	def __init__(self, ip_address="", username="pi", password="raspberry"):
		self.ip_address = ip_address
		self.username = username
		self.password = password
		# See if putty exists.  If not, download it.
		try:
			self.file = open("putty.exe")
			self.file.close()
		except FileNotFoundError:
			self.download_putty()

	@staticmethod
	def download_putty(self):
		file_url = "https://the.earth.li/~sgtatham/putty/latest/w64/putty.exe"
		r = requests.get(file_url, stream=True)

		with open("putty.exe", "wb") as putty:
			for chunk in r.iter_content(chunk_size=1024):
				if chunk:
					putty.write(chunk)

	def start(self):
		try:
			subprocess.Popen(f"putty.exe {self.username}@{self.ip_address} -pw {self.password}")
		except Exception as e:
			print(e)


myssh = ssh("192.168.75.66", password="VG30dett")
myssh.start()
