##csv_util.py: Handles reading from and writing to CSV files. It's where your load_csv and save_csv functions reside.
import csv

def load_csv(filename):
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

def save_csv(filename, data, fieldnames):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)