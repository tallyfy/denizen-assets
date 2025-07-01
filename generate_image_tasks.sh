#!/bin/bash
# generate_image_tasks.sh - Generate Claude task queue for image processing

# Create task queue directory
mkdir -p task_queue

# Clear existing tasks
rm -f task_queue/*.prompt

# Task 1: Analyze current images
cat > task_queue/001_analyze_images.prompt << 'EOF'
Analyze all images in the assets/ directory and create a summary report including:
1. Total number of images per country
2. Any missing city codes (gaps in numbering 1-5)
3. Any files that don't follow the naming convention
Output the report as a markdown table.
EOF

# Task 2: Create image metadata script
cat > task_queue/002_create_metadata_script.prompt << 'EOF'
Create a Python script called generate_metadata.py that:
1. Scans all images in assets/, assets-small/, assets-medium/, and assets-large/
2. Extracts metadata (dimensions, file size, creation date)
3. Outputs a JSON file with all image metadata organized by country and city
Use PIL for image processing and include error handling.
EOF

# Task 3: Optimize resize script
cat > task_queue/003_optimize_resize.prompt << 'EOF'
Review resize_assets.py and create an improved version called resize_assets_optimized.py that:
1. Adds progress indicators using tqdm
2. Implements parallel processing for faster execution
3. Adds error handling for corrupted images
4. Creates a log file of processed images
5. Preserves aspect ratio for all sizes (including large)
EOF

# Task 4: Create validation script
cat > task_queue/004_create_validation.prompt << 'EOF'
Create a validate_assets.py script that checks:
1. All source images have corresponding resized versions
2. Image dimensions match expected sizes
3. File naming conventions are followed
4. No duplicate images exist
Output a validation report with any issues found.
EOF

echo "Generated $(ls task_queue/*.prompt | wc -l) tasks in task_queue/"
echo ""
echo "To process the queue, run:"
echo "  bash process_task_queue.sh"