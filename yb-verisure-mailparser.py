import json
import boto3
import email
import email.policy
import time
import os
import urllib3

s3 = boto3.client('s3')
bucket = os.environ['SRC_BUCKET']
url = os.environ['URL']
delete_src_mail = os.environ['DELETE_SRC_MAIL']

def send_data(data):
        http = urllib3.PoolManager()
        x = http.request(
           'POST', 
           url, 
           body=json.dumps(data), 
           headers={'Content-Type': 'application/json'})

def lambda_handler(event, context):
    '''
    Lambda function that looks for an object in S3 in a given bucket, tries to 
    parse it as a Verisure email notification and forward the relevant info to
    an external API endpoint.
    '''

    try:
        oid = event['Records'][0]['s3']['object']['key']
    except Exception as e:
        print('=-=-= Lambda triggered without s3 object key, ignoring =-=-=')
        return

    try:
        s3object = s3.get_object(Bucket=bucket, Key=oid)
        
        # default policy has to be set to parse as email.message.EmailMessage
        msg = email.message_from_bytes(
            s3object['Body'].read(), policy=email.policy.default)
        
        sender = msg.get('From')
        if (sender != "no-reply@verisure.com"):
            print(f'=-=-= Ignoring message from unknown sender {sender}... =-=-=')
            # return 'CONTINUE'
        
        subject = msg.get('Subject')
        print(f'=-=-= Received Verisure message with subject {subject} =-=-=')
        
        i = 0
        # Look for the text/plain part in the message that contains the info
        for part in msg.walk():
            i+=1
            ctype = part.get_content_type()
            if (ctype == 'text/plain'):
                
                body = part.get_payload(decode=True)

                if (subject == 'Upplåst utifrån'):
                    # Unlocked with code from outside, look for username
                    # look for "av " and parse everything up to next period
                    body_partition = str(body).partition('av ')
                    username = body_partition[2].partition('.')[0]
                    send_data({
                        "event": "Unlocked from outside", 
                        "username": username})

                elif (subject == 'Upplåst'):
                    # Unlocked remotely, look for username
                    # look for "av " and parse everything up to next period
                    body_partition = str(body).partition('av ')
                    username = body_partition[2].partition('.')[0]
                    send_data({
                        "event": "Remotely unlocked", 
                        "username": username})
                    
                elif (subject == 'Upplåst inifrån'):
                    # Unlocked from inside
                    send_data({
                        "event": "Unlocked from inside", 
                        "username": "unknown user"})
                    
                elif (subject == 'Låst inifrån'):
                    # Locked from inside
                    send_data({
                        "event": "Locked from inside", 
                        "username": "unknown user"})
                    
                else:
                    print('=-=-= Unknown event: =-=-=')
                    print(body)
                    send_data({
                        "event": subject, 
                        "username": "unknown user"})
                    
            else:
                print(f'=-=-= Ignoring {ctype} part {i}... =-=-=')

        # Optionally delete the email from S3
        if (delete_src_mail=='True'):
            s3.delete_object(Bucket=bucket,Key=oid)
        
    except Exception as e:
        print(e)
        print(f'Error getting object {oid} from bucket {bucket}')
        raise e
        
    return 'CONTINUE'

