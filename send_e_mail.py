#!/usr/bin/env python

import mysql_queries as mysql
import boto3
import time
import sched
import logmanager
import mysql_queries

client = boto3.client('sns')
log_m = logmanager.LogManager()
log = log_m.logger()

""" update daily ESC information via email to Sarath for now """

def update_process_via_email():
  py_subject = "Alert: logstash terminated"
  py_message = "Logstash killed.. please restart.. "
  response = client.list_subscriptions_by_topic(TopicArn='arn:aws:sns:us-west-2:796687173965:alert_esc_daily_update', NextToken='')
  log.debug(response)
  response = client.publish(TopicArn='arn:aws:sns:us-west-2:796687173965:alert_esc_daily_update', Message=py_message, Subject=py_subject, MessageStructure='Raw')
# Notify deployment details regarding e-mail

def update_esc_via_email():
  py_subject = "Update: ESC Daily Status Report"
  py_message = "ESC Name    Bytes Tx    Bytes Rx    Local IP    Remote IP Connected Since    Comm Status     Heartbeat Count     Software Ver    Firmware Ver\n\n"
  data = mysql_queries.mysql_query_select_esc_tblfor_email()   
  for line in data:
    if  line is not None:
      py_message += str(line)+ "\n\n"
  response = client.list_subscriptions_by_topic(TopicArn='arn:aws:sns:us-west-2:796687173965:alert_esc_daily_update', NextToken='')
  log.debug(response)
  response = client.publish(TopicArn='arn:aws:sns:us-west-2:796687173965:alert_esc_daily_update', Message=py_message, Subject=py_subject, MessageStructure='Raw')
