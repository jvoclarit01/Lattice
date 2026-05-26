import os
import re
import yaml

LATTICE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOMAINS_DIR = os.path.join(LATTICE_DIR, "domains")
OUTPUT_FILE = os.path.join(LATTICE_DIR, "cheatsheet.md")

print(f"Lattice Directory: {LATTICE_DIR}")
print(f"Domains Directory: {DOMAINS_DIR}")

def parse_skill_file(filepath):
    """
    Parses a single markdown skill file, extracting the name,
    description from YAML frontmatter, and the Iron Laws section.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Parse YAML Frontmatter
    frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    metadata = {}
    if frontmatter_match:
        try:
            metadata = yaml.safe_load(frontmatter_match.group(1))
        except Exception as e:
            print(f"Error parsing frontmatter in {filepath}: {e}")
            
    name = metadata.get("name", os.path.basename(filepath).replace(".md", ""))
    description = metadata.get("description", "").strip().replace("\n", " ")
    
    # 2. Extract Iron Laws Section
    iron_laws = []
    # Search for header e.g. ## Iron Laws (or case-insensitive variations)
    iron_laws_match = re.search(r"##\s*(?:Global\s*)?Iron\s*Laws.*?\n(.*?)(?=\n#|\Z)", content, re.DOTALL | re.IGNORECASE)
    if iron_laws_match:
        section_text = iron_laws_match.group(1).strip()
        # Extract individual bullet/numbered points
        for line in section_text.split("\n"):
            line = line.strip()
            if line.startswith("-") or line.startswith("*") or re.match(r"^\d+\.", line):
                # Clean up the bullet markers for the cheatsheet
                clean_line = re.sub(r"^[-*\d\.]+\s*", "", line).strip()
                if clean_line:
                    iron_laws.append(clean_line)
                    
    return {
        "name": name,
        "description": description,
        "iron_laws": iron_laws
    }

def main():
    domains = ["shared", "webdev", "ml", "thesis", "automation"]
    cheatsheet_content = []
    cheatsheet_content.append("# Lattice Micro-Heuristics Cheatsheet")
    cheatsheet_content.append("This is a compiled high-density index of the 66+ Lattice domain disciplines. Use this for global system prompt awareness and dynamic JIT skill loading.")
    cheatsheet_content.append("")
    
    total_skills = 0
    
    for domain in domains:
        domain_path = os.path.join(DOMAINS_DIR, domain)
        if not os.path.exists(domain_path):
            print(f"Warning: Domain path {domain_path} does not exist.")
            continue
            
        cheatsheet_content.append(f"## Domain: {domain.upper()}")
        cheatsheet_content.append("")
        
        # Sort files to ensure deterministic output
        files = sorted([f for f in os.listdir(domain_path) if f.endswith(".md")])
        for filename in files:
            filepath = os.path.join(domain_path, filename)
            try:
                parsed = parse_skill_file(filepath)
                total_skills += 1
                
                cheatsheet_content.append(f"### `{parsed['name']}`")
                cheatsheet_content.append(f"* **Description:** {parsed['description']}")
                
                if parsed["iron_laws"]:
                    cheatsheet_content.append("* **Iron Laws / Key Heuristics:**")
                    for idx, law in enumerate(parsed["iron_laws"], 1):
                        cheatsheet_content.append(f"  {idx}. {law}")
                else:
                    cheatsheet_content.append("* **Heuristics:** Enforce standard discipline for this domain.")
                cheatsheet_content.append("")
            except Exception as e:
                print(f"Error parsing file {filepath}: {e}")
                
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(cheatsheet_content))
        
    print(f"Successfully compiled {total_skills} skills into {OUTPUT_FILE}")
    
    # Inject Prompt Shadow Register into SKILL.md
    update_shadow_register(LATTICE_DIR)

def update_shadow_register(lattice_dir):
    """
    Parses the core protocols in the shared/ folder, compiles them into
    high-density micro-heuristics, and writes them into SKILL.md.
    """
    skill_file = os.path.join(lattice_dir, "SKILL.md")
    if not os.path.exists(skill_file):
        print(f"Warning: SKILL.md not found at {skill_file}")
        return

    shared_dir = os.path.join(lattice_dir, "shared")
    protocols = {
        "dpev-loop-protocol.md": "Core DPEV Loop",
        "verification-protocol.md": "Verification/Evidence",
        "unsure-protocol.md": "Unsure Protocol",
        "tombstone-template.md": "Failure Memory (Tombstone)"
    }
    
    register_lines = [""]
    
    for filename, title in protocols.items():
        filepath = os.path.join(shared_dir, filename)
        if not os.path.exists(filepath):
            print(f"Warning: Core protocol {filepath} not found.")
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract main rules/list items from content
        rules = []
        # Find lines starting with a list item, but clean them up
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("-") or line.startswith("*") or re.match(r"^\d+\.", line):
                clean_line = re.sub(r"^[-*\d\.]+\s*", "", line).strip()
                # Exclude examples or template blocks
                if clean_line and "example" not in clean_line.lower() and len(clean_line) > 10:
                    rules.append(clean_line)
                    
        # Limit to top 3 rules per protocol to keep it compact
        register_lines.append(f"### Core: {title}")
        for r in rules[:3]:
            register_lines.append(f"- {r}")
        register_lines.append("")
        
    with open(skill_file, 'r', encoding='utf-8') as f:
        skill_content = f.read()
        
    pattern = r"(<!-- SHADOW_REGISTER_START -->).*?(<!-- SHADOW_REGISTER_END -->)"
    replacement = f"\\1\\n" + "\\n".join(register_lines) + "\\n\\2"
    
    new_skill_content, count = re.subn(pattern, replacement, skill_content, flags=re.DOTALL)
    if count > 0:
        with open(skill_file, 'w', encoding='utf-8') as f:
            f.write(new_skill_content)
        print(f"Successfully injected prompt Shadow Register into {skill_file}")
    else:
        print(f"Warning: Shadow register markers not found in {skill_file}")

if __name__ == "__main__":
    main()
