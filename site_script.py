

import os
import smtplib
import requests
import logging
from linode_api4 import LinodeClient, Instance

EMAIL_ADDRESS = os.environ.get('EMAIL_USER') #first save the email as env variable
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')#save your password as env variable
LINODE_TOKEN = os.environ.get('LINODE_TOKEN') #the token to connect with your server, here it is linode
                                               # here it is linode server

#to get  an instance of our server, run the below code:

#for client in Instance:
#   y='client.servername: client.id'
#   print(y)

 
def notify_user():              #function to execute the script for sending mail
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        subject = 'YOUR SITE IS DOWN!'
        body = 'Make sure the server restarted and it is back up'
        msg = f'Subject: {subject}\n\n{body}'

        # logging.info('Sending Email...')
        smtp.sendmail(EMAIL_ADDRESS, 'INSERT_RECEIVER_ADDRESS', msg)


def reboot_server(): #function to reboot server when it is down
    client = LinodeClient(LINODE_TOKEN) #connecting to our linode server with token
    my_server = client.load(Instance, 376715) #opening a particular instance of our server
    my_server.reboot()
    logging.info('Attempting to reboot server...')


#TO CHECK WHETHER OUR SERVER IS DOWN IN EVERY TEN MINUTES i.e TO MAKE A SITE MONITOR:
#     WE WILL MAKE A COMMAND TO RUN THE SCRIPT INSTEAD OF RUNNING IT MANUALLY
#     COMMAND SYNTAX FOR IT IS FOUND IN COREY SCHAFER
#      TO SET THE TIMER OF 10 MIN WE USE TASK SCHEDULER IN WINDOWS WHICH WILL RUN
#       THE ABOVE COMMAND EVERY TEN MINUTES SO OUR SCRIPT IS AUTOMATIZED
# I HAVE NOT DONE IT IN BELOW CODE BUT U CAN DO IT YOURSELF CHECK COREY SCHAFER


try:                     #if there is response of any kind then try block
    r = requests.get('https://example.com', timeout=5)

    if r.status_code != 200:
        # logging.info('Website is DOWN!')
        notify_user()
        reboot_server()
    else:
        # logging.info('Website is UP')
except Exception as e:       # if there is no sort of response then except
    # logging.info('Website is DOWN!')
    notify_user()
    reboot_server()
