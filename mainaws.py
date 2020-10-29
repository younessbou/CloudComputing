import boto3
import statistics
import os


KEY = 'ASIA2NGG2JYVXY3ZIPGH'
SECRET = 'WzycbKZMvNy6O6BnqtkwOlJi1J3GnCIBwM8fHTYT'
Token='FwoGZXIvYXdzEAQaDH0l14FuKIBqxT9rdSLWAavkjQ4k395aRrE/2c0oBi70MxddsqhiXa0kMqr76KZ0Z73ax9WgRGyV1Tgqtp48/+gFQHlSK/pVwQoHnZXRNenlTJeaZjqYTwBFsmE7bVJyyHAKreMbTTgUGm8ec/QXlJ1EE8Acy0rzblTB2ZciKmZCXP5MywgBKfNQKqrC1yF7tfbbbjT0Xl6vwX2cbuMLxInYINqOXTcMWQNT5abWjcrr/uyQNnhB9DVVM23c9b3dirRlHr9pGeYmFRpj3Mxxo0DnLnehFpG89tczdmp0KT3PELEiOFMozaPs/AUyLRUWZKOYuQ/KvGrSKZwSGUeXfoa/DNEqIpO2DuwRUX/uKGrRbCGCm82qqvyl3w=='


# Using the default session
sqs = boto3.resource('sqs', aws_access_key_id=KEY,aws_secret_access_key= SECRET,aws_session_token=Token, region_name='us-east-1')

while True:
    # Récuperer queue
    response = sqs.get_queue_by_name(QueueName='requestQueue')
    # Récuperer message
    messages = response.receive_messages(MaxNumberOfMessages=1,MessageAttributeNames=['All'])
    n=None
    p=None
    #Recuperer liste d'entier a partir de la requestQueue
    for msg in messages:
        n=(msg.message_attributes.get('Liste').get(u'StringValue'))

    if(n!=None):
        liste1 = n.split (",")
        liste=[]
        for i in range (len(liste1)):
            if liste1[i].isdigit():
                liste.append(int(liste1[i]))
        response.purge();
        if len(liste)==0:
            liste.append(0)
        somme=sum(liste)
        min1=min(liste)
        max1=max(liste)
        median1=statistics.median(liste)
        mean1=statistics.mean(liste)
        #Connexion client sqs
        sqs1 = boto3.client('sqs', aws_access_key_id=KEY,aws_secret_access_key= SECRET,aws_session_token=Token, region_name='us-east-1')
        response1 = sqs1.get_queue_url(QueueName='responseQueue')
        # Envoyer message a responseQueue
        response1 = sqs1.send_message(
            QueueUrl=response1['QueueUrl'],
            DelaySeconds=10,
            MessageAttributes={
                'Min': {
                    'DataType': 'Number',
                    'StringValue': str(min1)
                },
                'Max': {
                    'DataType': 'Number',
                    'StringValue': str(max1)
                },
                'Median': {
                    'DataType': 'Number',
                    'StringValue': str(median1)
                },
                'Mean': {
                    'DataType': 'Number',
                    'StringValue': str(mean1)
                },
                'Liste': {
                    'DataType': 'String',
                    'StringValue': str(liste)
                }
            },
            MessageBody=(
                'Test message'
            )
        )
        #Ecrire dans un fichier txt
        os.mknod("log.txt")
        fichier = open("log.txt", "a")
        fichier.write("Liste: "+str(liste)+"\n"+"Min:"+str(min1)+"\n"+"Max:"+str(max1)+"\n"+"Median:"+str(median1)+"\n"+"Mean:"+str(mean1))
        fichier.close()
        #Envoi vers s3
        s3 = boto3.client('s3', aws_access_key_id=KEY,aws_secret_access_key=SECRET,aws_session_token=Token, region_name='us-east-1')
        with open("log.txt", "rb") as f:
            s3.upload_fileobj(f, "mybucket10", "Logfile")
        os.remove("log.txt")
    



