# QueryPal Setup

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

## Run and test the django server (leave the jupyter notebook window open)

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

5. Open the web link and start ask questions! 
Example questions: 
- What are all the tables in the postgres database?
What columns does the rental table have?
Show 5 sample records from the customer table.
Show the first and last names of customers who are currently active.
List the top 5 customers who paid the most money.
What’s the total payment amount received in February 2022?
For each customer, how many rentals have they made?
Show customers who have rented more than 20 times.
Update customer 2's email to 'PATRICIA.JOHNSON1@sakilacustomer.org'.
[following question] Show me the customer information with customer id ‘2’.
Find the rental and payment details (amount, date) for customer 269.

Add a new rental with inventory_id 8888, customer_id 123, rental_date on April 23, 2025 at noon, return_date two days later, handled by staff 1.
[following question] show me the rental with inventory_id 8888
Delete the rental made by customer 123 with inventory 8888 on April 23, 2025.




