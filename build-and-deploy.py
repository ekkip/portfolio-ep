#!/usr/bin/env python3
"""
Build and deploy script for portfolio
Compiles Tailwind and copies files to cloud folder with cache-busting version numbers
"""

import os
import shutil
import subprocess
import re
from pathlib import Path
from datetime import datetime

SOURCE_DIR = Path(__file__).resolve().parent
TARGET_DIR = Path(
    os.environ.get(
        "DEPLOY_TARGET",
        "/Users/ekki/Library/CloudStorage/CloudMounter-Programmator/portfolio23",
    )
)

def build_tailwind():
    """Compile Tailwind CSS"""
    print("Building Tailwind CSS...")
    os.chdir(SOURCE_DIR)
    subprocess.run(
        ["npm", "run", "build:css"],
        check=True,
        cwd=SOURCE_DIR,
    )

def add_version_to_css_links(content, version):
    """Add or update version number in CSS links"""
    # Pattern to match CSS links with or without existing version
    # Handle absolute paths (/customStyle.css, /dist/output.css)
    patterns = [
        (r'href="(/customStyle\.css)(\?[^"]*)?(")', rf'href="\1?v={version}\3'),
        (r'href="(/dist/output\.css)(\?[^"]*)?(")', rf'href="\1?v={version}\3'),
        # Also handle relative paths in case any remain
        (r'href="(\./customStyle\.css)(\?[^"]*)?(")', rf'href="\1?v={version}\3'),
        (r'href="(\./dist/output\.css)(\?[^"]*)?(")', rf'href="\1?v={version}\3'),
        (r'href="(\.\./customStyle\.css)(\?[^"]*)?(")', rf'href="\1?v={version}\3'),
        (r'href="(\.\./dist/output\.css)(\?[^"]*)?(")', rf'href="\1?v={version}\3'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    return content

def copy_and_version_files():
    """Copy files and add version numbers to HTML files"""
    # Generate version number (timestamp)
    version = int(datetime.now().timestamp())
    print(f"Copying files to cloud folder with version {version}...")
    
    # Copy CSS and assets
    for item in ['dist', 'customStyle.css', 'img', 'fonts', 'video']:
        src = SOURCE_DIR / item
        dst = TARGET_DIR / item
        if src.exists():
            if src.is_dir():
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
    
    # Copy and update root HTML files
    for html_file in SOURCE_DIR.glob("*.html"):
        if html_file.is_file():
            dst_file = TARGET_DIR / html_file.name
            content = html_file.read_text(encoding='utf-8')
            content = add_version_to_css_links(content, version)
            dst_file.write_text(content, encoding='utf-8')
    
    # Copy and update project HTML files
    projects_src = SOURCE_DIR / "projects"
    projects_dst = TARGET_DIR / "projects"
    
    if projects_src.exists():
        if projects_dst.exists():
            shutil.rmtree(projects_dst)
        shutil.copytree(projects_src, projects_dst)
        
        # Update CSS links in project HTML files
        for html_file in projects_dst.glob("*.html"):
            content = html_file.read_text(encoding='utf-8')
            content = add_version_to_css_links(content, version)
            html_file.write_text(content, encoding='utf-8')
    
    print(f"Build complete! Files copied to: {TARGET_DIR}")
    print(f"CSS files now have version ?v={version} for cache-busting")

if __name__ == "__main__":
    build_tailwind()
    copy_and_version_files()
