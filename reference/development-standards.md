# Denizen Assets — Development Standards

> Reference for denizen-assets — the single source of truth is CLAUDE.md at the repo root. Image-integrity / naming / variant / aspect-ratio validation rules, Python error-handling templates, the automated test framework, and the branch + code-quality workflow.

This file collects the operational standards that are NOT already covered in the root `CLAUDE.md`. For repository overview, the resize pipeline, the `safe_image_resize()` enhancement template, the `DenizenAssetsTestSuite` unittest example, Unsplash attribution, and cross-repo integration, read `CLAUDE.md` first — those are not repeated here.

---

## Pre-Commit Validations

Run these checks before committing any image or code change. They are the concrete, copy-paste versions of the "Quality Assurance" goals described in `CLAUDE.md`.

### 1. Image Integrity Check

Ensure no image is corrupt before it enters the pipeline:

```python
from PIL import Image
for img_path in new_images:
    Image.open(img_path).verify()  # Ensure not corrupt
```

### 2. Naming Convention Validation

Enforce the strict `[COUNTRY_CODE]-[CITY_CODE]-[NUMBER].jpg` pattern programmatically:

```python
import re
pattern = r'^[A-Z]{2}(-[A-Z0-9]+)?-[1-5]\.jpg$'
assert re.match(pattern, filename), f"Invalid filename: {filename}"
```

Examples of correct vs. incorrect names:

- ✅ `US-NYC-1.jpg` (US New York City, image 1)
- ✅ `FR-PAR-3.jpg` (France Paris, image 3)
- ✅ `GB-LON-5.jpg` (Great Britain London, image 5)
- ❌ `newyork1.jpg` (incorrect format)
- ❌ `US_NYC_1.jpg` (wrong separator)

Special cases:
- US states use the format `US-[STATE_CODE]-[NUMBER].jpg`
- Numbers range from 1–5 per location
- `default.jpg` exists as a fallback in each size directory

### 3. Variant Completeness

Every source image must have a corresponding small/medium/large variant. All four counts must be equal:

```bash
# Ensure all variants exist for each source image
source_count=$(ls assets/*.jpg | wc -l)
small_count=$(ls assets-small/*.jpg | wc -l)
medium_count=$(ls assets-medium/*.jpg | wc -l)
large_count=$(ls assets-large/*.jpg | wc -l)
# All counts must be equal
```

### 4. Aspect Ratio Verification

The large variant historically used `PIL.resize()` (forces exact 2400x1600, distorts). Verify variants preserve the source aspect ratio within tolerance:

```python
def check_aspect_ratios(source_path, variant_paths):
    source_ratio = get_aspect_ratio(source_path)
    for variant in variant_paths:
        variant_ratio = get_aspect_ratio(variant)
        assert abs(source_ratio - variant_ratio) < 0.01, "Aspect ratio distorted"
```

---

## Image Processing Standards

- **ALWAYS** preserve aspect ratios for ALL size variants.
- Use `PIL.thumbnail()`, NOT `PIL.resize()`, for dimension control.
- Process images from the original `assets/` directory only — never re-resize an already-resized variant (compounds quality loss).
- Maintain JPEG format with 90%+ quality.
- Implement comprehensive error handling for batch operations.

Repository structure the pipeline depends on:

```
assets/          # Source images (original resolution)
assets-small/    # 640x480 variants
assets-medium/   # 1920x1280 variants
assets-large/    # 2400x1600 variants (fix aspect ratio distortion)
```

---

## Python Error-Handling Templates

### Batch Processing with Per-Item Error Capture

Use this pattern for any operation over a list of images — it isolates per-file failures, counts successes, and logs every error rather than aborting the whole batch on the first exception:

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

Image processing scripts auto-stage variants. Always verify the staging command succeeded, and warn on unexpected uncommitted changes:

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

---

## Automated Test Suite — Coverage Requirements

The automated test suite must cover:

- Image integrity validation
- Naming convention compliance
- Variant completeness verification
- Aspect ratio preservation
- Integration with the Denizen service

> The reference `unittest` implementation (`DenizenAssetsTestSuite` with `test_naming_conventions`, `test_variant_completeness`, `test_image_integrity`) lives in the root `CLAUDE.md`. Use that as the starting point and extend it to cover the aspect-ratio and Denizen-integration cases above.

### Manual Verification Steps

1. Visual inspection of resized images
2. Verification of geographic accuracy
3. Check integration with Denizen API endpoints
4. Validate global CDN availability

---

## Branch Strategy & Code-Quality Workflow

### Feature Development

1. Work directly on the `main` branch (no feature branches).
2. Make atomic commits with clear descriptions.
3. Test locally before committing.
4. Coordinate with related repositories (see below).
5. Monitor service health after deployment.

### Code Quality

- Follow Python PEP 8 standards.
- Add comprehensive error handling.
- Include progress indicators for long operations.
- Write clear, descriptive commit messages.
- Document complex image-processing logic.

### Multi-Repository Coordination

When making changes, coordinate with:

1. `../denizen/` — update `mapping.json` if adding new locations.
2. `../cloudflare-workers/denizen/` — deploy asset updates.
3. `../api-v2/` — run integration tests.
4. `../client/` — verify UI rendering with new assets.

### Deployment Checklist

- [ ] Images processed and validated locally
- [ ] All variants generated successfully
- [ ] Git commits include proper descriptions
- [ ] Denizen service mapping updated if needed
- [ ] Cloudflare Workers deployment triggered
- [ ] Integration tests passing
- [ ] Global CDN availability verified
