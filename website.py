from flask import Flask, render_template,request
import boto3


app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/resultat',methods = ['POST'])
def resultat():
    sqs = boto3.client('sqs')
    result = request.form
    n = result['liste']
    response = sqs.get_queue_url(QueueName='requestQueue')
    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=response['QueueUrl'],
        DelaySeconds=10,
        MessageAttributes={
          'Liste': {
              'DataType': 'String',
              'StringValue': n
          }
        },
        MessageBody=(
          'Test message'
        )
    )
    
    median=None
    mean=None
    result = request.form
    sqs = boto3.resource('sqs')
    while(median==None):
        response = sqs.get_queue_by_name(QueueName='responseQueue')
        messages = response.receive_messages(MaxNumberOfMessages=1,MessageAttributeNames=['All'])
        for msg in messages:
            median=msg.message_attributes.get('Median').get(u'StringValue')
            mean=msg.message_attributes.get('Mean').get(u'StringValue')
            min=msg.message_attributes.get('Min').get(u'StringValue')
            max=msg.message_attributes.get('Max').get(u'StringValue')
            liste=msg.message_attributes.get('Liste').get(u'StringValue')
        if(median!=None):
            response.purge();

    return render_template("resultat.html", entier1=min, entier2=max, entier3=median, entier4=mean,entier5=liste)
    

if __name__ == "__main__":
    app.run(debug=True)
