from textnode import TextNode, TextType
import re

def text_to_textnodes(text: str) -> list[TextNode]:
    # Start with a single raw text node containing the entire string
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Order matters slightly; handle bold and italic delimiters first
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    # Then isolate dynamic markdown tag structures like images and links
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        original_text = node.text
        images = extract_markdown_images(original_text)
        
        if len(images) == 0:
            new_nodes.append(node)
            continue
            
        for image in images:
            image_alt, image_url = image
            sections = original_text.split(f"![{image_alt}]({image_url})", 1)
            
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
                
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            original_text = sections[1]
            
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
            
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.type != TextType.TEXT:
            new_nodes.append(node)
            continue
            
        original_text = node.text
        links = extract_markdown_links(original_text)
        
        if len(links) == 0:
            new_nodes.append(node)
            continue
            
        for link in links:
            link_text, link_url = link
            sections = original_text.split(f"[{link_text}]({link_url})", 1)
            
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
                
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            original_text = sections[1]
            
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
            
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    # Regex breakdown:
    # !\[      -> matches the literal exclamation mark and opening bracket
    # ([^\[\]]*) -> Capture Group 1 (Alt Text): matches anything that isn't a bracket
    # \]       -> matches the literal closing bracket
    # \(       -> matches the literal opening parenthesis
    # ([^\(\)]*) -> Capture Group 2 (URL): matches anything that isn't a parenthesis
    # \)       -> matches the literal closing parenthesis
    pattern = r"!\[([^\[\]]*)\]\(([^(\)]*)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    # This regex is identical to the image one, minus the leading exclamation mark (!)
    # Note: Using a negative lookbehind (?<!!) ensures we don't accidentally match images
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^(\)]*)\)"
    return re.findall(pattern, text)

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    
    for node in old_nodes:
        if node.type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0:
            raise ValueError(f"Invalid Markdown syntax: matching closing delimiter '{delimiter}' not found.")
            
        parts = node.text.split(delimiter)
        split_nodes = []
        
        for i, part in enumerate(parts):
            if part == "":
                continue
                
            if i % 2 == 0:
                split_nodes.append(TextNode(part, TextType.TEXT))
            else:
                split_nodes.append(TextNode(part, text_type))
                
        new_nodes.extend(split_nodes)
        
    return new_nodes