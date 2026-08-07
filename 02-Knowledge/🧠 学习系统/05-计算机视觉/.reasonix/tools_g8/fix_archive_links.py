import os, sys, re
sys.stdout.reconfigure(encoding='utf-8')
KB = "F:" + os.sep + "-"
CV = "02-Knowledge/🧠 学习系统/05-计算机视觉"
files = [CV + "/02-深度学习内核/AlexNet.md", CV + "/02-深度学习内核/GoogLeNet.md", CV + "/02-深度学习内核/VGGNet.md"]
repl = {
    CV + "/.归档/空壳文件/AlexNet": CV + "/02-深度学习内核/AlexNet",
    CV + "/.归档/空壳文件/VGGNet": CV + "/02-深度学习内核/VGGNet",
    CV + "/.归档/空壳文件/GoogLeNet": CV + "/02-深度学习内核/GoogLeNet",
    CV + "/.归档/空壳文件/LeNet": None,
}
for rel in files:
    p = os.path.join(KB, rel)
    with open(p, encoding='utf-8') as f:
        content = f.read()
    new = content
    for target, repl_target in repl.items():
        pat = re.compile(r'\[\[' + re.escape(target) + r'(\|[^\]]*)?\]\]')
        for m in pat.finditer(new):
            if repl_target is None:
                alias = m.group(1)
                text = alias[1:] if alias else "LeNet"
                new = new.replace(m.group(0), text)
            else:
                alias = m.group(1)
                if alias:
                    new = new.replace(m.group(0), '[[' + repl_target + '|' + alias[1:] + ']]')
                else:
                    new = new.replace(m.group(0), '[[' + repl_target + ']]')
    with open(p, 'w', encoding='utf-8') as f:
        f.write(new)
    print(rel, "剩余归档引用:", len(re.findall(r'\.归档/空壳文件', new)))
print("处理完成")
