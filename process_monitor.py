#!/usr/bin/env python
import psutil
import subprocess
import os
from time import sleep
import sys
import send_e_mail

data_list = []
new_list = []

def getpid(process_name):
    return [item.split()[1] for item in os.popen('tasklist').read().splitlines()[4:] if process_name in item.split()] 




def main():
  p = subprocess.Popen("ps -eaf | grep logstash", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  for line in p.stdout.readlines():
    data_list.append(line.replace(" ", ""))

  p.wait()

  new_list = (data_list[0])
  process_id = int(new_list[4:9])

  if process_id in psutil.pids():
    p = psutil.Process(process_id)
    if p.name() == 'java':
      p.exe()
      #print p.cmdline()
      p.pid

      p.status()
      p.create_time()
    else:
      print "Error"
  else:
    print "Process terminated()"
    send_e_mail.update_process_via_email()
    pass

if __name__ == '__main__':
  print 'Process monitoring for logstash started'
  while True:
    main()
    sleep(1)
