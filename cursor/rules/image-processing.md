# Image Processing Rules

## Core Principles

When working with image processing in the Denizen Assets repository:

1. **Always preserve originals**: Never modify files in the `assets/` directory directly. This is the source of truth.

2. **Use existing scripts**: Enhance `resize_assets.py` rather than creating new processing scripts.

3. **Maintain consistency**: All image variants must follow the same naming convention as their source.

## Technical Guidelines

### Image Resizing
- Small variants: 640x480 using PIL thumbnail (preserves aspect ratio)
- Medium variants: 1920x1280 using PIL thumbnail (preserves aspect ratio)
- Large variants: 2400x1600 (currently uses resize - be aware of potential distortion)

### File Naming
- Strict pattern: `[COUNTRY_CODE]-[CITY_CODE]-[NUMBER].jpg`
- Country codes: ISO 3166-1 alpha-2 for international, state-specific for US
- Numbers: 1-5 per location
- Special case: `default.jpg` as fallback

### Quality Standards
- Source images: High-resolution from Unsplash
- Output format: JPEG
- Processing: Always from original source, never from variants

## Automation

When using automation scripts:
- `generate_image_tasks.sh`: Creates task queue for batch operations
- `process_task_queue.sh`: Executes tasks with Claude CLI
- Ensure atomic operations that can be safely re-run

## Git Integration

The resize script automatically stages variants:
- Runs `git add .` in each size directory
- Assumes directory structure exists
- Does not commit - manual review required

## General Coding Practices

- **Reuse existing code**: Don't create new functions or scripts if you can extend or augment existing ones
- **Consider shared libraries**: Design reusable components for cross-repository use
- **Document your code**: Add clear comments explaining why functions exist and what they do
- **Update documentation**: Always update CLAUDE.md and cursor rules files after any code changes