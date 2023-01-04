##Introduction##

This tool basically used to consume/show/clear SQS messages which provided by a producer within this project [message-generators/Linux] ,you can see three core components this tool will deal with during processing [SQS container + SQS messages Consumer +  Postgres database container].

The process as whole can be explained like this [messages-generator > SQS > Postgres ] and each one will play a different role as follows:

- Messages-generator : to generate messages and push to SQS instance
- SQS : to store the messages that coming from the generator waiting for a consumer to process the data [the consumer here will be our tool]
- Postgres : to save the messages on a table with persistent volume using docker compose.

##How to Run the Tool##
Please follow these steps to run the tool successfully :

1# Requirements before starting >> you have to install  [docker , docker-compose , python3.10 , python3.10-venv ]

2# 
  - cd bayzat-sre-engineering-assignment-RamiMohammad-9rklkmfezp/
  -  chmod +x run.sh
  -  source run.sh     [this script will do most of the job for you including [pushing messages to SQS to be consumed, install reqs , creating virtualenv , running the docker containers for you and few needed configs to be ready to run the app]]


3# Now you can use the tool >> python app.py --help

Here more details to make things more clear :

 -  python app.py consume --count 3 >> this command will receive 3 messages from SQS > save the to database > delete from SQS.
 -  python app.py show >> this command will show you all the consumed messages. 
 -  python app.py clear >> this command will clear all the consumed messages from the database.

