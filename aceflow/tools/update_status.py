#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to automate the update of status.md file in aceflow framework.
It scans the status of various stages and tasks from iteration documents
and updates the status table accordingly.
Supports both old and new directory structures.
"""

import os
import re
import datetime
import argparse
from pathlib import Path

def extract_status_from_file(file_path):
    """Extract status from the Front-matter of a given file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            status_match = re.search(r'status:\s*([^\n\r]+)', content)
            if status_match:
                return status_match.group(1).strip()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return "未知"

def scan_iteration_status_old_structure(iteration_dir):
    """Scan the status of all stages and tasks in the given iteration directory (old structure)."""
    status_data = []
    stages = ['s1_user_story.md', 's2_tasks.md', 's3_testcases', 's4_implementation', 's5_test_report.md', 's6_codereview.md', 's7_demo_feedback.md', 's8_progress_index.md']
    for stage in stages:
        stage_path = os.path.join(iteration_dir, stage)
        if os.path.isdir(stage_path):
            # For directories like s3_testcases, check status of individual test cases
            stage_status = []
            for item in os.listdir(stage_path):
                if item.endswith('.md'):
                    item_path = os.path.join(stage_path, item)
                    status = extract_status_from_file(item_path)
                    stage_status.append(status)
            if stage_status:
                # Simplify status for the stage based on individual statuses
                if all(s == "已完成" for s in stage_status):
                    overall_status = "已完成"
                elif any(s == "进行中" for s in stage_status):
                    overall_status = "进行中"
                else:
                    overall_status = "待开始"
            else:
                overall_status = "待开始"
        elif os.path.isfile(stage_path):
            overall_status = extract_status_from_file(stage_path)
        else:
            overall_status = "待开始"
        status_data.append((stage.split('_')[0].upper(), overall_status))
    return status_data

def scan_iteration_status_new_structure(iteration_dir):
    """Scan the status of all stages and tasks in the given iteration directory (new structure with task subdirectories)."""
    status_data = []
    stages = ['s1_user_story.md', 's2_tasks.md', 's3_testcases.md', 's4_implementation.md', 's5_test_report.md', 's6_codereview.md', 's7_demo_feedback.md', 's8_progress_index.md']
    task_dirs = [d for d in os.listdir(iteration_dir) if os.path.isdir(os.path.join(iteration_dir, d))]
    
    if not task_dirs:
        return [("S" + str(i+1), "待开始") for i in range(8)]
    
    # Aggregate status across all tasks for each stage
    for i, stage in enumerate(stages):
        stage_status = []
        for task_dir in task_dirs:
            stage_path = os.path.join(iteration_dir, task_dir, stage)
            if os.path.isfile(stage_path):
                status = extract_status_from_file(stage_path)
                stage_status.append(status)
        
        if stage_status:
            if all(s == "已完成" for s in stage_status):
                overall_status = "已完成"
            elif any(s == "进行中" for s in stage_status):
                overall_status = "进行中"
            else:
                overall_status = "待开始"
        else:
            overall_status = "待开始"
        status_data.append(("S" + str(i+1), overall_status))
    return status_data

def scan_iteration_status(iteration_dir):
    """Determine the structure (old or new) and scan accordingly."""
    # Check if the directory contains task subdirectories (new structure)
    task_dirs = [d for d in os.listdir(iteration_dir) if os.path.isdir(os.path.join(iteration_dir, d)) and d.startswith('T-')]
    if task_dirs:
        print(f"Detected new structure for {iteration_dir}")
        return scan_iteration_status_new_structure(iteration_dir)
    else:
        print(f"Detected old structure for {iteration_dir}")
        return scan_iteration_status_old_structure(iteration_dir)

def update_status_md(status_file, iteration, status_data):
    """Update the status.md file with the latest status data."""
    try:
        with open(status_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the section for the given iteration
        iteration_section = f"## 📅 {iteration} 状态"
        start_idx = content.find(iteration_section)
        if start_idx == -1:
            print(f"Could not find section for {iteration}")
            return
        
        # Find the table start and end
        table_start = content.find('| 阶段 | 状态', start_idx)
        if table_start == -1:
            print(f"Could not find table for {iteration}")
            return
        
        table_end = content.find('---', table_start)
        if table_end == -1:
            print(f"Could not find table end for {iteration}")
            return
        
        # Generate new table content
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        new_table_content = "| 阶段 | 状态       | 更新时间           | 责任人    | 备注                     |\n"
        new_table_content += "|------|------------|--------------------|-----------|--------------------------|\n"
        for stage, status in status_data:
            new_table_content += f"| {stage}   | {status}     | {current_time}   | AI Assistant | 自动更新状态          |\n"
        
        # Replace old table content with new
        updated_content = content[:table_start] + new_table_content + content[table_end:]
        
        with open(status_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"Successfully updated {status_file} for {iteration}")
    except Exception as e:
        print(f"Error updating {status_file}: {e}")

def load_config():
    """Load configuration from project.config.json."""
    import json
    config_file = os.path.join(os.path.dirname(__file__), "..", "project.config.json")
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def get_all_iterations(base_dir):
    """Get a list of all iteration directories in the iterations folder."""
    config = load_config()
    iteration_root = config.get('iterationRoot', './aceflow_result/iterations')
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    iterations_dir = os.path.abspath(os.path.join(project_root, iteration_root.lstrip('./')))
    if not os.path.exists(iterations_dir):
        print(f"Iterations directory {iterations_dir} does not exist.")
        return []
    return [d for d in os.listdir(iterations_dir) if os.path.isdir(os.path.join(iterations_dir, d))]

def main():
    """Main function to update status.md based on iteration documents."""
    parser = argparse.ArgumentParser(description="Update status.md for a specific iteration or all iterations.")
    parser.add_argument("--iteration", help="Specify the iteration to update (e.g., iteration-01). If not provided, defaults to iteration-01.")
    parser.add_argument("--all", action="store_true", help="Update all iterations.")
    args = parser.parse_args()
    
    base_dir = Path(__file__).parent.parent
    iterations = []
    
    if args.all:
        iterations = get_all_iterations(base_dir)
        if not iterations:
            print("No iterations found to update.")
            return
    elif args.iteration:
        iterations = [args.iteration]
    else:
        iterations = ["iteration-01"]  # Default iteration if none specified
    
    config = load_config()
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    status_file = os.path.abspath(os.path.join(project_root, "aceflow_result", "status.md"))
    if not os.path.exists(status_file):
        print(f"Status file {status_file} does not exist.")
        return
    
    for iteration in iterations:
        config = load_config()
        iteration_root = config.get('iterationRoot', './aceflow_result/iterations')
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        iteration_dir = os.path.abspath(os.path.join(project_root, iteration_root.lstrip('./'), iteration))
        if not os.path.exists(iteration_dir):
            print(f"Iteration directory {iteration_dir} does not exist.")
            continue
        
        status_data = scan_iteration_status(iteration_dir)
        update_status_md(status_file, iteration, status_data)

if __name__ == "__main__":
    main()
