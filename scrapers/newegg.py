# scraper.py
import aiohttp
import json
from bs4 import BeautifulSoup
from lib.cookie import get_cookies
from lib.user_agents import get_user_agent

async def fetch_page(session, url, headers):
    """Fetch the content of the URL with the given headers."""
    try:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()  # Raise HTTPError for bad responses
            return await response.text()
    except aiohttp.ClientError as e:
        print(f"Error fetching URL {url}: {e}")
        return None


async def parse_product(html_content: str) -> dict:
    """
    Extract and clean the product title and price from HTML content.

    Args:
        html_content (str): The HTML content of the product page.

    Returns:
        dict: A dictionary containing the product title and price.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract product title
    title_tag = soup.find('h1', class_='product-title')
    title = title_tag.text.strip() if title_tag else 'Unknown Title'

    # Extract product price
    price_div = soup.find('div', class_='product-price')
    
    if price_div:
        price_element = price_div.find('li', class_='price-current')
        price = price_element.text.strip().replace('$', '') if price_element else 'N/A'
    else:
        price = 'N/A'

    return {'title': title, 'price': price}



async def execute(url):
    user_agent = get_user_agent()
    cookie = get_cookies('https://www.newegg.com/', {"User-Agent": user_agent})

    headers = {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Cookie": str(cookie)
    }

    async with aiohttp.ClientSession() as session:
        # Fetch the product page
        html_content = await fetch_page(session, url, headers)
        if not html_content:
            return {'error': 'Failed to fetch product page'}

        # Parse the product title
        data = await parse_product(html_content)
        product_title = data.get('title')
        price = data.get('price')

        # Extract SKU ID and fetch price
        sku_id = url.split('/p/')[-1]
        sku_id = sku_id.split('?')[0]
    

        return {
            'title': product_title,
            'item_sku': sku_id,
            'price': price,
            'url': url,
            'scraper': 'newegg'
        }


def main():
    import sys, asyncio
    if len(sys.argv) != 2:
        print("Usage: python scraper.py <URL>")
        sys.exit(1)

    url = sys.argv[1]

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(execute(url))
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()