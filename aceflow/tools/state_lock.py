import argparse
import os
import json
import yaml
from datetime import datetime

LOCK_FILE = "aceflow/status.lock.json"
CONTEXT_DIR = ".context"

def load_lock():
    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"[state_lock] ⚠️ 锁文件格式错误，已重置为空")
    return {}

def save_lock(lock):
    os.makedirs(os.path.dirname(LOCK_FILE), exist_ok=True)
    with open(LOCK_FILE, "w", encoding="utf-8") as f:
        json.dump(lock, f, indent=2, ensure_ascii=False)

def load_context(task_id):
    context_path = os.path.join(CONTEXT_DIR, f"{task_id}.yaml")
    if not os.path.exists(context_path):
        print(f"[state_lock] ❌ 未找到上下文文件: {context_path}")
        return None
    with open(context_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def lock_task(task_id):
    context = load_context(task_id)
    if not context:
        return

    lock = load_lock()
    if task_id in lock and lock[task_id]["status"] == "locked":
        print(f"[state_lock] ⚠️ 任务 {task_id} 已被锁定，无需重复锁定。")
    else:
        lock[task_id] = {
            "status": "locked",
            "timestamp": datetime.now().isoformat(),
            "iteration": context.get("iteration", "unknown"),
            "stage": context.get("stage", "unknown"),
            "doc_owner": context.get("doc_owner", "unknown")
        }
        save_lock(lock)
        print(f"[state_lock] ✅ 已锁定任务：{task_id}（阶段：{lock[task_id]['stage']}）")

def unlock_task(task_id):
    lock = load_lock()
    if task_id not in lock:
        print(f"[state_lock] ⚠️ 任务 {task_id} 当前未锁定")
    else:
        lock.pop(task_id)
        save_lock(lock)
        print(f"[state_lock] 🔓 已解锁任务：{task_id}")

def print_lock_status():
    lock = load_lock()
    if not lock:
        print("[state_lock] 🔍 当前无锁定任务")
    else:
        print("[state_lock] 🔐 当前锁定状态：")
        for task_id, meta in lock.items():
            ts = meta.get("timestamp", "unknown")
            stage = meta.get("stage", "unknown")
            owner = meta.get("doc_owner", "unknown")
            print(f"  └─ {task_id} 🟩 {stage} by {owner} at {ts}")

def main():
    parser = argparse.ArgumentParser(description="ACEFLOW 状态锁控制")
    parser.add_argument("--lock", action="store_true", help="锁定指定任务")
    parser.add_argument("--unlock", action="store_true", help="解锁指定任务")
    parser.add_argument("--status", action="store_true", help="查看当前所有锁定状态")
    parser.add_argument("--task", type=str, help="指定任务 ID")

    args = parser.parse_args()

    if args.status:
        print_lock_status()
        return

    if not args.task:
        print("[state_lock] ❌ 请通过 --task 指定任务 ID")
        return

    if args.lock:
        lock_task(args.task)
    elif args.unlock:
        unlock_task(args.task)
    else:
        print("[state_lock] ❗ 未指定操作类型，请使用 --lock / --unlock / --status")

if __name__ == "__main__":
    main()
