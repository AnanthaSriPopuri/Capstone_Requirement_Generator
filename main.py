#import anthropic
import random
import json
import os
from datetime import datetime

#from config import ANTHROPIC_API_KEY
from sectors.sector_registry import SECTORS, get_random_sector
from datasets.generator import generate_dataset, save_dataset
from datasets.injector import inject_inconsistencies
from prompts.prompt_builder import build_all_prompts
from output.word_generator import generate_word_doc
from output.agile_sheet import update_agile_sheet

#client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def call_llm(prompt_text, prompt_index):
    print(f"    Calling Claude API for prompt {prompt_index} ...")
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt_text}]
    )
    return response.content[0].text

def run_single_project(sector_name=None):
    if not sector_name:
        sector_name = get_random_sector()

    sector_data = SECTORS[sector_name]
    print(f"\n{'='*60}")
    print(f"  GENERATING PROJECT: {sector_data['display'].upper()}")
    print(f"{'='*60}")

    # Step A: Build all 8 prompts
    print("\n[1/4] Building prompts ...")
    prompts = build_all_prompts(sector_name, sector_data)

    # Step B: Call LLM for each prompt
    print("\n[2/4] Calling Claude API for all 8 prompts ...")
    stories = []
    for p in prompts:
        story = call_llm(p["text"], p["index"])
        stories.append({
            "index":  p["index"],
            "module": p["module"],
            "entity": p["entity"],
            "story":  story
        })
        print(f"    Got story {p['index']}: {len(story)} chars")

    # Step C: Generate & save datasets
    print("\n[3/4] Generating datasets ...")
    datasets_info = []
    for entity in sector_data["entities"]:
        df = generate_dataset(entity, rows=90000)
        df, issues = inject_inconsistencies(df, count=17)
        fp = save_dataset(df, entity, sector_name)
        datasets_info.append({"entity": entity["name"], "format": entity["format"], "path": fp, "rows": len(df), "issues": issues})

    # Step D: Generate Word document
    print("\n[4/4] Generating Word document ...")
    doc_path = f"output/{sector_name}_capstone.docx"
    generate_word_doc(sector_name, sector_data, stories, datasets_info, doc_path)

    # Update AGILE sheet
    update_agile_sheet("output/agile_tracker.xlsx", f"Generate {sector_data['display']} project", "Done", f"8 stories, {len(datasets_info)} datasets")

    print(f"\n  Project complete: {doc_path}")
    return doc_path

def run_all_five_projects():
    sector_names = random.sample(list(SECTORS.keys()), 5)
    print(f"Selected 5 sectors: {sector_names}")
    results = []
    for sn in sector_names:
        path = run_single_project(sn)
        results.append(path)
    print(f"\n\nAll 5 projects generated:")
    for r in results:
        print(f"  {r}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "all":
        run_all_five_projects()
    else:
        # Run one random sector
        run_single_project()