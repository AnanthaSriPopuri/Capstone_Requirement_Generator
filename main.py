import anthropic
import random
import json
import os
import sys
import argparse
from datetime import datetime

from config import ANTHROPIC_API_KEY
from sectors.sector_registry import SECTORS, get_random_sector
from datasets.generator import generate_dataset, save_dataset
from datasets.injector import inject_inconsistencies
from prompts.prompt_builder import build_all_prompts
from output.word_generator import generate_word_doc
from output.agile_sheet import update_agile_sheet

# ── Anthropic client ──────────────────────────────────────────────────────────
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def call_llm(prompt_text, prompt_index):
    """Call Claude API. Falls back to placeholder if API key missing or call fails."""
    try:
        print(f"    Calling Claude API for prompt {prompt_index}/8 ...")
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt_text}]
        )
        return response.content[0].text
    except Exception as e:
        print(f"    WARNING: API call {prompt_index} failed — {e}")
        return (
            f"USER STORY ID   : US-{prompt_index:02d}\n"
            f"User Story      : As a data engineer, I want to process the entity dataset "
            f"using this technology module so that analytical insights are generated.\n"
            f"Acceptance Criteria:\n"
            f"  AC1: Operation completes without errors on 90 000-row dataset\n"
            f"  AC2: Output is validated and saved correctly\n"
            f"Solution        : [Set ANTHROPIC_API_KEY to generate a real solution]\n"
        )


def run_single_project(sector_name=None, use_llm=True):
    if not sector_name:
        sector_name = get_random_sector()

    sector_data = SECTORS[sector_name]
    print(f"\n{'='*60}")
    print(f"  SECTOR : {sector_data['display'].upper()}")
    print(f"  STARTED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")

    # Step 1 — Build 8 prompts
    print("\n[1/4] Building prompts ...")
    prompts = build_all_prompts(sector_name, sector_data)

    # Step 2 — Call LLM for each prompt
    print("\n[2/4] Calling Claude API ...")
    stories = []
    for p in prompts:
        story = call_llm(p["text"], p["index"]) if use_llm else (
            f"[Placeholder story {p['index']} for {p['module']} — run without --no-llm for real stories]"
        )
        stories.append({
            "index":  p["index"],
            "module": p["module"],
            "entity": p["entity"],
            "story":  story,
        })
        print(f"    Story {p['index']}: {len(story)} chars")

    # Step 3 — Generate datasets
    print("\n[3/4] Generating datasets ...")
    datasets_info = []
    for entity in sector_data["entities"]:
        df = generate_dataset(entity, rows=90000)
        df, issues = inject_inconsistencies(df, count=17)
        fp = save_dataset(df, entity, sector_name)
        datasets_info.append({
            "entity":  entity["name"],
            "format":  entity["format"],
            "path":    fp,
            "rows":    len(df),
            "issues":  issues,
        })

    # Step 4 — Generate Word document
    print("\n[4/4] Generating Word document ...")
    os.makedirs("output", exist_ok=True)
    doc_path = f"output/{sector_name}_capstone.docx"
    generate_word_doc(sector_name, sector_data, stories, datasets_info, doc_path)

    # Update AGILE sheet
    update_agile_sheet(
        "output/agile_tracker.xlsx",
        f"Generate {sector_data['display']} project",
        "Done",
        f"8 stories, {len(datasets_info)} datasets",
    )

    print(f"\n  Project complete: {doc_path}")
    return doc_path


def run_all_five_projects(use_llm=True):
    sector_names = random.sample(list(SECTORS.keys()), 5)
    print(f"Selected 5 sectors: {sector_names}")
    results = []
    for sn in sector_names:
        path = run_single_project(sn, use_llm=use_llm)
        results.append(path)
    print("\nAll 5 projects generated:")
    for r in results:
        print(f"  {r}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capstone Requirement Generator")
    parser.add_argument("--all",    action="store_true", help="Generate 5 projects")
    parser.add_argument("--sector", type=str,            help="Specific sector name")
    parser.add_argument("--no-llm", action="store_true", help="Skip Claude API (use placeholders)")
    args = parser.parse_args()

    use_llm = not args.no_llm
    if not ANTHROPIC_API_KEY and use_llm:
        print("WARNING: ANTHROPIC_API_KEY not set. Using placeholder stories.")
        print("To use real AI stories: export ANTHROPIC_API_KEY='sk-ant-...'")
        use_llm = False

    if args.all:
        run_all_five_projects(use_llm=use_llm)
    else:
        run_single_project(sector_name=args.sector, use_llm=use_llm)