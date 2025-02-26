import random
from datetime import date, timedelta
from ..mysqlDB import db_utils
from typing import List, Optional

def insert_shopping_cycle_user_history(user_id: str, 
                                       num_weeks: int = 260, 
                                       product_ids: Optional[List[int]] = None) -> None:
    """
    Simulates a shopping cycle where:
      - In "high" weeks (even-indexed weeks), the user buys a lot of nearly all products.
      - In "low" weeks (odd-indexed weeks), the user buys only a little from some products.
      
    For each week and product, the function calculates the total number of units purchased,
    then splits them into thrown and consumed events. Each unit is inserted as a separate row in the new table:
    (user_id, product_id, is_thrown, date_entered).
    """
    if product_ids is None:
        product_ids = list(range(36))
    today = date.today()
    current_monday = today - timedelta(days=today.weekday())    
    rows = []
    
    for week in range(num_weeks):
        purchase_date = current_monday - timedelta(weeks=(num_weeks - week - 1))
            
        week_offset = random.randint(0, 24)
        offset = random.choice([2, 3])
        for product_id in product_ids:
            if week_offset % offset in [0, 1]:  
                quantity_purchased = random.randint(5, 8)  # Bulk purchase week
                thrown_fraction = random.uniform(0.4, 0.8)
            else:
                quantity_purchased = random.randint(1, 3)   # Low purchase week
                thrown_fraction = random.uniform(0.15, 0.25)

            high = random.choice([True, False])
            if high and week_offset % offset:
                noise = int(random.gauss(3, 6))
            else:
                noise = int(random.gauss(0, 3))
            quantity_purchased = max(1, quantity_purchased + noise)
            quantity_thrown_out = int(round(quantity_purchased * thrown_fraction))
            quantity_consumed = quantity_purchased - quantity_thrown_out    
          
            # For each unit, insert a row indicating whether it was thrown or not.
            for _ in range(quantity_thrown_out):
                rows.append((
                    user_id,   # user_id as string per new schema
                    product_id,
                    True,           # is_thrown
                    purchase_date.strftime('%Y-%m-%d')
                ))
            for _ in range(quantity_consumed):
                rows.append((
                    user_id,
                    product_id,
                    False,          # not thrown means it was consumed
                    purchase_date.strftime('%Y-%m-%d')
                ))
    
    query = """
        INSERT INTO user_product_history 
        (user_id, product_id, is_thrown, date_entered)
        VALUES (%s, %s, %s, %s)
    """
    
    execute_query(query, params=rows, commit=True)


if __name__ == "__main__":

    insert_shopping_cycle_user_history("0NNRFLhbXJRFk3ER2_iTr8VulFm4", 260, [1, 4, 6, 9, 10])
