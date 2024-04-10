import xml.etree.ElementTree as ET
import pandas as pd
import logging
import tkinter as tk
from tkinter import filedialog
import argparse

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='task.log'
                    )

def parse_xml(input_file):
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
    
def process_string(input_str):
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

def save_data(data, output_file, str):
    data.to_excel(output_file, index=False)
    logging.info("Excel file saved successfully")
    # with open("output.docx", "w") as writer:
    #         writer.write(output_str)
    print("The modified string is: ",str)    
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

    data = parse_xml(input_file)
    save_to_excel(data, output_file)

def cli(input_str, input_file, output_file):
    data = parse_xml(input_file)
    str = process_string(input_str)
    save_data(data, output_file, str)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--str_input','-i1')
    parser.add_argument('--file_input','-i2')
    parser.add_argument('--output', '-o')
    args = parser.parse_args()

    if args.str_input and args.file_input and args.output :
        logging.debug("Input via command line")
        cli(args.str_input, args.file_input, args.output)
    else:
        logging.debug("Input via gui")
        gui()