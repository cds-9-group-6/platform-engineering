#!/usr/bin/env python3
"""
Git Status Checker for CDS Group Repositories

This script scans all repositories in the CDS-9 Group 6 folder and reports:
1. Repositories with uncommitted changes
2. Repositories with unpushed commits
3. Repositories where remote has updates available
4. Overall summary of repository states

Usage: python git_status_checker.py
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class RepoStatus:
    """Data class to hold repository status information"""
    name: str
    path: str
    has_uncommitted_changes: bool = False
    has_unpushed_commits: bool = False
    has_remote_updates: bool = False
    current_branch: str = ""
    uncommitted_files: List[str] = None
    unpushed_commits_count: int = 0
    remote_commits_count: int = 0
    error: Optional[str] = None
    
    def __post_init__(self):
        if self.uncommitted_files is None:
            self.uncommitted_files = []

class GitStatusChecker:
    """Main class for checking git status across repositories"""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.repositories: List[RepoStatus] = []
    
    def run_git_command(self, repo_path: Path, command: List[str]) -> Tuple[bool, str, str]:
        """
        Run a git command in the specified repository
        
        Returns:
            Tuple of (success, stdout, stderr)
        """
        try:
            result = subprocess.run(
                ["git"] + command,
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out"
        except Exception as e:
            return False, "", str(e)
    
    def is_git_repository(self, path: Path) -> bool:
        """Check if a directory is a git repository"""
        return (path / ".git").exists()
    
    def get_current_branch(self, repo_path: Path) -> str:
        """Get the current branch name"""
        success, stdout, _ = self.run_git_command(repo_path, ["branch", "--show-current"])
        return stdout if success else "unknown"
    
    def check_uncommitted_changes(self, repo_path: Path) -> Tuple[bool, List[str]]:
        """Check for uncommitted changes (modified, untracked, staged files)"""
        success, stdout, _ = self.run_git_command(repo_path, ["status", "--porcelain"])
        if not success:
            return False, []
        
        files = []
        for line in stdout.split('\n'):
            if line.strip():
                files.append(line.strip())
        
        return len(files) > 0, files
    
    def check_unpushed_commits(self, repo_path: Path, branch: str) -> Tuple[bool, int]:
        """Check for unpushed commits"""
        if not branch or branch == "unknown":
            return False, 0
        
        # First, try to get the upstream branch
        success, upstream, _ = self.run_git_command(repo_path, ["rev-parse", "--abbrev-ref", f"{branch}@{{upstream}}"])
        if not success:
            # No upstream branch configured
            return False, 0
        
        # Check how many commits ahead we are
        success, stdout, _ = self.run_git_command(repo_path, ["rev-list", "--count", f"{upstream}..{branch}"])
        if not success:
            return False, 0
        
        try:
            count = int(stdout)
            return count > 0, count
        except ValueError:
            return False, 0
    
    def check_remote_updates(self, repo_path: Path, branch: str) -> Tuple[bool, int]:
        """Check if remote has updates available"""
        if not branch or branch == "unknown":
            return False, 0
        
        # Fetch latest changes from remote (without merging)
        success, _, _ = self.run_git_command(repo_path, ["fetch", "--dry-run"])
        if not success:
            # Try without dry-run - some repositories might not support it
            success, _, _ = self.run_git_command(repo_path, ["fetch"])
            if not success:
                return False, 0
        
        # Check if remote branch exists
        success, upstream, _ = self.run_git_command(repo_path, ["rev-parse", "--abbrev-ref", f"{branch}@{{upstream}}"])
        if not success:
            return False, 0
        
        # Check how many commits behind we are
        success, stdout, _ = self.run_git_command(repo_path, ["rev-list", "--count", f"{branch}..{upstream}"])
        if not success:
            return False, 0
        
        try:
            count = int(stdout)
            return count > 0, count
        except ValueError:
            return False, 0
    
    def check_repository(self, repo_path: Path) -> RepoStatus:
        """Check the status of a single repository"""
        repo_name = repo_path.name
        status = RepoStatus(name=repo_name, path=str(repo_path))
        
        try:
            # Get current branch
            status.current_branch = self.get_current_branch(repo_path)
            
            # Check for uncommitted changes
            has_changes, files = self.check_uncommitted_changes(repo_path)
            status.has_uncommitted_changes = has_changes
            status.uncommitted_files = files
            
            # Check for unpushed commits
            has_unpushed, unpushed_count = self.check_unpushed_commits(repo_path, status.current_branch)
            status.has_unpushed_commits = has_unpushed
            status.unpushed_commits_count = unpushed_count
            
            # Check for remote updates
            has_remote_updates, remote_count = self.check_remote_updates(repo_path, status.current_branch)
            status.has_remote_updates = has_remote_updates
            status.remote_commits_count = remote_count
            
        except Exception as e:
            status.error = str(e)
        
        return status
    
    def scan_repositories(self) -> None:
        """Scan all repositories in the base path"""
        print(f"🔍 Scanning repositories in: {self.base_path}")
        print("=" * 80)
        
        if not self.base_path.exists():
            print(f"❌ Error: Path {self.base_path} does not exist")
            return
        
        repo_count = 0
        for item in self.base_path.iterdir():
            if item.is_dir() and self.is_git_repository(item):
                print(f"📁 Checking repository: {item.name}")
                status = self.check_repository(item)
                self.repositories.append(status)
                repo_count += 1
        
        print(f"\n✅ Scanned {repo_count} repositories")
    
    def print_summary(self) -> None:
        """Print a summary of all repository statuses"""
        print("\n" + "=" * 80)
        print("📊 REPOSITORY STATUS SUMMARY")
        print("=" * 80)
        
        repos_with_uncommitted = []
        repos_with_unpushed = []
        repos_with_remote_updates = []
        repos_with_errors = []
        
        for repo in self.repositories:
            if repo.error:
                repos_with_errors.append(repo)
            if repo.has_uncommitted_changes:
                repos_with_uncommitted.append(repo)
            if repo.has_unpushed_commits:
                repos_with_unpushed.append(repo)
            if repo.has_remote_updates:
                repos_with_remote_updates.append(repo)
        
        # Print repositories with uncommitted changes
        if repos_with_uncommitted:
            print(f"\n🔄 REPOSITORIES WITH UNCOMMITTED CHANGES ({len(repos_with_uncommitted)}):")
            print("-" * 60)
            for repo in repos_with_uncommitted:
                print(f"  📁 {repo.name} (branch: {repo.current_branch})")
                for file in repo.uncommitted_files[:5]:  # Show first 5 files
                    print(f"    • {file}")
                if len(repo.uncommitted_files) > 5:
                    print(f"    ... and {len(repo.uncommitted_files) - 5} more files")
                print()
        
        # Print repositories with unpushed commits
        if repos_with_unpushed:
            print(f"\n⬆️  REPOSITORIES WITH UNPUSHED COMMITS ({len(repos_with_unpushed)}):")
            print("-" * 60)
            for repo in repos_with_unpushed:
                print(f"  📁 {repo.name} (branch: {repo.current_branch})")
                print(f"    • {repo.unpushed_commits_count} commit(s) ahead of remote")
                print()
        
        # Print repositories with remote updates
        if repos_with_remote_updates:
            print(f"\n⬇️  REPOSITORIES WITH REMOTE UPDATES AVAILABLE ({len(repos_with_remote_updates)}):")
            print("-" * 60)
            for repo in repos_with_remote_updates:
                print(f"  📁 {repo.name} (branch: {repo.current_branch})")
                print(f"    • {repo.remote_commits_count} commit(s) behind remote")
                print()
        
        # Print repositories with errors
        if repos_with_errors:
            print(f"\n❌ REPOSITORIES WITH ERRORS ({len(repos_with_errors)}):")
            print("-" * 60)
            for repo in repos_with_errors:
                print(f"  📁 {repo.name}: {repo.error}")
        
        # Print clean repositories
        clean_repos = [
            repo for repo in self.repositories 
            if not repo.has_uncommitted_changes 
            and not repo.has_unpushed_commits 
            and not repo.has_remote_updates 
            and not repo.error
        ]
        
        if clean_repos:
            print(f"\n✅ CLEAN REPOSITORIES ({len(clean_repos)}):")
            print("-" * 60)
            for repo in clean_repos:
                print(f"  📁 {repo.name} (branch: {repo.current_branch})")
        
        # Overall statistics
        print(f"\n📈 OVERALL STATISTICS:")
        print("-" * 60)
        print(f"  Total repositories: {len(self.repositories)}")
        print(f"  Repositories with uncommitted changes: {len(repos_with_uncommitted)}")
        print(f"  Repositories with unpushed commits: {len(repos_with_unpushed)}")
        print(f"  Repositories with remote updates: {len(repos_with_remote_updates)}")
        print(f"  Repositories with errors: {len(repos_with_errors)}")
        print(f"  Clean repositories: {len(clean_repos)}")
    
    def export_to_json(self, output_file: str) -> None:
        """Export results to JSON file"""
        data = {
            "scan_timestamp": datetime.now().isoformat(),
            "base_path": str(self.base_path),
            "repositories": []
        }
        
        for repo in self.repositories:
            repo_data = {
                "name": repo.name,
                "path": repo.path,
                "current_branch": repo.current_branch,
                "has_uncommitted_changes": repo.has_uncommitted_changes,
                "has_unpushed_commits": repo.has_unpushed_commits,
                "has_remote_updates": repo.has_remote_updates,
                "uncommitted_files": repo.uncommitted_files,
                "unpushed_commits_count": repo.unpushed_commits_count,
                "remote_commits_count": repo.remote_commits_count,
                "error": repo.error
            }
            data["repositories"].append(repo_data)
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n💾 Results exported to: {output_file}")

def main():
    """Main function"""
    import argparse
    
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(
        description="Git Status Checker for CDS Group 6 Repositories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 git_status_checker.py /path/to/your/cds-group-6
  python3 git_status_checker.py ~/Documents/github/cds-9-group-6
  python3 git_status_checker.py ~/Projects/cds-9-group-6
        """
    )
    
    parser.add_argument(
        'base_path',
        help='Base directory containing CDS Group 6 repositories (REQUIRED - specify your local path)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Git Status Checker v1.0'
    )
    
    args = parser.parse_args()
    
    # Expand user path (handles ~ notation)
    base_path = os.path.expanduser(args.base_path)
    
    # Validate that the base path exists
    if not os.path.exists(base_path):
        print(f"❌ Error: Base path '{base_path}' does not exist!")
        print("💡 Please provide a valid directory path containing your CDS Group 6 repositories.")
        print("\nUsage examples:")
        print("  python3 git_status_checker.py /path/to/your/cds-group-6")
        print("  python3 git_status_checker.py ~/Documents/github/cds-9-group-6")
        print("  python3 git_status_checker.py ~/Projects/cds-9-group-6")
        sys.exit(1)
    
    if not os.path.isdir(base_path):
        print(f"❌ Error: '{base_path}' is not a directory!")
        sys.exit(1)
    
    print("🚀 Git Status Checker for CDS Group 6 Repositories")
    print(f"⏰ Scan started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Scanning: {base_path}")
    
    # Create checker instance and run scan
    checker = GitStatusChecker(base_path)
    checker.scan_repositories()
    checker.print_summary()
    
    # Ask if user wants to export to JSON
    try:
        export_choice = input("\n💡 Would you like to export results to JSON? (y/n): ").lower().strip()
        if export_choice in ['y', 'yes']:
            output_file = f"git_status_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            checker.export_to_json(output_file)
    except (EOFError, KeyboardInterrupt):
        print("\n💡 Skipping JSON export (non-interactive mode)")
        pass
    
    print("\n🎉 Scan completed!")

if __name__ == "__main__":
    main()
