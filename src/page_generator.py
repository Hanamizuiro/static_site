import os
from block_markdown import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    if not os.path.exists(from_path):
        raise FileNotFoundError(f"Markdown content source file not found at: {from_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()
        
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"HTML template file not found at: {template_path}")
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()
        
    html_node = markdown_to_html_node(markdown_content)
    html_string = html_node.to_html()

    page_title = extract_title(markdown_content)
    
    # Replace layout templates placeholders
    final_html = template_content.replace("{{ Title }}", page_title)
    final_html = final_html.replace("{{ Content }}", html_string)
    
    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.read = f.write(final_html)
        
    print(f"Successfully generated: {dest_path}")
    
    import os
from block_markdown import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path} (Basepath: {basepath})")
    
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()
        
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()
        
    html_node = markdown_to_html_node(markdown_content)
    html_string = html_node.to_html()
    
    page_title = extract_title(markdown_content)
    
    final_html = template_content.replace("{{ Title }}", page_title)
    final_html = final_html.replace("{{ Content }}", html_string)
    
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')
    
    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)
        
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    if not os.path.exists(dir_path_content):
        raise ValueError(f"Content directory '{dir_path_content}' does not exist.")

    for item in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, item)
        
        if os.path.isfile(source_path):
            if item.endswith(".md"):
                relative_html_name = item.replace(".md", ".html")
                target_dest_path = os.path.join(dest_dir_path, relative_html_name)
                generate_page(source_path, template_path, target_dest_path, basepath)
        else:
            nested_dest_dir = os.path.join(dest_dir_path, item)
            os.makedirs(nested_dest_dir, exist_ok=True)
            generate_pages_recursive(source_path, template_path, nested_dest_dir, basepath)