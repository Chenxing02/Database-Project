# Database-Project

# Food Company Membership Level Predictor

This project is a **web-based application** for predicting the membership level of customers in a food company using their demographic information and yearly spend. It leverages a **Decision Tree Classifier** to classify customers into five levels based on their spending patterns.

## Project Structure
```
DMS_FINAL/
├── project_code/
│   ├── templates/
│   │   └── index.html       # Front-end interface (HTML + JavaScript)
│   ├── app.py               # Flask back-end application
│   ├── decision_tree_model.pkl # Pre-trained Decision Tree model
│   └── project_code.zip     # Zipped project folder
```

## Features
1. **Data Processing and Modeling**:
   - Prepares and cleans data from a MySQL database.
   - Trains a Decision Tree Classifier to predict membership levels.
   - Discretizes continuous spending data into five quantiles (membership levels 1 to 5).

2. **Front-End Interface**:
   - Built with HTML and Bootstrap for a responsive design.
   - Accepts customer demographic and spending data as inputs.
   - Displays predicted membership levels dynamically.

3. **Back-End API**:
   - Developed using Flask for handling predictions.
   - Connects to a MySQL database to fetch and preprocess data.

## How It Works
1. **User Input**:
   - The user inputs:
     - Customer name
     - Age group
     - Gender
     - Average yearly spend

2. **Prediction**:
   - The `app.py` back-end processes the input and passes it to the trained model.
   - The Decision Tree predicts the customer's membership level.

3. **Output**:
   - The result is displayed on the web page dynamically without reloading.

## Setup Instructions
### Prerequisites
- Python 3.8+
- MySQL Database
- Required Python Libraries:
  - Flask
  - pandas
  - scikit-learn
  - pymysql

### Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd DMS_FINAL/project_code
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the database:
   - Update the database credentials in `app.py` under `app.config`:
     ```python
     app.config['MYSQL_HOST'] = '127.0.0.1'
     app.config['MYSQL_USER'] = 'root'
     app.config['MYSQL_PASSWORD'] = 'your_password'
     app.config['MYSQL_DB'] = 'ECM'
     ```

4. Run the Flask application:
   ```bash
   python app.py
   ```

5. Open the application in your browser:
   ```
   http://127.0.0.1:5000
   ```

## How to Use
1. Navigate to the homepage.
2. Enter customer details in the form:
   - Customer name (optional)
   - Age group (e.g., 18-25)
   - Gender (Male/Female)
   - Average yearly spend (numeric value)
3. Click **"Get the Prediction"**.
4. View the predicted membership level.
