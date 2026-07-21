# -*- coding: utf-8 -*-
import zipfile, re, os

base = r'D:/Program Files/AnsysEM'
files = [
    '附件1：2026年成都工业学院大学生射频微波电路设计竞赛题目.docx',
    '附件5：2026年成都工业学院大学生射频微波电路设计竞赛评分细则.doc'
]

out = open(os.path.expanduser('~/Desktop/competition_text.txt'), 'w', encoding='utf-8')

for fname in files:
    path = base + '/' + fname
    out.write('='*60 + '\n')
    out.write(fname + '\n')
    out.write('='*60 + '\n')
    try:
        z = zipfile.ZipFile(path)
        xml = z.read('word/document.xml').decode('utf-8')
        text = re.sub(r'<[^>]+>', ' ', xml)
        text = re.sub(r'\s+', ' ', text).strip()
        out.write(text[:10000])
    except:
        with open(path, 'rb') as f:
            data = f.read()
        # Try to extract readable text
        text = data.decode('utf-8', errors='ignore')
        out.write(text[:10000])
    out.write('\n\n')

out.close()
print('Done. See ~/Desktop/competition_text.txt')
