#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CrewAI 多应用启动器
API 配置统一在.env 文件中管理
"""

import os
import sys

# 应用注册表 - 在此添加新应用
APPLICATIONS = {
    "1": {
        "name": "金融市场监管热点分析",
        "module": "apps.financial_market_analyzer",  # 更新路径
        "description": "分析金融市场热点、监管动态和投资策略"
    },
    "2": {
        "name": "国内 ETF 投资分析",
        "module": "apps.etf_analyzer",  # 更新路径
        "description": "分析国内 ETF 市场，评估投资机会和风险"
    },
    # 添加新应用示例:
    # "3": {"name": "智能客服助手", "module": "apps.customer_service_bot", "description": "基于 CrewAI 的智能客服系统"},
}


def setup_environment():
    """设置环境"""
    print("=" * 60)
    print(" " * 18 + "CrewAI 多应用启动器")
    print("=" * 60)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    if os.getcwd() != script_dir:
        os.chdir(script_dir)

    print(f"[目录] {os.getcwd()}")
    print(f"[Python] {sys.version.split()[0]}")

    # 加载.env 文件（优先使用绝对路径）
    env_path = os.path.join(script_dir, '.env')
    try:
        from dotenv import load_dotenv
        if os.path.exists(env_path):
            load_dotenv(env_path, override=True)
            print(f"[配置] 已加载：{env_path}")
        elif os.path.exists('.env'):
            load_dotenv('.env', override=True)
            print(f"[配置] 已加载：.env")
        else:
            print("[配置] 使用现有环境变量")
    except ImportError:
        print("[配置] 使用现有环境变量 (python-dotenv 未安装)")

    # 显示 API 配置
    api_key = os.getenv('QWEN_API_KEY')
    model = os.getenv('QWEN_MODEL', 'qwen3.5-plus')
    is_valid = api_key and not any(p in api_key.lower() for p in ['your-', 'example', 'test', 'dummy'])
    print(f"[API] {'Qwen: ' + api_key[:8] + '***' if is_valid else '模拟模式'} | 模型：{model}")
    print("=" * 60)
    
    return True  # 返回 True 表示环境已设置


def show_menu():
    """显示应用菜单"""
    print("\n请选择要启动的应用:\n")
    for key, app in APPLICATIONS.items():
        print(f"  [{key}] {app['name']}")
        print(f"      {app['description']}\n")
    print("  [0] 退出\n")


def launch(app_key):
    """启动应用"""
    if app_key not in APPLICATIONS:
        print(f"[错误] 无效选项：{app_key}")
        return

    app = APPLICATIONS[app_key]
    print(f"\n[启动] {app['name']}...")
    print("-" * 60)

    try:
        module = __import__(app['module'], fromlist=['main'])
        if hasattr(module, 'main'):
            module.main()
            print("-" * 60)
            print(f"[完成] {app['name']} 运行结束")
        else:
            print(f"[错误] 模块 {app['module']} 没有 main() 函数")
    except Exception as e:
        print(f"[错误] {type(e).__name__}: {e}")


def main():
    """主函数"""
    setup_environment()

    while True:
        show_menu()
        try:
            choice = input("请输入选项编号：").strip()
            if choice == "0":
                print("\n[退出] 再见!")
                break
            elif choice in APPLICATIONS:
                launch(choice)
                if input("\n是否继续？(y/n): ").strip().lower() != 'y':
                    print("\n[退出] 再见!")
                    break
            else:
                print(f"[提示] 请输入 0-{len(APPLICATIONS)} 之间的数字")
        except (KeyboardInterrupt, EOFError):
            print("\n\n[退出] 程序终止")
            break

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
