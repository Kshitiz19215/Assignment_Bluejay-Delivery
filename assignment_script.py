import csv
from datetime import datetime
import sys

def parse_datetime(date_str):
    datetime_str = f"{date_str}".strip()
    
    try:
        return datetime.strptime(datetime_str, "%m/%d/%Y %I:%M %p")
    except ValueError:
        print(f"Error parsing datetime: {datetime_str}")
        raise

def analyze_file(file_path):
    CONSECUTIVE_DAYS_THRESHOLD = 7
    MIN_HOURS_BETWEEN_SHIFTS = 1
    MAX_HOURS_IN_SINGLE_SHIFT = 14

    employee_data = {}

    # Redirect stdout to a file
    sys.stdout = open('output.txt', 'w')

    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            employee_name = row['Employee Name']
            position = row['Position ID']

            # Skip rows with empty time fields
            if not row['Time'] or not row['Time Out']:
                continue

            time_in = parse_datetime(row['Time'])
            time_out = parse_datetime(row['Time Out'])
            
            if employee_name not in employee_data:
                employee_data[employee_name] = {'positions': set(), 'shifts': []}

            employee_data[employee_name]['positions'].add(position)

            employee_data[employee_name]['shifts'].append({
                'position': position,
                'time_in': time_in,
                'time_out': time_out,
                'hours_worked': (time_out - time_in).total_seconds() / 3600
            })

    for employee_name, data in employee_data.items():
        shifts = data['shifts']

        for i in range(len(shifts) - CONSECUTIVE_DAYS_THRESHOLD + 1):
            consecutive_days = shifts[i:i + CONSECUTIVE_DAYS_THRESHOLD]
            if all((consecutive_days[j + 1]['time_in'] - consecutive_days[j]['time_out']).days == 1 for j in range(CONSECUTIVE_DAYS_THRESHOLD - 1)):
                print(f"{employee_name} worked for 7 consecutive days.")

        for i in range(len(shifts) - 1):
            hours_between_shifts = (shifts[i + 1]['time_in'] - shifts[i]['time_out']).total_seconds() / 3600
            if 1 < hours_between_shifts < 10:
                print(f"{employee_name} has less than 10 hours between shifts (but greater than 1 hour).")

        for shift in shifts:
            if shift['hours_worked'] > MAX_HOURS_IN_SINGLE_SHIFT:
                print(f"{employee_name} worked for more than 14 hours in a single shift.")

    sys.stdout.close()
    sys.stdout = sys.__stdout__

file_path = 'Assignment_Timecard.csv'
analyze_file(file_path)