
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_product_recommendation.settings')
django.setup()

from sklearn.feature_extraction.text import TfidfVectorizer  # to automatically create
from sklearn.metrics.pairwise import cosine_similarity

from home.models import Product

def get_similar_products(product_id, no_of_products = 10):

    # this will ignore common words like in, the, of, that etc.
    vectorizer = TfidfVectorizer(stop_words='english')

    # get descriptions of the products
    product_descriptions = Product.objects.all().values_list('description', flat = True)

    # this will create 2D array and assign values to each produc, like [[0.023,],[0.235,]]
    tfid_matrix = vectorizer.fit_transform(product_descriptions)

    # target product through which it will create list of similar products
    target_product = Product.objects.get(id = product_id)

    all_products = list(Product.objects.all())

    # this will get the index of product
    target_index = all_products.index(target_product)

    cosine_similar = cosine_similarity(tfid_matrix[target_index], tfid_matrix).flatten()

    # this will return indices in numpy array
    similar_indices = cosine_similar.argsort()[-no_of_products-1:-1][::-1]

    # convert above numpy array into normal array
    similar = [i for i in similar_indices if i != target_index]

    # get similar products
    similar_products = []
    for i in similar:
        similar_products.append(all_products[i])

    return similar_products


get_similar_products(2616)



######## Bellow script is for just upload products in bulk ##########
import pandas as pd
import csv
from home.models import Product

file_path = 'flipkart_com-ecommerce_sample.csv'

with open(file_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    for row in reader:
        try:
            product_name = row['product_name']
            product_image = eval(row['image'])[0]
            description = row['description']
            category = row['product_category_tree'].split('>>')[0].strip('[]"')
            price = row['retail_price']

            print(
                product_name,
                product_image,
                description,
                category,
                price
            )

            Product.objects.update_or_create(
                name = product_name,
                defaults={
                    'product_image': product_image,
                    'description': description,
                    'category': category,
                    'price': price,
                }
            )

        except Exception as e:
            print(e)

print('All products are imported successfully')