"""
金融市场监管热点分析与投资机会捕捉应用
使用 CrewAI 框架协调多个 AI 代理完成复杂的金融分析任务

注意：.env 文件由 launch_app.py 统一加载，此文件直接使用环境变量
"""

import os
from crewai import Agent, Task, Crew

# 确保环境变量已加载（如果直接运行此文件）
if not os.getenv('QWEN_API_KEY'):
    from dotenv import load_dotenv
    load_dotenv('.env', override=True)

# 工具函数已简化，如需使用可导入 read_file, save_file
# from crewai.tools import read_file, save_file


def create_financial_analysis_app():
    """
    创建金融市场监管热点分析与投资机会捕捉应用
    """
    print("[启动] 金融市场监管热点分析与投资机会捕捉应用")
    print("=" * 70)

    # 获取 API 配置（从.env 文件读取，由 launch_app.py 加载）
    api_key = os.getenv('QWEN_API_KEY')
    api_base = os.getenv('QWEN_API_BASE')
    model = os.getenv('QWEN_MODEL')

    # 默认值
    if not api_base:
        api_base = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
    if not model:
        model = 'qwen3.5-plus'

    # 检查 API 密钥是否有效
    def is_valid_key(key):
        if not key:
            return False
        patterns = ['your-', 'example', 'test', 'dummy', 'placeholder']
        return not any(p in key.lower() for p in patterns)

    print(f"[模型] {model}")
    print(f"[API] {api_base}")
    print(f"[密钥] {'已设置' if is_valid_key(api_key) else '未设置/无效，使用模拟模式'}")

    print("\n[团队] 组建金融分析 AI 团队...")

    # 创建专业的金融分析 AI 代理
    market_researcher = Agent(
        role='金融市场研究员',
        goal='追踪全球金融市场动态，识别新兴趋势和投资机会',
        backstory='您是经验丰富的金融市场研究员，拥有 10 年以上金融分析经验，专精于宏观经济分析、行业趋势预测和投资机会识别。',
        verbose=True,
        model=model
    )

    investment_analyst = Agent(
        role='投资分析师',
        goal='评估投资机会的风险收益比，提供投资建议',
        backstory='您是资深投资分析师，精通财务分析、估值建模和风险评估，拥有 CFA 资格认证，善于识别具有潜力的投资标的。',
        verbose=True,
        model=model
    )

    risk_manager = Agent(
        role='风险管理师',
        goal='评估投资风险，提供风险控制建议',
        backstory='您是风险管理专家，拥有丰富的市场风险、信用风险和流动性风险评估经验，致力于保护投资组合免受重大损失。',
        verbose=True,
        model=model
    )

    portfolio_strategist = Agent(
        role='投资组合策略师',
        goal='制定最优投资组合策略，平衡风险与收益',
        backstory='您是资产配置专家，精通现代投资组合理论，善于构建多元化投资组合以实现长期稳健回报。',
        verbose=True,
        model=model
    )

    print("[成功] AI 团队组建完成:")
    print(f"   1. {market_researcher.role}")
    print(f"   2. {investment_analyst.role}")
    print(f"   3. {risk_manager.role}")
    print(f"   4. {portfolio_strategist.role}")

    print("\n[任务] 定义金融分析任务...")

    # 定义金融分析任务
    market_trend_analysis = Task(
        description='分析当前全球金融市场的主要趋势，重点关注科技、新能源、生物医药、金融科技等热门板块。识别潜在的投资机会和风险因素。',
        expected_output='详细的市场趋势分析报告，包括热门板块表现、资金流向、政策影响、技术分析等。',
        agent=market_researcher
    )

    investment_opportunity_evaluation = Task(
        description='基于市场趋势分析，评估 3-5 个最具潜力的投资机会。计算预期收益率、风险指标和投资时机。',
        expected_output='投资机会评估报告，包含详细的基本面分析、估值模型、风险收益比计算。',
        agent=investment_analyst
    )

    risk_assessment = Task(
        description='对识别出的投资机会进行全面风险评估，包括市场风险、政策风险、流动性风险等。计算 VaR（风险价值）和压力测试结果。',
        expected_output='风险评估报告，包含各类风险指标、风险控制建议、止损策略等。',
        agent=risk_manager
    )

    portfolio_recommendation = Task(
        description='基于投资机会评估和风险评估结果，制定最优投资组合配置建议。考虑投资者风险偏好、投资期限和收益目标。',
        expected_output='投资组合建议报告，包含资产配置比例、投资时间表、监控指标等。',
        agent=portfolio_strategist
    )

    print("[成功] 任务定义完成:")
    print(f"   1. {market_trend_analysis.description[:50]}...")
    print(f"   2. {investment_opportunity_evaluation.description[:50]}...")
    print(f"   3. {risk_assessment.description[:50]}...")
    print(f"   4. {portfolio_recommendation.description[:50]}...")

    print("\n[团队] 创建金融分析团队...")

    # 创建金融分析团队
    financial_crew = Crew(
        agents=[market_researcher, investment_analyst, risk_manager, portfolio_strategist],
        tasks=[market_trend_analysis, investment_opportunity_evaluation, risk_assessment, portfolio_recommendation],
        verbose=True
    )

    print(f"[成功] 团队创建完成：{len(financial_crew.agents)}名专业 AI 分析师")
    print(f"[任务] 任务分配：{len(financial_crew.tasks)}项金融分析任务")

    print("\n[执行] 开始金融市场监管热点分析...")

    # 执行金融分析
    results = financial_crew.kickoff()

    print("\n" + "=" * 70)
    print("[完成] 金融市场分析完成!")
    print("=" * 70)

    # 输出分析结果 - 显示完整内容
    task_names = [
        "市场趋势分析",
        "投资机会评估",
        "风险评估",
        "投资组合建议"
    ]

    print("\n" + "=" * 70)
    print(" " * 25 + "详细分析结果")
    print("=" * 70)
    
    for i, (task_name, result) in enumerate(zip(task_names, results)):
        print(f"\n【{task_name}】")
        print("-" * 70)
        # 直接输出完整结果，不截断
        print(result)
        print()

    print("=" * 70)
    print(" " * 25 + "分析摘要")
    print("=" * 70)

    print(f"\n[成果]")
    print(f"   - 市场趋势：已识别")
    print(f"   - 投资机会：已评估")
    print(f"   - 风险评估：已完成")
    print(f"   - 投资建议：已制定")
    print(f"   - 状态：分析完成")

    print(f"\n[指标]")
    print(f"   - 分析维度：多角度综合分析")
    print(f"   - 风险控制：全面风险评估")
    print(f"   - 投资建议：量化策略推荐")
    print(f"   - 实用性：可操作的投资策略")

    print(f"\n[后续]")
    print(f"   1. 仔细审阅各项分析报告")
    print(f"   2. 评估投资建议的可行性")
    print(f"   3. 制定具体的投资执行计划")
    print(f"   4. 设定风险监控和调整机制")

    print(f"\n[声明]")
    print(f"   本分析结果仅供学习参考，不构成投资建议。")
    print(f"   投资有风险，入市需谨慎。")

    return results


def main():
    """
    主函数 - 启动金融分析应用
    """
    print("[应用] 金融市场监管热点分析与投资机会捕捉应用")
    print("[框架] CrewAI 多 AI 代理协作")
    print("=" * 70)

    # 运行金融分析应用
    results = create_financial_analysis_app()

    print(f"\n[完成] 金融分析应用执行完成!")
    print(f"应用成功使用 CrewAI 框架协调多个 AI 代理完成了金融市场监管热点分析。")

    return results


if __name__ == "__main__":
    results = main()
