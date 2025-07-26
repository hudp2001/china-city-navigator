#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to automate the update of flowchart in aceflow framework.
It reads the status from status.md and generates a Mermaid flowchart
to be embedded in index.md or other main files.
Supports both old and new directory structures.
"""

import os
import re
import argparse
from pathlib import Path

def read_status_from_file(status_file, iteration):
    """Read status data for the given iteration from status.md."""
    status_data = []
    try:
        with open(status_file, 'r', encoding='utf-8') as f:
            content = f.read()
            iteration_section = f"## 📅 {iteration} 状态"
            start_idx = content.find(iteration_section)
            if start_idx == -1:
                print(f"Could not find section for {iteration}")
                return status_data
            
            table_start = content.find('| 阶段 | 状态', start_idx)
            if table_start == -1:
                print(f"Could not find table for {iteration}")
                return status_data
            
            lines = content[table_start:].splitlines()
            for line in lines[2:]:  # Skip header and separator lines
                if line.strip() and not line.startswith('---'):
                    parts = line.split('|')
                    if len(parts) >= 3:
                        stage = parts[1].strip()
                        status = parts[2].strip()
                        status_data.append((stage, status))
                    if len(status_data) == 8:  # Assuming 8 stages S1-S8
                        break
    except Exception as e:
        print(f"Error reading {status_file}: {e}")
    return status_data

def generate_mermaid_flowchart(status_data):
    """Generate Mermaid flowchart code based on status data."""
    mermaid_code = "```mermaid\n"
    mermaid_code += "graph LR\n"
    mermaid_code += "    S1[需求分析 S1] --> S2[任务拆解 S2]\n"
    mermaid_code += "    S2 --> S3[测试用例设计 S3]\n"
    mermaid_code += "    S3 --> S4[初步实现 S4]\n"
    mermaid_code += "    S4 --> S5[自动化测试 S5]\n"
    mermaid_code += "    S5 --> S6[代码审查 S6]\n"
    mermaid_code += "    S6 --> S7[演示反馈 S7]\n"
    mermaid_code += "    S7 --> S8[进度总结 S8]\n"
    
    # Apply styles based on status
    for stage, status in status_data:
        color = "#95a5a6"  # Default gray for "待开始"
        stroke = "#7f8c8d"
        text_color = "#000"
        if status == "已完成":
            color = "#2ecc71"
            stroke = "#27ae60"
            text_color = "#fff"
        elif status == "进行中":
            color = "#f1c40f"
            stroke = "#f39c12"
            text_color = "#000"
        mermaid_code += f"    style {stage} fill:{color},stroke:{stroke},color:{text_color}\n"
    
    mermaid_code += "```\n"
    return mermaid_code

def update_index_md(index_file, iteration, flowchart_code):
    """Update the index.md file with the latest flowchart code."""
    try:
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find or create flowchart section
        flowchart_section = f"## {iteration} 流程图"
        start_idx = content.find(flowchart_section)
        if start_idx == -1:
            # If section doesn't exist, append it
            content += f"\n\n{flowchart_section}\n\n{flowchart_code}"
        else:
            # Find the mermaid code block
            mermaid_start = content.find("```mermaid", start_idx)
            if mermaid_start == -1:
                # If no mermaid block, append flowchart code after section header
                content = content[:start_idx + len(flowchart_section)] + f"\n\n{flowchart_code}" + content[start_idx + len(flowchart_section):]
            else:
                mermaid_end = content.find("```", mermaid_start + 10)
                if mermaid_end == -1:
                    print("Could not find end of mermaid block")
                    return
                # Replace existing mermaid code with new one
                content = content[:mermaid_start] + flowchart_code + content[mermaid_end + 3:]
        
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully updated {index_file} with flowchart for {iteration}")
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
    """Main function to update flowchart in index.md based on status.md."""
    parser = argparse.ArgumentParser(description="Update flowchart in index.md for a specific iteration or all iterations.")
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
    
    status_file = os.path.join(base_dir, "status.md")
    index_file = os.path.join(base_dir, "index.md")
    
    if not os.path.exists(status_file):
        print(f"Status file {status_file} does not exist.")
        return
    
    if not os.path.exists(index_file):
        print(f"Index file {index_file} does not exist.")
        return
    
    for iteration in iterations:
        status_data = read_status_from_file(status_file, iteration)
        if status_data:
            flowchart_code = generate_mermaid_flowchart(status_data)
            update_index_md(index_file, iteration, flowchart_code)
        else:
            print(f"No status data found to generate flowchart for {iteration}.")

if __name__ == "__main__":
    main()
