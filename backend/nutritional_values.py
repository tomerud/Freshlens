import requests
from typing import Dict, Union
api_key = '_API_FRO_APP'
# can replace the defult API key in the function with valid one
def get_usda_nutritional_info(product_name: str, api_key: str) -> Dict[str, Union[str, Dict[str, Union[str, float]]]]:
    # get ID for search
    search_url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={product_name}&api_key={api_key}"
    search_response = requests.get(search_url)
    if search_response.status_code == 200:
        search_data = search_response.json()
        if search_data.get('foods'):
            # Get the first food item from the search results - we might need to make it more sophisticated, but for now will be enough
            food = search_data['foods'][0]
            fdc_id = food['fdcId']
            food_url = f"https://api.nal.usda.gov/fdc/v1/food/{fdc_id}?api_key={api_key}"
            food_response = requests.get(food_url)
            if food_response.status_code == 200:
                food_data = food_response.json()
                # values per 100g, we also will take weight (if exist) then we can adjust
                nutrition_data = {}
                for nutrient in food_data.get('foodNutrients', []):
                    nutrient_name = nutrient['nutrient']['name']
                    nutrient_value = nutrient.get('amount', 0.0)
                    unit = nutrient['nutrient']['unitName']
                    if nutrient_name == "Energy":
                        nutrition_data['energy_kcal_100g'] = nutrient_value
                    elif nutrient_name == "Protein":
                        nutrition_data['proteins_100g'] = nutrient_value
                    elif nutrient_name == "Total lipid (fat)":
                        nutrition_data['fats_100g'] = nutrient_value
                    elif nutrient_name == "Carbohydrate, by difference":
                        nutrition_data['carbohydrates_100g'] = nutrient_value
                    elif nutrient_name == "Total Sugars":
                        nutrition_data['sugars_100g'] = nutrient_value
                    elif nutrient_name == "Sodium, Na":
                        nutrition_data['salt_100g'] = nutrient_value
                    elif nutrient_name == "Fiber, total dietary":
                        nutrition_data['fiber_100g'] = nutrient_value
                    elif nutrient_name == "Vitamin C, total ascorbic acid":
                        nutrition_data['vitamin_c_100g'] = nutrient_value
                    elif nutrient_name == "Iron, Fe":
                        nutrition_data['iron_100g'] = nutrient_value
                    elif nutrient_name == "Calcium, Ca":
                        nutrition_data['calcium_100g'] = nutrient_value
                    elif nutrient_name == "Potassium, K":
                        nutrition_data['potassium_100g'] = nutrient_value
                    elif nutrient_name == "Cholesterol":
                        nutrition_data['cholesterol_100g'] = nutrient_value
                    elif nutrient_name == "Fatty acids, total saturated":
                        nutrition_data['saturated_fats_100g'] = nutrient_value
                    elif nutrient_name == "Fatty acids, total trans":
                        nutrition_data['trans_fats_100g'] = nutrient_value
                    elif nutrient_name == "Vitamin A, IU":
                        nutrition_data['vitamin_a_100g'] = nutrient_value

                # Get the weight of 1 - not always exist
                serving_size = food_data.get('servingSize', 'N/A')
                # Annoying but it seem can be dict or float
                if isinstance(serving_size, dict):
                    serving_weight = serving_size.get('amount', 'N/A')
                else:
                    # If it's not a dictionary, assume it's a float value representing the weight
                    serving_weight = serving_size if serving_size else 'N/A'

                # Structure data for DB storage - check in api data diffrence serving_size and weight - tomer need to handle db
                db_data = {'product_name': product_name,'nutrition_per_100g': nutrition_data,'serving_size' : serving_size,'serving_weight': serving_weight}
                return db_data
            else:
                return {"Error fetching data"}
        else:
            return {f"No results for {product_name}"}
    else:
        return {"Error fetching search data."}

# Example usage
d={0:'apple',1:'orange',2: 'cheddar cheese'}
all_products = {}
for product_id, product_name in d.items():
    nutrition_info = get_usda_nutritional_info(product_name, api_key)
    all_products[product_name] = nutrition_info

print(all_products)
#instead of print, insert to the table