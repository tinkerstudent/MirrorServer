import subprocess
import re

KB = 1024
MB = 1024 * KB
MB_64= 64 * MB

def get_ip():
	output = subprocess.check_output(["ifconfig"])
	eth_num = 0
	eth_start_index = output.index("en" + str(eth_num))
	eth_end_index = output.index("en" + str(eth_num+1))
	ip = None
	while eth_start_index != -1:
		if eth_end_index != -1:
			s = output[eth_start_index:eth_end_index]
		else:
			s = output[eth_start_index:len(output)]
		m = re.search('(?<=inet )[0-9]+.[0-9]+.[0-9]+.[0-9]+', s)
		if m:
			ip = m.group(0)
			break
		else:
			eth_num = eth_num + 1
			eth_start_index = output.index("en" + (eth_num))
			eth_end_index = output.index("en" + (eth_num+1))
	return ip

