

import xml.etree.ElementTree as ET
import pandas as pd
import logging
import tkinter as tk
from tkinter import filedialog
import argparse

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='xml_text_transformer.log'
                    )

def parse_xml(xml_input_file):
    tree = ET.parse(xml_input_file)
    logging.info(f"parsing started {xml_input_file}")
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
    transform_text = ''

    for char in input_str:
        if char != ' ': 
            if capitalize_next:
                transform_text += char.upper()
            else:
                transform_text += char.lower()
            capitalize_next = not capitalize_next
        else:
            transform_text += char

    logging.info(f"Processing completed: {transform_text}")
    return transform_text

def save_data(data, output_file, str):
    data.to_excel(output_file, index=False)
    logging.info("Excel file saved successfully")
 
    print("The modified string is: ",str)    
    logging.info("String displayed successfully")

def save_to_excel(data, output_file):
    data.to_excel(output_file,index = False)
    logging.info("Excel file saved successfully")

def gui():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    xml_input_file = filedialog.askopenfilename(title="Select XML File")
    if not xml_input_file:
        logging.error("No input file selected")
        return

    output_file = filedialog.asksaveasfilename(title="Save As", defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if not output_file:
        logging.error("No output file selected")
        return

    data = parse_xml(xml_input_file)
    save_to_excel(data, output_file)

def cli(input_str, xml_input_file, output_file):
    data = parse_xml(xml_input_file)
    str = process_string(input_str)
    save_data(data, output_file, str)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-string_input','-Is')
    parser.add_argument('-xml_file_input','-If')
    parser.add_argument('-excel_file_output', '-Of')
    args = parser.parse_args()

    if args.string_input and args.xml_file_input and args.excel_file_output :
        logging.debug("Input through command line")
        cli(args.string_input, args.xml_file_input, args.excel_file_output)
    else:
        logging.debug("input through GUI")
        gui()
