#!/usr/bin/env python3
import subprocess
import os
import sys
import datetime
import argparse

def run_maven_test(test_class, project_dir):
    """执行 Maven 测试命令"""
    # 构建 Maven 命令
    maven_cmd = ["mvn", "clean", "test", f"-Dtest={test_class}"]
    
    # 切换到项目目录执行命令
    try:
        print(f"执行测试: {test_class}")
        print(f"命令: {' '.join(maven_cmd)}")
        print(f"项目目录: {project_dir}")
        
        # 执行命令并捕获输出
        process = subprocess.run(
            maven_cmd,
            cwd=project_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=False
        )
        output = process.stdout + process.stderr
        
        # 检查测试是否成功
        if "BUILD SUCCESS" in output:
            status = "通过"
        else:
            status = "失败"
            
        print(f"测试状态: {status}")
        return status, output
        
    except Exception as e:
        error_msg = f"测试执行过程中发生错误: {str(e)}\n"
        print(error_msg)
        return "错误", error_msg

def main():
    parser = argparse.ArgumentParser(description="运行单个 Maven 测试类")
    parser.add_argument("test_class", help="要测试的类名，例如: UserControllerIntegrationTest")
    parser.add_argument("--project-dir", default="src/backend", help="Maven 项目目录")
    
    args = parser.parse_args()
    
    # 获取当前迭代和任务信息（假设脚本在 aceflow/tools 目录下运行）
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    iteration_task_dir = os.path.basename(os.path.dirname(base_dir))
    iteration_dir = os.path.basename(os.path.dirname(os.path.dirname(base_dir)))
    
    # 执行测试
    status, output = run_maven_test(args.test_class, os.path.join(base_dir, args.project_dir))
    
    # 输出结果摘要
    print("\n测试结果摘要:")
    print(f"测试类: {args.test_class}")
    print(f"状态: {status}")
    
    # 如果测试失败，输出错误信息摘要
    if status != "通过":
        print("\n错误摘要:")
        error_lines = [line for line in output.splitlines() if "ERROR" in line or "Failed" in line]
        if error_lines:
            print("\n".join(error_lines[:5]))  # 最多显示前5行错误信息
        else:
            print("未找到详细错误信息，请查看完整输出。")

if __name__ == "__main__":
    main()
