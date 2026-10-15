# CLAUDE.md

> **NEVER use auto memory** (`~/.claude/projects/*/memory/`) — store all knowledge in this repo's CLAUDE.md file.


This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the **Tallyfy Denizen Assets Repository** - a carefully curated collection of location-specific images sourced from Unsplash for use in Tallyfy's Denizen service ecosystem. This repository serves as the static asset backend for the Denizen API (microservice located at `../denizen`), which provides geolocation-based images and greetings for Tallyfy's workflow automation platform.

### Business Context

**Tallyfy** is an AI-powered workflow management platform with four main products:
- **Tallyfy Pro** (flagship): Core workflow automation platform
- **Tallyfy Forms**: Document and form management 
- **Tallyfy Booking**: Appointment scheduling
- **Tallyfy Library**: Process template marketplace

**Denizen Service** provides hyperlocal imagery for user interfaces based on geographical location, enhancing user experience with contextually relevant visuals in landing pages, applications, and workflow interfaces.

### Repository Architecture

This repository works in conjunction with:
- `../denizen/`: Go-based microservice API that serves these images
- `../api-v2/`: Laravel-based main Tallyfy API
- `../client/`: Angular-based Tallyfy client application
- The Cloudflare Pages project `denizen-assets`, which publishes this repo at `denizen-images.tallyfy.com` (see Cloudflare Pages Distribution below). `../cloudflare-workers/` has no Denizen Worker.

The repository contains **398 curated images**, each in four sizes, across **38 countries**. Only the United States is covered city by city (44 cities); every other country is covered as a whole. Measured on 2026-10-15 at `c7d217b`.

## Commands

### Image Processing

#### Primary Resize Command
```bash
python resize_assets.py
```

This command processes all images in the `assets/` directory and creates three size variants:
- **Small**: 640x480 (using `PIL.thumbnail()` - preserves aspect ratio)
- **Medium**: 1920x1280 (using `PIL.thumbnail()` - preserves aspect ratio)
- **Large**: full size, not 2400x1600. The script calls `im.resize((2400, 1600))` but throws away the new image that call returns, so each large file is its source image saved again as a JPEG at the source's own width and height. Nothing is resized, cropped or distorted.

**The large variant stays full size on purpose**: the owner decided on 2026-10-12 to keep the 398 large files at full size and leave the script as it is (tallyfy/work-queue#3856). Switching to `im.thumbnail((2400, 1600))` would rewrite every large file in this public repo and change what the Denizen service serves as `asset_large`, so do not make that change without a new decision. Measured on 2026-10-12 at `fc27bc9`: all 42 sampled large files have exactly their source's width and height, none is 2400x1600, and none of the 398 large files is byte-identical to its source, because the save re-encodes it.

#### Resizing only some images
```bash
printf 'assets/US-NYC-1.jpg\n' > /tmp/new-images.txt
python resize_assets.py --files-from /tmp/new-images.txt
```

With `--files-from`, the script resizes only the images listed in the file, one `assets/<name>` path per line, and stages only their copies. An empty list resizes nothing. If any line is not a file directly in `assets/` that the script resizes, it refuses the whole list and changes nothing. Prefer this to the all-images command: a newer Pillow encodes the same picture to slightly different bytes, so redoing every image rewrites copies nobody changed (89 of them with Pillow 12.3.0, measured on 2026-10-09).

#### The Resize assets workflow
`.github/workflows/resize_assets.yaml` runs on every push to `main` that touches `assets/`, `resize_assets.py` or the workflow. It lists the images that push added or changed, by comparing the commit before the push with the one after, resizes only those with `--files-from`, and commits their copies as "Push variants". A push that changes no image ends green with no commit. A push that creates `main` or force-pushes it resizes nothing and fails on purpose, so resize its images by hand with `--files-from`.

#### Automation Scripts
```bash
# Generate task queue for batch operations
bash generate_image_tasks.sh

# Process automation queue with Claude
bash process_task_queue.sh
```

### Dependencies & Environment

#### Required Dependencies
- **Python 3.7+** with PIL/Pillow library
- **Git** for version control and automated staging
- **Claude CLI** for automation workflows (optional)

#### Installation
```bash
# Install Pillow
pip install Pillow

# For Claude automation (optional)
npm install -g @anthropic/claude-cli
```

## Architecture & Structure

### Directory Layout
```
denizen-assets/
├── assets/              # Source images (original Unsplash resolution)
├── assets-small/        # 640x480 variants (thumbnails, aspect ratio preserved)
├── assets-medium/       # 1920x1280 variants (thumbnails, aspect ratio preserved)
├── assets-large/        # full-size JPEG re-saves of the sources (not resized)
├── resize_assets.py     # Main image processing script
├── generate_image_tasks.sh  # Task queue generator for automation
├── process_task_queue.sh    # Claude automation processor
├── CLAUDE.md           # This file - AI development guidance
└── README.md           # Public repository documentation
```

### Image Naming Convention

**Two shapes.** Only United States images carry a city code.

- **Outside the United States**: `[COUNTRY_CODE]-[NUMBER].jpg`, such as `FR-3.jpg`. These images are chosen per country, so there is no city code.
- **United States**: `US-[CITY_CODE]-[NUMBER].jpg`, such as `US-NYC-1.jpg`.

Measured on 2026-10-15 at `c7d217b` with `git ls-tree`: `assets/` holds 398 images. 183 have the first shape across 37 country codes, 213 have the second across 44 city codes, one is `default.jpg`, and one is `US-HT-4.jpg.jpg`. No image outside the United States has a city code.

#### Country Codes
- **Outside the United States**: ISO 3166-1 alpha-2 codes (AR, AU, BD, BR, CA, CN, CO, DE, EG, ES, ET, FR, GB, ID, IN, IR, IT, JP, KE, KR, MA, MM, MX, MY, NG, NP, PH, PK, PL, RU, SA, TH, TR, TW, UA, VN, ZA)
- **United States**: `US`, always followed by a city code

#### City Codes (United States only)
Custom abbreviations, one per city, as `../denizen/microservice/mapping.json` uses them. They are city codes, not state codes: `US-AL` is Albuquerque, not Alabama.
- AL (Albuquerque), AR (Arlington), AT (Atlanta), AU (Austin), BA (Baltimore), BO (Boston), CH (Chicago), CHA (Charlotte), CO (Columbus), DA (Dallas), DE (Denver), DET (Detroit), FW (Fort Worth), HT (Houston), IN (Indianapolis), JA (Jacksonville), KC (Kansas City), LA (Los Angeles), LB (Long Beach), LV (Las Vegas), ME (Memphis), MI (Milwaukee), MIA (Miami), MIN (Minneapolis), NA (Nashville), NYC (New York City), OAK (Oakland), OKC (Oklahoma City), OM (Omaha), PHI (Philadelphia), PHO (Phoenix), PO (Portland), RA (Raleigh), SA (San Antonio), SAC (Sacramento), SD (San Diego), SE (Seattle), SF (San Francisco), SJ (San Jose), STL (St Louis, whose images the mapping also uses for Kirkwood), TU (Tulsa), TUC (Tucson), WA (Washington), WI (Wichita)

#### Numbering System
- **Range**: 1-5 images per location
- **Purpose**: Provides variety for dynamic content rotation
- **Gap Handling**: Missing numbers (e.g., AR-3.jpg missing) should be identified and filled

#### Special Files
- **`default.jpg`**: Fallback image present in each size directory
- **Naming Anomaly**: `US-HT-4.jpg.jpg` (double extension). Renaming it changes its public URL in all four folders and starts the Resize assets workflow, and `../denizen/microservice/mapping.json` has to name the file exactly as it is called here. So rename it only in step with a mapping change in denizen.

### Technical Implementation Details

#### Image Processing Pipeline

**Current Implementation** (the loop at the end of `resize_assets.py`):
```python
# Small variant - CORRECT: preserves aspect ratio
im.thumbnail((640, 480))  # PIL thumbnail method

# Medium variant - CORRECT: preserves aspect ratio  
im.thumbnail((1920, 1280))  # PIL thumbnail method

# Large variant - full size: resize() returns a new image, which the script
# discards, so the source is saved again at its own width and height
im.resize((2400, 1600))
```

The large variant stays full size by the owner's decision of 2026-10-12 (tallyfy/work-queue#3856), described under "Primary Resize Command" above. Do not switch it to `thumbnail()` without a new decision.

#### Git Integration
- **Automated Staging**: Script automatically runs `git add .` in each size directory
- **Command**: `os.system("cd assets-small && git add . && cd .. && cd assets-medium && git add . && cd .. && cd assets-large && git add .")`
- **Assumption**: Requires existing directory structure

#### Image Quality Considerations
- **Source Format**: JPEG compression from Unsplash
- **Output Format**: JPEG maintained throughout pipeline
- **Quality Loss**: Multiple resize operations may degrade quality
- **Best Practice**: Always resize from original `assets/` files, not from previously resized versions

#### Error Handling
- **Current State**: Minimal error handling in `resize_assets.py`
- **Missing Features**: No validation for corrupt images, naming conventions, or missing files
- **Recommended**: Add try-catch blocks and validation logic

### Development Environment

#### Repository Characteristics
- **No dependency management**: No `requirements.txt`, `Pipfile`, or `pyproject.toml`
- **No automated testing**: No test files or CI/CD configuration
- **No linting**: No `.pylintrc`, `flake8`, or black configuration
- **Simple structure**: Minimal tooling for rapid development

#### Git Workflow
- **Branching**: Single `main` branch (no feature branches)
- **Commit Pattern**: Recent commits focus on "variants", "batches", and "rule improvements"
- **Integration**: Works with Claude automation scripts for batch processing

### Critical Operational Notes

#### Adding New Images
1. **Placement**: Add source images to `assets/` directory only
2. **Naming**: Use `[COUNTRY_CODE]-[NUMBER].jpg`, or `US-[CITY_CODE]-[NUMBER].jpg` for a United States city (see Image Naming Convention)
3. **Processing**: Push to `main` and let the Resize assets workflow make the variants, or run `python resize_assets.py --files-from <a file listing the new images>`
4. **Verification**: Check that all three size directories contain the new images
5. **Git**: Variants are automatically staged by the script

#### Image Source Requirements
- **Origin**: Curated from Unsplash collections
- **Legal**: Must follow Unsplash API attribution requirements when accessed programmatically
- **Quality**: High-resolution source images preferred
- **Content**: Location-appropriate imagery representing cities/countries accurately

## AI Automation Framework

This repository implements a sophisticated AI-driven development approach using Claude Code for large-scale image processing and repository management. The automation framework is designed for handling batch operations across thousands of images.

### Automation Architecture

#### Core Philosophy
- **Atomic Operations**: Each task completes independently
- **Sequential Processing**: Tasks execute in numbered order
- **Stateless Design**: No dependencies between automation tasks
- **Fail-Fast**: Stop processing on errors to prevent data corruption

#### Task Queue System

**Generation Script** (`generate_image_tasks.sh`):
```bash
# Creates standardized .prompt files for Claude processing
# Pre-defined tasks:
# 001_analyze_images.prompt - Image audit and validation
# 002_create_metadata_script.prompt - Metadata extraction automation
# 003_optimize_resize.prompt - Performance improvements
# 004_create_validation.prompt - Quality assurance automation
```

**Processing Script** (`process_task_queue.sh`):
```bash
# Executes tasks with Claude CLI
# Features:
# - Sequential processing with error handling
# - Progress reporting
# - Automatic cleanup of completed tasks
# - Comprehensive logging
```

### Claude Code Integration Patterns

#### Non-Interactive Batch Processing
```bash
# Standard execution pattern
claude -p "$(cat task_file.prompt)" --dangerously-skip-permissions

# With error handling and logging
if claude -p "$(cat $prompt_file)" --dangerously-skip-permissions; then
    echo "✓ Completed: $(basename "$prompt_file")"
    rm "$prompt_file"
else
    echo "✗ Failed: $(basename "$prompt_file")"
    exit 1
fi
```

#### Task Template Examples

**Image Analysis Task**:
```
Analyze all images in the assets/ directory and create a summary report including:
1. Total number of images per country
2. Any missing city codes (gaps in numbering 1-5)
3. Any files that don't follow the naming convention
Output the report as a markdown table.
```

**Metadata Generation Task**:
```
Create a Python script called generate_metadata.py that:
1. Scans all images in assets/, assets-small/, assets-medium/, and assets-large/
2. Extracts metadata (dimensions, file size, creation date)
3. Outputs a JSON file with all image metadata organized by country and city
Use PIL for image processing and include error handling.
```

### Advanced Automation Capabilities

#### Large-Scale Operations

**Batch Image Processing**:
- Process 100+ images simultaneously
- Parallel validation across multiple size variants
- Automated quality assurance checks
- Git staging coordination

**Repository Maintenance**:
- Naming convention validation
- Missing file detection
- Duplicate image identification
- Metadata synchronization

#### Integration with Tallyfy Ecosystem

**Cross-Repository Operations**:
```bash
# Update mapping.json in ../denizen based on new images
# Sync with ../api-v2 image references
# Update ../client asset references
# Push to main, which the Cloudflare Pages project deploys (nothing to run by hand)
```

### Automation Best Practices

#### Task Design Principles
1. **Idempotent Operations**: Safe to run multiple times
2. **Clear Success Criteria**: Unambiguous completion indicators
3. **Comprehensive Logging**: Detailed operation tracking
4. **Rollback Capability**: Easy reversal of failed operations
5. **Validation Steps**: Verify results before completion

#### Error Handling Strategy
```bash
# Comprehensive error handling in automation scripts
set -e  # Exit on any error
set -u  # Exit on undefined variables
set -o pipefail  # Exit on pipe failures

# Progress tracking
echo "Processing $(ls task_queue/*.prompt | wc -l) tasks"

# Cleanup on exit
trap 'echo "Automation interrupted. Check task_queue/ for remaining tasks."' EXIT
```

#### Performance Optimization
- **Parallel Processing**: Multiple Claude instances for independent tasks
- **Batch Operations**: Group related tasks for efficiency
- **Resource Management**: Monitor system resources during large operations
- **Rate Limiting**: Respect API and system limits

### Integration with Related Repositories

#### Denizen Microservice Coordination
```bash
# Update mapping.json when new images are added
# Sync with ../denizen/microservice/mapping.json
# Validate image URLs match service expectations
# Test service endpoints after image updates
```

#### Cloudflare Pages Deployment
```bash
# A push to main deploys through the Cloudflare Pages project; no Worker is involved
# Read that push's Pages deployment until it succeeds
# Validate global availability after deployment
# Monitor performance metrics across regions
```

### Quality Assurance Automation

#### Automated Validation Suite
- **Image Integrity**: Validate all images can be opened by PIL
- **Naming Conventions**: Verify strict adherence to patterns
- **Size Consistency**: Ensure all variants exist for each source image
- **Aspect Ratio Verification**: Check for distorted images
- **Metadata Validation**: Verify geographic accuracy of image content

#### Continuous Monitoring
```bash
# Daily validation runs
# Performance benchmarking
# Repository health checks
# Integration testing with dependent services
```

## Development Workflows

### Standard Development Process

#### Adding New Images
1. **Source Acquisition**
   ```bash
   # Download high-resolution images from Unsplash
   # Ensure proper licensing and attribution
   # Verify geographical accuracy
   ```

2. **File Preparation**
   ```bash
   # Rename to [COUNTRY_CODE]-[NUMBER].jpg, or US-[CITY_CODE]-[NUMBER].jpg for a US city
   # Place in assets/ directory
   # Verify image quality and content appropriateness
   ```

3. **Processing Pipeline**
   ```bash
   # Run resize script on the new images only (one assets/<name> path per line)
   python resize_assets.py --files-from new-images.txt
   
   # Verify all variants created
   ls assets-small/ assets-medium/ assets-large/
   
   # Check git staging
   git status
   ```

4. **Quality Validation**
   ```bash
   # Manual verification of all variants
   # Check for aspect ratio preservation
   # Verify naming consistency
   ```

#### Batch Operations
```bash
# For large batches (50+ images)
# 1. Use automation framework
bash generate_image_tasks.sh
bash process_task_queue.sh

# 2. Monitor progress
tail -f /tmp/claude_automation.log

# 3. Validate results
python validate_batch_results.py
```

### Code Modification Guidelines

#### Improving resize_assets.py
```python
# The large variant: resize() returns a new image that the script discards,
# so each large file keeps its source's full size. The owner chose on
# 2026-10-12 to keep it that way (tallyfy/work-queue#3856), so leave this line.
im.resize((2400, 1600))

# Additional enhancements needed:
# - Add progress bars with tqdm
# - Implement parallel processing
# - Add comprehensive error handling
# - Create processing logs
# - Validate input/output
```

#### Error Handling Implementation
```python
import logging
from pathlib import Path
from PIL import Image, ImageOps

def safe_image_resize(input_path, output_path, size, method='thumbnail'):
    \"\"\"
    Safely resize image with comprehensive error handling
    \"\"\"
    try:
        with Image.open(input_path) as img:
            if method == 'thumbnail':
                img.thumbnail(size, Image.Resampling.LANCZOS)
            else:
                img = img.resize(size, Image.Resampling.LANCZOS)
            
            img.save(output_path, 'JPEG', quality=95, optimize=True)
            logging.info(f\"Successfully processed: {input_path} -> {output_path}\")
            return True
    except Exception as e:
        logging.error(f\"Failed to process {input_path}: {str(e)}\")
        return False
```

### Integration Patterns

#### Denizen Microservice Integration

The images in this repository are consumed by the Go-based Denizen microservice located at `../denizen/`. Understanding this integration is crucial for development:

**Service Architecture** (`../denizen/microservice/main.go`):
```go
// Loads mapping.json which references images in this repository
func loadMapping() {
    file, _ := ioutil.ReadFile(\"mapping.json\")
    err := json.Unmarshal([]byte(file), &routes.Mapping)
}

// Routes that serve images from this repository
// / - Redirects to location-specific image
// /text - Returns greeting text
// /data - Returns metadata
```

**Image URL Generation**:
```go
// Base URL points to this repository's assets
BASE_ASSETS_URL := \"https://denizen-images.tallyfy.com/assets-medium/\"
imageURL := BASE_ASSETS_URL + imageFilename
```

**Critical Dependencies**:
- Image filenames in `mapping.json` must exactly match files in this repository
- URL paths must be consistent with directory structure
- Image availability directly affects service uptime

#### Cloudflare Pages Distribution

Images ship through the Cloudflare Pages project `denizen-assets`, not a Worker. The project is connected to this GitHub repo with `main` as its production branch, no build command and no path filter, so every push to `main` publishes the whole repo, docs included, to `denizen-images.tallyfy.com` and `denizen-assets.pages.dev`. There is nothing to deploy by hand. Read on 2026-10-15 from the Cloudflare Pages API: the latest production deployment was triggered by `github:push` for commit `c7d217b`. `../cloudflare-workers/` has no Denizen Worker and no `denizen` folder.

**Edge Caching Strategy**:
- Assets cached at edge locations worldwide
- Cache invalidation required after image updates
- Geographic routing for optimal performance

**Deployment Coordination**:
```bash
# After pushing to main, read the Pages deployment for that commit until it succeeds,
# then verify global availability
curl -I https://denizen-images.tallyfy.com/assets-medium/US-NYC-1.jpg
```

### Performance Considerations

#### Image Optimization

**Current Limitations**:
- No progressive JPEG encoding
- No WebP format generation for modern browsers
- No responsive image serving (srcset)
- Limited compression optimization

#### Repository Size Management

**Current State**:
- Repository size: ~2.5GB (measured 2026-10-15: 2.33 GiB packed, for 398 images in each of the four folders)
- Git LFS not implemented
- Large binary files in main repository


### Security & Legal Compliance

#### Unsplash Attribution Requirements

**API Usage** (when programmatically accessing Unsplash):
```markdown
Photo by [Photographer Name](photographer_url) on [Unsplash](https://unsplash.com/)
```

**Legal Considerations**:
- Commercial use permitted under Unsplash License
- Attribution required when using Unsplash API
- Cannot replicate competing image service
- No rights to trademarks/people appearing in photos

#### Content Validation


### Monitoring & Analytics

#### Repository Health Metrics

**Key Performance Indicators**:
- Image processing time per batch
- Error rates during resize operations
- Repository size growth rate
- Missing image detection frequency
- Integration test success rates


### Troubleshooting Guide

#### Common Issues & Solutions

**Issue**: `resize_assets.py` fails with PIL errors
```bash
# Solution: Verify PIL installation and image integrity
pip install --upgrade Pillow
python -c \"from PIL import Image; print('PIL working')\"

# Check for corrupt images
for img in assets/*.jpg; do
    python -c \"from PIL import Image; Image.open('$img').verify()\" || echo \"Corrupt: $img\"
done
```

**Issue**: Git staging fails in automation scripts
```bash
# Solution: Verify directory structure and permissions
ls -la assets-*/ || mkdir -p assets-small assets-medium assets-large
chmod +w assets-*/ 
```

**Issue**: Missing images in Denizen service
```bash
# Solution: list every name mapping.json uses that assets/ on origin/main lacks.
# Run from this repo's root, with tallyfy/denizen cloned beside it, after fetching both.
# The control name is made up each run and must always be printed, which proves the check can fail.
ctl="ZZ-$RANDOM$RANDOM.jpg"
comm -23 \
  <( { jq -r '.[] | (.images[]?.url), (.cities[]?.images[]?.url)' ../denizen/microservice/mapping.json; echo "$ctl"; } | LC_ALL=C sort -u ) \
  <( git ls-tree --name-only origin/main assets/ | sed 's|^assets/||' | LC_ALL=C sort -u )
# A clean result prints only the control name. Any other line is a missing image.
```

**Issue**: Large repository clone times
```bash
# Solution: Implement shallow clones for development
git clone --depth 1 https://github.com/tallyfy/denizen-assets.git

# Or use sparse checkout for specific directories
git config core.sparseCheckout true
echo \"assets-medium/\" > .git/info/sparse-checkout
git read-tree -m -u HEAD
```

### Advanced Development Patterns

#### Multi-Repository Coordination

```bash
# Coordinate changes across related repositories
function update_denizen_ecosystem() {
    # 1. Add the new images to assets/ and push to main. The Resize assets workflow
    #    makes their variants, and the Cloudflare Pages project deploys the push.
    #    There is no Worker to deploy.

    # 2. Check that the new images answer on the image host
    curl -I https://denizen-images.tallyfy.com/assets-medium/US-NYC-1.jpg

    # 3. Only then name them in ../denizen/microservice/mapping.json, through a pull
    #    request in denizen (see its CLAUDE.md). A merge there deploys the service.
    #    api-v2 has no Denizen integration test; its login and register pages call
    #    denizen.tallyfy.com/data, so check one of those pages afterwards.
}
```

#### Automated Testing Framework

```python
# Comprehensive test suite for repository integrity
import unittest
from pathlib import Path
from PIL import Image

class DenizenAssetsTestSuite(unittest.TestCase):
    
    def test_naming_conventions(self):
        \"\"\"Verify all images follow naming convention\"\"\"
        pattern = re.compile(r'^(US-[A-Z]+|[A-Z]{2})-[1-5]\.jpg$')
        for image_path in Path('assets').glob('*.jpg'):
            self.assertTrue(pattern.match(image_path.name))
    
    def test_variant_completeness(self):
        \"\"\"Ensure all source images have corresponding variants\"\"\"
        source_images = set(p.name for p in Path('assets').glob('*.jpg'))
        for variant_dir in ['assets-small', 'assets-medium', 'assets-large']:
            variant_images = set(p.name for p in Path(variant_dir).glob('*.jpg'))
            self.assertEqual(source_images, variant_images)
    
    def test_image_integrity(self):
        \"\"\"Validate all images can be opened and processed\"\"\"
        for image_path in Path('assets').glob('*.jpg'):
            with Image.open(image_path) as img:
                self.assertGreater(img.width, 0)
                self.assertGreater(img.height, 0)
                self.assertEqual(img.format, 'JPEG')
```

## General Coding Practices

When modifying or extending this repository:

- **Reuse existing code**: Don't create new functions or scripts if you can extend or augment existing ones. The `resize_assets.py` script should be enhanced rather than replaced.
- **Consider shared libraries**: When adding functionality that could be used across multiple Tallyfy repositories, design it as a reusable component.
- **Document your code**: Add clear comments explaining why functions exist and what they do, especially for image processing logic that may not be immediately obvious.
- **Update documentation**: Always update CLAUDE.md and cursor rules files after any code changes to keep AI assistance current with the codebase state.
## 🔗 AI reference doc (consolidated from Cursor rules, 2026-06-04)

This CLAUDE.md is the single source of truth. Reference (path relative to repo root):
- reference/development-standards.md — image validations, error-handling templates, testing, branch/quality workflow
