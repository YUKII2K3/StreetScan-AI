#!/usr/bin/env python3
"""
GitHub Push Helper Script
Automatically pushes the RTSP Vehicle Detection System to GitHub.

Crafted by Yukthesh - Building intelligent solutions for the future
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def main():
    """Main function to push to GitHub."""
    print("🚀 GitHub Push Helper - Crafted by Yukthesh")
    print("=" * 60)
    
    # Get GitHub details from user
    print("Please provide your GitHub details:")
    username = input("GitHub Username: ").strip()
    repo_name = input("Repository Name (e.g., StreetScan-AI): ").strip()
    
    if not username or not repo_name:
        print("❌ Username and repository name are required!")
        return
    
    # Set up remote repository
    remote_url = f"https://github.com/{username}/{repo_name}.git"
    
    print(f"\n📋 Repository Details:")
    print(f"   Username: {username}")
    print(f"   Repository: {repo_name}")
    print(f"   Remote URL: {remote_url}")
    
    # Confirm with user
    confirm = input("\nProceed with pushing to GitHub? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Push cancelled by user")
        return
    
    # Add remote
    result = run_command(f"git remote add origin {remote_url}", "Adding remote repository")
    if not result:
        print("⚠️  Remote might already exist, continuing...")
        run_command("git remote set-url origin " + remote_url, "Updating remote URL")
    
    # Push to GitHub
    result = run_command("git push -u origin master", "Pushing to GitHub")
    if result:
        print("\n🎉 Successfully pushed to GitHub!")
        print(f"📖 View your repository at: https://github.com/{username}/{repo_name}")
        print("\n🎨 Your RTSP Vehicle Detection System is now live with Yukthesh branding!")
    else:
        print("\n❌ Failed to push to GitHub. Please check:")
        print("1. Repository exists on GitHub")
        print("2. You have write permissions")
        print("3. Your GitHub credentials are correct")

if __name__ == "__main__":
    main() 