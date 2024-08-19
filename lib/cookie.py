import requests


def get_cookies(url, headers):
    # Send a GET request to the URL
    response = requests.get(url, headers=headers)
    
    # Extract cookies from the response
    cookies = response.cookies.get_dict()
    if isinstance(cookies, dict):
        return '; '.join(f'{key}={value}' for key, value in cookies.items())
    return str(cookies)
    


    

# Example usage
if __name__ == "__main__":
    url = 'https://www.bestbuy.com/site/apple-macbook-air-13-6-laptop-m2-chip-8gb-memory-256gb-ssd-midnight/6509650.p?skuId=6509650'

    cookies = get_cookies(url)
    
    print("Cookies obtained:")
    print(cookies)
    for key, value in cookies.items():
        print(f"{key}: {value}")
