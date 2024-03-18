
import pandas as pd
import csv
import re

###########################################
# Run this file from the root directory   #
###########################################

data_folder = 'backend/webscrape/data/'


###########################################
# Define helper functions                 #
###########################################

def get_shelf_life_in_days(shelf_life_str):
    if shelf_life_str == None:
        return None, None
    else:
        time_units = {"day": 1,"week": 7,"month": 30,"year": 365}
        unit_list = [x for x in time_units if x in shelf_life_str]
        
        if unit_list:
            unit = unit_list[0]
            unit_factor = time_units[unit]
        else:
            unit = ''

        int_list = re.findall(r'\d+',shelf_life_str)
        int_list = [int(i) for i in int_list]

        if unit in time_units.keys():
            min_shelf_life = min(int_list)*unit_factor
            max_shelf_life = max(int_list)*unit_factor
        else:
            min_shelf_life = ''
            max_shelf_life = ''

    return min_shelf_life, max_shelf_life


###########################################
# Read in categories data                 #
###########################################

categories_filename = data_folder+'stilltasty_food_categories.csv'
try:
    category_index_numbers = []
    categories = []
    with open(categories_filename, mode ='r') as file:    
        csvFile = csv.reader(file)
        next(csvFile, None) #Skip the header
        for line in csvFile:
            category_index_numbers.append(line[0])
            categories.append(line[1])
    print("Existing categories file has been read in.")

except FileNotFoundError:
    print(f"Categories file not found. Run still_tasty_scrape.py to create it.")


###########################################
# Read in items data                      #
###########################################

df = pd.DataFrame()
for cat in categories:
    cat_trimmed = cat.replace(' ','').replace('&','').replace(',','').lower()
    food_items_filename = data_folder+f'stilltasty_food_items_{cat_trimmed}.csv'

    try:
        df = pd.concat([df, pd.read_csv(food_items_filename, encoding = "ISO-8859-1")])
        print(f"{food_items_filename} added to dataframe")
    except FileNotFoundError:
        print(f'{cat} file is missing')


###########################################
# Get storage locations                   #
###########################################

# Create storage_locations column
df['storage_locations'] = df['shelf_life'].apply(lambda x: list(eval(x).keys()))

storage_locations = []
for x in df.storage_locations:
    storage_locations.extend(x)

storage_locations = list(set(storage_locations))
print(storage_locations)


###########################################
# Transform Shelf Life Columns            #
###########################################

#Split shelf life by storage location
df['refrigerator_shelf_life'] = df['shelf_life'].apply(lambda x: eval(x).get('Refrigerator'))
df['pantry_shelf_life'] = df['shelf_life'].apply(lambda x: eval(x).get('Pantry'))
df['freezer_shelf_life'] = df['shelf_life'].apply(lambda x: eval(x).get('Freezer'))

#Get the min/max shelf life in days for each storage location
df['refrigerator_shelf_life'] = df['refrigerator_shelf_life'].apply(lambda x: get_shelf_life_in_days(x))
df['refrigerator_min_shelf_life'] = df['refrigerator_shelf_life'].apply(lambda x: x[0])
df['refrigerator_max_shelf_life'] = df['refrigerator_shelf_life'].apply(lambda x: x[1])

df['pantry_shelf_life'] = df['pantry_shelf_life'].apply(lambda x: get_shelf_life_in_days(x))
df['pantry_min_shelf_life'] = df['pantry_shelf_life'].apply(lambda x: x[0])
df['pantry_max_shelf_life'] = df['pantry_shelf_life'].apply(lambda x: x[1])

df['freezer_shelf_life'] = df['freezer_shelf_life'].apply(lambda x: get_shelf_life_in_days(x))
df['freezer_min_shelf_life'] = df['freezer_shelf_life'].apply(lambda x: x[0])
df['freezer_max_shelf_life'] = df['freezer_shelf_life'].apply(lambda x: x[1])


###########################################
# Limit to final columns and write to csv #
###########################################

columns = ['item_name', 'category', 'url', 'food_tips',
            'refrigerator_min_shelf_life', 'refrigerator_max_shelf_life',
            'pantry_min_shelf_life', 'pantry_max_shelf_life',
            'freezer_min_shelf_life', 'freezer_max_shelf_life',
            'storage_locations']
output_df = df[columns]

final_item_filename = data_folder+'item.csv'
output_df.to_csv(final_item_filename, sep='\t')

print("Output file has been written")