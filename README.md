# Shopify_Technical_Challenge_Summer2022

This is my submission for the Shopify Technical Challenge (Summer 2022). 

I created the CRUD (Create, Read, Update, Delete) product tracking web app by writing a Flask backend in Python. 
The app uses Flask-SQLAlchemy with a SQLite model, HTML and Jinja2 templating to render the user-facing view, and Flask routes for the controller.
For the additional feature requirement, I created a button that users can push to export product data to a CSV.

I chose Flask as my web framework because it can be used for MVC (Model, View, Controller) architecture, making it a great fit for the CRUD app requirements. Flask apps can be easily adapted to fit a diverse range of requirements by using packages like Flask-SQLAlchemy as well as other Python packages, like BytesIO and csv, which helped me create the export CSV feature.

The app can be run using a replit I have configured, accessible through [this link](https://replit.com/@molecule/ShopifyTechnicalChallengeS22#.replit). Click the green "Run" button and then click "Open Website".

Alternatively, you can run the app directly via [this link](https://shopifytechnicalchallenges22--molecule.repl.co/).
