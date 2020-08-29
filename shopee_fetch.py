import time
import requests
import json

def shopeeAPI_Scraper(keyword, n_items, minPrice = 1, maxPrice = 200000000, locations = '', ratingFilter = 3, preferred = False, officialMall = False):
    print(str.lower(str(preferred)))
    search_url = f'https://shopee.tw/api/v1/search_items/\
?by=relevancy\
&locations={locations}\
&keyword={keyword}\
&limit={n_items}\
&maxPrice={maxPrice}\
&minPrice={minPrice}\
&locations={locations}\
&ratingFilter={ratingFilter}\
&preferred={str.lower(str(preferred))}\
&officialMall={str.lower(str(officialMall))}'

    print(search_url)
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    }
    search_result = requests.get(search_url, headers=headers)
    print("response")
    api1_data = json.loads(search_result.text)
    
    for i in range(n_items):
        itemid = api1_data['items'][i]['itemid']
        shopid = api1_data['items'][i]['shopid']
        
        product_url = f'https://shopee.tw/api/v2/item/get?itemid={itemid}&shopid={shopid}'
        product_info = requests.get(product_url, headers=headers)
        api2_data = json.loads(product_info.text)
        currency_unit = api2_data['item']['coin_info']['spend_cash_unit']
        output = api2_data['item']['name'].ljust(70) +': ' + str(api2_data['item']['price'] / currency_unit)
        print(output)
        product_weblink = f'https://shopee.tw/product/{shopid}/{itemid}'
        print(product_weblink)
        photo_count = 0
        for photo_hash in api2_data['item']['images']:
            photo_count += 1
            photo_link = f'https://cf.shopee.tw/file/{photo_hash}'
            print('Photo\t'+photo_link)
        # time.sleep(0.1)
    
def main():
    # Testing functions
    shopeeAPI_Scraper(keyword = 'iPhone 11', n_items = 20, locations = -1, ratingFilter = 4)
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