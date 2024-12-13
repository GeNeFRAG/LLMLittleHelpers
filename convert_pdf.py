import fitz  # PyMuPDF
import json
import os
import sys
import argparse
import psutil
import time

def pdf_to_text(pdf_path):
    """
    Extract text from a PDF file and save it as a TXT file.
    
    Args:
        pdf_path (str): The path to the PDF file.
        
    Returns:
        str: The path to the generated TXT file.
    """
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    
    txt_path = os.path.splitext(pdf_path)[0] + ".txt"
    with open(txt_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(text)
    
    return txt_path

def pdf_to_json(pdf_path):
    """
    Extract text from a PDF file and save it as a JSON file.
    
    Args:
        pdf_path (str): The path to the PDF file.
        
    Returns:
        str: The path to the generated JSON file.
    """
    doc = fitz.open(pdf_path)
    pages = []
    for page_num, page in enumerate(doc):
        text = page.get_text()
        pages.append({"page": page_num + 1, "text": text})
    
    json_path = os.path.splitext(pdf_path)[0] + ".json"
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(pages, json_file, indent=4, ensure_ascii=False)
    
    return json_path

def main(pdf_path, to_text, to_json):
    start_time = time.time()
    process = psutil.Process(os.getpid())
    cpu_usage = process.cpu_percent(0.0)
    
    if to_text:
        txt_path = pdf_to_text(pdf_path)
        print(f"Text file saved at: {txt_path}")
    
    if to_json:
        json_path = pdf_to_json(pdf_path)
        print(f"JSON file saved at: {json_path}")
    
    end_time = time.time()
    cpu_usage = process.cpu_percent(0.0)
    memory_info = process.memory_info()
    
    print(f"CPU usage: {cpu_usage}%")
    print(f"Memory usage: {memory_info.rss / (1024 * 1024):.2f} MB")
    print(f"Execution time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF to TXT and JSON formats.")
    parser.add_argument("pdf_path", type=str, help="The path to the PDF file.")
    parser.add_argument("--to_text", action="store_true", help="Convert PDF to TXT format.")
    parser.add_argument("--to_json", action="store_true", help="Convert PDF to JSON format.")
    args = parser.parse_args()
    
    if not args.to_text and not args.to_json:
        print("Error: At least one of --to_text or --to_json must be specified.")
        sys.exit(1)
    
    main(args.pdf_path, args.to_text, args.to_json)