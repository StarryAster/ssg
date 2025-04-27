from textnode import *
from blocktype import *
import shutil
import os
import sys
from pathlib import Path

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file1:
        md_page = file1.read()
    with open(template_path) as file2:
        template = file2.read()
    html_page = markdown_to_html_node(md_page).to_html()
    final_page = template.replace("{{ Title }}", extract_title(md_page)).replace("{{ Content }}", html_page).replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    
    with open(dest_path, "w") as page:
        page.write(final_page)
    

def copy_files(folder1, folder2):
    file_list = os.listdir(folder1)
    for file in file_list:
        print(f"Copying {file} from {folder1} into {folder2}")
        if os.path.isdir(os.path.join(folder1, file)):
            os.mkdir(os.path.join(folder2, file))
            copy_files(os.path.join(folder1, file), os.path.join(folder2, file))
        else:
            shutil.copy(os.path.join(folder1, file), os.path.join(folder2, file))
    return

def fill_public():
    p = Path('.')
    # print(p.absolute())
    if os.path.exists(os.path.join(p,"docs")):
        shutil.rmtree(os.path.join(p,"docs"))
    os.mkdir(os.path.join(p,"docs"))
    copy_files(os.path.join(p,"static"), os.path.join(p,"docs"))
    return


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    content_list = os.listdir(dir_path_content)
    for item in content_list:
        if item.endswith(".md"):
            generate_page(os.path.join(dir_path_content, item), template_path, os.path.join(dest_dir_path, f"{item[:-3]}.html"), basepath)
        elif "." not in item:
            os.mkdir(os.path.join(dest_dir_path, item))
            generate_pages_recursive(os.path.join(dir_path_content, item), template_path, os.path.join(dest_dir_path, item), basepath)
    return

def main():
    if len(sys.argv) < 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    fill_public()
    generate_pages_recursive(os.path.join(Path('.'), "content"), os.path.join(Path('.'),"template.html"), os.path.join(Path('.'), "docs"), basepath)


main()