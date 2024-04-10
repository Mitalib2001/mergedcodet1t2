import xml.etree.ElementTree as ET
import pandas as pd
import logging
import tkinter as tk
from tkinter import filedialog
import argparse

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='task.log')

def extract_data(input_file):
    tree = ET.parse(input_file)
    logging.info(f"Started parsing {input_file}")
    root = tree.getroot()

    data = []
    ns = {'autosar': 'http://autosar.org/schema/r4.0'}
    for containers in root.findall('.//autosar:CONTAINERS',ns):
        short_name_container = containers.find('.//autosar:SHORT-NAME', ns).text
        definition_ref_container = containers.find('.//autosar:DEFINITION-REF', ns).text
        data.append({'Tag':'Container','Short Name': short_name_container, 'Definition Ref': definition_ref_container})
        for sub_containers in containers.findall('.//autosar:SUB-CONTAINERS', ns):
            short_name = sub_containers.find('.//autosar:SHORT-NAME', ns).text
            definition_ref = sub_containers.find('.//autosar:DEFINITION-REF', ns).text
            data.append({'Tag':'Sub-container','Short Name': short_name, 'Definition Ref': definition_ref})
    logging.debug("Parsing completed")
    return pd.DataFrame(data)
    
def transform_string(input_str):
    logging.info("String processing started")
    capitalize_next = True
    processed_output = ''

    for char in input_str:
        if char != ' ': 
            if capitalize_next:
                processed_output += char.upper()
            else:
                processed_output += char.lower()
            capitalize_next = not capitalize_next
        else:
            processed_output += char

    logging.info(f"Processing completed: {processed_output}")
    return processed_output

def save_data(data, output_file, processed_string):
    data.to_excel(output_file, index=False)
    logging.info(f"Excel file saved successfully at {output_file}")
    print("The modified string is: ", processed_string)
    logging.info("String displayed successfully")

def save_to_excel(data, output_file):
    data.to_excel(output_file,index = False)
    logging.info("Excel file saved successfully")

def gui():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    input_file = filedialog.askopenfilename(title="Select XML File")
    if not input_file:
        logging.error("No input file selected")
        return

    output_file = filedialog.asksaveasfilename(title="Save As", defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if not output_file:
        logging.error("No output file selected")
        return

    data = extract_data(input_file)
    save_to_excel(data, output_file)

def cli(input_str, input_file, result_file):
    data = extract_data(input_file)
    processed_str = transform_string(input_str)
    save_data(data, result_file, processed_str)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_str','-Is', help="Input string")
    parser.add_argument('--input_file','-If', help="Input file")
    parser.add_argument('--result_file', '-Of', help="Result file")
    args = parser.parse_args()

    if args.input_str and args.input_file and args.result_file:
        logging.debug("Command line input detected")
        cli(args.input_str, args.input_file, args.result_file)
    else:
        logging.debug("GUI input detected")
        gui()
