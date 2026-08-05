import os

FILES_TO_FIX = [
    r"f:\-\03-Projects\机器学习与AI应用\05-计算机视觉\项目-CIFAR10.md",
    r"f:\-\03-Projects\机器学习与AI应用\05-计算机视觉\项目-CNN可视化.md",
    r"f:\-\03-Projects\机器学习与AI应用\05-计算机视觉\项目-HDR.md",
    r"f:\-\03-Projects\机器学习与AI应用\05-计算机视觉\项目-Panorama.md",
    r"f:\-\03-Projects\机器学习与AI应用\05-计算机视觉\项目-医学分割.md",
    r"f:\-\03-Projects\机器学习与AI应用\05-计算机视觉\项目-图像搜索.md",
    r"f:\-\03-Projects\机器学习与AI应用\05-计算机视觉\项目-姿态估计.md",
    r"f:\-\03-Projects\机器学习与AI应用\05-计算机视觉\项目-自定义检测.md",
    r"f:\-\03-Projects\机器学习与AI应用\05-计算机视觉\项目-风格迁移.md"
]

def fix_nine():
    for path in FILES_TO_FIX:
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8-sig") as f:
            content = f.read()

        if content.startswith("---type:"):
            content = "---\ntype:" + content[8:]

        # Add flow, kind, track if missing
        lines = content.splitlines()
        new_lines = []
        in_fm = False
        fm_added = False

        for i, line in enumerate(lines):
            if i == 0 and line.startswith("---"):
                new_lines.append("---")
                in_fm = True
                continue
            if in_fm and line.startswith("---"):
                if not fm_added:
                    new_lines.append('flow: project')
                    new_lines.append('kind: project')
                    new_lines.append('track: "机器学习与AI应用"')
                    fm_added = True
                new_lines.append("---")
                in_fm = False
                continue
            new_lines.append(line)

        new_content = "\n".join(new_lines)
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)

    print("Fixed 9 CV project files.")

if __name__ == "__main__":
    fix_nine()
