import argparse
import urllib.request
import logging
import datetime
import csv

def downloadData(url):
    """Downloads the data"""
    if url.startswith('http'):
        response = urllib.request.urlopen(url)
        return response.read().decode('utf-8')
    else:
        with open(url, 'r') as file:
            return file.read()

def processData(file_content):
    """Process the data"""
    data = csv.reader(file_content.splitlines())
    personData = {}
    logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(asctime)s %(message)s')
        
    for line_num, row in enumerate(data, 1):
        try:
            id, name, birthday_str = row
            birthday = datetime.datetime.strptime(birthday_str, '%d/%m/%Y').date()
            personData[int(id)] = (name, birthday)
        except ValueError as e:
            logging.error(f'Error processing line #{line_num} for ID #{id}: {e}')
    
    return personData

def calculate_age(birthdate):
    today = datetime.date.today()  # Corrected from datetime.today().date()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

def displayPerson(id, personData):
    """Display person info"""
    person = personData.get(id)
    if person:
        name, birthday = person
        age = calculate_age(birthday)  # This should work if calculate_age is defined correctly
        print(f"Person #{id} is {name}, their birthday is {birthday.strftime('%Y-%m-%d')} and they are {age} years old.")
    else:
        print("No user found with that id.")
        

def main(url):
    print(f"Running main with URL = {url}...")
    try:
        data = downloadData(url)
    except Exception as e:
        print(f"An error occurred while downloading the data: {e}")
        return
    
    personData = processData(data)
    
    while True:
        try:
            id_str = input("Please enter an ID to lookup or type 'exit' to quit: ")
            if id_str.lower() == "exit":
                break
            id = int(id_str)
            displayPerson(id, personData)
        except ValueError:
            print("ID should be an integer. Please try again.")

if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    
    # If the script is run without any arguments, use the provided local path for the CSV file
    if not args.url:
        args.url = "C:/Users/faruk/Downloads/birthdays100.csv"
    
    main(args.url)
