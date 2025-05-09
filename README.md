# ChatDB

## Setup

1. Run this command with downloaded perm key:
```chmod 400 "chatdb.pem"```

2. Connect to your instance:
```ssh -i "chatdb.pem" -L 8888:localhost:8888 ubuntu@ec2-18-191-236-139.us-east-2.compute.amazonaws.com```

3. Open jupyter notebook:

```jupyter notebook```

4. Copy the following link to your browser (replace with your own generated token):

```http://localhost:8888/tree?token=1634398389932c4e2447f49ac5c9218005bdca99bd963494 ```




