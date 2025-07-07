# Development Workflow Rules

## Standard Processes

### Image Addition Workflow
1. Source high-resolution images from Unsplash
2. Rename following convention: `[COUNTRY_CODE]-[CITY_CODE]-[NUMBER].jpg`
3. Place in `assets/` directory
4. Run `python resize_assets.py`
5. Verify all variants created
6. Check git status (variants auto-staged)
7. Manual review before commit

### Batch Operations
For 50+ images:
1. Use `generate_image_tasks.sh` to create task queue
2. Run `process_task_queue.sh` for automation
3. Monitor progress and validate results
4. Manual quality check required

## Error Handling

### Common Issues
- **PIL errors**: Verify Pillow installation with `pip install --upgrade Pillow`
- **Git staging fails**: Check directory structure exists
- **Missing images in service**: Sync with denizen mapping.json

### Validation Steps
- Check for corrupt images before processing
- Verify naming convention compliance
- Ensure all variants exist for each source
- Validate aspect ratios preserved (except large variant)

## Performance Considerations

### Current Limitations
- No progressive JPEG encoding
- No WebP format support
- No responsive image serving
- Large variant may distort aspect ratio

### Repository Size
- ~2.5GB estimated size
- No Git LFS implemented
- Consider shallow clones for development

## Legal Compliance

### Unsplash Requirements
- Commercial use permitted
- Attribution required when using API
- Cannot replicate competing service
- No rights to trademarks/people in photos

## General Coding Practices

- **Reuse existing code**: Don't create new functions or scripts if you can extend or augment existing ones
- **Consider shared libraries**: Design reusable components for cross-repository use
- **Document your code**: Add clear comments explaining why functions exist and what they do
- **Update documentation**: Always update CLAUDE.md and cursor rules files after any code changes