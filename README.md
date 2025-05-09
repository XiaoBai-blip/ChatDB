# ChatDB

## Connect to the shared EC2

1. Download the pem key and run this command:
```
chmod 400 "chatdb.pem"
```

2. Connect to your instance:
```
ssh -i "chatdb.pem" -L 8888:localhost:8888 ubuntu@ec2-18-191-236-139.us-east-2.compute.amazonaws.com
```

## Access to the jupyter notebook:

1. Run the command line within EC2
```
jupyter notebook
```

2. Copy the following link to your browser (replace with your own token):

```
http://localhost:8888/tree?token=1634398389932c4e2447f49ac5c9218005bdca99bd963494 
```

## Connect to Django backend within EC2

1. 




