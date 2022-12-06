import pandas as pd
import re

BAD_TOKENS = ['width=', '.jpg', 'preview.redd.it', 'https:', 'and#x200B;']

def clean_text(data, columns: list):
    # Check if inputs are of the correct type
    if not isinstance(columns, list):
        raise TypeError('columns is not list')
    elif not isinstance(data, pd.DataFrame):
        raise TypeError('data is not pd.DataFrame')
    pass
    
    for col in columns:
        col_cleaned = []
        for row in data[col]:
            string_clean = (
                row
                .replace("/", ' ')
                .replace('&amp;', 'and')
                .strip()
            )
            processed_token = [i for i  in re.split('\s|\n|\t', string_clean.strip()) if i != '']
            processed_token = list(filter (lambda s:any([c.isalnum() for c in s]), processed_token))
            processed_token = [item for item in processed_token if not any(substring in item for substring in BAD_TOKENS)]
            col_cleaned.append((' '.join(processed_token)))
        data[col] = col_cleaned
    return data