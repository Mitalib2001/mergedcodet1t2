import logging
import sys
import xml.etree.ElementTree as ET
import pandas as pd

# Configure logging
logging.basicConfig(filename='xml_text_transformer.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def transform_text(user_input):
    try:
        user_input = user_input.strip()  # Remove leading and trailing whitespaces
        if len(user_input.split()) < 3:
            logging.warning("Less than 3 words inputted.")
            return "Please input a minimum of 3 words."

        transformed_text = ""
        capitalize_next = True
        for char in user_input:
            if char.isalpha():
                if capitalize_next:
                    transformed_text += char.upper()
                else:
                    transformed_text += char.lower()
                capitalize_next = not capitalize_next
            else:
                transformed_text += char

        logging.info("Text transformed successfully.")
        return transformed_text
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return "An error occurred during transformation."

def parse_xml(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        data = []

        for container in root.findall('.//{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE'):
            short_name = container.find('.//{http://autosar.org/schema/r4.0}SHORT-NAME').text
            definition_ref = container.find('.//{http://autosar.org/schema/r4.0}DEFINITION-REF').text
            data.append({'Short Name': short_name, 'Definition Ref': definition_ref})

            for sub_container in container.findall('.//{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE'):
                sub_short_name = sub_container.find('.//{http://autosar.org/schema/r4.0}SHORT-NAME').text
                sub_definition_ref = sub_container.find('.//{http://autosar.org/schema/r4.0}DEFINITION-REF').text
                data.append({'Short Name': sub_short_name, 'Definition Ref': sub_definition_ref})

        return data
    except Exception as e:
        error_msg = f"Error parsing XML file: {str(e)}"
        logging.error(error_msg)
        print(error_msg)
        return []

def generate_excel(data, output_path):
    try:
        if not data:
            error_msg = "No data to create Excel file."
            logging.warning(error_msg)
            print(error_msg)
            return

        df = pd.DataFrame(data)
        df.to_excel(output_path, index=False)
        success_msg = f"Excel file created successfully: {output_path}"
        logging.info(success_msg)
        print(success_msg)
    except Exception as e:
        error_msg = f"Error creating Excel file: {str(e)}"
        logging.error(error_msg)
        print(error_msg)

def cli_mode(xml_file, output_path, input_text):
    try:
        transformed_text = transform_text(input_text)
        print("Transformed Text:", transformed_text)

        data = parse_xml(xml_file)
        generate_excel(data, output_path)
    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        logging.error(error_msg)
        print(error_msg)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        print("Usage: python xml_text_transformer.py <xml_file> <output_path> <input_text>")
        sys.exit(1)
    cli_mode(sys.argv[1], sys.argv[2], sys.argv[3])
