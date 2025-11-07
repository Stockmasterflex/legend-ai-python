# Claude Code Development Workflow

## 🎯 Branch Strategy

This repository uses a specific branch strategy for Claude Code development:

### **Active Development Branch** (for Claude Code)
```
claude/initial-repo-review-011CUsBeQ3RGbnNF3EMZgqJ2
```

### **Production Branch** (merges only)
```
main
```

---

## 📋 Required Steps for Claude Code

### ✅ BEFORE starting any work:

1. **Read `.claude-branch` file** to identify the active branch
   ```bash
   cat .claude-branch
   # Output: claude/initial-repo-review-011CUsBeQ3RGbnNF3EMZgqJ2
   ```

2. **Check current branch**
   ```bash
   git status
   # Should show: "On branch claude/initial-repo-review-..."
   ```

3. **If not on correct branch, switch immediately**
   ```bash
   git checkout $(cat .claude-branch)
   git pull origin $(cat .claude-branch)
   ```

### ✅ DURING development:

1. **All commits go to the claude branch** (never main)
   ```bash
   # CORRECT:
   git add -A
   git commit -m "feature: description"
   git push origin $(cat .claude-branch)

   # WRONG:
   git push origin main  # ❌ DO NOT DO THIS
   ```

2. **Use descriptive commit messages**
   ```bash
   # Good examples:
   git commit -m "✨ Add VCP pattern detector with Minervini rules"
   git commit -m "🐛 Fix cup & handle roundedness calculation"
   git commit -m "📚 Add detector integration guide"
   git commit -m "🔧 Improve ATR calculation performance"
   ```

### ✅ AFTER completing features:

1. **Push to claude branch**
   ```bash
   git push origin $(cat .claude-branch)
   ```

2. **DO NOT manually merge to main**
   - Main is only for production-ready merges
   - Railway will deploy from the claude branch directly
   - Merges happen through GitHub UI only

---

## 🚀 Production Deployment

When ready for production:

1. **Create a Pull Request** from claude branch → main via GitHub UI
2. **Railway watches the claude branch** and deploys automatically
3. **After review**, merge PR to main

---

## 🔍 How to Identify the Correct Branch

### Method 1: Read the marker file
```bash
cat .claude-branch
```

### Method 2: Check git config
```bash
git remote -v
# Should show the correct remote URLs
```

### Method 3: Last resort
```bash
git branch -v
# Look for the branch with most recent commits
# Usually the one with ✨, 🐛, 📚 emojis from Claude
```

---

## 📂 File Structure

```
.claude-branch                    ← Always read this first!
├── Contains: claude/initial-repo-review-011CUsBeQ3RGbnNF3EMZgqJ2
└── This tells Claude Code which branch to use

.git/
├── refs/heads/
│   ├── main (production)
│   └── claude/initial-repo-review-... (development) ✅
```

---

## ⚠️ Common Mistakes to Avoid

### ❌ WRONG: Committing to main
```bash
git checkout main
git add -A
git commit -m "new feature"
git push origin main  # WRONG!
```

### ✅ CORRECT: Committing to claude branch
```bash
git checkout claude/initial-repo-review-011CUsBeQ3RGbnNF3EMZgqJ2
git add -A
git commit -m "new feature"
git push origin claude/initial-repo-review-011CUsBeQ3RGbnNF3EMZgqJ2  # Correct
```

### ❌ WRONG: Forgetting to check which branch you're on
```bash
git status  # ALWAYS do this before committing
# On branch main  ← STOP! Switch to claude branch first
```

### ✅ CORRECT: Verify branch before committing
```bash
git status
# On branch claude/initial-repo-review-011CUsBeQ3RGbnNF3EMZgqJ2  ✓ Good to go
```

---

## 🔄 Workflow Example

```bash
# 1. Start work: Verify correct branch
git status
# On branch claude/initial-repo-review-011CUsBeQ3RGbnNF3EMZgqJ2 ✓

# 2. Pull latest changes
git pull origin $(cat .claude-branch)

# 3. Make changes
# ... edit files ...

# 4. Check status
git status

# 5. Commit your work
git add -A
git commit -m "✨ Add new pattern detector"

# 6. Push to claude branch
git push origin $(cat .claude-branch)

# 7. Verify pushed successfully
git log --oneline -3  # Should show your new commit
```

---

## 🛠️ Configuration for Claude Code

If you need to automate branch detection in future sessions, use:

```bash
# Check which branch Claude Code should use
CLAUDE_BRANCH=$(cat .claude-branch)
echo "Using branch: $CLAUDE_BRANCH"

# Automatically switch if needed
if [ "$(git rev-parse --abbrev-ref HEAD)" != "$CLAUDE_BRANCH" ]; then
    git checkout "$CLAUDE_BRANCH"
    git pull origin "$CLAUDE_BRANCH"
fi
```

---

## 📖 Reference

### Git Branch Commands

```bash
# Check current branch
git branch
git status

# Switch to claude branch
git checkout $(cat .claude-branch)

# Pull latest from claude branch
git pull origin $(cat .claude-branch)

# Push to claude branch
git push origin $(cat .claude-branch)

# View commit history on claude branch
git log --oneline -10

# View all branches
git branch -a
```

### Railway Integration

- **Production URL**: `https://legend-ai-python-production.up.railway.app`
- **Deploys from**: `claude/initial-repo-review-011CUsBeQ3RGbnNF3EMZgqJ2` (claude branch)
- **Deployment takes**: 2-3 minutes after push
- **Check status**: Monitor Railway dashboard or test endpoint

---

## ✅ Checklist Before Every Commit

- [ ] Read `.claude-branch` to confirm correct branch name
- [ ] Run `git status` and verify correct branch
- [ ] Run `git log -1` to see where HEAD is
- [ ] Commit with clear message and emoji
- [ ] Push to claude branch only (not main)
- [ ] Verify in GitHub that commit appeared in correct branch

---

## 🎓 Why This Structure?

1. **Keeps main clean** - Only production-ready code
2. **Enables rapid development** - Claude branch gets all experimental features
3. **Clear deployment path** - Claude branch → PR → main → Railway
4. **Prevents accidents** - `.claude-branch` file acts as explicit marker
5. **Easier to review** - All Claude changes in one branch before merging to main

---

## 🚨 Emergency: Restore from Mistake

If you accidentally committed to main:

```bash
# 1. Check what you did
git log --oneline main -5

# 2. Reset main to before your commits
git checkout main
git reset --hard <commit-before-your-changes>
git push origin main --force-with-lease

# 3. Switch to claude branch and cherry-pick your commits
git checkout $(cat .claude-branch)
git cherry-pick <your-commit-hashes>
git push origin $(cat .claude-branch)
```

---

**Status**: ✅ This workflow is in effect starting 2025-11-06
**Last Updated**: 2025-11-06
**Branch Name**: `claude/initial-repo-review-011CUsBeQ3RGbnNF3EMZgqJ2`

Always verify by reading `.claude-branch` before you start! 🎯
