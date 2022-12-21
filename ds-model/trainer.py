
import pandas as pd
import numpy as np

from pycaret.regression import *

data = pd.read_csv('data/insurance.csv')

r2 = setup(data, target='charges', session_id=123,
           normalize=True,
           polynomial_features=True, trigonometry_features=True,
           feature_interaction=True, 
           bin_numeric_features= ['age', 'bmi'])

# Model Training and Validation 
lr = create_model('lr')

# save transformation pipeline and model 
save_model(lr, model_name='binaries/deployment_28042020')

# plot residuals of trained model
plot_model(lr, plot='residuals')