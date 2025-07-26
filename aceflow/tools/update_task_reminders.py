#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to automate the generation of task reminders in aceflow framework.
It scans the status of various stages and tasks from iteration documents
and generates a reminders list in task_reminders.md.
Supports both old and new directory structures.
"""

import os
import re
import datetime
import argparse
from pathlib import Path

def extract_status_from_file(file_path):
    """Extract status and other metadata from the Front-matter of a given file."""
    metadata = {"status": "未知", "doc_owner": "未知", "task_id": "未知"}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            status_match = re.search(r'status:\s*([^\n\r]+)', content)
            if status_match:
                metadata["status"] = status_match.group(1).strip()
            owner_match = re.search(r'doc_owner:\s*([^\n\r]+)', content)
            if owner_match:
                metadata["doc_owner"] = owner_match.group(1).strip()
            task_match = re.search(r'task_id:\s*([^\n\r]+)', content)
            if task_match:
                metadata["task_id"] = task_match.group(1).strip()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return metadata

def scan_iteration_tasks_old_structure(iteration_dir):
    """Scan for tasks that are not completed in the given iteration directory (old structure)."""
    reminders = []
    stages = [
        ('S1', 's1_user_story.md'),
        ('S2', 's2_tasks.md'),
        ('S3', 's3_testcases'),
        ('S4', 's4_implementation'),
        ('S5', 's5_test_report.md'),
        ('S6', 's6_codereview.md'),
        ('S7', 's7_demo_feedback.md'),
        ('S8', 's8_progress_index.md')
    ]
    for stage_name, stage_path in stages:
        full_path = os.path.join(iteration_dir, stage_path)
        if os.path.isdir(full_path):
            # For directories like s3_testcases, check individual files
            for item in os.listdir(full_path):
                if item.endswith('.md'):
                    item_path = os.path.join(full_path, item)
                    metadata = extract_status_from_file(item_path)
                    if metadata["status"] not in ["已完成", "取消"]:
                        reminders.append({
                            "stage": stage_name,
                            "task": metadata["task_id"],
                            "status": metadata["status"],
                            "owner": metadata["doc_owner"],
                            "path": item_path.replace(iteration_dir + os.sep, "")
                        })
        elif os.path.isfile(full_path):
            metadata = extract_status_from_file(full_path)
            if metadata["status"] not in ["已完成", "取消"]:
                reminders.append({
                    "stage": stage_name,
                    "task": stage_path.split('.')[0].upper(),
                    "status": metadata["status"],
                    "owner": metadata["doc_owner"],
                    "path": full_path.replace(iteration_dir + os.sep, "")
                })
    return reminders

def scan_iteration_tasks_new_structure(iteration_dir):
    """Scan for tasks that are not completed in the given iteration directory (new structure with task subdirectories)."""
    reminders = []
    task_dirs = [d for d in os.listdir(iteration_dir) if os.path.isdir(os.path.join(iteration_dir, d))]
    stages = [
        ('S1', 's1_user_story.md'),
        ('S2', 's2_tasks.md'),
        ('S3', 's3_testcases.md'),
        ('S4', 's4_implementation.md'),
        ('S5', 's5_test_report.md'),
        ('S6', 's6_codereview.md'),
        ('S7', 's7_demo_feedback.md'),
        ('S8', 's8_progress_index.md')
    ]
    
    for task_dir in task_dirs:
        task_path = os.path.join(iteration_dir, task_dir)
        for stage_name, stage_file in stages:
            stage_path = os.path.join(task_path, stage_file)
            if os.path.isfile(stage_path):
                metadata = extract_status_from_file(stage_path)
                if metadata["status"] not in ["已完成", "取消"]:
                    reminders.append({
                        "stage": stage_name,
                        "task": task_dir,
                        "status": metadata["status"],
                        "owner": metadata["doc_owner"],
                        "path": stage_path.replace(iteration_dir + os.sep, "")
                    })
    
    return reminders

def scan_iteration_tasks(iteration_dir):
    """Determine the structure (old or new) and scan accordingly."""
    # Check if the directory contains task subdirectories (new structure)
    task_dirs = [d for d in os.listdir(iteration_dir) if os.path.isdir(os.path.join(iteration_dir, d)) and d.startswith('T-')]
    if task_dirs:
        print(f"Detected new structure for {iteration_dir}")
        return scan_iteration_tasks_new_structure(iteration_dir)
    else:
        print(f"Detected old structure for {iteration_dir}")
        return scan_iteration_tasks_old_structure(iteration_dir)

def update_task_reminders_md(reminders_file, iteration, reminders):
    """Update the task_reminders.md file with the latest reminders list."""
    try:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        content = f"# {iteration} 任务提醒\n\n"
        content += f"**更新时间**: {current_time}\n\n"
        content += "以下是当前迭代中尚未完成的任务列表，供团队成员参考和管理。\n\n"
        
        if not reminders:
            content += "**当前没有待办任务。**\n"
        else:
            content += "| 阶段 | 任务编号 | 状态 | 责任人 | 文档路径 |\n"
            content += "|------|----------|------|--------|----------|\n"
            for reminder in reminders:
                content += f"| {reminder['stage']} | {reminder['task']} | {reminder['status']} | {reminder['owner']} | [{reminder['path']}]({reminder['path']}) |\n"
        
        with open(reminders_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully updated {reminders_file} with task reminders for {iteration}")
    except Exception as e:
        print(f"Error updating {reminders_file}: {e}")

def get_all_iterations(base_dir):
    """Get a list of all iteration directories in the iterations folder."""
    iterations_dir = os.path.join(base_dir, "iterations")
    if not os.path.exists(iterations_dir):
        print(f"Iterations directory {iterations_dir} does not exist.")
        return []
    return [d for d in os.listdir(iterations_dir) if os.path.isdir(os.path.join(iterations_dir, d))]

def main():
    """Main function to generate task reminders based on iteration documents."""
    parser = argparse.ArgumentParser(description="Update task reminders for a specific iteration or all iterations.")
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
    
    reminders_file = os.path.join(base_dir, "task_reminders.md")
    
    for iteration in iterations:
        iteration_dir = os.path.join(base_dir, "iterations", iteration)
        if not os.path.exists(iteration_dir):
            print(f"Iteration directory {iteration_dir} does not exist.")
            continue
        
        reminders = scan_iteration_tasks(iteration_dir)
        update_task_reminders_md(reminders_file, iteration, reminders)

if __name__ == "__main__":
    main()
