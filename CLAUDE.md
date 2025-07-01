# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the Tallyfy Denizen assets repository - a curated collection of city images from Unsplash for use in the Denizen service. The repository contains static image assets organized by size variants.

## Commands

### Image Resizing
```bash
python resize_assets.py
```
This command processes all images in the `assets/` directory and creates three size variants:
- **Small**: 640x480 (thumbnail)
- **Medium**: 1920x1280 (thumbnail)
- **Large**: 2400x1600 (resize - note: this may distort aspect ratio)

After resizing, the script automatically stages the new files in git.

### Dependencies
- Python with PIL/Pillow library installed

## Architecture & Structure

### Directory Layout
- `assets/` - Source images (original size)
- `assets-small/` - Images resized to max 640x480
- `assets-medium/` - Images resized to max 1920x1280
- `assets-large/` - Images resized to 2400x1600

### Image Naming Convention
Images follow the pattern: `[COUNTRY_CODE]-[CITY_CODE]-[NUMBER].jpg`
- Country codes: ISO 2-letter codes (US, GB, FR, etc.)
- City codes: Custom abbreviations (NYC, LA, LON, PAR, etc.)
- Numbers: 1-5 for each city (multiple images per location)
- Special: `default.jpg` exists in each size directory

### Key Technical Details
1. The resize script (`resize_assets.py`) uses PIL's `thumbnail()` method for small/medium sizes (preserves aspect ratio) but uses `resize()` for large (may distort).
2. The script includes git staging commands that assume a specific directory structure.
3. No automated tests or linting configuration exists.
4. No dependency management files - PIL/Pillow must be manually installed.

### Important Notes
- When adding new images, place them in the `assets/` directory and run the resize script
- Ensure new images follow the naming convention
- The large size variant uses fixed dimensions (2400x1600) which may distort images

## AI Automation Approach

This codebase supports automated workflows using Claude's non-interactive mode. Complex tasks should be broken down into atomic, single-purpose operations that can be executed sequentially.

### Non-Interactive Execution Pattern
```bash
claude -p "YOUR_PROMPT_HERE" --dangerously-skip-permissions
```

### File-Based Task Queue Pattern
For large-scale operations (e.g., processing hundreds of images or updating metadata), use a file-based queue:

1. Create a `task_queue/` directory
2. Add `.prompt` files with specific tasks (numbered for order)
3. Process queue with a script that executes and removes completed tasks

Example automation for batch image processing:
```bash
# Generate task queue
mkdir -p task_queue
echo "Analyze all images in assets/ and identify any that don't follow naming conventions" > task_queue/001_analyze.prompt
echo "Create a resize script for images in assets/new/ with proper error handling" > task_queue/002_resize_new.prompt
echo "Generate metadata JSON for all images including dimensions and file sizes" > task_queue/003_metadata.prompt

# Process queue
for prompt_file in task_queue/*.prompt; do
    claude -p "$(cat $prompt_file)" --dangerously-skip-permissions
    rm "$prompt_file"  # Remove completed task
done
```

### Best Practices for Automation
1. Each task should complete independently without requiring state from previous tasks
2. Use specific file paths and clear success criteria in prompts
3. Include validation steps after generation tasks
4. Keep prompts atomic and focused on a single outcome