#!/usr/bin/env python3
"""Export script - creates a distributable zip of the web/ folder."""

import shutil
import zipfile
from pathlib import Path
from datetime import datetime


def export(output_name: str = None):
    """
    Create distributable zip of web/ folder:
    - index.html
    - css/styles.css
    - js/app.js
    - spots/*.html + *.json
    """
    project_dir = Path(__file__).parent
    export_dir = project_dir / "export"
    web_dir = project_dir / "web"
    spots_dir = web_dir / "spots"

    # Check if spots exist (now in subfolders like 25bb/, 20bb/, etc.)
    html_files = list(spots_dir.glob("**/*.html")) if spots_dir.exists() else []
    if not html_files:
        print("ERROR: No spot files found in web/spots/")
        print("Run 'python fetch.py <TOKEN>' first to fetch data.")
        return None

    # Create export directory
    export_dir.mkdir(exist_ok=True)

    # Generate output name with timestamp if not provided
    if not output_name:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_name = f"poker_spins_{timestamp}"

    zip_path = export_dir / f"{output_name}.zip"

    print(f"Creating export: {zip_path}")
    print("=" * 40)

    # Count files
    json_files = list(spots_dir.glob("**/*.json"))
    print(f"Spots: {len(html_files)} HTML + {len(json_files)} JSON")

    # Create zip directly from web/ folder
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in web_dir.rglob('*'):
            if file_path.is_file():
                # Archive path relative to web/ folder
                arcname = file_path.relative_to(web_dir)
                zf.write(file_path, arcname)

    print("")
    print("=" * 40)
    print(f"Export complete: {zip_path}")
    print(f"Size: {zip_path.stat().st_size / 1024:.1f} KB")
    print("")
    print("To use: unzip and open index.html in a browser")

    return zip_path


if __name__ == "__main__":
    import sys

    output_name = sys.argv[1] if len(sys.argv) > 1 else None
    export(output_name)
