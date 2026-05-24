import zipfile
import xml.etree.ElementTree as ET
import os

def extract_docx_text(docx_path, out_path):
    WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    PARA = WORD_NAMESPACE + 'p'
    TEXT = WORD_NAMESPACE + 't'
    
    with zipfile.ZipFile(docx_path) as docx:
        tree = ET.parse(docx.open('word/document.xml'))
        root = tree.getroot()
        paragraphs = []
        for paragraph in root.iter(PARA):
            texts = [node.text for node in paragraph.iter(TEXT) if node.text]
            if texts:
                paragraphs.append(''.join(texts))
            else:
                # Add empty line for paragraph spacing if it's empty
                paragraphs.append('')
        
        with open(out_path, 'w', encoding='utf-8') as f:
            for p in paragraphs:
                f.write(p + '\n')

if __name__ == '__main__':
    extract_docx_text('【Ai分享】- 5.25.docx', 'docx_content.txt')
    print("Done extracting docx content.")
