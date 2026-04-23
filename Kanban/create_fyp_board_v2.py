#!/usr/bin/env python3
"""
FYP GitHub Project Board Creator v2 — with Milestones
Creates 4 milestones (Week 1, Week 2, Week 3, Ongoing) with due dates,
then creates all 25 issues assigned to the correct milestone.

Usage:
  1. Paste your GitHub token below
  2. Run: python3 create_fyp_board_v2.py
"""

import requests
import json
import os
import time

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
TOKEN  = "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"
OWNER  = "BAK23592238"
REPO   = "VOLog"

token = os.environ.get("GITHUB_TOKEN", TOKEN)
HEADERS = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}
REST_URL = f"https://api.github.com/repos/{OWNER}/{REPO}"

# ─────────────────────────────────────────────
# MILESTONES
# ─────────────────────────────────────────────
MILESTONES = [
    {"title": "Week 1 — Dataset & core implementation", "due": "2025-04-17T23:59:59Z", "description": "Days 1–7: Get dataset ready and core YOLO/ALPR pipeline running"},
    {"title": "Week 2 — Integration & writing",         "due": "2025-04-24T23:59:59Z", "description": "Days 8–14: Integrate pipeline, build dashboard, write report sections"},
    {"title": "Week 3 — Testing, evaluation & final report", "due": "2025-05-01T23:59:59Z", "description": "Days 15–21: Evaluate, write up, proofread and submit"},
    {"title": "Ongoing throughout",                     "due": "2025-05-01T23:59:59Z", "description": "Tasks that run across all 21 days"},
]

# ─────────────────────────────────────────────
# TASKS
# ─────────────────────────────────────────────
TASKS = [
    # Week 1
    {"title": "Finish labelling dataset (target: ~300-400 usable images)",             "milestone": "Week 1 — Dataset & core implementation", "label": "do"},
    {"title": "Finalise dataset split: train / val / test (80/10/10)",                 "milestone": "Week 1 — Dataset & core implementation", "label": "do"},
    {"title": "Set up YOLOv8 training on Colab/Kaggle with labelled data",             "milestone": "Week 1 — Dataset & core implementation", "label": "do"},
    {"title": "Run first training run — note baseline mAP, loss curves",               "milestone": "Week 1 — Dataset & core implementation", "label": "do"},
    {"title": "Implement ALPR module (use pre-trained model, test on UK plates)",      "milestone": "Week 1 — Dataset & core implementation", "label": "do"},
    {"title": "Supervisor meeting — show progress, get sign-off on dataset",           "milestone": "Week 1 — Dataset & core implementation", "label": "ongoing"},
    {"title": "Update GitHub with all commits from this week",                         "milestone": "Week 1 — Dataset & core implementation", "label": "ongoing"},

    # Week 2
    {"title": "Integrate occupancy model + ALPR into a single pipeline",               "milestone": "Week 2 — Integration & writing", "label": "do"},
    {"title": "Build basic React dashboard (entry log table, gate filter, timestamp)", "milestone": "Week 2 — Integration & writing", "label": "do"},
    {"title": "Write Tools & Methods section (rationale for YOLO, Colab, React, datasets)", "milestone": "Week 2 — Integration & writing", "label": "write"},
    {"title": "Write Requirements / Specifications section (user stories, use case diagram, wireframes)", "milestone": "Week 2 — Integration & writing", "label": "write"},
    {"title": "Write Solution Design section (system architecture diagram, data flow)", "milestone": "Week 2 — Integration & writing", "label": "write"},
    {"title": "Supervisor meeting — demo pipeline, get feedback on report sections",   "milestone": "Week 2 — Integration & writing", "label": "ongoing"},

    # Week 3
    {"title": "Run evaluation: mAP, precision/recall on test set, confusion matrix",   "milestone": "Week 3 — Testing, evaluation & final report", "label": "do"},
    {"title": "Conduct usability / think-aloud test of dashboard with 1-2 users",     "milestone": "Week 3 — Testing, evaluation & final report", "label": "do"},
    {"title": "Write Solution Implementation section (sprint-by-sprint, key challenges)", "milestone": "Week 3 — Testing, evaluation & final report", "label": "write"},
    {"title": "Write Testing & Evaluation section (metrics, usability findings)",      "milestone": "Week 3 — Testing, evaluation & final report", "label": "write"},
    {"title": "Write Discussion and Conclusion sections",                              "milestone": "Week 3 — Testing, evaluation & final report", "label": "write"},
    {"title": "Write Abstract (after everything else is done, max 300 words)",         "milestone": "Week 3 — Testing, evaluation & final report", "label": "write"},
    {"title": "Check word count — must be under 8,000 words",                         "milestone": "Week 3 — Testing, evaluation & final report", "label": "write"},
    {"title": "Final proofread: third-person voice, figures captioned, IEEE references", "milestone": "Week 3 — Testing, evaluation & final report", "label": "write"},
    {"title": "Submit to Turnitin / final submission portal",                          "milestone": "Week 3 — Testing, evaluation & final report", "label": "submit"},

    # Ongoing
    {"title": "Keep GitHub commits descriptive (used as evidence in report)",          "milestone": "Ongoing throughout", "label": "ongoing"},
    {"title": "Log all supervisor meetings (required as appendix evidence)",           "milestone": "Ongoing throughout", "label": "ongoing"},
    {"title": "Update project management tool screenshots",                            "milestone": "Ongoing throughout", "label": "ongoing"},
]

LABEL_COLORS = {
    "do":      "0075ca",
    "write":   "e4b429",
    "ongoing": "5319e7",
    "submit":  "0e8a16",
}

def rest(method, path, payload=None):
    url = f"{REST_URL}/{path}"
    resp = getattr(requests, method)(url, headers=HEADERS, json=payload)
    resp.raise_for_status()
    return resp.json()

# ─────────────────────────────────────────────
# STEP 1 — Labels
# ─────────────────────────────────────────────
def ensure_labels():
    print("📌 Setting up labels...")
    existing = {l["name"] for l in rest("get", "labels")}
    for name, color in LABEL_COLORS.items():
        if name not in existing:
            rest("post", "labels", {"name": name, "color": color})
            print(f"  ✅ Created: {name}")
        else:
            print(f"  — Exists:  {name}")

# ─────────────────────────────────────────────
# STEP 2 — Milestones
# ─────────────────────────────────────────────
def create_milestones():
    print("\n🏁 Creating milestones...")
    existing = {m["title"]: m["number"] for m in rest("get", "milestones?state=all")}
    milestone_map = {}
    for m in MILESTONES:
        if m["title"] in existing:
            milestone_map[m["title"]] = existing[m["title"]]
            print(f"  — Exists:  {m['title']}")
        else:
            result = rest("post", "milestones", {
                "title": m["title"],
                "due_on": m["due"],
                "description": m["description"]
            })
            milestone_map[m["title"]] = result["number"]
            print(f"  ✅ Created: {m['title']} (due {m['due'][:10]})")
    return milestone_map

# ─────────────────────────────────────────────
# STEP 3 — Issues
# ─────────────────────────────────────────────
def create_issues(milestone_map):
    print(f"\n📝 Creating {len(TASKS)} issues...")
    for task in TASKS:
        issue = rest("post", "issues", {
            "title": task["title"],
            "labels": [task["label"]],
            "milestone": milestone_map[task["milestone"]],
        })
        print(f"  ✅ #{issue['number']} — {task['title'][:65]}")
        time.sleep(0.3)

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    print("🚀 VOLog FYP Board Setup v2\n" + "="*40)

    me = requests.get("https://api.github.com/user", headers=HEADERS).json()
    if "login" not in me:
        print("❌ Auth failed — check your token.")
        return
    print(f"✅ Authenticated as: {me['login']}\n")

    ensure_labels()
    milestone_map = create_milestones()
    create_issues(milestone_map)

    print("\n" + "="*40)
    print("🎉 Done!")
    print(f"📋 Issues:     https://github.com/{OWNER}/{REPO}/issues")
    print(f"🏁 Milestones: https://github.com/{OWNER}/{REPO}/milestones")
    print("\nTip: Click a milestone to see all its tasks and a progress bar as you close them!")

if __name__ == "__main__":
    main()
