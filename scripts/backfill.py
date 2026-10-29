#!/usr/bin/env python3
"""
touchGrasscias - GitHub Contribution Reforestation & Backfill Engine
Author: Ibrahim Muliatama (bimbap / Vynzx)
Purpose: Retroactively generate backdated git commits to turn contribution heatmaps vibrant green.
"""

import argparse
import datetime
import os
import random
import subprocess
import sys

SAMPLE_MESSAGES = [
    "feat(engine): optimize event loop throughput",
    "fix(cache): resolve intermittent eviction bug",
    "perf(memory): reduce buffer allocation overhead",
    "refactor(stream): decouple chunk processing pipeline",
    "chore(deps): update runtime dependency matrix",
    "docs(api): clarify parameter constraints in docstrings",
    "test(core): add edge cases for timestamp validation",
    "ci(actions): tune parallel job execution runners",
    "feat(logger): introduce structured json telemetry",
    "style(fmt): harmonize whitespace across source modules",
    "fix(parser): handle unexpected nil tokens gracefully",
    "refactor(auth): simplify session token verification",
    "feat(cli): add granular verbosity flags",
    "perf(query): index frequent lookup keys",
    "chore(cleanup): purge obsolete experimental mocks",
    "fix(worker): prevent race condition during teardown",
    "feat(config): support dynamic environment variable overrides",
    "test(e2e): expand integration coverage for edge boundaries",
    "docs(arch): record state machine transition diagram",
    "refactor(utils): extract reusable string helpers",
    "chore(heartbeat): sync repository telemetry state",
    "fix(retry): implement exponential backoff jitter",
    "feat(metrics): track p99 latency histograms",
    "perf(io): batch asynchronous filesystem writes",
    "style(linter): resolve remaining static analysis hints",
    "test(regression): verify backwards compatibility matrix",
    "refactor(handler): streamline incoming payload validation",
    "chore(release): bump internal patch milestone version"
]

BANNER = r"""
  __                  __   ______               _           
 / /_____  __  ______/ /_ / ____/________ _____ (_)___ ______
/ __/ __ \/ / / / __  / // / __/ ___/ __ `/ ___/ / __ `/ ___/
/ /_/ /_/ / /_/ / /_/ / // /_/ / /  / /_/ (__  ) / /_/ (__  ) 
\__/\____/\__,_/\__,_/_(_)____/_/   \__,_/____/_/\__,_/____/  
   >> GitHub Heatmap Reforestation & Contribution Painter <<
"""

def run_cmd(cmd, env=None, cwd=None):
    result = subprocess.run(cmd, env=env, cwd=cwd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"\n[ERROR] Command failed: {cmd}\n{result.stderr}")
        sys.exit(1)
    return result.stdout.strip()

def parse_date(date_str):
    if not date_str:
        return None
    s = date_str.strip()
    import re
    parts = re.split(r'[-/.]', s)
    if len(parts) == 3:
        try:
            y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
            return datetime.date(y, m, d)
        except Exception as e:
            pass
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d"):
        try:
            return datetime.datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    raise ValueError(f"Invalid date format '{date_str}'. Please use YYYY-MM-DD (e.g. 2025-12-01).")

def get_git_config(key, default=""):
    try:
        val = subprocess.check_output(["git", "config", key], text=True).strip()
        return val if val else default
    except Exception:
        return default

def get_commit_count_range(intensity, weekday):
    is_weekend = weekday in (5, 6)
    if intensity == "low":
        return (1, 3)
    elif intensity == "medium":
        return (3, 6)
    elif intensity == "high":
        return (6, 12)
    elif intensity == "ultra":
        return (12, 22)
    elif intensity == "organic":
        # Realistic pattern: higher on weekdays, occasional rest days
        if is_weekend:
            if random.random() < 0.35:
                return (0, 0) # Day off
            return (1, 4)
        else:
            if random.random() < 0.10:
                return (0, 0) # Occasional rest day
            return (4, 11)
    return (2, 5)

def main():
    print(BANNER)
    parser = argparse.ArgumentParser(description="Seed backdated commits for GitHub contribution graph.")
    parser.add_argument("--start-date", type=str, help="Start date (YYYY-MM-DD). Defaults to 365 days ago.")
    parser.add_argument("--end-date", type=str, help="End date (YYYY-MM-DD). Defaults to today.")
    parser.add_argument("--intensity", choices=["low", "medium", "high", "ultra", "organic"], default="organic",
                        help="Commit density level (default: organic).")
    parser.add_argument("--email", type=str, help="Author & committer email. Defaults to git config user.email.")
    parser.add_argument("--name", type=str, help="Author & committer name. Defaults to git config user.name.")
    parser.add_argument("--dry-run", action="store_true", help="Calculate and preview commits without writing to git.")
    parser.add_argument("--target-file", type=str, default="ACTIVITY.md", help="File to mutate for commits.")

    args = parser.parse_args()

    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    os.chdir(repo_dir)

    # Resolve committer identity
    user_email = args.email or get_git_config("user.email", "imta.dev@gmail.com")
    user_name = args.name or get_git_config("user.name", "bimbap")

    # Dates
    today = datetime.date.today()
    try:
        end_date = parse_date(args.end_date) if args.end_date else today
        start_date = parse_date(args.start_date) if args.start_date else (end_date - datetime.timedelta(days=365))
    except ValueError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    if start_date > end_date:
        print("[ERROR] Start date must be before or equal to end date.")
        sys.exit(1)

    total_days = (end_date - start_date).days + 1
    print(f"Target Repository : {repo_dir}")
    print(f"Committer Identity: {user_name} <{user_email}>")
    print(f"Date Range        : {start_date} -> {end_date} ({total_days} days)")
    print(f"Intensity Profile : {args.intensity.upper()}")
    print(f"Dry Run Mode      : {args.dry_run}\n")

    # Plan commits
    schedule = []
    current = start_date
    while current <= end_date:
        min_c, max_c = get_commit_count_range(args.intensity, current.weekday())
        count = random.randint(min_c, max_c) if max_c > 0 else 0
        if count > 0:
            schedule.append((current, count))
        current += datetime.timedelta(days=1)

    total_commits = sum(count for _, count in schedule)
    active_days = len(schedule)
    print(f"Planned Summary:")
    print(f"  - Active Days   : {active_days} / {total_days} days ({active_days/total_days*100:.1f}%)")
    print(f"  - Total Commits : {total_commits} commits (avg {total_commits/max(active_days, 1):.1f} commits/active day)")

    if args.dry_run:
        print("\n[DRY RUN COMPLETE] No git changes were made.")
        return

    confirm = input("\nProceed with generating these commits? [y/N]: ").strip().lower()
    if confirm not in ("y", "yes"):
        print("Aborted by user.")
        return

    print("\nGenerating commits...")
    target_filepath = os.path.join(repo_dir, args.target_file)
    
    # Initialize target file if missing
    if not os.path.exists(target_filepath):
        with open(target_filepath, "w", encoding="utf-8") as f:
            f.write("# touchGrasscias Activity Log\n\nContinuous telemetry stream.\n\n")

    generated = 0
    start_time = datetime.datetime.now()

    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = user_name
    env["GIT_AUTHOR_EMAIL"] = user_email
    env["GIT_COMMITTER_NAME"] = user_name
    env["GIT_COMMITTER_EMAIL"] = user_email

    for day, count in schedule:
        # Generate varied hours during working and evening periods
        # e.g., 09:00 to 23:45
        minutes_pool = sorted(random.sample(range(9 * 60, 23 * 60 + 50), count))
        for m in minutes_pool:
            hour = m // 60
            minute = m % 60
            second = random.randint(0, 59)
            commit_dt = datetime.datetime(day.year, day.month, day.day, hour, minute, second)
            iso_time = commit_dt.strftime("%Y-%m-%dT%H:%M:%S")

            env["GIT_AUTHOR_DATE"] = iso_time
            env["GIT_COMMITTER_DATE"] = iso_time

            msg = random.choice(SAMPLE_MESSAGES)
            entry = f"- `{iso_time}`: {msg}\n"

            with open(target_filepath, "a", encoding="utf-8") as f:
                f.write(entry)

            run_cmd(f'git add "{args.target_file}"', env=env)
            run_cmd(f'git commit -m "{msg}"', env=env)
            generated += 1

            if generated % 50 == 0 or generated == total_commits:
                pct = (generated / total_commits) * 100
                print(f"  [{pct:5.1f}%] Generated {generated}/{total_commits} commits... (Current: {day})")

    elapsed = (datetime.datetime.now() - start_time).total_seconds()
    print(f"\n[SUCCESS] Successfully generated {generated} backdated commits in {elapsed:.1f}s!")
    print(f"\nNext Steps:")
    print(f"  1. Review history: git log -n 5 --oneline")
    print(f"  2. Push to GitHub: git push origin master")
    print(f"  3. Check your GitHub profile graph to see the green reforestation!")

if __name__ == "__main__":
    main()

