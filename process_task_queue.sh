#!/bin/bash
# process_task_queue.sh - Process Claude automation task queue

# Create task queue directory if it doesn't exist
mkdir -p task_queue

# Function to process a single prompt file
process_prompt() {
    local prompt_file="$1"
    if [ -f "$prompt_file" ]; then
        echo "Processing: $(basename "$prompt_file")"
        claude -p "$(cat "$prompt_file")" --dangerously-skip-permissions
        
        # Check exit status
        if [ $? -eq 0 ]; then
            echo "✓ Completed: $(basename "$prompt_file")"
            rm "$prompt_file"
        else
            echo "✗ Failed: $(basename "$prompt_file")"
            return 1
        fi
    fi
}

# Process all prompt files in order
for prompt_file in task_queue/*.prompt; do
    if [ -f "$prompt_file" ]; then
        process_prompt "$prompt_file"
        
        # Stop on error
        if [ $? -ne 0 ]; then
            echo "Stopping due to error. Remaining tasks:"
            ls task_queue/*.prompt 2>/dev/null || echo "None"
            exit 1
        fi
        
        # Small delay between tasks
        sleep 1
    fi
done

echo "All tasks completed successfully!"