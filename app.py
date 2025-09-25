from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Load voting data once at startup
voting_df = pd.read_csv('Voting Final.csv')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Your existing prediction logic
    return render_template('index.html', prediction_text="Prediction result here.")

@app.route('/voting')
def voting():
    countries = sorted(voting_df['To_Country'].unique())
    return render_template('voting.html', countries=countries)

@app.route('/voting_result', methods=['POST'])
def voting_result():
    selected_country = request.form['country']
    filtered = voting_df[voting_df['To_Country'] == selected_country]
    top_giver = (
        filtered.groupby('From_Country')['Points']
        .sum()
        .sort_values(ascending=False)
        .idxmax()
    )
    result = f"The country that has given the most points to {selected_country} is {top_giver}!"
    countries = sorted(voting_df['To_Country'].unique())
    return render_template('voting.html', countries=countries, result=result)