import os
import json

AGENTS = "agents"
COMMANDS = "commands"
SKILLS = "skills"

# AGENTS.md保存先
CLAUDE_AGENTS_MD = os.path.join(os.getcwd(), "CLAUDE.md")
COPILOT_AGENTS_MD = os.path.join(os.getcwd(), ".github", "copilot-instructions.md")
GEMINI_AGENTS_MD = os.path.join(os.getcwd(), "GEMINI.md")

###############################################################
#
#                 ディレクトリが無ければ作成
#
###############################################################
# Claude用ディレクトリ作成
if not os.path.exists(".claude/agents"):
    os.makedirs(".claude/agents")
if not os.path.exists(".claude/commands"):
    os.makedirs(".claude/commands")

# Copilot用ディレクトリ作成
if not os.path.exists(".github/agents"):
    os.makedirs(".github/agents")
if not os.path.exists(".github/prompts"):
    os.makedirs(".github/prompts")

# Gemini用ディレクトリ作成
if not os.path.exists(".gemini/commands"):
    os.makedirs(".gemini/commands")

###############################################################
#
#                 コピー用関数
#
###############################################################
# Claude用コピー
def copy_to_claude(filepath, type, header):
    try:
        if type == AGENTS:
            src = os.path.join(".ai", "agents", filepath)
            dst = os.path.join(".claude", "agents", filepath)
            with open(src, "r", encoding="utf-8") as f:
                content = f.read()
            with open(dst, "w", encoding="utf-8") as f:
                f.write("---\n")
                f.write(f"name: {header['name']}\n")
                f.write(f"description: {header['description']}\n")
                if "tools" in header:
                    f.write(f"tools: {header['tools']}\n")
                f.write(f"model: {header['model']}\n")
                if "color" in header:
                    f.write(f"color: {header['color']}\n")
                f.write("---\n\n")
                f.write(content)
        elif type == COMMANDS:
            fpath = filepath.split("/")
            src = os.path.join(".ai", "commands", *fpath)
            dst = os.path.join(".claude", "commands", *fpath)
            with open(src, "r", encoding="utf-8") as f:
                content = f.read()
            if not os.path.exists(os.path.dirname(dst)):
                os.makedirs(os.path.dirname(dst))
            with open(dst, "w", encoding="utf-8") as f:
                f.write(content)
    except Exception as e:
        print(f"Error copying to Claude: {e}")

# Copilot用コピー
def copy_to_copilot(filepath, type, header):
    try:
        if type == AGENTS:
            src = os.path.join(".ai", "agents", filepath)
            dst = os.path.join(".github", "agents", filepath.replace(".md", ".agent.md"))
            with open(src, "r", encoding="utf-8") as f:
                content = f.read()
            with open(dst, "w", encoding="utf-8") as f:
                f.write("---\n")
                f.write(f"name: {header['name']}\n")
                f.write(f"description: {header['description']}\n")
                f.write("---\n\n")
                f.write(content)
        elif type == COMMANDS:
            fpath = filepath.split("/")
            src = os.path.join(".ai", "commands", *fpath)
            dst = os.path.join(".github", "prompts", filepath.replace("/", "__").replace(".md", ".prompt.md"))
            with open(src, "r", encoding="utf-8") as f:
                content = f.read()
            if not os.path.exists(os.path.dirname(dst)):
                os.makedirs(os.path.dirname(dst))
            with open(dst, "w", encoding="utf-8") as f:
                f.write("---\n")
                f.write(f"agent: '{header['agent']}'\n")
                f.write(f"description: '{header['description']}'\n")
                f.write("---\n\n")
                f.write(content)
    except Exception as e:
        print(f"Error copying to Copilot: {e}")

# Gemini用コピー
def copy_to_gemini(filepath, type, header):
    try:
        if type == COMMANDS:
            fpath = filepath.split("/")
            src = os.path.join(".ai", "commands", *fpath)
            dst = os.path.join(".gemini", "commands", *fpath).replace(".md", ".toml")
            with open(src, "r", encoding="utf-8") as f:
                content = f.read()
            if not os.path.exists(os.path.dirname(dst)):
                os.makedirs(os.path.dirname(dst))
            with open(dst, "w", encoding="utf-8") as f:
                f.write(f"description = \"{header['description']}\"\n\n")
                f.write(f"prompt = \"\"\"\n")
                f.write(content)
                f.write("\"\"\"\n")
    except Exception as e:
        print(f"Error copying to Gemini: {e}")

###############################################################
#
#                     main処理
#
#################################################################

# AGENTS.mdのコピー
with open(os.path.join(".ai", "AGENTS.md"), "r", encoding="utf-8") as f:
    content = f.read()

with open(CLAUDE_AGENTS_MD, "w", encoding="utf-8") as f:
    f.write(content)
with open(GEMINI_AGENTS_MD, "w", encoding="utf-8") as f:
    f.write(content)
with open(COPILOT_AGENTS_MD, "w", encoding="utf-8") as f:
    f.write(content)


# その他ファイルコピー
with open(os.path.join(".ai", "copy-info.json"), "r", encoding="utf-8") as f:
    copy_info = json.load(f)
model = copy_info["model"]

for tp, data in copy_info.items():
    if tp in ["agents", "commands", "skills"]:
        for filename, model in data.items():
            if "claude" in model:
                copy_to_claude(filename, tp, model["claude"].get("header", {}))
            if "copilot" in model:
                copy_to_copilot(filename, tp, model["claude"].get("header", {}))
            if "gemini" in model:
                copy_to_gemini(filename, tp, model["claude"].get("header", {}))
            print(f"Copied {tp}: {filename}")



