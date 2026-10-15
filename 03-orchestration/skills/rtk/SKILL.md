---
name: rtk
description: >-
  Rust Token Killer — global CLI proxy for token-efficient file operations. Use
  ALWAYS instead of reading full files. Replaces expensive full-file reads with
  surgical targeted queries: line ranges, symbol extraction, ripgrep patterns,
  and structured diff summaries. Reduces context window consumption by 60-90%.
  Triggers whenever any file operation is needed, especially on files > 100 lines.
  Core principle: never read what you don't need.
---

# RTK — Rust Token Killer

**The Universal Token Conservation Protocol.**

RTK is a mandatory operating discipline that replaces wasteful full-file reads with
precision surgical queries. Every token consumed reading irrelevant code is a token
stolen from reasoning, planning, and implementation.

> **GLOBAL RULE**: Before calling `view_file` on any file > 100 lines, you MUST
> first apply an RTK strategy to determine the minimum viable read range. Full-file
> reads on large files without prior targeting are a protocol violation.

---

## Core Principle: The Token Hierarchy

Read operations must follow this cost hierarchy (cheapest first):

```
TIER 1 — FREE:   Directory listing (list_dir)
TIER 2 — CHEAP:  Pattern search (ripgrep / Select-String)
TIER 3 — MEDIUM: Targeted line range (view_file with StartLine/EndLine)
TIER 4 — COSTLY: Full file read (view_file without bounds) — LAST RESORT ONLY
TIER 5 — BANNED: Reading the same file twice without a mutation in between
```

**Always start at Tier 1 and descend only as far as needed.**

---

## The Seven RTK Operations

### RTK-1: Scout (Replace Full-File Read)

**Trigger**: You need to understand a file you've never read.

**Protocol**:
1. `list_dir` on the file's parent to get size context.
2. Read only the **first 50 lines** (imports, exports, top-level declarations).
3. Read only the **last 30 lines** (export statements, module registration).
4. Use search to find the specific function/class you need.

**Never** read the full file on first contact.

**PowerShell command** for quick file summary:
```powershell
# Get first 50 lines (imports + exports)
Get-Content "path\to\file.ts" | Select-Object -First 50

# Get last 30 lines
Get-Content "path\to\file.ts" | Select-Object -Last 30

# Count total lines
(Get-Content "path\to\file.ts").Count
```

---

### RTK-2: Snipe (Symbol Extraction)

**Trigger**: You need a specific function, class, interface, or type.

**Protocol**:
1. Use `Select-String` (PowerShell) or `ripgrep` to find the symbol's line number.
2. Read only a 20-line window around that line number.
3. Expand by 10 lines if the block isn't complete.

**PowerShell commands**:
```powershell
# Find a function/class definition line
Select-String -Path "src\**\*.ts" -Pattern "function myFunc|class MyClass|interface MyType" -Recurse

# Find all exports in a file
Select-String -Path "lib\types.ts" -Pattern "^export"

# Find where a symbol is used
Select-String -Path "components\**\*.tsx" -Pattern "useGameEngine" -Recurse | Select-Object -First 20
```

**Then** use `view_file` with `StartLine` / `EndLine` set to the discovered range.

---

### RTK-3: Grep-First (Search Before Read)

**Trigger**: You need to find where something is defined or used across the codebase.

**Protocol**:
1. Always run a search BEFORE opening any file.
2. Use the search results to build a map of exactly which files and line ranges
   are relevant.
3. Open only the relevant ranges, never the full files.

**PowerShell pattern**:
```powershell
# Cross-codebase symbol search
Select-String -Path ".\**\*.ts",".\**\*.tsx" -Pattern "SYMBOL_NAME" -Recurse |
  Select-Object Filename, LineNumber, Line |
  Format-Table -AutoSize

# Find all files that import a module
Select-String -Path ".\**\*.ts" -Pattern "from ['\"]@/lib/game-engine" -Recurse |
  Select-Object Filename | Sort-Object -Unique

# Find all TODO/FIXME comments
Select-String -Path ".\**\*.ts",".\**\*.tsx" -Pattern "TODO|FIXME|HACK|XXX" -Recurse |
  Format-Table Filename, LineNumber, Line -AutoSize
```

---

### RTK-4: Diff-Scope (Understand Changes Without Full Read)

**Trigger**: You need to understand what changed before implementing something.

**Protocol**:
1. Use `git diff` or `git show` to see only the changed lines.
2. Use `git log --oneline -10` to get recent context.
3. Never read the full file when git can show you only the delta.

**Commands**:
```powershell
# See all unstaged changes
git diff

# See changes in a specific file
git diff HEAD~1 -- "path/to/file.ts"

# See what a specific commit changed
git show --stat HEAD

# See changes in the last 3 commits
git log -3 --patch --follow "path/to/file.ts"
```

---

### RTK-5: Structure-Map (Directory Before Files)

**Trigger**: You're entering a new codebase or directory you haven't mapped yet.

**Protocol**:
1. `list_dir` at the root level first.
2. `list_dir` on subdirectories that are relevant to your task.
3. Build a mental model from directory structure before reading any files.
4. Only descend into files when the directory map has told you which ones matter.

**Token Budget per Exploration:**
```
Root list_dir:          ~50 tokens
Subdir list_dir (×3):   ~150 tokens
Total orientation:      ~200 tokens

vs.

Reading 3 wrong files:  ~6,000+ tokens wasted
```

The structure-map pays for itself 30x.

---

### RTK-6: Append-Write (Write Without Re-Reading)

**Trigger**: You need to add content to a file you've already partially read.

**Protocol**:
1. Never re-read a file just to write to it.
2. Use `StartLine`/`EndLine` to target only the specific block being changed.
3. Use `multi_replace_file_content` for non-contiguous edits (avoids re-read).
4. Track file structure in memory from initial Scout (RTK-1).

**Anti-pattern** (BANNED):
```
❌ view_file(full) → edit → view_file(full again to verify) → edit again
```

**RTK pattern** (REQUIRED):
```
✓ RTK-1 Scout → targeted edit → targeted verify on changed range only
```

---

### RTK-7: Cache-and-Skip (Never Read Twice)

**Trigger**: You've already read a file in this session.

**Protocol**:
1. Track what you've read in your working memory.
2. If you need info from a file you've already read, check your memory first.
3. Only re-read if the file was mutated since your last read.
4. Use the `StartLine`/`EndLine` from your memory map to read only the changed section.

**Memory template** (maintain mentally per session):
```
FILE CACHE:
  lib/types/mold-types.ts     → read lines 1-50 (imports), 380-443 (exports)
  components/home/home-screen.tsx → read lines 1-80 (structure)
  app/globals.css             → NOT YET READ
```

---

## RTK Decision Tree

```
Need info from a file?
        │
        ▼
Is it in your FILE CACHE? → YES → Use cached knowledge, skip read
        │ NO
        ▼
Is it < 50 lines? → YES → Full read is acceptable
        │ NO
        ▼
Do you know the symbol name? → YES → RTK-2: Snipe (search + targeted read)
        │ NO
        ▼
Do you need cross-file info? → YES → RTK-3: Grep-First
        │ NO
        ▼
Do you need structure context? → YES → RTK-1: Scout (first 50 + last 30)
        │ NO
        ▼
Do you need change context? → YES → RTK-4: Diff-Scope (git commands)
        │ NO
        ▼
RTK-5: Structure-Map (list_dir first, then targeted descent)
```

---

## Token Budget Enforcement

### Per-File Budgets

| File Size | Max Tokens to Spend | Strategy |
|-----------|---------------------|----------|
| < 50 lines | Full read OK | `view_file` no bounds |
| 50–200 lines | Scout + targeted | RTK-1 + RTK-2 |
| 200–800 lines | Grep-first mandatory | RTK-3 → RTK-2 |
| 800+ lines | Multi-pass only | RTK-3 → RTK-2 → max 200 lines per pass |

### Session Budget Tracking

At session start, allocate a conceptual token budget:

```
SESSION BUDGET:
  Total allocation:   ~100,000 tokens
  Reserved for code generation: 40% = 40,000
  Reserved for reasoning:       30% = 30,000
  Available for file reads:     30% = 30,000

  RTK Target: spend < 15,000 tokens on file reads
  (reading the same info more efficiently = more budget for quality output)
```

---

## RTK Report Format

When completing a significant task, output an RTK efficiency report:

```
RTK EFFICIENCY REPORT
=====================
Files accessed:        N
Full reads:            N (only files < 50 lines)
Targeted reads:        N (average range: X lines each)
Search operations:     N
Cache hits:            N (reads avoided by memory)

Estimated tokens spent on reads:  ~X tokens
Estimated tokens saved vs naive:  ~Y tokens (Z% reduction)

Token violations detected: [NONE / list any full reads on large files]
```

---

## PowerShell Quick Reference (Windows)

Since the OS is Windows and shell is PowerShell, use these native commands:

```powershell
# ── SEARCH ──────────────────────────────────────────────────────────────────
# Find pattern in all TypeScript files
Select-String -Path ".\**\*.ts",".\**\*.tsx" -Pattern "PATTERN" -Recurse

# Find pattern, show 3 lines of context
Select-String -Path ".\**\*.ts" -Pattern "PATTERN" -Context 3,3 -Recurse

# Case-insensitive search
Select-String -Path ".\**\*.ts" -Pattern "pattern" -CaseSensitive:$false -Recurse

# ── FILE INFO ────────────────────────────────────────────────────────────────
# Count lines in a file
(Get-Content "file.ts").Count

# Get file size in bytes
(Get-Item "file.ts").Length

# List files by size (find large files)
Get-ChildItem -Recurse -Include "*.ts","*.tsx" |
  Sort-Object Length -Descending |
  Select-Object Name, Length -First 20

# ── RANGE READS ──────────────────────────────────────────────────────────────
# Read specific line range
Get-Content "file.ts" | Select-Object -Skip 99 -First 50  # lines 100–150

# Read first N lines
Get-Content "file.ts" | Select-Object -First 50

# Read last N lines
Get-Content "file.ts" | Select-Object -Last 30

# ── GIT DIFF ────────────────────────────────────────────────────────────────
# See what changed
git diff --stat
git diff HEAD~1 -- "path/to/file.ts"
git log --oneline -10
```

---

## Integration with view_file Tool

When using the native `view_file` tool, RTK mandates:

1. **ALWAYS specify `StartLine` and `EndLine`** for files > 100 lines.
2. **Maximum 200 lines per view_file call** on large files.
3. **Use multiple targeted calls** rather than one large range.

```
✓ view_file(path, StartLine=1, EndLine=50)      ← RTK compliant
✓ view_file(path, StartLine=340, EndLine=390)   ← RTK compliant
❌ view_file(path)  [on 800-line file]           ← RTK violation
```

---

## Common Mistakes

1. **Reading the entire file to find one function**: Use RTK-2 (Snipe) instead.
2. **Re-reading after writing**: Track your edit location, read only the changed
   range to verify.
3. **Grep without a plan**: Always know what you're searching for before searching.
   Blind greps waste time and tokens.
