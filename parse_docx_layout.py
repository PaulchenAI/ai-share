import zipfile
import xml.etree.ElementTree as ET

def parse_docx_layout(docx_path, output_path):
    w_ns = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    r_ns = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
    
    with zipfile.ZipFile(docx_path) as docx:
        # Load relationships
        rels_xml = docx.read('word/_rels/document.xml.rels')
        rels_tree = ET.fromstring(rels_xml)
        rid_to_target = {}
        for rel in rels_tree.findall('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship'):
            rid = rel.get('Id')
            target = rel.get('Target')
            rid_to_target[rid] = target
        
        # Load main document xml
        doc_xml = docx.read('word/document.xml')
        doc_tree = ET.fromstring(doc_xml)
        
        body = doc_tree.find(w_ns + 'body')
        
        element_idx = 0
        with open(output_path, 'w', encoding='utf-8') as f:
            for p in body.iter(w_ns + 'p'):
                # Extract text
                text_parts = []
                for t in p.iter(w_ns + 't'):
                    if t.text:
                        text_parts.append(t.text)
                text = ''.join(text_parts).strip()
                
                # Find images
                images = []
                for drawing in p.iter(w_ns + 'drawing'):
                    for blip in drawing.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}blip'):
                        embed_id = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                        if embed_id in rid_to_target:
                            images.append(rid_to_target[embed_id])
                
                if text or images:
                    f.write(f"[{element_idx}] TEXT: {text}\n")
                    for img in images:
                        f.write(f"    IMAGE REF: {img}\n")
                    element_idx += 1

if __name__ == '__main__':
    parse_docx_layout('【Ai分享】- 5.25.docx', 'docx_layout_mapping.txt')
    print("Done generating mapping.")
