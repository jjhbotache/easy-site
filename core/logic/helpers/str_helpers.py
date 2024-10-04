import re
import unicodedata

def txt_to_url(text):
  """totally creaded by AI

  Args:
      text (str): The input text to be converted.

  Returns:
      str: The URL-friendly version of the input text.
  """
  # Normalize the text to NFKD form
  text = unicodedata.normalize('NFKD', text)
  # Encode to ASCII bytes, ignore non-ASCII characters
  text = text.encode('ascii', 'ignore').decode('ascii')
  # Replace spaces with hyphens
  text = re.sub(r'\s+', '-', text)
  # Remove any characters that are not alphanumeric, hyphens, or underscores
  text = re.sub(r'[^\w\-]', '', text)
  # Convert to lowercase
  text = text.lower()
  # Remove leading and trailing hyphens
  text = text.strip('-')
  return text

def get_company_name_from_url(url):
    """Extracts the company name from a given URL.

    Args:
        url (str): The input URL.

    Returns:
        str: The extracted company name or an empty string if not found.
    """
    # Split the URL by '/'
    parts = url.split('/')
    
    # Check if there are at least two parts after splitting
    if len(parts) > 1:
    # turn - to in case of company name with space
        return parts[1].replace('-', ' ')
        
    
    # Return an empty string if the company name is not found
    
    
    return ''