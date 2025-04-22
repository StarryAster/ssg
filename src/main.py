from textnode import *
import shutil

def copy_files(folder1, folder2):
    file_list = os.listdir(folder)
    for file in file_list:
        shutil.copy(folder1, f"{folder2}/{file}")
        print(f"copied {file} from {folder1} into {folder2}")
        if os.path.isdir(file) == True:
            copy_files(file, f"{folder2}/{file}")
    return

def fill_public():
    shutil.rmtree("public")
    os.mkdir("public")
    copy_files("static", "public")
    return


def main():
    a = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(a)
    fill_public()

main()