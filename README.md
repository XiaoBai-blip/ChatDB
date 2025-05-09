# ChatDB

## Setup

Connect to EC2:
```chmod 400 "chatdb.pem"```
```ssh -i "chatdb.pem" -L 8888:localhost:8888 ubuntu@ec2-18-191-236-139.us-east-2.compute.amazonaws.com```




## Setup

1. Install node:
   https://nodejs.org/en/download

2. Install dependencies
   
   ```npm install```

4. Generate chart
   
   ```node Visuals/[ChartType].mjs```


## Worker interaction

1. Worker is currently set up and deployed on Miles' Cloudflare account (will move to Annenberg after testing)

2. For javascript fetching: 

```
fetch('https://dps-chart-worker.miles-kirkbride.workers.dev/{filename_of_resource}')
  .then(response => response.json())
  .then(data => console.log(data));
```


