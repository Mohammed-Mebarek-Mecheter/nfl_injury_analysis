# In src/utils/predictive_analytics.py

import pickle
import numpy as np
import pandas as pd
from pathlib import Path

def load_model_and_metadata():
    model_dir = Path(__file__).parent.parent / 'models'
    with open(model_dir / 'injury_prediction_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open(model_dir / 'injury_prediction_metadata.pkl', 'rb') as f:
        metadata = pickle.load(f)
    return model, metadata

def predict_future_injuries(df_concussions):
    model, metadata = load_model_and_metadata()

    max_days = metadata['max_days']
    first_date = metadata['first_date']

    # Generate future days as a NumPy array
    future_days = np.arange(max_days, max_days + 365).reshape(-1, 1)

    # Make predictions
    future_predictions = model.predict(future_days)

    # Generate future dates
    future_dates = [first_date + pd.Timedelta(days=int(day)) for day in future_days.flatten()]

    return future_days.flatten(), future_predictions

