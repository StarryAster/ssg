from enum import Enum
from htmlnode import *
from md_to_tn import *
from textnode import *

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        nb_unit = block.strip()
        if nb_unit != "":
            new_blocks.append(nb_unit)
    return new_blocks



class BlockType(Enum):
    PG = "paragraph"
    HN = "heading"
    BQ = "blockquote"
    CODE = "code"
    UL = "unordered_list"
    OL = "ordered_list"


class BlockNode:
    def __init__(self, text, block_type):
        self.text = text
        self.block_type = block_type

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.block_type == other.block_type
        )
    
    def __repr__(self):
        return f"BlockNode({self.text}, {self.block_type.value})"

def block_to_block_type(markdown):
    if markdown != markdown.lstrip("# "):
        return BlockType.HN
    elif markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE
    elif markdown.startswith(">"):
        return BlockType.BQ
    elif markdown.startswith("- "):
        return BlockType.UL
    elif markdown.startswith("1. "):
        list_list = markdown.split("\n")
        i = 1
        for listed in list_list:
            if listed.startswith(f"{i}. ") == False:
                return BlockType.PG
            i += 1
        return BlockType.OL
    else:
        return BlockType.PG
                

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PG:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HN:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OL:
        return olist_to_html_node(block)
    if block_type == BlockType.UL:
        return ulist_to_html_node(block)
    if block_type == BlockType.BQ:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)