import subprocess
import datetime
logfile=open("/mnt/bigdiskA/log/dflog.txt", "a")
subprocess.call('df > /mnt/bigdiskA/log/df.txt', shell=True)
with open('/mnt/bigdiskA/log/df.txt', 'r') as f:
    for line in f:
        tokens=line.split()
        print line
        print len(tokens)
        if len(tokens)==6 and tokens[5]=='/mnt/bigdiskA':
            if int(tokens[4][:2]) > 90:
                subprocess.call('df | mail -s "bigdiskA close to full"  anovikova@gqrr.com maida@gqrr.com drooney@gqrr.com', shell=True)
            else:
                logfile.write('\t'.join([datetime.datetime.now().isoformat(), str(tokens[4])]) + '\n')

                
