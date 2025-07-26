#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to automate the generation of document navigation links in aceflow framework.
It scans the file structure of iterations and generates a navigation index
to be embedded in index.md or other main files.
Supports both old and new directory structures.
"""

import os
import argparse
from pathlib import Path

def scan_iteration_documents_old_structure(iteration_dir):
    """Scan all documents in the given iteration directory for navigation links (old structure)."""
    navigation_data = []
    stages = [
        ('S1 需求分析', 's1_user_story.md'),
        ('S2 任务拆解', 's2_tasks.md'),
        ('S3 测试用例设计', 's3_testcases'),
        ('S4 初步实现', 's4_implementation'),
        ('S5 自动化测试', 's5_test_report.md'),
        ('S6 代码审查', 's6_codereview.md'),
        ('S7 演示反馈', 's7_demo_feedback.md'),
        ('S8 进度总结', 's8_progress_index.md')
    ]
    for stage_name, stage_path in stages:
        full_path = os.path.join(iteration_dir, stage_path)
        if os.path.isdir(full_path):
            # For directories, list all .md files inside
            stage_docs = []
            for item in sorted(os.listdir(full_path)):
                if item.endswith('.md'):
                    item_path = os.path.join(full_path, item)
                    rel_path = item_path.replace(iteration_dir + os.sep, "")
                    stage_docs.append((item.split('.')[0], rel_path))
            if stage_docs:
                navigation_data.append((stage_name, stage_docs))
        elif os.path.isfile(full_path):
            rel_path = full_path.replace(iteration_dir + os.sep, "")
            navigation_data.append((stage_name, [(stage_path.split('.')[0].upper(), rel_path)]))
    return navigation_data

def scan_iteration_documents_new_structure(iteration_dir):
    """Scan all documents in the given iteration directory for navigation links (new structure with task subdirectories)."""
    navigation_data = []
    task_dirs = [d for d in os.listdir(iteration_dir) if os.path.isdir(os.path.join(iteration_dir, d))]
    stages = [
        ('S1 需求分析', 's1_user_story.md'),
        ('S2 任务拆解', 's2_tasks.md'),
        ('S3 测试用例设计', 's3_testcases.md'),
        ('S4 初步实现', 's4_implementation.md'),
        ('S5 自动化测试', 's5_test_report.md'),
        ('S6 代码审查', 's6_codereview.md'),
        ('S7 演示反馈', 's7_demo_feedback.md'),
        ('S8 进度总结', 's8_progress_index.md')
    ]
    
    for task_dir in task_dirs:
        task_path = os.path.join(iteration_dir, task_dir)
        task_docs = []
        for stage_name, stage_file in stages:
            stage_path = os.path.join(task_path, stage_file)
            if os.path.isfile(stage_path):
                rel_path = stage_path.replace(iteration_dir + os.sep, "")
                task_docs.append((stage_name.split(' ')[0], rel_path))
        if task_docs:
            navigation_data.append((task_dir, task_docs))
    
    return navigation_data

def scan_iteration_documents(iteration_dir):
    """Determine the structure (old or new) and scan accordingly."""
    # Check if the directory contains task subdirectories (new structure)
    task_dirs = [d for d in os.listdir(iteration_dir) if os.path.isdir(os.path.join(iteration_dir, d)) and d.startswith('T-')]
    if task_dirs:
        print(f"Detected new structure for {iteration_dir}")
        return scan_iteration_documents_new_structure(iteration_dir)
    else:
        print(f"Detected old structure for {iteration_dir}")
        return scan_iteration_documents_old_structure(iteration_dir)

def update_navigation_index(index_file, iteration, navigation_data):
    """Update the index.md file with the latest navigation index."""
    try:
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find or create navigation section
        navigation_section = f"## {iteration} 文档导航"
        start_idx = content.find(navigation_section)
        if start_idx == -1:
            # If section doesn't exist, append it
            new_content = f"\n\n{navigation_section}\n\n"
            new_content += "以下是当前迭代中各个阶段的文档链接，方便快速访问：\n\n"
            for stage_name, docs in navigation_data:
                new_content += f"- **{stage_name}**\n"
                for doc_name, doc_path in docs:
                    new_content += f"  - [{doc_name}]({doc_path})\n"
            content += new_content
        else:
            # Find the end of the navigation section (next heading or end of file)
            next_section_idx = content.find("## ", start_idx + len(navigation_section))
            if next_section_idx == -1:
                next_section_idx = len(content)
            
            # Replace existing navigation content with new
            new_content = f"{navigation_section}\n\n"
            new_content += "以下是当前迭代中各个阶段的文档链接，方便快速访问：\n\n"
            for stage_name, docs in navigation_data:
                new_content += f"- **{stage_name}**\n"
                for doc_name, doc_path in docs:
                    new_content += f"  - [{doc_name}]({doc_path})\n"
            content = content[:start_idx] + new_content + content[next_section_idx:]
        
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully updated {index_file} with navigation index for {iteration}")
    except Exception as e:
        print(f"Error updating {index_file}: {e}")

def get_all_iterations(base_dir):
    """Get a list of all iteration directories in the iterations folder."""
    iterations_dir = os.path.join(base_dir, "iterations")
    if not os.path.exists(iterations_dir):
        print(f"Iterations directory {iterations_dir} does not exist.")
        return []
    return [d for d in os.listdir(iterations_dir) if os.path.isdir(os.path.join(iterations_dir, d))]

def main():
    """Main function to generate document navigation links in index.md."""
    parser = argparse.ArgumentParser(description="Update navigation index in index.md for a specific iteration or all iterations.")
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
    
    index_file = os.path.join(base_dir, "index.md")
    if not os.path.exists(index_file):
        print(f"Index file {index_file} does not exist.")
        return
    
    for iteration in iterations:
        iteration_dir = os.path.join(base_dir, "iterations", iteration)
        if not os.path.exists(iteration_dir):
            print(f"Iteration directory {iteration_dir} does not exist.")
            continue
        
        navigation_data = scan_iteration_documents(iteration_dir)
        update_navigation_index(index_file, iteration, navigation_data)

if __name__ == "__main__":
    main()
