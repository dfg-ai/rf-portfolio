# -*- coding: utf-8 -*-
import re, os

path = r'D:/Program Files/AnsysEM/附件5：2026年成都工业学院大学生射频微波电路设计竞赛评分细则.doc'

with open(path, 'rb') as f:
    data = f.read()

# Try to extract readable Chinese text from binary .doc
# .doc uses OLE compound document format
text = data.decode('utf-16-le', errors='ignore')
# Clean up
text = re.sub(r'[^一-鿿　-〿＀-￯a-zA-Z0-9\s\.\,\;\:\!\?\-\+\(\)\[\]\{\}\/\@\#\$\%\^\&\*\_\=\~\`\|\"\'\<\>\n\r]', '', text)
text = re.sub(r'\s+', ' ', text)
text = re.sub(r' +', ' ', text)

out = open(os.path.expanduser('~/Desktop/scoring_text.txt'), 'w', encoding='utf-8')
out.write(text[:10000])
out.close()
print('Done. Length:', len(text))
