import aiohttp
import asyncio

async def test_pubmed_search():
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    
    # Case 1: Empty API Key (Suspected Cause)
    params_empty_key = {
        "db": "pubmed",
        "term": "cancer",
        "retmax": 5,
        "retmode": "json",
        "api_key": "" 
    }
    
    # Case 2: No API Key (Correct Way)
    params_no_key = {
        "db": "pubmed",
        "term": "cancer",
        "retmax": 5,
        "retmode": "json"
    }

    async with aiohttp.ClientSession() as session:
        print("Testing with api_key='' ...")
        async with session.get(url, params=params_empty_key, ssl=False) as resp1:
            print(f"Status: {resp1.status}")
            if resp1.status != 200:
                print(f"Response: {await resp1.text()}")

        print("\nTesting without api_key parameter...")
        async with session.get(url, params=params_no_key, ssl=False) as resp2:
            print(f"Status: {resp2.status}")
            if resp2.status != 200:
                print(f"Response: {await resp2.text()}")

if __name__ == "__main__":
    asyncio.run(test_pubmed_search())
