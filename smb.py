import subprocess

def smb_vuln(host):

	result = subprocess.run(
		f"smbclient -L //{host} -U 'Convidado' -N 2>/dev/null | awk '{{if ($0 ~ /listing/) print $2}}' ",
		shell=True, capture_output=True, text=True
	)

	return bool(result.stdout.strip())

if __name__ == "__main__":
	import sys

	if len(sys.argv) < 2:
		print("Usage: <IP ADRESS>")
		sys.exit(1)

	host = sys.argv[1]
	if smb_vuln(host):
		print("Vulnerable")
	else:
		print("Safe")
