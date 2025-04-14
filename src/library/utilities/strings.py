'''
Utility functions for text processing and data handling.
'''
import unicodedata
import re

def remove_czech_diacritics(text):
    """
    Converts Czech characters with diacritics to their ASCII equivalents.

    Args:
        text (str): The input string containing Czech characters.

    Returns:
        str: The string with diacritics removed.
    """
    # Normalize the text to decompose characters with diacritics
    normalized_text = unicodedata.normalize('NFD', text)
    # Filter out diacritic marks and return the ASCII equivalent
    ascii_text = ''.join(char for char in normalized_text if unicodedata.category(char) != 'Mn')
    return ascii_text

def clean_and_format_string(text):
    """
    Removes special characters from the string and replaces spaces with underscores.

    Args:
        text (str): The input string.

    Returns:
        str: The cleaned and formatted string.
    """
    leading_characters = " "
    # Remove special characters using regex
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    cleaned_text = cleaned_text.lstrip(leading_characters).rstrip(leading_characters)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    # Replace spaces with underscores
    formatted_text = cleaned_text.replace(' ', '_')
    return formatted_text


# Example usage
if __name__ == "__main__":
    czechText = "Příliš žluťoučký kůň úczechTextké ódy."
    print(remove_czech_diacritics(czechText))
    # Output: "Prilis zlutoucky kun upel dabelske ody."
