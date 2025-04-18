import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []

        pos = 0
        for mo in re.finditer(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", old_node.text):
            url = mo.group(2)
            alt = mo.group(1)
            
            previous_text = old_node.text[pos:mo.start()]
            if previous_text != "":
                split_nodes.append(TextNode(previous_text, TextType.TEXT))
            split_nodes.append(TextNode(alt, TextType.IMAGE, url))
            pos = mo.end()
        last_text = old_node.text[pos:]
        if last_text != "":
            split_nodes.append(TextNode(last_text, TextType.TEXT))
        
        new_nodes.extend(split_nodes)
    return new_nodes
        

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []

        pos = 0
        for mo in re.finditer(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", old_node.text):
            url = mo.group(2)
            alt = mo.group(1)
            
            previous_text = old_node.text[pos:mo.start()]
            if previous_text != "":
                split_nodes.append(TextNode(previous_text, TextType.TEXT))
            split_nodes.append(TextNode(alt, TextType.LINK, url))
            pos = mo.end()
        last_text = old_node.text[pos:]
        if last_text != "":
            split_nodes.append(TextNode(last_text, TextType.TEXT))
        
        new_nodes.extend(split_nodes)
    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes