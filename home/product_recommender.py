from sklearn.feature_extraction.text import TfidfVectorizer  # to automatically create
from sklearn.metrics.pairwise import cosine_similarity

from home.views import Product


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