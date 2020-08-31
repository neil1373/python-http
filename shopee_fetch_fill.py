import time
import requests
import json
from tqdm import tqdm   # 進度條，pip3 install tqdm
import constant_file

# YOU COULD ALSO ADD SOME ATTRIBUTE ON YOUR OWN.
class product(object):
    name = 'name'
    price = 1
    weblink = 'weblink'
    photo_count = 0
    photolinks = []
    avg_rating = 4.0
    rating_count_list = [] #[total, 1, 2, 3, 4, 5]

def getAllItems(keyword, n_items = 30, minPrice = 1, maxPrice = 200000000, locations = '', ratingFilter = 3, preferred = False, officialMall = False):
    print(str.lower(str(preferred)))
    search_url = f'<fill here>'

    # print(search_url)

    search_result = requests.get( <fill here>, headers = <fill here>)
    search_data = json.loads( <fill here> )
    product_list = []

    for i in tqdm(range(n_items), desc = 'Processing search data...'):
        '''
        <fill here>
        '''
    return product_list


def getItemInfo(itemid, shopid):
    product_object = product()
    product_url = f'<fill here>'
    # Example URL: https://shopee.tw/product/27695857/990047817
    product_info = requests.get( <fill here>, headers = <fill here>)
    
    product_data = json.loads( <fill here> )

    '''
    Description: For each Product, you will need attributes 'name', 'price', 
    'weblink', 'photo_count, 'photolinks (list)', 'avg_rating', 'rating_count_list'
    for each product. Try to find each corresponding info in the example json file.
    Note: There is some tricky thing with product price.
    '''
    
    # print(product_name, product_price)

    setattr(product_object, 'name', <fill here>)

    setattr(product_object, 'price', <fill here>)

    setattr(product_object, 'weblink', <fill here>)

    setattr(product_object, 'photo_count', <fill here>)

    setattr(product_object, 'photolinks', <fill here>)

    setattr(product_object, 'avg_rating', <fill here>)

    setattr(product_object, 'rating_count_list', <fill here>)
    
    time.sleep(0.15) # to avoid of being recognized as robot by shopee server
    return product_object
    
def main():
    # Testing functions
    product_list = getAllItems(keyword = 'iPhone 11', n_items = 40, locations = -1, ratingFilter = 4)
    print("product_list = ", product_list)
    print("itemid = ", product_list[0].itemid, "shopid = ", product_list[0].shopid)
    product_object = getItemInfo(product_list[0].itemid, product_list[0].shopid)
    print(product_object.name)

    # Simple Filters
    '''
    keyword: <str>
    n_items: <positive int>
    '''

    '''
    locations:
        -1 : Taiwan
        -2 : Abroad
    '''

    '''
    ratingFilter: <positive int>
    preferred = <bool> 蝦皮優選賣家
    officialMall = <bool> 蝦皮商城賣家
    '''

if __name__ == '__main__':
    main()