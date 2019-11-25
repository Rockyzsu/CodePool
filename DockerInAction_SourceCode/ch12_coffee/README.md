# CoffeeFinder
CoffeeFinder is a simple flask application for keeping track of coffee shops. It exposes a single endpoint:
`/api/coffeeshops/`

You can `POST` to this endpoint to add a coffee shop to the database. Make sure you set the `Content-Type` to `application/json` and include all of the following in your `POST` body:

- `name` The name of the coffee shop. Must be unique across all coffee shops. (**String**)
- `address` The street address of the coffee shop (**String**)
- `zipcode` The zipcode of the coffee shop (**Integer**)
- `price` The price range of the coffee shop (**Integer between 1 and 5 inclusive**)
- `max_seats` The maximum number of seats in the coffee shop (**Integer**)
- `power` Whether or not the coffee shop has outlets available (**Boolean**)
- `wifi` Whether or not the coffee shop has wifi available (**Boolean**)

Example request:  
`curl -H "Content-Type: application/json" -X POST -d '{"name":"Cartel Coffee Lab", "address": "123 Derp Street #202", "zipcode": 85283, "price": 2, "max_seats": 40, "power": true, "wifi": true}' http://127.0.0.1:5000/api/coffeeshops/`

You can call the endpoint with `GET` to get a list of all coffeeshops:

```json{
  "coffeeshops": [
    {
      "address": "123 Derp Street #202", 
      "id": 1, 
      "max_seats": 40, 
      "name": "Cartel Coffee Lab", 
      "power": true, 
      "price": 2, 
      "wifi": true, 
      "zipcode": 85283
    }, 
    {
      "address": "123 Derp Street #202", 
      "id": 17, 
      "max_seats": 40, 
      "name": "Cartel Coffee Lab2", 
      "power": true, 
      "price": 2, 
      "wifi": true, 
      "zipcode": 85283
    }
  ]
}
```

# Deployment

CoffeeFinder assumes you use **postgresql** as the backing store for the coffee shops, and that you are deploying with **gunicorn**. To deploy it, make sure you've installed python and have a postgresql server running, and have created a database on that server.

We'll use python's fantastic `virtualenv` to isolate the installation of our python package requirements:  
`virtualenv coffee_env`  
Now we need to install our required python packages:  
`coffee_env/bin/pip install -r requirements/prod.txt`

We're almost ready to create our database and deploy our application. First we need to set a few environment variables:
- `COFFEEFINDER_DB_URI` This is the postgresql database URI. It should be in the form: `postgresql//username:password@host:port/database`
- `COFFEEFINDER_CONFIG` This is the configuration to use e.g. `development` or `production`. If unspecified CoffeeFinder will use the default configuration as specificed in `config.py`
 
Now we can create our database tables:  
`coffee_env/bin/python manage.py create_tables`

Finally we are ready to deploy:  
`coffee_env/bin/gunicorn -w 4 -b 127.0.0.1:3000 app.wsgi:app`

