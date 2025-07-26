#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to run all update tools in aceflow framework.
This script sequentially executes update_status.py, update_flowchart.py,
update_task_reminders.py, and update_navigation.py to ensure all components
are updated in the correct order.
"""

import os
import subprocess
import argparse
from pathlib import Path

def run_script(script_name, iteration=None, all_iterations=False):
    """Run a specified Python script and return its output."""
    try:
        script_path = os.path.join(tools_dir, script_name)
        if not os.path.exists(script_path):
            print(f"Script {script_path} does not exist.")
            return False
        cmd = ['python', script_path]
        if script_name == "load_attention_prompts.py":
            # Provide a default stage for attention prompts loading
            cmd.extend(['--stage', 'S1'])
        if all_iterations:
            cmd.append('--all')
        elif iteration:
            cmd.extend(['--iteration', iteration])
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(f"Running {script_name}:")
        print(result.stdout)
        if result.stderr:
            print(f"Errors in {script_name}:")
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running {script_name}: {e}")
        return False

def get_all_iterations(base_dir):
    """Get a list of all iteration directories in the iterations folder."""
    iterations_dir = os.path.join(base_dir, "iterations")
    if not os.path.exists(iterations_dir):
        print(f"Iterations directory {iterations_dir} does not exist.")
        return []
    return [d for d in os.listdir(iterations_dir) if os.path.isdir(os.path.join(iterations_dir, d))]

def main():
    """Main function to run all update scripts in sequence."""
    global tools_dir
    tools_dir = Path(__file__).parent
    
    parser = argparse.ArgumentParser(description="Run all update scripts for a specific iteration or all iterations.")
    parser.add_argument("--iteration", help="Specify the iteration to update (e.g., iteration-01). If not provided, defaults to iteration-01.")
    parser.add_argument("--all", action="store_true", help="Update all iterations.")
    args = parser.parse_args()
    
    print("Starting update process for aceflow framework...\n")
    
    # Run scripts in sequence
    scripts = [
        "update_status.py",
        "update_flowchart.py",
        "update_task_reminders.py",
        "update_navigation.py",
        "load_attention_prompts.py"
    ]
    
    all_successful = True
    for script in scripts:
        if not run_script(script, args.iteration, args.all):
            all_successful = False
            print(f"Warning: {script} did not complete successfully. Continuing with other scripts...\n")
    
    if all_successful:
        print("All update scripts completed successfully.")
    else:
        print("Some update scripts encountered errors. Please check the output for details.")

if __name__ == "__main__":
    main()
