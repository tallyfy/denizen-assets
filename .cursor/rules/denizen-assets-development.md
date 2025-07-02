# Denizen Assets Development Rules

## Repository Overview

This repository contains curated city images for Tallyfy's Denizen service ecosystem. You are working with a static asset repository that serves geolocation-based images to Tallyfy's workflow automation platform.

**Critical Context:**
- Repository contains 1,000+ images across 40+ countries 
- Images are processed into 3 size variants (small/medium/large)
- Integrates with Go-based Denizen microservice at ../denizen/
- Deployed globally via Cloudflare Workers
- Part of Tallyfy's AI-powered workflow platform

## Core Development Principles

### Image Processing Standards
- **ALWAYS** preserve aspect ratios for ALL size variants
- Use `PIL.thumbnail()` method, NOT `PIL.resize()` for dimension control
- Process images from original `assets/` directory only
- Maintain JPEG format with 90%+ quality
- Implement comprehensive error handling for batch operations

### Naming Convention Enforcement
**Strict Pattern**: `[COUNTRY_CODE]-[CITY_CODE]-[NUMBER].jpg`

Examples:
- ✅ `US-NYC-1.jpg` (US New York City, image 1)
- ✅ `FR-PAR-3.jpg` (France Paris, image 3)
- ✅ `GB-LON-5.jpg` (Great Britain London, image 5)
- ❌ `newyork1.jpg` (incorrect format)
- ❌ `US_NYC_1.jpg` (wrong separator)

**Special Cases:**
- US states use format: `US-[STATE_CODE]-[NUMBER].jpg`
- Numbers range from 1-5 per location
- `default.jpg` exists as fallback in each size directory

### Repository Structure Requirements
```
assets/          # Source images (original resolution)
assets-small/    # 640x480 variants  
assets-medium/   # 1920x1280 variants
assets-large/    # 2400x1600 variants (fix aspect ratio distortion)
```

## Code Modification Guidelines

### When Editing resize_assets.py
**Current Problem** (Line 22-24):
```python
im.resize((2400, 1600))  # BAD: Forces exact dimensions, distorts images
```

**Required Fix**:
```python
im.thumbnail((2400, 1600))  # GOOD: Preserves aspect ratio
```

**Enhanced Implementation Pattern**:
```python
def safe_image_resize(input_path, output_path, size, method='thumbnail'):
    try:
        with Image.open(input_path) as img:
            if method == 'thumbnail':
                img.thumbnail(size, Image.Resampling.LANCZOS)
            else:
                img = img.resize(size, Image.Resampling.LANCZOS)
            
            img.save(output_path, 'JPEG', quality=95, optimize=True)
            return True
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False
```

### Automation Script Standards
- Use task queue pattern for batch operations
- Implement progress tracking with clear output
- Add comprehensive error handling and rollback
- Validate all operations before git staging
- Follow atomic operation principles

### Integration Awareness
**Critical Dependencies:**
- Image filenames must match entries in `../denizen/microservice/mapping.json`
- URL paths must be consistent with Cloudflare Workers configuration
- Changes affect live Denizen API service endpoints
- Updates require coordination with related repositories

## Required Validations

### Before Committing Code
1. **Image Integrity Check**:
   ```python
   from PIL import Image
   for img_path in new_images:
       Image.open(img_path).verify()  # Ensure not corrupt
   ```

2. **Naming Convention Validation**:
   ```python
   import re
   pattern = r'^[A-Z]{2}(-[A-Z0-9]+)?-[1-5]\.jpg$'
   assert re.match(pattern, filename), f"Invalid filename: {filename}"
   ```

3. **Variant Completeness**:
   ```bash
   # Ensure all variants exist for each source image
   source_count=$(ls assets/*.jpg | wc -l)
   small_count=$(ls assets-small/*.jpg | wc -l)
   medium_count=$(ls assets-medium/*.jpg | wc -l) 
   large_count=$(ls assets-large/*.jpg | wc -l)
   # All counts must be equal
   ```

4. **Aspect Ratio Verification**:
   ```python
   def check_aspect_ratios(source_path, variant_paths):
       source_ratio = get_aspect_ratio(source_path)
       for variant in variant_paths:
           variant_ratio = get_aspect_ratio(variant)
           assert abs(source_ratio - variant_ratio) < 0.01, "Aspect ratio distorted"
   ```

## Performance Requirements

### Repository Size Management
- Monitor repo size (currently ~2.5GB)
- Consider Git LFS for large binary files
- Implement compression optimization for new images
- Use progressive JPEG encoding when possible

### Processing Efficiency  
- Implement parallel processing for batch operations
- Add progress indicators using tqdm or similar
- Cache intermediate results when appropriate
- Optimize for minimal memory usage during batch processing

## Security & Legal Compliance

### Unsplash Attribution
When adding new images from Unsplash API:
```markdown
Photo by [Photographer Name](photographer_url) on [Unsplash](https://unsplash.com/)
```

### Content Validation
- Verify geographical accuracy of images
- Ensure appropriate content for business use
- Validate licensing compliance
- Check for trademark/recognizable person restrictions

## Error Handling Patterns

### Robust File Operations
```python
import logging
from pathlib import Path

def process_image_batch(image_paths):
    success_count = 0
    errors = []
    
    for path in image_paths:
        try:
            if process_single_image(path):
                success_count += 1
            else:
                errors.append(f"Processing failed: {path}")
        except Exception as e:
            errors.append(f"Exception in {path}: {str(e)}")
    
    logging.info(f"Processed {success_count}/{len(image_paths)} images")
    if errors:
        logging.error(f"Errors encountered: {errors}")
    
    return success_count == len(image_paths)
```

### Git Operations Safety
```bash
# Always verify git operations succeed
if ! git add assets-small/ assets-medium/ assets-large/; then
    echo "Error: Git staging failed"
    exit 1
fi

# Check for uncommitted changes
if [[ -n $(git status --porcelain) ]]; then
    echo "Warning: Uncommitted changes detected"
fi
```

## Testing Requirements

### Automated Test Suite
Create comprehensive tests covering:
- Image integrity validation
- Naming convention compliance  
- Variant completeness verification
- Aspect ratio preservation
- Integration with Denizen service

### Manual Verification Steps
1. Visual inspection of resized images
2. Verification of geographic accuracy
3. Check integration with Denizen API endpoints
4. Validate global CDN availability

## Integration Coordination

### Multi-Repository Updates
When making changes, coordinate with:
1. `../denizen/` - Update mapping.json if adding new locations
2. `../cloudflare-workers/denizen/` - Deploy asset updates
3. `../api-v2/` - Run integration tests
4. `../client/` - Verify UI rendering with new assets

### Deployment Checklist
- [ ] Images processed and validated locally
- [ ] All variants generated successfully
- [ ] Git commits include proper descriptions
- [ ] Denizen service mapping updated if needed
- [ ] Cloudflare Workers deployment triggered
- [ ] Integration tests passing
- [ ] Global CDN availability verified

## Troubleshooting Quick Reference

**Common Issues:**
- PIL installation problems → `pip install --upgrade Pillow`
- Git staging failures → Check directory permissions and structure
- Aspect ratio distortion → Use `thumbnail()` instead of `resize()`
- Missing variants → Run full `resize_assets.py` script
- Integration failures → Verify mapping.json synchronization

**Emergency Rollback:**
```bash
git reset --hard HEAD~1  # Rollback last commit
python resize_assets.py   # Regenerate variants
git add . && git commit -m "Rollback and regenerate variants"
```

## Development Workflow Standards

### Feature Development
1. Work directly on main branch (no feature branches)
2. Make atomic commits with clear descriptions
3. Test locally before committing
4. Coordinate with related repositories
5. Monitor service health after deployment

### Code Quality
- Follow Python PEP 8 standards
- Add comprehensive error handling
- Include progress indicators for long operations
- Write clear, descriptive commit messages
- Document complex image processing logic

This file ensures Cursor IDE provides optimal assistance for developing within the Denizen Assets repository while maintaining consistency with Claude Code's guidance.