import argparse
import os
import sys
import yaml
import re

CONTEXT_DIR = ".context"

def load_context(task_id):
    context_path = os.path.join(CONTEXT_DIR, f"{task_id}.yaml")
    if not os.path.exists(context_path):
        print(f"[FlowSentinel] ❌ 上下文文件不存在: {context_path}")
        return None
    try:
        with open(context_path, "r", encoding="utf-8") as f:
            context = yaml.safe_load(f)
        return context
    except Exception as e:
        print(f"[FlowSentinel] ❌ 解析上下文失败: {e}")
        return None

def parse_frontmatter(md_path):
    """
    解析 Markdown 文件中的 frontmatter YAML 块
    返回 dict 或 None
    """
    if not os.path.exists(md_path):
        print(f"[FlowSentinel] ❌ 文件不存在: {md_path}")
        return None
    try:
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
        fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not fm_match:
            print(f"[FlowSentinel] ❌ Frontmatter 格式错误或缺失: {md_path}")
            return None
        fm_content = fm_match.group(1)
        fm_data = yaml.safe_load(fm_content)
        return fm_data
    except Exception as e:
        print(f"[FlowSentinel] ❌ 读取或解析文件失败: {e}")
        return None

def validate_frontmatter(fm_data, required_fields):
    """
    校验 frontmatter 是否包含所有必填字段
    返回 (bool, list_of_missing_fields)
    """
    if not fm_data:
        return False, required_fields
    missing = [f for f in required_fields if f not in fm_data]
    return len(missing) == 0, missing

def main():
    parser = argparse.ArgumentParser(description="ACEFLOW 流程守护器 - 阶段产物校验")
    parser.add_argument("--stage", required=True, help="阶段名称，如 S1")
    parser.add_argument("--task", required=True, help="任务 ID，如 T-001")
    parser.add_argument("--strict", action="store_true", help="启用严格校验，发现问题退出非零码")
    args = parser.parse_args()

    context = load_context(args.task)
    if not context:
        print("[FlowSentinel] ❌ 无法加载上下文，终止执行")
        if args.strict:
            sys.exit(1)
        else:
            return

    iteration = context.get("iteration")
    if not iteration:
        print(f"[FlowSentinel] ❌ 上下文缺少 iteration 字段")
        if args.strict:
            sys.exit(1)
        else:
            return

    # 拼接阶段产物文件路径，格式示例：
    # aceflow/iterations/iteration-01/T-001/s1_user_story.md
    stage_lower = args.stage.lower()
    stage_num = args.stage[1:]  # "S1" -> "1"
    file_prefix_map = {
        "s1": "user_story",
        "s2": "tasks",
        "s3": "testcases",
        "s4": "implementation",
        "s5": "test_report",
        "s6": "codereview",
        "s7": "demo_feedback",
        "s8": "progress_index"
    }
    prefix = file_prefix_map.get(stage_lower, None)
    if not prefix:
        print(f"[FlowSentinel] ❌ 未知阶段：{args.stage}")
        if args.strict:
            sys.exit(1)
        else:
            return

    md_file = os.path.join(
        "aceflow", "iterations", iteration, args.task, f"s{stage_num}_{prefix}.md"
    )

    fm_data = parse_frontmatter(md_file)
    if fm_data is None:
        print(f"[FlowSentinel] 🚫 阶段产物缺失或格式错误：{md_file}")
        if args.strict:
            sys.exit(1)
        else:
            return
    else:
        print(f"[FlowSentinel] ✅ 阶段产物存在且 Frontmatter 可解析：{md_file}")

    # 必填字段校验
    required_fields = ["stage", "iteration", "task_id", "status", "created_at"]
    valid, missing = validate_frontmatter(fm_data, required_fields)
    if not valid:
        print(f"[FlowSentinel] 🚫 Frontmatter 缺失字段: {missing}")
        if args.strict:
            sys.exit(1)
        else:
            return

    # 简单状态校验：status 必须是 '已完成' 或 '通过'
    status = fm_data.get("status", "").strip()
    if status not in ["已完成", "通过"]:
        print(f"[FlowSentinel] ⚠️ 阶段状态非完成或通过: 当前 status = '{status}'")
        if args.strict:
            sys.exit(1)

    print(f"[FlowSentinel] ✅ 阶段 {args.stage} 产物状态校验通过")

if __name__ == "__main__":
    main()
