from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

def errorprint(s):
    print('Error: '+ s)



class sensorHealthDB(object):
    def __init__(self, region='us-west-2',tablename='ESC_Sensor_Health'):
        self._dynamodb = boto3.resource('dynamodb', region_name=region)
        self._table = self._dynamodb.Table(tablename)

    def getItem(self, siteID):
        response = self._table.get_item(
        Key={'ESCID':siteID}
        )
        if 'Item' in response:
            return response['Item']
        else:
            errorprint('Item not found')

    def deleteItem(self,iap_id):
        response = self._table.delete_item(
                Key={
                    'ESCID': iap_id
                }
        )
        print("deleteItem succeeded:")
        print(json.dumps(response, indent=4, cls=DecimalEncoder))

    def createItem(self,site_id):
        try:
            self._table.put_item(
                    Item={
                        'ESCID' : site_id,
                        'bandIndex' : decimal.Decimal('0.0'),
                        'timeStampHealthcheck' : "NA",
                        'agcGain' : decimal.Decimal('0.0'),
                        'gpioOverLoad' : decimal.Decimal('0.0'),
                        'gpioSPIvalue' : decimal.Decimal('0.0'),
                        'rmsAverage' : "NA",
                        'agcMaxVal' : decimal.Decimal('0.0'),
                        'noiseRssiDbm' : "NA",
                        'dcI' : decimal.Decimal('0.0'),
                        'dcQ' : decimal.Decimal('0.0'),
                        'iqImbalanceGaindB' : decimal.Decimal('0.0'),
                        'iqImbalancePhaseDeg' : decimal.Decimal('0.0'),
                        'numDmaOverflows' : decimal.Decimal('0.0'),
                        'adiRxLoHz' : decimal.Decimal('0.0'),
                        'adiTxLoHz' : decimal.Decimal('0.0'),
                        'adiGainValue' : decimal.Decimal('0.0'),
                        'adiTxAttenutation' : decimal.Decimal('0.0'),
                        'adiRxClockHz' : decimal.Decimal('0.0'),
                        'adiTxClockHz' : decimal.Decimal('0.0'),
                        'oneMinLoad' : decimal.Decimal('0.0'),
                        'memoryFreeKb' : decimal.Decimal('0.0'),
                        'memoryTotalKb' : decimal.Decimal('0.0'),
                        'upTime' : decimal.Decimal('0.0'),
                        'cpuClockSpeed' : decimal.Decimal('0.0'),
                        'humidity' : "NA",
                        'temperature' : "NA",
                        'xAxis' : decimal.Decimal('0.0'),
                        'yAxis' : decimal.Decimal('0.0'),
                        'zAxis' : decimal.Decimal('0.0'),
                        'compassChange' : decimal.Decimal('0.0'),
                    },
                    ConditionExpression=Attr("ESCID").ne(site_id)
                )

        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                print(e.response['Error']['Message'])
            else:
                raise
        else:
            print("+++ createitem succeeded +++")

    def setItem(self, site_id, bandIndex, timeStampHealthcheck, agcGain, gpioOverLoad, gpioSPIvalue, rmsAverage, agcMaxVal,
                noiseRssiDbm, dcI, dcQ, iqImbalanceGaindB, iqImbalancePhaseDeg, numDmaOverflows, adiRxLoHz, adiTxLoHz, adiGainValue,
                adiTxAttenutation, adiRxClockHz, adiTxClockHz, oneMinLoad, memoryFreeKb, memoryTotalKb, upTime, cpuClockSpeed,
                humidity, temperature, xAxis, yAxis, zAxis, compassChange):
        response = self._table.update_item(
            Key={
                'ESCID': site_id,
            },
            UpdateExpression="set bandIndex= :a, timeStampHealthcheck= :b, agcGain= :c, gpioOverLoad= :d, gpioSPIvalue= :e, rmsAverage= :g, agcMaxVal= :h, noiseRssiDbm= :i, dcI= :j, dcQ= :k, iqImbalanceGaindB= :l, iqImbalancePhaseDeg= :m, numDmaOverflows= :n, adiRxLoHz= :o, adiTxLoHz= :p, adiGainValue= :q, adiTxAttenutation= :r, adiRxClockHz= :s, adiTxClockHz= :t, oneMinLoad= :u, memoryFreeKb= :v, memoryTotalKb= :w, upTime= :x, cpuClockSpeed= :y, humidity= :z, temperature= :aa, xAxis= :ab, yAxis= :ac, zAxis= :ad, compassChange= :ae",
            ExpressionAttributeValues={
            ':a': bandIndex,
            ':b': timeStampHealthcheck,
            ':c': agcGain,
            ':d': gpioOverLoad,
            ':e': gpioSPIvalue,
            ':g': rmsAverage,
            ':h': agcMaxVal,
            ':i': noiseRssiDbm,
            ':j': dcI,
            ':k': dcQ,
            ':l': iqImbalanceGaindB,
            ':m': iqImbalancePhaseDeg,
            ':n': numDmaOverflows,
            ':o': adiRxLoHz,
            ':p': adiTxLoHz,
            ':q': adiGainValue,
            ':r': adiTxAttenutation,
            ':s': adiRxClockHz,
            ':t': adiTxClockHz,
            ':u': oneMinLoad,
            ':v': memoryFreeKb,
            ':w': memoryTotalKb,
            ':x': upTime,
            ':y': cpuClockSpeed,
            ':z': humidity,
            ':aa': temperature,
            ':ab': xAxis,
            ':ac': yAxis,
            ':ad': zAxis,
            ':ae': compassChange,
            },
            ReturnValues="UPDATED_NEW"
        )
        print("setItem succeeded:")
        #print(json.dumps(response, indent=4, cls=DecimalEncoder))


#Fetch the ESC configuration details
class ConfigDB(object):
    def __init__(self, region='us-west-2',tablename='ESC_CONFIG'):
        self._dynamodb = boto3.resource('dynamodb', region_name=region)
        self._table = self._dynamodb.Table(tablename)

    def getItem(self, siteID):
        response = self._table.get_item(
        Key={'ESCID':siteID}
        )
        if 'Item' in response:
            return response['Item']
        else:
            errorprint('Item not found')
            return None

#_________________________________________________________________________
#Fetch the ESC deploy details
class deployDB(object):
    def __init__(self, region='us-west-2',tablename='ESC_DEPLOY_INFO'):
        self._dynamodb = boto3.resource('dynamodb', region_name=region)
        self._table = self._dynamodb.Table(tablename)

    def getItem(self, siteID):
        response = self._table.get_item(
        Key={'SITE_ID':siteID}
        )
        if 'Item' in response:
            return response['Item']
        else:
            errorprint('Item not found')
            return None

    def createItem(self,site_id):
        try:
            self._table.put_item(
                    Item={
                        'SITE_ID' : site_id,
                        'ESC_LABEL_NO' : decimal.Decimal(0),
                        'DEPLOY_STATUS' : decimal.Decimal(0) 
                    },
                    ConditionExpression=Attr("SITE_ID").ne(site_id)
                )

        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                print(e.response['Error']['Message'])
            else:
                raise
        else:
            print("createitem succeeded")

    def setItem(self,site_id, label, status):
        response = self._table.update_item(
            Key={
                'SITE_ID': site_id,
            },
            UpdateExpression="set ESC_LABEL_NO= :i, DEPLOY_STATUS  =:p",
            ExpressionAttributeValues={
            ':i': label,
            ':p': status,
            },
            ReturnValues="UPDATED_NEW"
        )
        print("setItem succeeded:")
        print(json.dumps(response, indent=4, cls=DecimalEncoder))


#_________________________________________________________________________




# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


class DynamoDB(object):
    def __init__(self, region='us-west-2',tablename='FW_MTEP_IAP_PORT_MAP'):
        self._dynamodb = boto3.resource('dynamodb', region_name=region)
        self._table = self._dynamodb.Table(tablename)


    
    def getItem(self,iap_id):
        response = self._table.get_item(
        Key={'IAP_ID':iap_id}
        )
        print(response)
        if 'Item' in response:
            return response['Item']
        else:
            errorprint('Item not found')
            return None
    
    def getIP(self,iap_id):
        item = self.getItem(iap_id)
        if item == None:
            errorprint('Item not found')
            return None
        return item['IAP_IP']
    
    def getProtoMap(self,iap_id,proto_name):
        item = self.getItem(iap_id)
        if item == None:
            errorprint('Item not found')
            return None
        return item['proto_map'][proto_name]
    
    def getAWSPort(self,iap_id,proto_name):
        protomap = self.getProtoMap(iap_id,proto_name)
        if protomap == None:
            errorprint('protomap not found')
            return None
        return protomap['AWS_PORT']
    
    def getIAPPort(self,iap_id,proto_name):
        protomap = self.getProtoMap(iap_id,proto_name)
        if protomap == None:
            errorprint('protomap not found')
            return None
        return protomap['IAP_PORT']

    def createItem(self,iap_id,default_proto='ssh',default_port=22):
        try:
            self._table.put_item(
                    Item={
                        'IAP_ID' : iap_id,
                        'IAP_IP' : '0.0.0.0',
                        'proto_map' : {
                            default_proto : {
                                'AWS_PORT' : decimal.Decimal(0), 'IAP_PORT' : decimal.Decimal(default_port)
                             }
                        }
                    },
                    ConditionExpression=Attr("IAP_ID").ne(iap_id)
                )
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                print(e.response['Error']['Message'])
            else:
                raise
        else:
            print("createitem succeeded")
        
    def setItem(self,iap_id,iap_ip,proto_name,aws_port,iap_port):
        response = self._table.update_item(
            Key={
                'IAP_ID':iap_id,
            },
            UpdateExpression="set IAP_IP = :i, proto_map." + proto_name +  "=:p",
            ExpressionAttributeValues={
            ':i': iap_ip,
            ':p': {'AWS_PORT' : aws_port, 'IAP_PORT' : iap_port}
            },
            ReturnValues="UPDATED_NEW"
        )
        print("setItem succeeded:")
        print(json.dumps(response, indent=4, cls=DecimalEncoder))

    def deleteItem(self,iap_id):
        response = self._table.delete_item(
                Key={
                    'IAP_ID': iap_id
                }
        )
        print("deleteItem succeeded:")
        print(json.dumps(response, indent=4, cls=DecimalEncoder))
        
        

        
        



