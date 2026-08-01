# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
sales_revenue_predictor_api = Flask("SuperKart Sales Revenue Predictor Application")

# Load the trained machine learning model
model = joblib.load("superkart_model.joblib")

# Define a route for the home page (GET request)
@sales_revenue_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the SuperKart Sales Revenue Prediction API!"

# Define an endpoint for single store revenue prediction (POST request)
@sales_revenue_predictor_api.post('/v1/revenue')
def predict_sales_revenue():
    """
    This function handles POST requests to the '/v1/revenue' endpoint.
    It expects a JSON payload containing products & stores and returns
    the predicted sales revenue as a JSON response.
    """
    # Get the JSON data from the request body
    product_store_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'Product_Weight': product_store_data['Product_Weight'], 
        'Product_Sugar_Content': product_store_data['Product_Sugar_Content'], 
        'Product_Allocated_Area': product_store_data['Product_Allocated_Area'],
        'Product_MRP': product_store_data['Product_MRP'], 
        'Store_Size': product_store_data['Store_Size'], 
        'Store_Location_City_Type': product_store_data['Store_Location_City_Type'],
        'Store_Type': product_store_data['Store_Type'], 
        'Product_Id_Char': product_store_data['Product_Id_Char'],
        'Store_Age_Years': product_store_data['Store_Age_Years'],
        'Product_Type_Category': product_store_data['Product_Type_Category']
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction (get product_store_sales_total)
    predicted_product_store_sales_total = model.predict(input_data)[0]

    # Convert predicted_price to Python float
    predicted_product_store_sales_total = round(float(predicted_product_store_sales_total), 2)

    # Return the actual price
    return jsonify({'Predicted sales revenue (in dollars)': predicted_product_store_sales_total})


# Define an endpoint for batch prediction (POST request)
@sales_revenue_predictor_api.post('/v1/revenuebatch')
def predict_sales_revenue_batch():
    """
    This function handles POST requests to the '/v1/revenuebatch' endpoint.
    It expects a CSV file containing SuperKart details for multiple stores
    and returns the predicted sales revenue as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all stores in the DataFrame (get product_store_sales_total)
    predicted_sales_revenue = model.predict(input_data).tolist()

    # Create a dictionary of predictions with product_store_id IDs as keys
    product_store_id = input_data['id'].tolist()  # Assuming 'id' is the product & store combination ID column
    output_dict = dict(zip(product_store_id, predicted_sales_revenue)) 

    # Return the predictions dictionary as a JSON response
    return output_dict

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    sales_revenue_predictor_api.run(debug=True)
