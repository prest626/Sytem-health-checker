#Develop a script that performs routine system health checks (disk space, CPU usage, memory usage).
#Generate reports or notifications for any anomalies or potential issues.
import psutil
from email.mime.text import MIMEText 
from email.mime.image import MIMEImage 
from email.mime.application import MIMEApplication 
from email.mime.multipart import MIMEMultipart 
import smtplib 
import os
import apscheduler
from apscheduler.schedulers import Scheduler

#getting logins to email it admin 
computer_user = 'user@gmail.com'
user_password = 'user.password'
sent_from = computer_user
to = ['it_admin@gmail.com']

smtp = smtplib.SMTP('smtp.gmail.com', 587) 
smtp.ehlo() 
smtp.starttls() 
smtp.login(computer_user, user_password) 

def message(subject="System Notification",  
            text="", img=None, 
            attachment=None): 
    
    # build message contents 
    msg = MIMEMultipart() 
      
    # Add Subject 
    msg['Subject'] = subject   
      
    # Add text contents 
    msg.attach(MIMEText(text))   
    return msg
    

def check_disk_space(threshold_percent):

    disk_usage = psutil.disk_usage('/')
    if disk_usage.percent > threshold_percent:
        #email it admin
        msg = message("Disk Space Issue",f"Disk space is running low: {disk_usage.precent}% used")
        smtp.sendmail(from_addr=computer_user,to_addrs="it_admin@gmail.com",msg=msg.as_string)
        smtp.quit
def check_cpu_usage(threshold_precent):
    cpu_usage = psutil.cpu.precent()
    if cpu_usage > threshold_precent:
        #email it admin
        msg = message("CPU Usage Issue",f"High CPU usage detected: {cpu_usage}%")
        smtp.sendmail(from_addr=computer_user,to_addrs="it_admin@gmail.com",msg=msg.as_string)
        smtp.quit

def check_memory_usage(threshold_precent):
    memory_usage = psutil.virtual_memory().percent
    if memory_usage > threshold_precent:
        #email it admin
        msg = message("Memory Usage Issue",f"High memory usage detected: {memory_usage}%")
        smtp.sendmail(from_addr=computer_user,to_addrs="it_admin@gmail.com",msg=msg.as_string)
        smtp.quit

def main():
    
    #set threshold precentages
    disk_threshold=90
    cpu_threshold=80
    memory_threshold=85

    #perform the health checks
    #performing health check every hour
    check = Scheduler()
    check.start()
    check.add_job(check_disk_space(disk_threshold),'interval',seconds = 3600)
    check.add_job(check_cpu_usage(cpu_threshold),'interval',seconds = 3600)
    check.add_job(check_memory_usage(memory_threshold),'intervavl',seconds = 3600)

if __name__ == "__main__":
    main()