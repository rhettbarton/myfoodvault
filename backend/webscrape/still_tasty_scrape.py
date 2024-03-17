import requests
import csv
from bs4 import BeautifulSoup
from time import sleep
from collections import Counter


###########################################
# Run this file from the root directory   #
###########################################

data_folder = 'backend/webscrape/data/'

###########################
# Define helper functions #
###########################

def scrape_stilltasty(index,category):
    print(f'Now scraping index {index}. Category: {category}')
    # URL of the page to scrape
    url = f'https://www.stilltasty.com/Fooditems/index/{index}'
    
    # Pause to avoid 403 erros 
    sleep(3)

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        #Get item name
        item_name = soup.find('h2').text.strip()

        # Find storage location elements
        storage_location_elements = soup.find_all('div', class_='food-storage-left')
        # Initialize a dictionary to store values
        shelf_life = {}
        # Loop through storage location elements and find the associated shelf life
        for e in storage_location_elements:
            storage_location = e.text.strip()
            # Find associated shelf life information
            shelf_life_info_element = e.find_next_sibling('div')
            shelf_life_info = shelf_life_info_element.text.strip()
            shelf_life[storage_location] = shelf_life_info
        
        #Find food tips
        tips = soup.find('div', class_='food-tips').text.strip()
        #Remove Author Info
        n = tips.find('About Our Author')
        tips = tips[:n]

        return {'item_name': item_name, 'category': category, 'url': url, 'shelf_life': shelf_life, 'food_tips': tips}
    else:
        # Print an error message if the request was not successful
        raise Exception(f"Error: Failed to retrieve data from {url}. Status code: {response.status_code}")


def get_index_numbers(url,target_string,get_names=False):
    index_numbers = []
    object_names = []

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all links with href attribute containing target_string
        links = soup.find_all('a', href=lambda href: href and target_string in href)
        #Remove image links
        links = [link for link in links if not link.find('img')]
        # Extract index numbers from href attributes
        for link in links:
            href = link['href']
            index_number = href.split('/')[-1]
            index_numbers.append(index_number)
            if get_names:
                object_name = link.text.strip()
                object_names.append(object_name)
            
        return index_numbers, object_names 
    
    else:
        raise Exception(f"Error: Failed to retrieve data from {url}. Status code: {response.status_code}")


########################################################
# Get the StillTasty food categories and their indices #
########################################################
    
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
    print(f"Categories file not found. Proceeding to scrape categories from StillTasty.")
    url = 'https://www.stilltasty.com/Fooditems/index'
    target_string = "/searchitems/index/"
    category_index_numbers, categories = get_index_numbers(url,target_string,True)
    cat_list = [{'index': category_index_numbers[i], 'category': categories[i]} for i in range(len(categories))]
    #Write to csv
    keys = cat_list[0].keys()
    with open(categories_filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(cat_list)
    print(f"Categories scrape complete and new file written.")
     


#######################################################
# Loop through the search results of each category   #
# Store the indices of all the associated food items #
######################################################

all_index_numbers = []
all_categories = []
food_indices_filename = data_folder+'stilltasty_food_indices.csv'
try:
    with open(food_indices_filename, mode ='r') as file:    
        csvFile = csv.reader(file)
        next(csvFile, None) #Skip the header
        for line in csvFile:
            all_index_numbers.append(line[0])
            all_categories.append(line[1])
    print("Existing Food Indices file has been read in.")

except FileNotFoundError:
    print(f"Food Indices file not found. Proceeding to scrape from StillTasty.")
    for x,i in enumerate(category_index_numbers):
        url = f'https://www.stilltasty.com/searchitems/index/{i}'
        #Initial results pages
        results_pages = [f'{i}']+get_index_numbers(url,"/searchitems/index/")[0]
        results_pages = list(set(results_pages))
        results_pages.sort()
        new_pages = results_pages
        while new_pages:
            print(new_pages)
            for j in new_pages:         
                print(f"Now scraping index {j}")
                url = f'https://www.stilltasty.com/searchitems/index/{j}'
                index_numbers = get_index_numbers(url,"/Fooditems/index/")[0]
                if index_numbers:
                    all_index_numbers = all_index_numbers + index_numbers
                    all_categories = all_categories + [categories[x]]*len(index_numbers)
                print(f'Completed index {j}')
                # Pause to avoid 403 erros 
                sleep(3)
            #Check for additional pages
            print('Getting new pages')
            url = f'https://www.stilltasty.com/searchitems/index/{new_pages[-1]}'
            results_pages = results_pages+new_pages
            new_pages = [k for k in get_index_numbers(url,"/searchitems/index/")[0] if k not in results_pages]
            new_pages = list(set(new_pages))
            new_pages.sort()

    #Data check
    if not len(all_index_numbers) == len(all_categories) == len(set(all_index_numbers)):
        raise Exception('Something is wrong with the all_index_numbers list!')

    #Counts by category
    print(Counter(all_categories))

    init_food_list = [{'index': all_index_numbers[i], 'category': all_categories[i]} for i in range(len(all_index_numbers))]
    #Write to csv
    keys = init_food_list[0].keys()
    with open(food_indices_filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(init_food_list)
    print(f"Food Indices scrape complete and new file written.")


################################################################
# Loop through each food item                                  #
# Scrape the relevant data and store in a list of dictionaries #
# Write to csv                                                 #
################################################################

food_items_filename = data_folder+'stilltasty_food_items.csv'

food_list = [scrape_stilltasty(all_index_numbers[i],all_categories[i]) for i in range(len(all_index_numbers))]

#Write to csv
keys = food_list[0].keys()
with open(food_items_filename, 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(food_list)

print('All food items have been scraped and a new file written')