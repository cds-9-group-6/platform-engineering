# Git Status Checker for CDS Group 6 Repositories

This directory contains utilities to check the git status across all repositories in the CDS-9 Group 6 project folder.

## 📋 Available Scripts

### 1. `git_status_checker.py` (Comprehensive Python Version)

A detailed Python script that provides comprehensive git status information.

**Features:**
- ✅ Checks for uncommitted changes (modified, untracked, staged files)
- ✅ Identifies repositories with unpushed commits
- ✅ Detects remote updates available for pulling
- ✅ Shows detailed file lists and commit counts
- ✅ Exports results to JSON format
- ✅ Provides error handling and detailed reporting
- ✅ Shows current branch information
- ✅ Timeout protection for git operations

**Usage:**
```bash
# Run with your repository path (REQUIRED)
python3 git_status_checker.py /path/to/your/cds-group-6
python3 git_status_checker.py ~/Documents/github/cds-9-group-6
python3 git_status_checker.py ~/Projects/cds-9-group-6

# Show help
python3 git_status_checker.py --help

# Or run directly (if executable)
./git_status_checker.py /path/to/your/repos
```

**Sample Output:**
```
🚀 Git Status Checker for CDS Group 6 Repositories
⏰ Scan started at: 2025-10-10 14:30:15

🔍 Scanning repositories in: /Users/rajranja/Documents/github/cds-9-group-6
================================================================================
📁 Checking repository: sasya-chikitsa
📁 Checking repository: sasya-arogya-engine
📁 Checking repository: prescription-rag
📁 Checking repository: platform-engineering
📁 Checking repository: sasya-arogya-mcp
📁 Checking repository: sasya-arogya-app

✅ Scanned 6 repositories

================================================================================
📊 REPOSITORY STATUS SUMMARY
================================================================================

🔄 REPOSITORIES WITH UNCOMMITTED CHANGES (1):
------------------------------------------------------------
  📁 sasya-chikitsa (branch: main)
    • M docs/architecture.drawio

⬆️  REPOSITORIES WITH UNPUSHED COMMITS (0):
------------------------------------------------------------

⬇️  REPOSITORIES WITH REMOTE UPDATES AVAILABLE (0):
------------------------------------------------------------

✅ CLEAN REPOSITORIES (5):
------------------------------------------------------------
  📁 sasya-arogya-engine (branch: main)
  📁 prescription-rag (branch: main)
  📁 platform-engineering (branch: main)
  📁 sasya-arogya-mcp (branch: main)
  📁 sasya-arogya-app (branch: main)

📈 OVERALL STATISTICS:
------------------------------------------------------------
  Total repositories: 6
  Repositories with uncommitted changes: 1
  Repositories with unpushed commits: 0
  Repositories with remote updates: 0
  Repositories with errors: 0
  Clean repositories: 5
```

### 2. `quick_git_status.sh` (Parallel Shell Version)

A lightweight shell script with **PARALLEL PROCESSING** for ultra-fast status checks.

**Features:**
- 🚀 **PARALLEL EXECUTION** - Checks all repositories simultaneously
- ⚡ **3-5x faster** than sequential processing
- ✅ Basic git status checking
- ✅ Shows branch information
- ✅ Identifies changes, unpushed commits, and remote updates
- ✅ Simple summary report
- 🔒 Automatic cleanup of temporary files

**Usage:**
```bash
# Run with your repository path (REQUIRED - FASTEST)
./quick_git_status.sh /path/to/your/cds-group-6
./quick_git_status.sh ~/Documents/github/cds-9-group-6
./quick_git_status.sh ~/Projects/cds-9-group-6

# Show help and options
./quick_git_status.sh --help

# Time the execution to see performance
time ./quick_git_status.sh /path/to/your/repos
```

### 3. `quick_git_status_sequential.sh` (Sequential Shell Version)

The original sequential version for comparison or when parallel processing isn't desired.

**Features:**
- 🐌 Sequential execution (one repository at a time)
- ✅ Basic git status checking
- ✅ More predictable output order
- ✅ Lower resource usage

**Usage:**
```bash
# Run with your repository path (REQUIRED)
./quick_git_status_sequential.sh /path/to/your/cds-group-6
./quick_git_status_sequential.sh ~/Documents/github/cds-9-group-6
./quick_git_status_sequential.sh ~/Projects/cds-9-group-6

# Show help
./quick_git_status_sequential.sh --help
```

## 🎯 What These Scripts Check

### Uncommitted Changes
- Modified files
- Untracked files
- Staged files waiting to be committed

### Unpushed Commits
- Local commits that haven't been pushed to remote
- Shows count of commits ahead of remote branch

### Remote Updates
- Commits available on remote that aren't in local branch
- Shows count of commits behind remote branch

### Repository Health
- Current branch information
- Git repository validity
- Remote connection status

## 📊 Output Categories

The scripts categorize repositories into:

1. **🔄 Repositories with Uncommitted Changes**
   - Need `git add` and `git commit`
   - Shows specific files that are modified/untracked

2. **⬆️ Repositories with Unpushed Commits**
   - Need `git push`
   - Shows count of commits ahead of remote

3. **⬇️ Repositories with Remote Updates Available**
   - Need `git pull` or `git merge`
   - Shows count of commits behind remote

4. **✅ Clean Repositories**
   - Up to date with remote
   - No uncommitted changes
   - Ready for development

5. **❌ Repositories with Errors**
   - Git operation failures
   - Network connectivity issues
   - Repository access problems

## 🔧 Requirements

### For Python Script
- Python 3.6 or higher
- Git installed and accessible in PATH
- Network access to fetch remote updates

### For Shell Scripts
- Bash shell (version 4.0+ recommended for optimal parallel processing)
- Git installed and accessible in PATH
- Network access to fetch remote updates
- Sufficient system resources for parallel processes (parallel version only)

## ⚡ Performance Comparison

| **Script** | **Mode** | **Typical Time (10 repos)** | **Use Case** |
|------------|----------|------------------------------|--------------|
| `quick_git_status.sh` | **Parallel** | **~4-6 seconds** | ⚡ **Fastest** - Daily use |
| `quick_git_status_sequential.sh` | Sequential | ~15-25 seconds | 🐌 Compatibility or debugging |
| `git_status_checker.py` | Sequential | ~12-20 seconds | 📊 Detailed analysis & reports |

*Performance varies based on network speed and repository sizes*

## 🎛️ Configuration & Team Usage

### For Team Members

All scripts now accept a custom base directory as a command-line argument, making them portable across different team setups:

```bash
# Each team member can use their own path
./quick_git_status.sh ~/Projects/cds-9-group-6
./quick_git_status.sh /Users/alice/repos/cds-9-group-6  
./quick_git_status.sh /home/bob/workspace/cds-9-group-6

# Python version
python3 git_status_checker.py ~/Projects/cds-9-group-6
python3 git_status_checker.py /Users/alice/repos/cds-9-group-6
```

### Mandatory Path Specification

All scripts now **require** you to specify the base directory path - no defaults are provided to ensure team-wide compatibility.

### Path Expansion

Scripts support `~` (tilde) expansion for home directory:
```bash
./quick_git_status.sh ~/Documents/github/cds-9-group-6  # ✅ Works
./quick_git_status.sh $HOME/Documents/github/cds-9-group-6  # ✅ Works  
./quick_git_status.sh /full/absolute/path/cds-9-group-6  # ✅ Works
```

## 📤 Export Options

The Python script offers JSON export functionality:
```json
{
  "scan_timestamp": "2025-10-10T14:30:15.123456",
  "base_path": "/Users/rajranja/Documents/github/cds-9-group-6",
  "repositories": [
    {
      "name": "sasya-chikitsa",
      "path": "/Users/rajranja/Documents/github/cds-9-group-6/sasya-chikitsa",
      "current_branch": "main",
      "has_uncommitted_changes": true,
      "has_unpushed_commits": false,
      "has_remote_updates": false,
      "uncommitted_files": ["M docs/architecture.drawio"],
      "unpushed_commits_count": 0,
      "remote_commits_count": 0,
      "error": null
    }
  ]
}
```

## 🚨 Important Notes

- **Non-Destructive**: These scripts only READ git status - they never modify repositories
- **Network Calls**: Scripts perform `git fetch` to check remote updates
- **Timeout Protection**: Python script has 30-second timeout for git operations
- **Parallel Processing**: Shell script runs repository checks simultaneously for speed
- **Temporary Files**: Parallel version uses `/tmp/git_status_$$` for coordination (auto-cleanup)
- **Error Handling**: All scripts handle repositories with missing remotes or network issues

## 🔍 Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   chmod +x git_status_checker.py
   chmod +x quick_git_status.sh
   chmod +x quick_git_status_sequential.sh
   ```

2. **Python Not Found**
   - Use `python3` instead of `python`
   - Ensure Python 3.6+ is installed

3. **Git Not Found**
   - Ensure git is installed and in PATH
   - Test with `git --version`

4. **Network Issues**
   - Scripts will report errors for repositories without remote access
   - Check internet connection and git remote URLs

5. **Parallel Processing Issues**
   - If parallel version fails, try sequential version: `./quick_git_status_sequential.sh`
   - Check system resources - parallel processing uses more CPU/memory temporarily
   - Temporary files in `/tmp/` are automatically cleaned up

### Debug Mode

For the Python script, you can modify the timeout or add debug prints by editing the script directly.

## 💡 Usage Tips

1. **Daily Workflow**: Use `./quick_git_status.sh ~/your/repos/path` for fastest daily checks
2. **Team Setup**: Each member can use their own path without modifying scripts
3. **Detailed Analysis**: Use Python script when you need comprehensive reports
4. **Performance Testing**: Use `time ./quick_git_status.sh` to measure execution time
5. **Team Coordination**: Share JSON exports from Python script with team members
6. **CI/CD Integration**: Parallel version is ideal for automated workflows  
7. **Cross-Platform**: Works on macOS, Linux, and Windows (with Git Bash)
8. **Troubleshooting**: Use sequential version if parallel execution has issues

### Quick Team Setup Guide

1. **Clone scripts**: Each team member gets the scripts from platform-engineering repo
2. **Make executable**: `chmod +x *.sh` 
3. **Test with your path**: `./quick_git_status.sh ~/your/path/to/cds-9-group-6`
4. **Create alias** (optional): `alias gstatus='./path/to/quick_git_status.sh ~/your/repos'`

## 🤝 Contributing

To modify or extend these scripts:

1. **Python Script**: Add new checks in the `check_repository()` method
2. **Parallel Shell Script**: Modify `check_repo()` function and result collection logic
3. **Sequential Shell Script**: Add new conditions in the `check_repo()` function  
4. **Output Formats**: Modify the summary printing functions
5. **Performance**: Parallel processing can be further optimized with process pools

## 📝 License

These scripts are part of the CDS-9 Group 6 project and follow the same licensing terms.
