import os

PROJECTS_ROOT = r"f:\-\03-Projects"

def fix_concatenated_frontmatter():
    fixed = 0
    for root, dirs, files in os.walk(PROJECTS_ROOT):
        for f in files:
            if f.endswith(".md"):
                abs_path = os.path.join(root, f)
                with open(abs_path, "r", encoding="utf-8") as file_in:
                    content = file_in.read()

                if content.startswith("---type:"):
                    content = "---\ntype:" + content[8:]
                    with open(abs_path, "w", encoding="utf-8") as file_out:
                        file_out.write(content)
                    fixed += 1

    print(f"Fixed {fixed} files with concatenated ---type: frontmatter.")

if __name__ == "__main__":
    fix_concatenated_frontmatter()
