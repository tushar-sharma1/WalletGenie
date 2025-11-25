import pandas as pd
import io
from typing import List, Dict

def parse_csv(file_content: bytes) -> List[Dict]:
    """
    Parses a CSV file content and returns a list of normalized transaction dictionaries.
    Expected columns: Date, Description, Amount, Category (optional).
    """
    try:
        df = pd.read_csv(io.BytesIO(file_content))
        
        # Normalize column names to lowercase
        df.columns = df.columns.str.lower().str.strip()
        
        # Basic mapping (can be improved with AI later)
        # We look for common column names
        
        normalized_data = []
        
        for _, row in df.iterrows():
            # Date parsing (naive)
            date_val = row.get('date') or row.get('transaction date')
            
            # Description
            desc_val = row.get('description') or row.get('details') or row.get('narration')
            
            # Amount
            amount_val = row.get('amount') or row.get('debit') or row.get('credit')
            
            # Category
            cat_val = row.get('category') or 'Uncategorized'
            
            # Type (Debit/Credit) logic
            # If 'debit' and 'credit' columns exist
            type_val = 'debit' # default
            if 'credit' in df.columns and pd.notna(row.get('credit')):
                 amount_val = row.get('credit')
                 type_val = 'credit'
            elif 'debit' in df.columns and pd.notna(row.get('debit')):
                 amount_val = row.get('debit')
                 type_val = 'debit'
            elif amount_val is not None:
                # If amount is negative, it's usually a debit
                try:
                    amt_float = float(str(amount_val).replace(',', ''))
                    if amt_float < 0:
                        type_val = 'debit'
                        amount_val = abs(amt_float)
                    else:
                        type_val = 'credit' # Assumption: positive is credit? Or depends on bank. 
                        # Actually for most statements, -ve is debit. 
                        # Let's assume standard: -ve = debit, +ve = credit.
                        # But wait, usually spending is positive in "Debit" column.
                        # Let's keep it simple: if 'debit' column exists, use that.
                        pass
                except:
                    pass

            if date_val and amount_val:
                normalized_data.append({
                    "date": str(date_val),
                    "description": str(desc_val),
                    "amount": float(str(amount_val).replace(',', '')),
                    "type": type_val,
                    "category": str(cat_val),
                    "source": "csv_upload"
                })
                
        return normalized_data
    except Exception as e:
        print(f"Error parsing CSV: {e}")
        return []
