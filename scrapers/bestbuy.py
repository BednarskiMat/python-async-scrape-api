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

async def parse_product_title(html_content):
    """Extract and clean the product title from HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    title_tag = soup.find('title')
    if title_tag:
        return title_tag.text.replace('- Best Buy', '').strip()
    return 'Unknown Title'

async def get_price(session, sku_id, user_agent):
    """Fetch the price for the given SKU ID."""
    api_url = (f"https://www.bestbuy.com/pricing/v1/price/item?"
               f"allFinanceOffers=true&catalog=bby&context=offer-list"
               f"&effectivePlanPaidMemberType=NULL&includeOpenboxPrice=true"
               f"&paidMemberSkuInCart=false&salesChannel=LargeView"
               f"&skuId={sku_id}&useCabo=true&usePriceWithCart=true"
               f"&visitorId=c706c8c0-3967-11ef-9760-128a771c0c87")

    headers = {
        "User-Agent": user_agent,
        "Accept": "application/json",
        "X-CLIENT-ID": "lib-price-browser"
    }

    html_content = await fetch_page(session, api_url, headers)
    if html_content:
        try:
            data = json.loads(html_content)
            return data.get('currentPrice', 'N/A')
        except json.JSONDecodeError:
            print("Error parsing JSON response.")
            return 'N/A'
    return 'N/A'

async def execute(url):
    user_agent = get_user_agent()
    cookie = get_cookies('https://www.bestbuy.com/', {"User-Agent": user_agent})

    headers = {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://www.bestbuy.com/",
        "Cookie": cookie
    }

    async with aiohttp.ClientSession() as session:
        # Fetch the product page
        html_content = await fetch_page(session, url, headers)
        if not html_content:
            return {'error': 'Failed to fetch product page'}

        # Parse the product title
        product_title = await parse_product_title(html_content)

        # Extract SKU ID and fetch price
        sku_id = url.split('skuId=')[-1]
        price = await get_price(session, sku_id, user_agent)

        return {
            'title': product_title,
            'product_id': sku_id,
            'price': price,
            'url': url,
            'scraper': 'bestbuy'
        }
