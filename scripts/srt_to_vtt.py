#!/usr/bin/env python3
import sys
from pathlib import Path
import re
import shutil

def convert(path: Path):
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
    out_lines = []

    timestamp_re = re.compile(r"^(\s*\d{2}:\d{2}:\d{2}),(\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}),(\d{3}).*$")

    for line in lines:
        # skip index lines that contain only digits (SRT numbering)
        if line.strip().isdigit():
            continue
        # Convert SRT-style timestamps (commas) to WebVTT-style (periods)
        m = timestamp_re.match(line)
        if m:
            # replace commas with dots only for the timestamp section
            left = m.group(1) + '.' + m.group(2)
            right = m.group(3) + '.' + m.group(4)
            line = f"{left} --> {right}"
        out_lines.append(line)

    # Ensure header
    if not out_lines or not out_lines[0].strip().startswith('WEBVTT'):
        out_lines.insert(0, '')
        out_lines.insert(0, 'WEBVTT')

    # Backup original
    backup = path.with_suffix(path.suffix + '.bak')
    shutil.copy2(path, backup)

    # Write cleaned file (ensure trailing newline)
    path.write_text('\n'.join(out_lines) + '\n', encoding='utf-8')
    print(f'Converted and wrote: {path}\nBackup created: {backup}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: srt_to_vtt.py input-file')
        sys.exit(1)
    p = Path(sys.argv[1])
    if not p.exists():
        print(f'File not found: {p}')
        sys.exit(1)
    convert(p)
