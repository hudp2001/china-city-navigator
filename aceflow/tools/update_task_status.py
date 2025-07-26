import os
import datetime

def update_task_status(file_path, updates):
    if not os.path.exists(file_path):
        print(f"Error: Task status table {file_path} not found.")
        return
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    updated_lines = []
    for line in lines:
        for key, value in updates.items():
            if key in line:
                line = line.replace(key, value)
        updated_lines.append(line)
    
    with open(file_path, 'w') as f:
        f.writelines(updated_lines)
    
    print(f"Task status table {file_path} updated successfully.")

# 示例更新数据
updates = {
    "进行中": "已完成",
    "2025-07-01 03:30": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
}

update_task_status('./aceflow_result/iterations/task_status_table.md', updates)