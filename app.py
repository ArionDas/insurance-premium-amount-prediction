from flask import Flask, request, jsonify, render_template, session, url_for, redirect
from flask_wtf import FlaskForm
from flask_wtf import Form
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, SelectField
import pickle
import joblib
import numpy as np

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/' ## this doesn't need to be hidden as of now - some random gibbersih I wrote
model = joblib.load('model.pkl')


def return_prediction(model, input_json) : 
    
    input_data = [[input_json[k] for k in input_json.keys()]]
    prediction = model.predict(input_data)[0]
    
    return prediction


class PredictForm(FlaskForm):
    age = StringField("Age")
    gender = SelectField("Gender", choices=[('male', 'Male'), ('female', 'Female')])
    annual_income = StringField("Annual Income")
    marital_status = SelectField("Marital Status", choices=[('married', 'Married'), ('single', 'Single'), ('divorced', 'Divorced')])
    dependents = StringField("Number of Dependents")
    education_level = SelectField("Education Level", choices=[('high_school', "High School"), ('bachelors', "Bachelor's"), ("masters", "'Master's"), ('phd', "PHD")])
    occupation = SelectField("Occupation", choices=[('unemployed', 'Unemployed'), ('self_employed', 'Self-Employed'), ('employed', 'Employed')])
    health_score = StringField("Health Score")
    location = SelectField("Location", choices=[('rural', 'Rural'), ('suburban', 'Suburban'), ('urban', 'Urban')])
    policy_type = SelectField("Policy Type", choices=[('basic', 'Basic'), ('comprehensive', 'Comprehensive'), ('premium', 'Premium')])
    previous_claims = StringField("Previous Claims")
    vehicle_age = StringField("Vehicle Age (in years)")
    credit_score = StringField("Credit Score")
    insurance_duration = StringField("Insurance Duration")
    customer_feedback = SelectField("Customer Feedback", choices=[('poor', 'Poor'), ('average', 'Average'), ('good', 'Good')])
    smoking_status = SelectField("Smoking Status", choices=[('yes', 'Yes'), ('no', 'No')])
    exercise_frequency = SelectField("Exercise Frequency", choices=[('rarely', 'Rarely'), ('monthly', 'Monthly'), ('weekly', 'Weekly'), ('daily', 'Daily')])
    property_type = SelectField("Property Type", choices=[('apartment', 'Apartment'), ('condo', 'Condo'), ('house', 'House')])
    year = StringField("Year")
    day = StringField("Day (of the month)")
    month = StringField("Month (1-12)")
    month_name = ""
    day_of_week = StringField("Day of the Week (1-7)")
    
    contract_length = ""
    income_per_dependent = ""
    credit_score_insurance_duration = ""
    health_risk_score = ""
    credit_health_score = ""
    health_age_interaction = ""
    
    submit = SubmitField("Predict")
    


@app.route('/', methods=['GET', 'POST'])
def index():
    
    form = PredictForm()
    
    if form.validate_on_submit():
        
        # age
        session['age'] = form.age.data
        
        # gender
        if(form.gender.data == 'female'):
            session['pronoun'] = 0
            session['gender'] = 'Female'
        else:
            session['pronoun'] = 1
            session['gender'] = 'Male'
            
        # annual income
        session['annual_income'] = form.annual_income.data
        
        # marital status
        if(form.marital_status.data == 'married'):
            session['married'] = 0
            session['marital_status'] = 'Married'
        elif(form.marital_status.data == 'single'):
            session['married'] = 2
            session['marital_status'] = 'Single'
        else:
            session['married'] = 1
            session['marital_status'] = 'Divorced'
            
        # dependents
        session['dependents'] = form.dependents.data
        
        # education level
        if(form.education_level.data == 'high_school'):
            session['education'] = 0
            session['education_level'] = 'High School'
        elif(form.education_level.data == 'bachelors'):
            session['education'] = 1
            session['education_level'] = 'Bachelor\'s'
        elif(form.education_level.data == 'masters'):
            session['education'] = 2
            session['education_level'] = 'Master\'s'
        else:
            session['education'] = 3
            session['education_level'] = 'PHD'
            
        # occupation
        if(form.occupation.data == 'unemployed'):
            session['occupation'] = 0
            session['occupation_status'] = 'Unemployed'
        elif(form.occupation.data == 'self_employed'):
            session['occupation'] = 1
            session['occupation_status'] = 'Self-Employed'
        else:
            session['occupation'] = 2
            session['occupation_status'] = 'Employed'
            
        # health score
        session['health_score'] = form.health_score.data
        
        # location
        if(form.location.data == 'rural'):
            session['place'] = 0
            session['location'] = 'Rural'
        elif(form.location.data == 'suburban'):
            session['place'] = 1
            session['location'] = 'Suburban'
        else:
            session['place'] = 2
            session['location'] = 'Urban'
            
        # policy type
        if(form.policy_type.data == 'basic'):
            session['policy_type'] = 0
            session['policy'] = 'Basic'
        elif(form.policy_type.data == 'comprehensive'):
            session['policy_type'] = 1
            session['policy'] = 'Comprehensive'
        else:
            session['policy_type'] = 2
            session['policy'] = 'Premium'
            
        # previous claims
        session['previous_claims'] = form.previous_claims.data
        
        # vehicle age
        session['vehicle_age'] = form.vehicle_age.data
        
        # credit score
        session['credit_score'] = form.credit_score.data
        
        # insurance duration
        session['insurance_duration'] = form.insurance_duration.data
        
        # customer feedback
        if(form.customer_feedback.data == 'poor'):
            session['feedback'] = 0
            session['feedback_status'] = 'Poor'
        elif(form.customer_feedback.data == 'average'):
            session['feedback'] = 1
            session['feedback_status'] = 'Average'
        else:
            session['feedback'] = 2
            session['feedback_status'] = 'Good'
            
        # smoking status
        if(form.smoking_status.data == 'yes'):
            session['smoke'] = 1
            session['smoking_status'] = 'Yes'
        else:
            session['smoke'] = 0
            session['smoking_status'] = 'No'
            
        # exercise frequency
        if(form.exercise_frequency.data == 'rarely'):
            session['exercise'] = 0
            session['exercise_frequency'] = 'Rarely'
        elif(form.exercise_frequency.data == 'monthly'):
            session['exercise'] = 1
            session['exercise_frequency'] = 'Monthly'
        elif(form.exercise_frequency.data == 'weekly'):
            session['exercise'] = 2
            session['exercise_frequency'] = 'Weekly'
        else:
            session['exercise'] = 3
            session['exercise_frequency'] = 'Daily'
            
        # property type
        if(form.property_type.data == 'apartment'):
            session['property'] = 0
            session['property_type'] = 'Apartment'
        elif(form.property_type.data == 'condo'):
            session['property'] = 1
            session['property_type'] = 'Condo'
        else:
            session['property'] = 2
            session['property_type'] = 'House'
            
        # year
        session['year'] = form.year.data
        
        # day
        session['day'] = form.day.data
        
        # month
        session['month'] = form.month.data
        
        session['month_name'] = form.month.data
        
        # day of the week
        session['day_of_week'] = form.day_of_week.data
        
        # contract length
        session['contract_length'] = 0
        if(float(session['insurance_duration']) < 1):
            session['contract_length'] = 0
        elif(float(session['insurance_duration']) < 5):
            session['contract_length'] = 1
        else:
            session['contract_length'] = 2
        
        if(float(session['dependents']) == 0):
            session['dependents'] = 1
        
        # income per dependent   
        session['income_per_dependent'] = float(session['annual_income']) / float(session['dependents'])
        
        # credit score insurance duration
        session['credit_score_insurance_duration'] = float(session['credit_score']) * float(session['insurance_duration'])
        
        # health risk score
        session['health_risk_score'] = float(session['smoke']) + float(session['exercise']) - float(session['health_score']) / 20
        
        # credit health score
        session['credit_health_score'] = float(session['credit_score']) * float(session['health_score'])
        
        # health age interaction
        session['health_age_interaction'] = float(session['health_score']) * float(session['age'])

        return redirect(url_for('predict'))
    
    return render_template('index.html', form=form)
            
        
    
    # return """
    # <h1>Model Deployment</hjson>
    # <p>Use a POST request to /predict to get a prediction of Premium Amount</p>
    # <ul>
    # <li>Annual Income</li>
    # <li>Age</li>
    # <li>Gender</li>
    # <li>Dependents</li>
    # </ul>
    # """

@app.route('/predict')
def predict():
    
    content = {}
    
    content['Age'] = float(session['age'])
    content['Gender'] = float(session['pronoun'])
    content['Annual Income'] = float(session['annual_income'])
    content['Marital Status'] = float(session['married'])
    content['Number of Dependents'] = float(session['dependents'])
    content['Education Level'] = float(session['education'])
    content['Occupation'] = float(session['occupation'])
    content['Health Score'] = float(session['health_score'])
    content['Location'] = float(session['place'])
    content['Policy Type'] = float(session['policy_type'])
    content['Previous Claims'] = float(session['previous_claims'])
    content['Vehicle Age'] = float(session['vehicle_age'])
    content['Credit Score'] = float(session['credit_score'])
    content['Insurance Duration'] = float(session['insurance_duration'])
    content['Customer Feedback'] = float(session['feedback'])
    content['Smoking Status'] = float(session['smoke'])
    content['Exercise Frequency'] = float(session['exercise'])
    content['Property Type'] = float(session['property'])
    content['Year'] = float(session['year'])
    content['Day'] = float(session['day'])
    content['Month'] = float(session['month'])
    content['Month Name'] = float(session['month_name'])
    content['Day of the Week'] = float(session['day_of_week'])
    content['contract length'] = float(session['contract_length'])
    content['Income to Dependents Ratio'] = float(session['income_per_dependent'])
    content['CreditScore_InsuranceDuration'] = float(session['credit_score_insurance_duration'])
    content['Health_Risk_Score'] = float(session['health_risk_score'])
    content['Credit_Health_Score'] = float(session['credit_health_score'])
    content['Health_Age_Interaction'] = float(session['health_age_interaction'])
    
    prediction = return_prediction(model, content)
    prediction = np.expm1(prediction)
    return render_template('prediction.html', prediction=prediction)

Bootstrap = Bootstrap(app)
if __name__ == '__main__':
    app.run(debug=True)