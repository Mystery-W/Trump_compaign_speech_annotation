import os
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
from tqdm import tqdm
import stanza

# Initialize Stanza NLP pipeline with minimal processors
nlp = stanza.Pipeline('en')

# Define directories
source_dir = r"D:\\Lesson\\语料库建设与应用\\Trump rally\\cleaned"
output_dir = r"D:\\Lesson\\语料库建设与应用\\Trump rally\\xml"

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def extract_metadata_from_filename(filename):
    """Extracts metadata like city, state (if available), and date from the filename."""
    parts = filename.replace('.txt', '').split(' - ')
    if len(parts) < 2:
        raise ValueError(f"Filename does not match the expected format: {filename}")
    city_state = parts[0]
    date = parts[1]

    city_state_parts = city_state.split(', ')
    city = city_state_parts[0]
    state = city_state_parts[1] if len(city_state_parts) > 1 else "Unknown"
    return city, state, date

def prettify_xml(elem):
    """Returns a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def process_paragraphs(paragraphs):
    """Process all paragraphs with Stanza and return the annotated XML elements."""
    root_body = ET.Element('body')
    for p_idx, paragraph in enumerate(paragraphs, start=1):
        if paragraph.strip():  # Skip empty paragraphs
            p_elem = ET.SubElement(root_body, 'paragraph', id=str(p_idx))
            doc = nlp(paragraph.strip())
            for s_idx, sentence in enumerate(doc.sentences, start=1):
                s_elem = ET.SubElement(p_elem, 'sentence', id=str(s_idx))
                for w_idx, word in enumerate(sentence.words, start=1):
                    w_elem = ET.SubElement(s_elem, 'word', id=str(w_idx))
                    w_elem.text = word.text
    return root_body

def convert_to_xml(input_path, output_path):
    """Converts a text file to XML, numbering paragraphs, sentences, and words."""
    with open(input_path, 'r', encoding='utf-8') as file:
        paragraphs = file.readlines()  # Read all lines as paragraphs

    filename = os.path.basename(input_path)
    city, state, date = extract_metadata_from_filename(filename)

    # Create XML structure
    root = ET.Element('document')
    metadata = ET.SubElement(root, 'metadata')
    ET.SubElement(metadata, 'city').text = city
    ET.SubElement(metadata, 'state').text = state
    ET.SubElement(metadata, 'date').text = date

    # Annotate paragraphs and add to body
    body = process_paragraphs(paragraphs)
    root.append(body)

    # Write XML to file with pretty formatting
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(prettify_xml(root))

# Process all .txt files in the source directory
files = [f for f in os.listdir(source_dir) if f.endswith('.txt')]

for file_name in tqdm(files, desc="Processing files"):
    try:
        input_file = os.path.join(source_dir, file_name)
        output_file = os.path.join(output_dir, file_name.replace('.txt', '.xml'))
        convert_to_xml(input_file, output_file)
    except Exception as e:
        print(f"Error processing {file_name}: {e}")
