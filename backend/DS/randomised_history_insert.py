import random
from datetime import date, timedelta
from ..mysqlDB import db_utils
from typing import List, Optional
import math

def insert_shopping_cycle_user_history(user_id: int, 
                                       num_weeks: int = 260, 
                                       product_ids: Optional[List[int]] = None) -> None:
    """
    The pattern is:
      - In "high" weeks (even-indexed weeks), the user buys a lot of nearly all products.
      - In "low" weeks (odd-indexed weeks), the user buys only a little from some products.
    """
    if product_ids is None:
        product_ids = list(range(36))
    today = date.today()
    current_monday = today - timedelta(days=today.weekday())    
    rows = []
    
    for week in range(num_weeks):
        purchase_date = current_monday - timedelta(weeks=(num_weeks - week - 1))
            
        week_offset = random.randint(0, 24)
        offset=random.choice([2,3])
        for product_id in product_ids:
            if week_offset % offset in [0, 1]:  
                quantity_purchased = random.randint(5, 8)  # Bulk purchase week
                thrown_fraction = random.uniform(0.4, 0.8)

            else:
                quantity_purchased = random.randint(1, 3)   # Low purchase week
                thrown_fraction = random.uniform(0.15, 0.25)

            high=random.choice([True,False])
            if high and week_offset % offset:
                noise = int(random.gauss(3, 6))
            else:
                noise = int(random.gauss(0, 3))
            quantity_purchased = max(1, quantity_purchased + noise)
            quantity_thrown_out = int(round(quantity_purchased * thrown_fraction))
            quantity_consumed = quantity_purchased - quantity_thrown_out    
          
            rows.append((
                user_id,
                product_id,
                purchase_date.strftime('%Y-%m-%d'),
                quantity_purchased,
                quantity_consumed,
                quantity_thrown_out
            ))
    
    query = """
        INSERT INTO user_product_history 
        (user_id, product_id, purchase_date, quantity_purchased, quantity_consumed, quantity_thrown_out)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    db_utils.execute_query(query, params=rows, commit=True)





if __name__ == "__main__":
<<<<<<< HEAD
    insert_shopping_cycle_user_history(101,260,[1,4,6,9,10])
=======
    insert_shopping_cycle_user_history(101,260,[5])
>>>>>>> origin/main
