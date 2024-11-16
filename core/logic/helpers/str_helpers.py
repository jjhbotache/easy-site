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

def adjust_color_value(value, percentage):
    """
    Ajusta el valor de un componente RGB (R, G, o B) en base a un porcentaje.
    Si el porcentaje es positivo, aclara el color. Si es negativo, lo oscurece.
    """
    return max(0, min(255, int(value * (1 + percentage))))


# ------------------------------------------------------------------------------------------
def hex_to_rgb(hex_color):
    """
    Convierte un color en formato hexadecimal a su representación RGB.
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb_color):
    """
    Convierte un color en formato RGB a su representación hexadecimal.
    """
    return '#{:02x}{:02x}{:02x}'.format(*rgb_color)

def get_color_variations(hex_color, adjustment_percentage=0.3):
    """
    Dado un color en formato hexadecimal, devuelve un diccionario con el color original,
    una versión más clara y una versión más oscura. 
    El ajuste se hace en base a un porcentaje dado (por defecto 50%).
    
    Parámetros:
    - hex_color: (str) Color en formato hexadecimal (#rrggbb).
    - adjustment_percentage: (float) Porcentaje de ajuste para aclarar/oscurecer (e.g., 0.2 es un 20%).
    
    Retorna:
    - dict con 'color', 'lighter' y 'darker' en formato hexadecimal.
    """
    # Convertir el color hexadecimal a RGB
    r, g, b = hex_to_rgb(hex_color)
    
    # Calcular el color más claro (incrementa cada componente RGB)
    lighter_rgb = (
        adjust_color_value(r, adjustment_percentage),
        adjust_color_value(g, adjustment_percentage),
        adjust_color_value(b, adjustment_percentage)
    )
    
    # Calcular el color más oscuro (reduce cada componente RGB)
    darker_rgb = (
        adjust_color_value(r, -adjustment_percentage),
        adjust_color_value(g, -adjustment_percentage),
        adjust_color_value(b, -adjustment_percentage)
    )
    
    # Convertir los colores RGB de nuevo a hexadecimal
    output_colors = {
        'color': hex_color,
        'lighter': rgb_to_hex(lighter_rgb)[1:],
        'darker': rgb_to_hex(darker_rgb)[1:]
    }

    # print(output_colors)
    return output_colors

# ------------------------------------------------------------------------------------------