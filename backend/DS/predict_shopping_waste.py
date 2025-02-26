"""
predict_shopping_waste

this module will handle the creation, training and prediction using prophet
return prediction for user, in the upcoming week(s) will:
product | amount_buy | amount_wasted
"""
import plotly.graph_objects as go
import pandas as pd
from typing import Tuple
from prophet import Prophet
from mysqlDB.db_utils import execute_query 
from mysqlDB.products import products_queries

# TODO:
# change logic after demo - make it integrated to all the other db parts
# notice date in user_product_history is in WEEKS!!!!!
# change continoue in function for more modular!!!!

def plot_forecast_with_go2(forecast, title="Forecast"):
    forecast_2025 = forecast[forecast['ds'].dt.year == 2025]
    cutoff_date = pd.Timestamp("2025-02-10")
    forecast_2025 = forecast[(forecast['ds'].dt.year == 2025) & (forecast['ds'] >= cutoff_date)]
    # Create a trace for the forecast
    trace = go.Scatter(
        x=forecast_2025['ds'], 
        y=forecast_2025['yhat'], 
        mode='lines+markers', 
        name='Forecast',
    )
    # Layout for the plot
    layout = go.Layout(
        title=title,
        xaxis=dict(title="Date"),
        yaxis=dict(title="Quantity", showticklabels=False),
        hovermode="closest"
    )
    fig = go.Figure(data=[trace], layout=layout)
    fig.show()


def get_user_history(user_id:int) -> pd.DataFrame:
    """ 
    this function get a user id and should send get the data, 
    for now implemented Naivly instead for speed of implementation
    """
    query = "SELECT * FROM user_product_history"
    result = execute_query(query, fetch_all=True)

    if result is None:
        return None
    else:
        df = pd.DataFrame(result)
        df['purchase_date'] = pd.to_datetime(df['purchase_date'])
    return df
    

def process_db(df:pd.DataFrame,product_id:int, user_id:str,
               ) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df['user_id'] = df['user_id'].astype(str)
    df_filtered = df[(df['user_id'] == user_id) & (df['product_id'] == product_id)].copy()
    df_filtered.sort_values('purchase_date', inplace=True)
                   
    df_purchase = df_filtered[['purchase_date', 'quantity_purchased']].rename(
        columns={'purchase_date': 'ds', 'quantity_purchased': 'y'}
    )
    df_thrown = df_filtered[['purchase_date', 'quantity_thrown_out']].rename(
        columns={'purchase_date': 'ds', 'quantity_thrown_out': 'y'}
    )
    return df_purchase, df_thrown


# def initialize_prophets(df:pd.DataFrame) -> Prophet:
#     """Build Prophet Models"""
#     model = Prophet()
#     model.add_seasonality(name='biweekly', period=14, fourier_order=7)
#     model.fit(df)
#     return model

def initialize_prophets(df:pd.DataFrame) -> Prophet:
    """Build Prophet Models"""
    model =  Prophet(
    yearly_seasonality=False,
    weekly_seasonality=False,
)
    model.add_seasonality(name="quarterly", period=90, fourier_order=3)  
    model.add_seasonality(name='monthly', period=30.5, fourier_order=3)
    model.fit(df)
    return model
    
def pipeline(user_id: str):
    user_history = get_user_history(user_id)
    
    # Ensure there are at least two non-NaN rows before proceeding
    if user_history.dropna().shape[0] < 2:
        return None  

    products = user_history['product_id'].dropna().unique()
    results = []

    for product in products:
        try:
            df_purchase, df_thrown = process_db(user_history, product, user_id)

            # Predict purchases for the next 2 weeks
            model_purchase = initialize_prophets(df_purchase)
            future_purchase = model_purchase.make_future_dataframe(periods=1, freq='W-MON')
            forecast_purchase = model_purchase.predict(future_purchase).tail(1)

            # Predict waste for the next 2 weeks
            model_thrown = initialize_prophets(df_thrown)
            future_thrown = model_thrown.make_future_dataframe(periods=1, freq='W-MON')
            forecast_thrown = model_thrown.predict(future_thrown).tail(1)

            forecast_combined = pd.DataFrame({
                'ds': forecast_purchase['ds'],
                'quantity_estimated': forecast_purchase['yhat'].round(0),
                'amount_thrown_out_estimated': forecast_thrown['yhat'].round(0)
            })

            # Keep only products where estimated purchases are at least 1
            forecast_combined = forecast_combined[forecast_combined['quantity_estimated'] >= 1]

            if not forecast_combined.empty:
                forecast_combined['user_id'] = user_id
                product_data = products_queries.get_product_name_from_db(int(product))
                product_name = product_data[0]['product_name']
                forecast_combined['product'] = product_name
                results.append(forecast_combined)
        except Exception as e:
            continue

    return pd.concat(results, ignore_index=True) if results else None

if __name__ == "__main__":
    print("work")
    res = pipeline('101')
    print(res)
    
    




        
        
        

    




