# Repository Structure Rules

## Directory Organization

Maintain strict directory structure for the Denizen Assets repository:

```
denizen-assets/
├── assets/              # Source images only (never modify)
├── assets-small/        # 640x480 variants
├── assets-medium/       # 1920x1280 variants  
├── assets-large/        # 2400x1600 variants
├── cursor/rules/        # Cursor AI rules
└── temporary/           # Temporary files (not committed)
```

## File Management

### Adding Images
1. Place new images in `assets/` directory only
2. Follow naming convention: `[COUNTRY_CODE]-[CITY_CODE]-[NUMBER].jpg`
3. Run `python resize_assets.py` to generate variants
4. Verify all three size directories contain new images

### Known Issues
- `US-HT-4.jpg.jpg` has double extension (needs correction)
- Missing images should be identified and filled (e.g., gaps in 1-5 numbering)

## Integration Points

This repository integrates with:
- `../denizen/`: Go microservice that serves these images
- `../api-v2/`: Laravel main API
- `../client/`: Angular client application
- `../cloudflare-workers/`: Edge distribution

### Critical Dependencies
- Image filenames must match `mapping.json` in denizen service
- URL paths must be consistent with directory structure
- Image availability affects service uptime

## Repository Characteristics

- No dependency management files (requirements.txt, etc.)
- No automated testing framework
- Single main branch workflow
- Minimal tooling for rapid development

## General Coding Practices

- **Reuse existing code**: Don't create new functions or scripts if you can extend or augment existing ones
- **Consider shared libraries**: Design reusable components for cross-repository use
- **Document your code**: Add clear comments explaining why functions exist and what they do
- **Update documentation**: Always update CLAUDE.md and cursor rules files after any code changes