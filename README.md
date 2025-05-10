# QueryPal Setup

## Connect to the shared EC2

1. Download the pem key and run the command:
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

1. Connect to your instance on a new terminal window: 
```
ssh -i "chatdb.pem" -L 8000:localhost:8000 ubuntu@ec2-18-191-236-139.us-east-2.compute.amazonaws.com
```

2. Go to chatdb: ```cd chatdb```
3. Command line for running the server: 
```
python manage.py runserver 0.0.0.0:8000
```

4. Open a new browser and go to the page: http://localhost:8000/  
You will see "Welcome to the Home Page!✌️" if successfully start the server



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

5. Open the web link and start asking questions! 


### Warning:
The backend project directories are hosted in a virtual Jupyter Notebook environment on the EC2 instance, so as long as the instance remains running, there's no need to download the files locally. API keys are hardcoded inside the file, feelfree to replace with your own key

## Example questions: 

### For SQL:
- What are all the tables in the postgres database?
- What columns does the rental table have?
- Show 5 sample records from the customer table.
- Show the first and last names of customers who are currently active.
- List the top 5 customers who paid the most money.
- What’s the total payment amount received in February 2022?
- For each customer, how many rentals have they made?
- Show customers who have rented more than 20 times.
- Update customer 2's email to 'PATRICIA.JOHNSON1@sakilacustomer.org'.
- [following question] Show me the customer information with customer id ‘2’.
- Find the rental and payment details (amount, date) for customer 269.
- Add a new rental with inventory_id 8888, customer_id 123, rental_date on April 23, 2025 at noon, return_date two days later, handled by staff 1.
- [following question] show me the rental with inventory_id 8888
- Delete the rental made by customer 123 with inventory 8888 on April 23, 2025.

### For Mongodb:

- What collections are currently available in the MongoDB database?
- Show me 3 sample documents from the customers collection.
- List all customers' names and emails.
- Show all orders with a total amount greater than $50.
- Show the top 5 customers who spent the most, with their names.
- Show all orders along with their item details.
- For each customer, show how many orders they have made.
- Find the top 5 customers who have spent the most in total across all their orders, and show their name, email, and total amount spent.
- Add a new customer named 'rachel' with email 'rachel@example.com'.
- Add two new customers to mongodb database. The first customer’s name is 'ddd' with email 'ddd@example.com', and the second customer’s name is ‘ffff’ with email ‘fff@example.com.’
- Update customer rachel’s email to 'tom.hardy2025@example.com'.
- Delete the customer with name rachel





