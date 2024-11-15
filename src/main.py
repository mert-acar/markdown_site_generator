import os
import shutil

from process import extract_title, markdown_to_blocks, markdown_to_html_node


def copy_directory(src, dest):
  if not os.path.exists(src):
    print(f"Source directory '{src}' does not exist.")
    return

  if os.path.exists(dest):
    shutil.rmtree(dest)
  os.makedirs(dest)

  for item in os.listdir(src):
    src_path = os.path.join(src, item)
    dest_path = os.path.join(dest, item)

    if os.path.isdir(src_path):
      copy_directory(src_path, dest_path)
    else:
      shutil.copy(src_path, dest_path)


def generate_page(from_path: str, template_path: str, dest_path: str):
  print(f"Generating from {from_path} to {dest_path} using {template_path}...")

  with open(from_path, "r") as f:
    markdown = f.read()

  with open(template_path, "r") as f:
    template = f.read()

  html = markdown_to_html_node(markdown).to_html()
  title = extract_title(markdown)
  template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
  with open(dest_path, "w") as f:
    f.write(template)


def generate_pages_recursive(content_dir_path: str, template_path: str, dest_dir_path: str):
  print(f"Generating from {content_dir_path} to {dest_dir_path} using {template_path}...")
  with open(template_path, "r") as f:
    template = f.read()

  for root, _, files in os.walk(content_dir_path):
    relative_path = os.path.relpath(root, content_dir_path)
    dest_dir = os.path.join(dest_dir_path, relative_path)

    os.makedirs(dest_dir, exist_ok=True)

    for file_name in files:
      content_file_path = os.path.join(root, file_name)
      dest_file_path = os.path.join(dest_dir, file_name.replace(".md", ".html"))

      with open(content_file_path, 'r') as f:
        content = f.read()

      html = markdown_to_html_node(content).to_html()
      title = extract_title(content)
      processed_content = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

      # Save the processed content to the destination file
      with open(dest_file_path, 'w', encoding='utf-8') as f:
        f.write(processed_content)


def main():
  copy_directory("./static", "./public")
  generate_pages_recursive("content/", "template.html", "public/")


if __name__ == "__main__":
  main()
