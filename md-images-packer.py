import os
import re
import shutil
from zipfile import ZipFile
from tkinter import Tk, filedialog, messagebox

Tk().withdraw()

md_file = filedialog.askopenfilename(
    title="選擇要打包的 md 檔",
    filetypes=[("md 文件", "*.md")]
)

if not md_file:
    messagebox.showinfo("取消", "file not selected ")
    exit()

# Vault root dir
vault_path = os.path.dirname(os.path.abspath(md_file))

with open(md_file, 'r', encoding='utf-8') as f:
    content = f.read()

# （![[...]] 或 ![...](...)）
pattern = r'!\[\[([^\]]+)\]\]|!\[.*?\]\((.*?)\)'
matches = re.findall(pattern, content)

# pics loca
image_files = set()
for m in matches:
    img = m[0] if m[0] else m[1]
    img_path = os.path.join(vault_path, img)
    if os.path.exists(img_path):
        image_files.add(img_path)

if not image_files:
    messagebox.showwarning("warning", "圖片引用失敗")
    exit()

output_zip = os.path.join(
    os.path.dirname(md_file),
    os.path.splitext(os.path.basename(md_file))[0] + "_with_images.zip"
)

with ZipFile(output_zip, 'w') as zipf:
    # add md
    zipf.write(md_file, os.path.basename(md_file))
    # add pics
    for img_path in image_files:
        zipf.write(img_path, os.path.join("images", os.path.basename(img_path)))

messagebox.showinfo("完成", f"已打包到：\n{output_zip}")
