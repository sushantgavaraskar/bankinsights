import os

def dump_project_to_txt(root_dir, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            level = dirpath.replace(root_dir, "").count(os.sep)
            indent = "│   " * level
            f.write(f"{indent}├─ {os.path.basename(dirpath)}/\n")
            sub_indent = "│   " * (level + 1)
            for filename in filenames:
                f.write(f"{sub_indent}├─ {filename}\n")
                full_path = os.path.join(dirpath, filename)
                if filename.endswith((".py", ".env", ".txt", ".json")):
                    try:
                        with open(full_path, "r", encoding="utf-8") as code_file:
                            code = code_file.read()
                            f.write(f"\n{sub_indent}# --- Begin: {filename} ---\n")
                            f.write(code + "\n")
                            f.write(f"{sub_indent}# --- End: {filename} ---\n\n")
                    except Exception as e:
                        f.write(f"{sub_indent}[Could not read {filename}: {e}]\n")

dump_project_to_txt(".", "project_dump.txt")
