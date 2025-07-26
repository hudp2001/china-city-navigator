import os
import argparse
import yaml
import sys
import re

REQUIRED_FIELDS = ["stage", "iteration", "task_id", "doc_owner", "status"]

def parse_frontmatter(file_path):
    """安全解析 frontmatter，返回 dict 或 None"""
    if not os.path.exists(file_path):
        print(f"[Validator] ❌ 文件不存在: {file_path}")
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            print(f"[Validator] ❌ Frontmatter 格式错误或缺失: {file_path}")
            return None
        fm_content = match.group(1)
        data = yaml.safe_load(fm_content)
        return data
    except Exception as e:
        print(f"[Validator] ❌ 解析异常: {e}")
        return None

def validate_fields(fm_data):
    """验证必填字段完整性"""
    missing = [f for f in REQUIRED_FIELDS if f not in fm_data]
    if missing:
        print(f"[Validator] 🚫 缺失必填字段: {missing}")
        return False
    return True

def validate_status(fm_data):
    """验证 status 字段语义"""
    valid_status = ["已完成", "通过"]
    status = fm_data.get("status", "").strip()
    if status not in valid_status:
        print(f"[Validator] ⚠️ status 字段异常: 当前值='{status}'，应为 {valid_status}")
        return False
    return True

def main():
    parser = argparse.ArgumentParser(description="阶段产物 frontmatter 校验器")
    parser.add_argument("--stage", required=True, help="阶段名称，如 S1")
    parser.add_argument("--task", required=True, help="任务ID，如 T-001")
    parser.add_argument("--iteration", default="iteration-01", help="迭代名称")
    parser.add_argument("--strict", action="store_true", help="严格模式，校验失败时退出非零码")
    args = parser.parse_args()

    # 阶段文件名映射
    stage_map = {
        "s1": "user_story",
        "s2": "tasks",
        "s3": "testcases",
        "s4": "implementation",
        "s5": "test_report",
        "s6": "codereview",
        "s7": "demo_feedback",
        "s8": "progress_index"
    }

    stage_lower = args.stage.lower()
    if stage_lower not in stage_map:
        print(f"[Validator] ❌ 未知阶段: {args.stage}")
        sys.exit(1 if args.strict else 0)

    file_path = os.path.join("aceflow", "iterations", args.iteration, args.task, f"s{args.stage[1]}_{stage_map[stage_lower]}.md")

    fm_data = parse_frontmatter(file_path)
    if fm_data is None:
        if args.strict:
            sys.exit(1)
        else:
            return

    if not validate_fields(fm_data):
        if args.strict:
            sys.exit(1)
        else:
            return

    if not validate_status(fm_data):
        if args.strict:
            sys.exit(1)

    print(f"[Validator] ✅ 文件校验通过: {file_path}")

if __name__ == "__main__":
    main()
