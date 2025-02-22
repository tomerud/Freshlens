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
from backend.mysqlDB import db_utils 
from backend.mysqlDB.products import products_queries
from prophet.plot import plot_plotly

# TODO:
# change logic after demo - make it integrated to all the other db parts
# notice date in user_product_history is in WEEKS!!!!!
# change continoue in function for more modular!!!!

import plotly.graph_objects as go
import pandas as pd
import plotly.graph_objects as go
import pandas as pd

import plotly.graph_objects as go

def plot_forecast_with_go2(forecast, title="Forecast"):

    forecast_2025 = forecast[forecast['ds'].dt.year == 2025]
    cutoff_date = pd.Timestamp("2025-02-10")
    forecast_2025 = forecast[(forecast['ds'].dt.year == 2025) & (forecast['ds'] >= cutoff_date)]

    trace = go.Scatter(
        x=forecast_2025['ds'], 
        y=forecast_2025['yhat'], 
        mode='lines+markers', 
        name='Forecast',
    )
    layout = go.Layout(
        title=title,
        xaxis=dict(title="Date"),
        yaxis=dict(title="Quantity", showticklabels=False),
        hovermode="closest"
    )
    fig = go.Figure(data=[trace], layout=layout)
    fig.show()


def plot_forecast_with_go(forecast, title="Forecast"):
    trace = go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Forecast')
    lower_bound = go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], mode='lines', name='Lower Bound', line=dict(dash='dash'))
    upper_bound = go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], mode='lines', name='Upper Bound', line=dict(dash='dash'))
    layout = go.Layout(
        title=title,
        xaxis=dict(title="Date"),
        yaxis=dict(title="Quantity"),
        hovermode="closest"
    )
    fig = go.Figure(data=[trace, lower_bound, upper_bound], layout=layout)
    fig.show()

def get_user_history(user_id:int) -> pd.DataFrame:
    """ 
    this function get a user id and should send get the data, 
    for now implemented Naivly instead for speed of implementation
    """
    query = "SELECT * FROM user_product_history"
    result = db_utils.execute_query(query, fetch_all=True)

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
    #df["cap"] = 15  # Max reasonable value
    #df["floor"] = 0 # Since negatives don't make sense
    """Build Prophet Models"""
    model =  Prophet(
    yearly_seasonality=False,
    weekly_seasonality=False,  # Weekly seasonality ? should think about
)
    model.add_seasonality(name="quarterly", period=90, fourier_order=3)  
    model.add_seasonality(name='monthly', period=30.5, fourier_order=3)
    model.fit(df)
    return model
    

def pipeline(user_id:str):
    user_history = get_user_history(user_id)
    #df['user_id'] = df['user_id'].astype(str)
    products = user_history['product_id'].dropna().unique()
    products=[5] # test - so wont show for too much products
    for product in products:
        df_purchase, df_thrown = process_db(user_history, product, user_id,)
            
        model_purchase = initialize_prophets(df_purchase)
        future_purchase = model_purchase.make_future_dataframe(periods=7, freq='W-MON')
        forecast_purchase = model_purchase.predict(future_purchase)
        print(forecast_purchase[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

        model_thrown = initialize_prophets(df_thrown)
        future_thrown = model_thrown.make_future_dataframe(periods=3, freq='W-MON')
        forecast_thrown = model_thrown.predict(future_thrown)
        print(forecast_thrown[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

        forecast_combined = pd.DataFrame({
        'ds': forecast_purchase['ds'],
        'quantity_estimated': forecast_purchase['yhat'],
        'amount_thrown_out_estimated': forecast_thrown['yhat']
        })
        forecast_combined['user_id'] = user_id
        product_data = products_queries.get_product_name_from_db(int(product))
        product_name = product_data[0]['product_name']
        forecast_combined['product'] = [product_name] * len(forecast_combined)
        print(forecast_combined.tail(2))
        
        fig_purchase = plot_plotly(model_purchase, forecast_purchase)
        fig_thrown = plot_plotly(model_thrown, forecast_thrown)
        
        plot_forecast_with_go2(forecast_purchase, f"Purchase Forecast {product_name}")

        plot_forecast_with_go(forecast_thrown, f"thrown Forecast {product_name}")
        




if __name__ == "__main__":
    pipeline('101')
        
        
        

    




