import sys
from copystatic import generate_clean_static_copy
from page_generator import generate_pages_recursive

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print(f"Starting site generation pipeline with basepath: '{basepath}'")
    
    target_output_dir = "docs"
    generate_clean_static_copy("static", target_output_dir)
    
    generate_pages_recursive("content", "template.html", target_output_dir, basepath)
    
    print("Site generation complete!")

if __name__ == "__main__":
    main()