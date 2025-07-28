import os
import json
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar

def extract_outline(pdf_path):
    outline = []
    title = ""
    fonts_seen = {}

    for page_num, page_layout in enumerate(extract_pages(pdf_path), start=1):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    line_text = text_line.get_text().strip()
                    if not line_text:
                        continue

                    font_sizes = [char.size for char in text_line if isinstance(char, LTChar)]
                    if not font_sizes:
                        continue

                    avg_font_size = sum(font_sizes) / len(font_sizes)
                    rounded_font = round(avg_font_size)

                    fonts_seen.setdefault(rounded_font, 0)
                    fonts_seen[rounded_font] += 1

                    if rounded_font >= 20 and not title:
                        title = line_text
                    elif rounded_font >= 16:
                        outline.append({"level": "H1", "text": line_text, "page": page_num})
                    elif 13 <= rounded_font < 16:
                        outline.append({"level": "H2", "text": line_text, "page": page_num})
                    elif 11 <= rounded_font < 13:
                        outline.append({"level": "H3", "text": line_text, "page": page_num})

    return {
        "title": title if title else "Untitled Document",
        "outline": outline
    }

def process_all_pdfs(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))
            print(f"Processing: {filename}")
            result = extract_outline(input_path)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)

if __name__ == "__main__":
    process_all_pdfs("/app/input", "/app/output")
