from flask import Flask, jsonify, request, render_template
import pymysql
pymysql.install_as_MySQLdb()
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle

app = Flask(__name__)

# Database configuration
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '20020329'
app.config['MYSQL_DB'] = 'ECM'

model = None  # Global variable for the model

def get_db_connection():
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB']
    )

def train_decision_tree():
    global model
    connection = get_db_connection()
    try:
        query = """
            SELECT 
                ci.Avg_Yearly_Spend AS x1, 
                ai.Gender AS x2, 
                oi.Price_At_Time_Of_Order AS label
            FROM customer_info ci
            JOIN account_info ai ON ci.Customer_ID = ai.Customer_ID
            JOIN orders o ON ci.Customer_ID = o.Customer_ID
            JOIN order_item oi ON o.Order_ID = oi.Order_ID
        """
        df = pd.read_sql(query, connection)

        # Handle missing or invalid data
        df['x1'] = pd.to_numeric(df['x1'], errors='coerce')  # Convert x1 to numeric, set invalid values to NaN
        df['x2'] = df['x2'].map({'Male': 0, 'Female': 1}).fillna(0.5)  # Map Gender to numeric, default 0.5 for other
        df['label'] = pd.to_numeric(df['label'], errors='coerce')  # Ensure Price_At_Time_Of_Order is numeric

        # Drop rows with missing or invalid values
        df = df.dropna(subset=['x1', 'x2', 'label'])

        # Discretize the 'label' column into 5 quantile-based bins
        df['label'] = pd.qcut(df['label'], q=5, labels=[1, 2, 3, 4, 5])

        X = df[['x1', 'x2']]
        y = df['label']

        # Train the decision tree classifier
        model = DecisionTreeClassifier()
        model.fit(X, y)

        # Optionally, save the model to disk
        with open('decision_tree_model.pkl', 'wb') as f:
            pickle.dump(model, f)
    finally:
        connection.close()



# Ensure the model is trained before the first request
@app.before_request
def ensure_model_is_trained():
    global model
    if model is None:
        train_decision_tree()

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle predictions
@app.route('/predict', methods=['POST'])

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse JSON data from the request
        data = request.get_json()

        # Extract inputs
        x1 = float(data['x1'])
        x2 = data['x2'].lower()

        # Encode categorical input 'Gender'
        if x2 not in ['male', 'female']:
            x2_encoded = 0.5  # Default for unknown or ambiguous values
        else:
            x2_encoded = 0 if x2 == 'male' else 1

        # Make a prediction using the trained model
        prediction = model.predict([[x1, x2_encoded]])[0]

        return jsonify({'prediction': int(prediction)})  # Ensure prediction is serialized correctly
    except Exception as e:
        return jsonify({'error': str(e)}), 400  # Return 400 Bad Request for errors


if __name__ == '__main__':
    app.run(debug=True)
