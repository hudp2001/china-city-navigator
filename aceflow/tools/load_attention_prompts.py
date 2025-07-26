#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to dynamically load attention mechanism prompt templates for AceFlow stages.
This script scans the attention prompt templates directory and loads the appropriate
template based on the specified stage.
"""

import os
import argparse
from pathlib import Path

def load_attention_prompt(stage):
    """Load the attention prompt template for the specified stage."""
    base_dir = Path(__file__).parent.parent
    template_dir = os.path.join(base_dir, "templates")
    template_file = f"prompt_snippet_attention_s{stage.lower()[1]}.md"
    template_path = os.path.join(template_dir, template_file)
    
    if not os.path.exists(template_path):
        print(f"[Attention Loader] 注意力机制模板文件不存在: {template_path}")
        return None
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"[Attention Loader] 成功加载注意力机制模板: {template_file}")
        return content
    except Exception as e:
        print(f"[Attention Loader] 加载模板时出错: {e}")
        return None

def main():
    """Main function to load attention prompt template for a specific stage."""
    parser = argparse.ArgumentParser(description="加载指定阶段的注意力机制提示词模板")
    parser.add_argument("--stage", required=True, help="阶段名称，如 S1")
    args = parser.parse_args()
    
    stage = args.stage.upper()
    if not stage.startswith('S') or len(stage) != 2 or not stage[1].isdigit() or int(stage[1]) not in range(1, 9):
        print(f"[Attention Loader] 无效的阶段名称: {stage}，应为 S1 到 S8")
        return
    
    prompt_content = load_attention_prompt(stage)
    if prompt_content:
        print("\n=== 注意力机制提示词内容 ===")
        print(prompt_content)
        print("=== 内容结束 ===")

if __name__ == "__main__":
    main()
