#!/bin/bash

# Quick Git Status Checker for CDS Group 6 Repositories
# Sequential version (original implementation)

# Function to show usage
show_usage() {
    echo "🚀 Quick Git Status Checker for CDS Group 6 Repositories (SEQUENTIAL MODE)"
    echo ""
    echo "Usage: $0 BASE_DIRECTORY"
    echo ""
    echo "Arguments:"
    echo "  BASE_DIRECTORY    Path to directory containing CDS Group 6 repositories (REQUIRED)"
    echo ""
    echo "Examples:"
    echo "  $0 /path/to/your/cds-group-6"
    echo "  $0 ~/Documents/github/cds-9-group-6"
    echo "  $0 ~/Projects/cds-9-group-6"
    echo ""
    echo "Options:"    
    echo "  -h, --help        Show this help message"
    echo "  -v, --version     Show version information"
}

# Function to show version
show_version() {
    echo "Quick Git Status Checker v1.0 (Sequential Mode)"
}

# Parse command line arguments
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    show_usage
    exit 0
fi

if [ "$1" = "-v" ] || [ "$1" = "--version" ]; then
    show_version
    exit 0
fi

# Check if base directory argument is provided
if [ -z "$1" ]; then
    echo "❌ Error: Base directory is required!"
    echo ""
    show_usage
    exit 1
fi

BASE_DIR="$1"

# Expand ~ to home directory if present
BASE_DIR="${BASE_DIR/#\~/$HOME}"

# Validate base directory
if [ ! -d "$BASE_DIR" ]; then
    echo "❌ Error: Base directory '$BASE_DIR' does not exist!"
    echo "💡 Please provide a valid directory path containing your CDS Group 6 repositories."
    echo ""
    echo "Usage examples:"
    echo "  $0 /path/to/your/cds-group-6"
    echo "  $0 ~/Documents/github/cds-9-group-6"
    echo "  $0 ~/Projects/cds-9-group-6"
    exit 1
fi

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "🚀 Quick Git Status Check for CDS Group 6 Repositories (SEQUENTIAL MODE)"
echo "⏰ Started at: $TIMESTAMP"
echo "📁 Base directory: $BASE_DIR"
echo "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "="

# Arrays to track repositories
repos_with_changes=()
repos_with_unpushed=()
repos_need_pull=()
repos_clean=()
repos_error=()

# Function to check a single repository
check_repo() {
    local repo_path="$1"
    local repo_name=$(basename "$repo_path")
    
    echo "🔍 Checking: $repo_name"
    
    # Change to repository directory
    cd "$repo_path" || {
        echo "  ❌ Error: Cannot access repository"
        repos_error+=("$repo_name")
        return
    }
    
    # Check if it's a git repository
    if [ ! -d ".git" ]; then
        echo "  ⚠️  Not a git repository"
        return
    fi
    
    # Get current branch
    current_branch=$(git branch --show-current 2>/dev/null)
    if [ -z "$current_branch" ]; then
        current_branch="(detached)"
    fi
    
    echo "  📋 Branch: $current_branch"
    
    # Check for uncommitted changes
    if ! git diff-index --quiet HEAD -- 2>/dev/null; then
        echo "  🔄 Has uncommitted changes"
        repos_with_changes+=("$repo_name")
    elif [ -n "$(git status --porcelain 2>/dev/null)" ]; then
        echo "  🔄 Has untracked/staged files"
        repos_with_changes+=("$repo_name")
    fi
    
    # Fetch remote updates (quietly)
    echo "  🌐 Fetching remote updates..."
    if git fetch --dry-run &>/dev/null || git fetch &>/dev/null; then
        # Check for unpushed commits
        upstream_branch="$current_branch@{upstream}"
        if git rev-parse --verify "$upstream_branch" &>/dev/null; then
            # Count commits ahead and behind
            commits_ahead=$(git rev-list --count "$upstream_branch..$current_branch" 2>/dev/null || echo "0")
            commits_behind=$(git rev-list --count "$current_branch..$upstream_branch" 2>/dev/null || echo "0")
            
            if [ "$commits_ahead" -gt 0 ]; then
                echo "  ⬆️  $commits_ahead commit(s) ahead of remote"
                repos_with_unpushed+=("$repo_name ($commits_ahead ahead)")
            fi
            
            if [ "$commits_behind" -gt 0 ]; then
                echo "  ⬇️  $commits_behind commit(s) behind remote"
                repos_need_pull+=("$repo_name ($commits_behind behind)")
            fi
            
            if [ "$commits_ahead" -eq 0 ] && [ "$commits_behind" -eq 0 ] && [[ ! " ${repos_with_changes[@]} " =~ " $repo_name " ]]; then
                echo "  ✅ Up to date"
                repos_clean+=("$repo_name")
            fi
        else
            echo "  ⚠️  No upstream branch configured"
        fi
    else
        echo "  ❌ Failed to fetch remote updates"
        repos_error+=("$repo_name")
    fi
    
    echo ""
}

# Main execution
echo ""
for dir in "$BASE_DIR"/*; do
    if [ -d "$dir" ]; then
        check_repo "$dir"
    fi
done

# Summary
echo "📊 SUMMARY REPORT"
echo "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "=" "="

if [ ${#repos_with_changes[@]} -gt 0 ]; then
    echo ""
    echo "🔄 REPOSITORIES WITH UNCOMMITTED CHANGES (${#repos_with_changes[@]}):"
    for repo in "${repos_with_changes[@]}"; do
        echo "  • $repo"
    done
fi

if [ ${#repos_with_unpushed[@]} -gt 0 ]; then
    echo ""
    echo "⬆️  REPOSITORIES WITH UNPUSHED COMMITS (${#repos_with_unpushed[@]}):"
    for repo in "${repos_with_unpushed[@]}"; do
        echo "  • $repo"
    done
fi

if [ ${#repos_need_pull[@]} -gt 0 ]; then
    echo ""
    echo "⬇️  REPOSITORIES THAT NEED PULLING (${#repos_need_pull[@]}):"
    for repo in "${repos_need_pull[@]}"; do
        echo "  • $repo"
    done
fi

if [ ${#repos_error[@]} -gt 0 ]; then
    echo ""
    echo "❌ REPOSITORIES WITH ERRORS (${#repos_error[@]}):"
    for repo in "${repos_error[@]}"; do
        echo "  • $repo"
    done
fi

if [ ${#repos_clean[@]} -gt 0 ]; then
    echo ""
    echo "✅ CLEAN REPOSITORIES (${#repos_clean[@]}):"
    for repo in "${repos_clean[@]}"; do
        echo "  • $repo"
    done
fi

echo ""
echo "📈 STATISTICS:"
echo "  Total repositories checked: $((${#repos_with_changes[@]} + ${#repos_with_unpushed[@]} + ${#repos_need_pull[@]} + ${#repos_clean[@]} + ${#repos_error[@]}))"
echo "  Repositories with changes: ${#repos_with_changes[@]}"
echo "  Repositories with unpushed commits: ${#repos_with_unpushed[@]}"
echo "  Repositories needing pull: ${#repos_need_pull[@]}"
echo "  Clean repositories: ${#repos_clean[@]}"
echo "  Repositories with errors: ${#repos_error[@]}"

FINISH_TIME=$(date '+%Y-%m-%d %H:%M:%S')
echo ""
echo "🎉 Sequential check completed at: $FINISH_TIME"
