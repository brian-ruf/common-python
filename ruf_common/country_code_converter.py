"""
Python functions to convert country names to ISO 3166-1 alpha-2 country codes.
Provides multiple approaches from simple dictionary lookup to library-based solutions.
"""
import logging

logger = logging.getLogger(__name__)

# Method 1: Simple dictionary approach (most common countries)
COUNTRY_TO_CODE = {
    # Major countries
    "United States": "US",
    "USA": "US",
    "United States of America": "US",
    "Canada": "CA",
    "United Kingdom": "GB",
    "UK": "GB",
    "Great Britain": "GB",
    "England": "GB",
    "Scotland": "GB",
    "Wales": "GB",
    "Northern Ireland": "GB",
    "Germany": "DE",
    "France": "FR",
    "Italy": "IT",
    "Spain": "ES",
    "Netherlands": "NL",
    "Belgium": "BE",
    "Switzerland": "CH",
    "Austria": "AT",
    "Sweden": "SE",
    "Norway": "NO",
    "Denmark": "DK",
    "Finland": "FI",
    "Poland": "PL",
    "Czech Republic": "CZ",
    "Hungary": "HU",
    "Portugal": "PT",
    "Greece": "GR",
    "Ireland": "IE",
    "Luxembourg": "LU",
    "Romania": "RO",
    "Bulgaria": "BG",
    "Estonia": "EE",
    "Croatia": "HR",
    
    # Asia-Pacific
    "Japan": "JP",
    "China": "CN",
    "South Korea": "KR",
    "Korea": "KR",
    "India": "IN",
    "Australia": "AU",
    "New Zealand": "NZ",
    "Singapore": "SG",
    "Malaysia": "MY",
    "Thailand": "TH",
    "Indonesia": "ID",
    "Philippines": "PH",
    "Vietnam": "VN",
    "Taiwan": "TW",
    "Hong Kong": "HK",
    
    # Americas
    "Brazil": "BR",
    "Mexico": "MX",
    "Argentina": "AR",
    "Chile": "CL",
    "Colombia": "CO",
    "Peru": "PE",
    "Venezuela": "VE",
    "Ecuador": "EC",
    "Uruguay": "UY",
    "Paraguay": "PY",
    "Bolivia": "BO",
    
    # Middle East & Africa
    "Israel": "IL",
    "Saudi Arabia": "SA",
    "United Arab Emirates": "AE",
    "UAE": "AE",
    "Bahrain": "BH",
    "Qatar": "QA",
    "Oman": "OM",
    "Turkey": "TR",
    "Egypt": "EG",
    "South Africa": "ZA",
    "Nigeria": "NG",
    "Kenya": "KE",
    "Morocco": "MA",
    
    # Others
    "Russia": "RU",
    "Russian Federation": "RU",
    "Ukraine": "UA",
    "Belarus": "BY",
    "Kazakhstan": "KZ",
}

def safe_country_name_to_code_map(country_name: str) -> str:
    """
    Save the country name to code map to a JSON file for future use.
    """
    country_code = COUNTRY_TO_CODE.get(country_name, "")
    if not country_code:
        logger.warning(f"Code for country name not found: {country_name}")

    return country_code


def country_name_to_code_simple(country_name: str) -> str:
    """
    Convert country name to ISO 3166-1 alpha-2 code using dictionary lookup.
    
    Args:
        country_name: Country name string
        
    Returns:
        Two-letter country code or empty string if not found
    """
    return COUNTRY_TO_CODE.get(country_name.strip(), "")

def country_name_to_code_fuzzy(country_name: str) -> str:
    """
    Convert country name to ISO code with fuzzy matching (case-insensitive).
    
    Args:
        country_name: Country name string
        
    Returns:
        Two-letter country code or empty string if not found
    """
    country_name = country_name.strip()
    
    # Try exact match first
    if country_name in COUNTRY_TO_CODE:
        return COUNTRY_TO_CODE[country_name]
    
    # Try case-insensitive match
    country_lower = country_name.lower()
    for name, code in COUNTRY_TO_CODE.items():
        if name.lower() == country_lower:
            return code
    
    # Try partial matches for common variations
    for name, code in COUNTRY_TO_CODE.items():
        if country_lower in name.lower() or name.lower() in country_lower:
            return code
    
    return ""

# Method 2: Using pycountry library (more comprehensive)
def country_name_to_code_pycountry(country_name: str) -> str:
    """
    Convert country name to ISO code using pycountry library.
    Requires: pip install pycountry
    
    Args:
        country_name: Country name string
        
    Returns:
        Two-letter country code or empty string if not found
    """
    try:
        import pycountry
        
        country_name = country_name.strip()
        
        # Try exact name match
        try:
            country = pycountry.countries.lookup(country_name)
            return getattr(country, "alpha_2", "")
        except LookupError:
            pass
        
        # Try fuzzy search
        try:
            country = pycountry.countries.search_fuzzy(country_name)[0]
            return getattr(country, "alpha_2", "")
        except (LookupError, IndexError):
            return ""
            
    except ImportError:
        print("pycountry library not installed. Use: pip install pycountry")
        return country_name_to_code_fuzzy(country_name)

# Method 3: Using requests to query REST Countries API
def country_name_to_code_api(country_name: str) -> str:
    """
    Convert country name to ISO code using REST Countries API.
    Requires internet connection and requests library.
    
    Args:
        country_name: Country name string
        
    Returns:
        Two-letter country code or empty string if not found
    """
    # Import requests first; if it's not available, fall back immediately.
    try:
        import requests
    except ImportError:
        return country_name_to_code_fuzzy(country_name)

    try:
        url = f"https://restcountries.com/v3.1/name/{country_name.strip()}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                return data[0].get('cca2', '')
        
        return ""
        
    except requests.RequestException:
        return country_name_to_code_fuzzy(country_name)
    except Exception:
        return country_name_to_code_fuzzy(country_name)

def demonstrate_conversion() -> None:
    """Demonstrate different country code conversion methods."""
    
    test_countries = [
        "United States",
        "USA",
        "United Kingdom",
        "Germany",
        "Japan",
        "Australia",
        "Brazil",
        "Invalid Country",
        "south korea",  # Test case sensitivity
        "UAE",
        "Russian Federation",
    ]
    
    print("=== COUNTRY NAME TO ISO CODE CONVERSION ===\n")
    
    for country in test_countries:
        print(f"Country: '{country}'")
        
        # Method 1: Simple dictionary
        code1 = country_name_to_code_simple(country)
        print(f"  Simple lookup: {code1 or 'Not found'}")
        
        # Method 2: Fuzzy matching
        code2 = country_name_to_code_fuzzy(country)
        print(f"  Fuzzy matching: {code2 or 'Not found'}")
        
        # Method 3: pycountry (if available)
        code3 = country_name_to_code_pycountry(country)
        print(f"  pycountry: {code3 or 'Not found'}")
        
        print()

def batch_convert_countries(country_list: list) -> dict:
    """
    Convert a list of country names to ISO codes.
    
    Args:
        country_list: List of country name strings
        
    Returns:
        Dictionary mapping country names to ISO codes
    """
    result = {}
    for country in country_list:
        code = country_name_to_code_fuzzy(country)
        result[country] = code
    return result

# Integration with location processing
def process_location_with_country_codes(locations_obj: list) -> list:
    """
    Process locations and add country codes.
    Assumes locations have a 'country' field.
    """
    processed = []
    
    for location in locations_obj:
        processed_location = location.copy()
        
        if 'country' in location:
            country_code = country_name_to_code_fuzzy(location['country'])
            processed_location['country_code'] = country_code
        
        processed.append(processed_location)
    
    return processed

if __name__ == "__main__":
    demonstrate_conversion()
    
    print("=== BATCH CONVERSION EXAMPLE ===")
    
    countries = ["United States", "Germany", "Japan", "Australia", "Brazil"]
    codes = batch_convert_countries(countries)
    
    for country, code in codes.items():
        print(f"{country} → {code}")
    
    print("\n=== LOCATION PROCESSING EXAMPLE ===")
    
    sample_locations = [
        {"name": "New York", "country": "United States", "type": "office"},
        {"name": "London", "country": "United Kingdom", "type": "office"},
        {"name": "Tokyo", "country": "Japan", "type": "datacenter"},
        {"name": "Sydney", "country": "Australia", "type": "warehouse"},
    ]
    
    processed = process_location_with_country_codes(sample_locations)
    
    for location in processed:
        print(f"{location['name']}, {location['country']} → {location.get('country_code', 'N/A')}")
