import csv
from datetime import datetime
import sys
from dateutil import parser
import pytz

def convert_cashapp_to_cointracker(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.writer(outfile)

        # Write CoinTracker header
        writer.writerow(['Date', 'Received Quantity', 'Received Currency', 'Sent Quantity', 'Sent Currency', 'Fee Amount', 'Fee Currency', 'Tag'])

        for row in reader:
            # Parse the date with dateutil, which can handle various formats
            date_obj = parser.parse(row['Date'])
            
            # Convert to UTC
            if date_obj.tzinfo:
                date_utc = date_obj.astimezone(pytz.UTC)
            else:
                # If no timezone info, assume it's in US/Pacific
                pacific = pytz.timezone('US/Pacific')
                date_obj = pacific.localize(date_obj)
                date_utc = date_obj.astimezone(pytz.UTC)
            
            # Format the UTC date as a string
            date = date_utc.strftime('%Y-%m-%d %H:%M:%S')

            transaction_type = row['Transaction Type']
            currency = row['Currency']
            amount = abs(float(row['Amount'].replace('$', '').replace(',', '')))
            fee = abs(float(row['Fee'].replace('$', '').replace(',', '')))
            asset_type = row['Asset Type']
            asset_amount = float(row['Asset Amount']) if row['Asset Amount'] else 0

            if transaction_type == 'Bitcoin Buy':
                writer.writerow([
                    date,
                    asset_amount,
                    'BTC',
                    amount,
                    currency,
                    fee,
                    currency,
                    ''
                ])
            elif transaction_type ==  ['Bitcoin Lightning Withdrawal', 'Bitcoin Withdrawal', 'Bitcoin Sale']:
                writer.writerow([
                    date,
                    amount,
                    currency,
                    asset_amount,
                    'BTC',
                    fee,
                    currency,
                    ''
                ])
            else:
                print(f"Unhandled transaction type: {transaction_type}", file=sys.stderr)

if __name__ == '__main__':
    input_file = 'cashapp_transactions.csv'
    output_file = 'cointracker_transactions.csv'
    convert_cashapp_to_cointracker(input_file, output_file)
    print(f"Conversion complete. Output saved to {output_file}")
