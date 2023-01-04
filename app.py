import psycopg2, sys, boto3, os, click, pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

conn_string = 'postgresql+psycopg2://root:4B+yBa09lobxOkdSWIsK@localhost:5432/test'

db = create_engine(conn_string)
conn = db.connect()

#Publishing messages to sqs
#messages2sqs = os.system("./message-generators/linux")

sqs_client = boto3.resource('sqs', aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key'), region_name=os.getenv('region_name'), endpoint_url=os.getenv('endpoint_url') )

queue_url = os.getenv('queue_url')

queue = sqs_client.get_queue_by_name(QueueName=os.getenv('queue_name'))

#numberofmessages = int(sys.argv[3])

# Receive message from SQS queue
@click.group()
def cli():
    pass

@click.command
@click.option("--show", metavar='',nargs=0)
def show(show):
    """
    Show all consumed messages ,Prints all consumed messages with message content and MessageId\n
    How to run >> python app.py show
    """
    sql_query = conn.execute('''select "ReceivedMessage","MessageId" from sqs_messages;''')
    df = pd.DataFrame(sql_query, columns = ['ReceivedMessage', 'MessageId'])
    print (df)

@click.command
@click.option("--clear", metavar='',nargs=0)
def clear(clear):
    """
    Clear all consumed messages from database\n
    How to run >> python app.py show
    """
    sql_query = conn.execute('''delete from sqs_messages;''')
    print ("All consumed messages now removed from database")

@click.command()
@click.option("--count", nargs=1, metavar='')

def consume(count):
    """
    Consume n messages, Prints n consumed messages with message content and MessageIds\n
    How to run >> python app.py consume --count 3
    """
    while (True):
      numberofmessages = int(sys.argv[3])
      messages = queue.receive_messages(QueueUrl=queue_url, MaxNumberOfMessages=numberofmessages, WaitTimeSeconds=5)
      try:
         d = []
         for message in messages:
             click.echo('ReceivedMessage: %s , MessageId: %s' % (message.body,message.message_id) )
             ## Here going to use pandas to send SQS messages to DB > Then delete from SQS ##
             d.append(
                 {
                     'ReceivedMessage': message.body,
                     'MessageId': message.message_id
                 }
             )
             df = pd.DataFrame(d)
             #print(df)
             message.delete()
         df.sort_values("ReceivedMessage", inplace=False)
         df2 = df.drop_duplicates(subset=['ReceivedMessage'], keep='first')
         #print(df2)
         df2.to_sql('sqs_messages', con=conn, if_exists='append', index=False)
         try:
            conn.execute("ALTER TABLE sqs_messages ADD COLUMN id SERIAL PRIMARY KEY;")
         except:
            conn.execute('''delete from sqs_messages a using sqs_messages b where a.id < b.id and a."ReceivedMessage" = b."ReceivedMessage";''')
            pass
         break
      except:
            print('Queue is empty')
            break

cli.add_command(consume)
cli.add_command(show)
cli.add_command(clear)

if __name__ == "__main__":
    cli()
    #consume()

