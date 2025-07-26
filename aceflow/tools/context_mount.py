#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to mount context for a specific task in the AceFlow framework.
This script loads context information from a YAML file and injects it into environment variables.
It also dynamically loads attention mechanism prompt templates based on the task's stage.
"""

import os
import argparse
import yaml
import sys
import subprocess
from pathlib import Path

CONTEXT_DIR = ".context"

def load_context(task_id: str, dry_run=False):
    """Load context information for the specified task and inject into environment variables."""
    context_path = os.path.join(CONTEXT_DIR, f"{task_id}.yaml")
    if not os.path.exists(context_path):
        print(f"[context_mount] 未找到上下文文件: {context_path}")
        sys.exit(1)

    with open(context_path, "r", encoding="utf-8") as f:
        context = yaml.safe_load(f) or {}

    print(f"[context_mount] 挂载上下文: {context_path}")
    for key, value in context.items():
        var_name = f"CTX_{key.upper()}"
        if dry_run:
            print(f"    └─ {var_name} = {value}")
        else:
            os.environ[var_name] = str(value)
            print(f"    └─ 注入变量: {var_name} = {value}")

    # 动态加载注意力机制模板
    stage = context.get('stage', 'S1')  # 从上下文中获取阶段，默认值为 S1
    attention_prompt = load_attention_prompt(stage, dry_run)
    if attention_prompt and not dry_run:
        os.environ['CTX_ATTENTION_PROMPT'] = attention_prompt
        print(f"    └─ 注入变量: CTX_ATTENTION_PROMPT = [注意力机制模板内容]")

    return context

def load_attention_prompt(stage: str, dry_run=False):
    """调用 load_attention_prompts.py 工具加载注意力机制模板"""
    base_dir = Path(__file__).parent
    tool_path = os.path.join(base_dir, "load_attention_prompts.py")
    if not os.path.exists(tool_path):
        print(f"[context_mount] 未找到注意力机制加载工具: {tool_path}")
        return None

    try:
        cmd = ['python', tool_path, '--stage', stage]
        if dry_run:
            print(f"[context_mount] 模拟加载注意力机制模板: {' '.join(cmd)}")
            return None
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            # 从输出中提取模板内容
            start_marker = "=== 注意力机制提示词内容 ==="
            end_marker = "=== 内容结束 ==="
            start_idx = result.stdout.find(start_marker) + len(start_marker)
            end_idx = result.stdout.find(end_marker)
            if start_idx > len(start_marker) and end_idx > start_idx:
                content = result.stdout[start_idx:end_idx].strip()
                print(f"[context_mount] 成功加载注意力机制模板 for {stage}")
                return content
        print(f"[context_mount] 加载注意力机制模板失败: {result.stderr}")
        return None
    except Exception as e:
        print(f"[context_mount] 加载注意力机制模板时出错: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="ACEFLOW v2.5 上下文挂载器")
    parser.add_argument("--task", required=True, help="任务 ID，例如 T-001")
    parser.add_argument("--print", action="store_true", help="仅打印变量，不注入环境")
    args = parser.parse_args()

    load_context(args.task, dry_run=args.print)

if __name__ == "__main__":
    main()
