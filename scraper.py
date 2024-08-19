import importlib
import pkgutil
from typing import List, Dict, Any
import asyncio

def list_scrapers() -> List[str]:
    """
    Lists all modules in the 'scrapers' package.

    Returns:
        List[str]: A list of module names within the 'scrapers' package.
    """
    package = importlib.import_module('scrapers')
    if not hasattr(package, '__path__'):
        raise ImportError("The 'scrapers' package does not have a __path__ attribute.")
        
    modules = [name for _, name, _ in pkgutil.iter_modules(package.__path__)]
    return modules

async def run_scrape(scraper: str, url: str) -> Dict[str, Any]:
    """
    Dynamically imports the specified scraper module and calls its 'execute' function.

    Args:
        scraper (str): The name of the scraper module to use.
        url (str): The URL to scrape.

    Returns:
        Dict[str, Any]: The result of the scraping function or an error message.
    """
    try:
        # Dynamically import the scraper module
        module = importlib.import_module(f"scrapers.{scraper}")

        # Get the 'execute' function from the module
        func = getattr(module, 'execute')

        if not asyncio.iscoroutinefunction(func):
            raise TypeError("The 'execute' function must be asynchronous.")

        # Call the asynchronous function
        result = await func(url)
        return result

    except ImportError as e:
        return {"error": f"Error importing module: {e}"}
    except AttributeError as e:
        return {"error": f"Error retrieving function: {e}"}
    except TypeError as e:
        return {"error": f"Function type error: {e}"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}



