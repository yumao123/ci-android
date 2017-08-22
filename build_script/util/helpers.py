import time, subprocess, datetime


def timeout_command(command, fileName= None, timeout= None):
	start = datetime.datetime.now()
	if fileName is not None:
		f = open(fileName, 'a')
		f.flush()
	process = subprocess.Popen(command, shell=True, bufsize=10000, close_fds=True, 
		stdout = f.fileno(), stderr = f.fileno())
	
	while process.poll() is None:
		time.sleep(0.1)
		now = datetime.datetime.now()
		if timeout is not None:
			if (now - start).seconds> timeout:
				try:
					process.terminate()
				except Exception,e:
					return None
				return None
	# out = process.communicate()[0]
	out = process.poll()
	if process.stdin:
		process.stdin.close()
	if process.stdout:
		process.stdout.close()
	if process.stderr:
		process.stderr.close()
	try:
		process.kill()
	except OSError:
		pass
	return out