import random
from config import PROMPT_SIZES, TECH_MODULES

USER_STORY_GUIDELINES = """
STRICT RULES:
- Output must be a USER STORY, never a question
- Format: "As a [role], I want [action] so that [benefit]"
- Include 3-5 measurable Acceptance Criteria
- Complexity level: Medium to Difficult
- No Indian names for any people mentioned
- No official registered company names (use fictional names)
- Requirements must be unique every single call
- Include specific dataset field names in the story
"""

def build_prompt(sector_name, sector_display, entity, tech_module, char_limit):
    fields_str = ", ".join(entity["fields"])
    base = f"""You are an expert Infosys capstone project requirement generator.

SECTOR: {sector_display}
ENTITY: {entity['name']} (stored as {entity['format'].upper()} format)
ENTITY FIELDS: {fields_str}
TECHNOLOGY MODULE: {tech_module}
DATASET SIZE: 80,000 to 1,00,000 records

{USER_STORY_GUIDELINES}

Generate ONE complete, detailed user story for the {tech_module} module using the {entity['name']} entity from the {sector_display} sector.

The story must:
1. Reference real field names from: {fields_str}
2. Be actionable and testable
3. Include a business scenario with a fictional organisation name
4. Specify exact technical operations for {tech_module}
5. Include input/output scope
6. Be India-contextual in business setting
7. Any person names used must NOT be Indian names

Generate now:
"""
    padding_sentence = f" Additional context: The {sector_display} sector in India processes large-scale data through {tech_module} to drive operational efficiency and data-driven decisions across all {entity['name']} records."
    while len(base) < char_limit - 100:
        base += padding_sentence
    return base[:char_limit]

def build_all_prompts(sector_name, sector_data):
    prompts = []
    entities = sector_data["entities"]
    display  = sector_data["display"]
    for i, size in enumerate(PROMPT_SIZES):
        entity = entities[i % len(entities)]
        module = TECH_MODULES[i]
        prompt = build_prompt(sector_name, display, entity, module, size)
        prompts.append({
            "index":  i + 1,
            "module": module,
            "entity": entity["name"],
            "size":   len(prompt),
            "limit":  size,
            "text":   prompt
        })
        print(f"  Built prompt {i+1}/8 — {module} — {len(prompt):,} chars")
    return prompts
if __name__ == "__main__":
    print("Prompt Builder Running ✅")