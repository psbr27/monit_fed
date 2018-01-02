#!/usr/bin/env python

import mysql_queries as mysql
import boto3

import logmanager

client = boto3.client('sns')
log_m = logmanager.LogManager()
log = log_m.logger()


# Notify SMS regarding the deployment
def notify_sms(esc_id, site_i_d, esc_label):
    py_subject = "Alert: ESC Deployed"
    py_message = "ESC deployed successfully at site: " + site_i_d + "\n" + " ESC Label Number: " + esc_label + "\n"
    response = client.list_subscriptions_by_topic(TopicArn='arn:aws:sns:us-west-2:796687173965:ESC_Deploy_Notification',
                                                  NextToken='')
    log.debug(response)
    response = client.publish(TopicArn='arn:aws:sns:us-west-2:796687173965:ESC_Deploy_Notification', Message=py_message,
                              Subject=py_subject, MessageStructure='Raw')


# Notify deployment details regarding e-mail

def notify_email(esc_id, site_i_d, esc_label):
    py_subject = "Alert: ESC Deployed"
    py_message = "ESC deployed successfully at site: " + site_i_d + "\n" + " ESC Label Number: " + esc_label + "\n"
    response = client.list_subscriptions_by_topic(TopicArn='arn:aws:sns:us-west-2:796687173965:NotifyDeployment',
                                                  NextToken='')
    log.debug(response)
    response = client.publish(TopicArn='arn:aws:sns:us-west-2:796687173965:NotifyDeployment', Message=py_message,
                              Subject=py_subject, MessageStructure='Raw')


#if __name__ == '__main__':
#  status = mysql.mysql_get_deploy_status('esc_sn010')
#  print status
#  if status == 0:
#    d_list = mysql.mysql_select_deploy_list('esc_sn010')
#    print d_list
#    notify_sms('esc_sn010',d_list[0],str(d_list[1]))
##    notify_email('esc_sn010',d_list[0],str(d_list[1]))
