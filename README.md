# ChatDB

## Connect to the shared EC2

1. Download the pem key and run this command:
```
chmod 400 "chatdb.pem"
```

## Access to the jupyter notebook:

1. Connect to your instance:
```
ssh -i "chatdb.pem" -L 8888:localhost:8888 ubuntu@ec2-18-191-236-139.us-east-2.compute.amazonaws.com
```

2. Run the command line within EC2
```
jupyter notebook
```

3. Copy the following link to your browser (replace with your own token):

```
http://localhost:8888/tree?token=1634398389932c4e2447f49ac5c9218005bdca99bd963494 
```

## Command line for open and testing the django server (leave the jupyter notebook window open)

1. Connect to your instance in a new terminal: 
```
ssh -i "chatdb.pem" -L 8000:localhost:8000 ubuntu@ec2-18-191-236-139.us-east-2.compute.amazonaws.com
```

2. Go to chatdb: ```cd chatdb```
3. Command line for running the server: 
```
python manage.py runserver 0.0.0.0:8000
```

## Run Angular frontend locally

1. Install Node.js

2. Install Angular CLI:

```
npm install -g @angular/cli
```

3. Clone repo and install project’s dependencies:

```
npm install
```

4. Run locally:

```
ng serve
```



