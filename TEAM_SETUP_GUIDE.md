# 🚀 Team Setup Guide - Git Status Checker

Quick setup guide for CDS-9 Group 6 team members to use git status checker scripts.

## 📋 One-Time Setup

### Step 1: Get the Scripts
```bash
# Navigate to your local platform-engineering repo
cd /path/to/your/cds-9-group-6/platform-engineering

# Pull latest changes to get the scripts
git pull origin main

# Make scripts executable
chmod +x git_status_checker.py
chmod +x quick_git_status.sh  
chmod +x quick_git_status_sequential.sh
```

### Step 2: Test with Your Path (REQUIRED)
```bash
# Replace with your actual path to CDS-9 Group 6 repositories (REQUIRED - no defaults)
./quick_git_status.sh ~/Documents/github/cds-9-group-6
./quick_git_status.sh /Users/yourname/Projects/cds-9-group-6
./quick_git_status.sh /home/yourname/workspace/cds-9-group-6

# This will now show an error (path is required):
./quick_git_status.sh
# ❌ Error: Base directory is required!
```

## 🎯 Daily Usage

### Quick Status Check (3-4 seconds)
```bash
./quick_git_status.sh ~/your/path/to/cds-9-group-6
```

### Detailed Analysis (15-20 seconds)
```bash
python3 git_status_checker.py ~/your/path/to/cds-9-group-6
```

## 🔧 Optional: Create Aliases

Add to your `~/.bashrc`, `~/.zshrc`, or `~/.bash_profile`:

```bash
# Quick git status for CDS projects (PATH IS REQUIRED)
alias cds-status='/path/to/platform-engineering/quick_git_status.sh ~/your/path/to/cds-9-group-6'
alias cds-detail='python3 /path/to/platform-engineering/git_status_checker.py ~/your/path/to/cds-9-group-6'

# Then just run:
# cds-status    # for quick check
# cds-detail    # for detailed analysis
```

## 📁 Common Directory Structures

### macOS Users
```bash
./quick_git_status.sh ~/Documents/GitHub/cds-9-group-6
./quick_git_status.sh ~/Projects/cds-9-group-6
./quick_git_status.sh ~/Developer/cds-9-group-6
```

### Linux Users  
```bash
./quick_git_status.sh ~/projects/cds-9-group-6
./quick_git_status.sh ~/workspace/cds-9-group-6
./quick_git_status.sh ~/code/cds-9-group-6
```

### Windows Users (Git Bash)
```bash
./quick_git_status.sh /c/Users/yourname/Documents/GitHub/cds-9-group-6
./quick_git_status.sh ~/Documents/GitHub/cds-9-group-6
```

## 📊 What You'll See

### Clean Output Example
```
🚀 Quick Git Status Check for CDS Group 6 Repositories (PARALLEL MODE)
⏰ Started at: 2025-10-10 10:30:15
📁 Base directory: /Users/yourname/Projects/cds-9-group-6

✅ CLEAN REPOSITORIES (8):
  • prescription-rag
  • sasya-arogya-app
  • sasya-arogya-engine
  • sasya-arogya-mcp
  • sasya-chikitsa
  • platform-engineering
  • inference-tracking
  • extract-plant-leaf

🎉 Parallel check completed at: 2025-10-10 10:30:19
```

### When Action Needed
```
🔄 REPOSITORIES WITH UNCOMMITTED CHANGES (2):
  • sasya-chikitsa
  • mlflow-samples

⬆️  REPOSITORIES WITH UNPUSHED COMMITS (1):
  • mlflow-samples (3 ahead)

⬇️  REPOSITORIES THAT NEED PULLING (1):
  • sasya-arogya-mcp (1 behind)
```

## 🆘 Troubleshooting

### Script Not Found
```bash
# Make sure you're in the right directory
cd /path/to/your/cds-9-group-6/platform-engineering
ls -la *.sh *.py
```

### Permission Denied
```bash
chmod +x quick_git_status.sh
chmod +x git_status_checker.py
```

### Path Not Found
```bash
# Verify your CDS-9 Group 6 directory exists
ls ~/your/path/to/cds-9-group-6

# Should show directories like:
# sasya-arogya-engine/
# prescription-rag/
# platform-engineering/
# etc.
```

### Python Not Found
```bash
# Try with python3
python3 git_status_checker.py ~/your/path

# Or check Python installation
python3 --version
```

## 💡 Pro Tips

1. **Run before starting work** - See what needs attention
2. **Share status with team** - Use JSON export from Python script
3. **Set up notifications** - Run in CI/CD pipelines  
4. **Use time command** - `time ./quick_git_status.sh` to see performance
5. **Help anytime** - `./quick_git_status.sh --help`

## 🤝 Team Coordination

### Morning Standup
```bash
# Quick team status check
./quick_git_status.sh ~/your/repos > team_status.txt
# Share team_status.txt in Slack/Teams
```

### Before Important Merges
```bash
# Detailed analysis with JSON export
python3 git_status_checker.py ~/your/repos
# Export to JSON when prompted for team review
```

### CI/CD Integration
```bash
# Add to your CI pipeline
./quick_git_status.sh $WORKSPACE/cds-9-group-6
```

---

🎉 **Happy coding!** If you have issues, ask in the team chat or check the main README.md for more details.
