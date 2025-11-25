import pandas as pd
import random
from datetime import datetime, timedelta

def generate_data():
    categories = [
        ('Housing', 2000, 2500, 'Rent'),
        ('Food', 50, 200, 'Groceries'),
        ('Food', 20, 100, 'Dining Out'),
        ('Transport', 20, 50, 'Uber'),
        ('Transport', 100, 200, 'Car Insurance'),
        ('Shopping', 50, 300, 'Amazon'),
        ('Utilities', 100, 200, 'Electric Bill'),
        ('Entertainment', 15, 50, 'Netflix'),
        ('Entertainment', 15, 50, 'Spotify'),
        ('Health', 100, 300, 'Gym'),
        ('Income', 5000, 6000, 'Salary')
    ]

    start_date = datetime.now() - timedelta(days=365)
    data = []

    for i in range(365):
        current_date = start_date + timedelta(days=i)
        
        # Monthly recurring
        if current_date.day == 1:
            data.append([current_date.strftime('%Y-%m-%d'), 'Rent', 2400.00, 'debit', 'Housing', 'Housing'])
            data.append([current_date.strftime('%Y-%m-%d'), 'Salary', 5500.00, 'credit', 'Income', 'Income'])
            data.append([current_date.strftime('%Y-%m-%d'), 'Electric Bill', random.uniform(120, 180), 'debit', 'Utilities', 'Utilities'])
            data.append([current_date.strftime('%Y-%m-%d'), 'Internet', 60.00, 'debit', 'Utilities', 'Utilities'])
            data.append([current_date.strftime('%Y-%m-%d'), 'Netflix', 15.99, 'debit', 'Entertainment', 'Entertainment'])
            data.append([current_date.strftime('%Y-%m-%d'), 'Spotify', 9.99, 'debit', 'Entertainment', 'Entertainment'])
            data.append([current_date.strftime('%Y-%m-%d'), 'Gym', 49.99, 'debit', 'Health', 'Health'])

        # Random daily spending
        if random.random() < 0.7: # 70% chance of spending
            cat, min_amt, max_amt, desc = random.choice(categories)
            if cat != 'Income' and cat != 'Housing': # Skip rent/income for random
                amt = random.uniform(min_amt, max_amt)
                data.append([current_date.strftime('%Y-%m-%d'), desc, round(amt, 2), 'debit', cat, cat])
                
        # Weekend splurges
        if current_date.weekday() >= 5: # Sat/Sun
             if random.random() < 0.5:
                data.append([current_date.strftime('%Y-%m-%d'), 'Bar/Club', random.uniform(50, 150), 'debit', 'Entertainment', 'Entertainment'])
                data.append([current_date.strftime('%Y-%m-%d'), 'Fancy Dinner', random.uniform(100, 250), 'debit', 'Food', 'Food'])

    df = pd.DataFrame(data, columns=['date', 'description', 'amount', 'type', 'category', 'source'])
    df.to_csv('transactions_12months.csv', index=False)
    print("Generated transactions_12months.csv")

if __name__ == "__main__":
    generate_data()
