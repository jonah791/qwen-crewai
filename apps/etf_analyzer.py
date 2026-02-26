#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
国内 ETF 投资分析应用

功能:
- 宏观经济政策解读
- 行业景气度跟踪
- 资金流向监测
- 技术指标量化
- 市场情绪感知
- 事件驱动捕捉
- 跨市场联动分析
- 投资决策融合
"""

import os
from crewai import Agent, Task, Crew

# 确保环境变量已加载（如果直接运行此文件）
if not os.getenv('QWEN_API_KEY'):
    from dotenv import load_dotenv
    load_dotenv('.env', override=True)


# ==================== Agent 配置区 ====================

AGENT_CONFIGS = [
    {
        "role": "宏观经济分析师",
        "goal": "解读国内宏观经济数据与重大政策，判断市场风险偏好和政策驱动方向",
        "backstory": "你是资深宏观经济分析师，拥有 10 年以上中国经济研究经验，"
                     "专精于 GDP、CPI、PPI、PMI 等经济数据解读，以及货币政策、"
                     "财政政策、产业政策分析。善于从宏观视角把握市场大方向。",
        "verbose": True,
        "enable_search": True,  # 启用搜索获取最新经济数据
        "search_options": {
            "search_strategy": "agent",  # 使用 agent 策略（多轮检索与整合）
            "enable_source": True,       # 返回搜索来源
            "freshness": 7,              # 7 天内的内容
        },
    },
    {
        "role": "行业研究员",
        "goal": "跟踪各行业高频数据，识别景气度向上或触底反转的行业",
        "backstory": "你是资深行业研究员，覆盖 30+ 个申万一级行业，"
                     "擅长通过高频数据（开工率、库存、价格、销量等）判断行业景气度变化，"
                     "能够及时发现行业拐点并给出投资建议。",
        "verbose": True,
        "enable_search": True,  # 启用搜索获取行业数据
        "search_options": {
            "search_strategy": "agent",  # agent 策略（多轮检索）
            "enable_source": True,
            "freshness": 7,
        },
    },
    {
        "role": "资金流向分析师",
        "goal": "监测北向资金、主力资金、两融余额、ETF 申赎数据，分析资金偏好",
        "backstory": "你是资金流向监测专家，实时跟踪北向资金、主力资金流向、"
                     "两融余额变化、ETF 申购赎回数据。善于从资金面发现主力意图，"
                     "识别资金持续流入的行业和个股。",
        "verbose": True,
        "enable_search": True,  # 启用搜索获取资金数据
        "search_options": {
            "search_strategy": "agent",  # agent 策略
            "enable_source": True,
            "freshness": 1,  # 只看最新数据
        },
    },
    {
        "role": "量化技术分析师",
        "goal": "对主要 ETF 计算技术指标，识别趋势和超买超卖信号",
        "backstory": "你是量化技术分析专家，精通 MA、MACD、KDJ、RSI、BOLL 等"
                     "常用技术指标，擅长趋势识别、支撑阻力位判断、超买超卖信号捕捉。"
                     "能够结合多周期共振给出精确的买卖点建议。",
        "verbose": True,
        "enable_search": True,  # 启用搜索获取最新行情和技术分析数据
        "search_options": {
            "search_strategy": "agent",  # agent 策略
            "enable_source": True,
            "freshness": 1,  # 只看最新行情
        },
    },
    {
        "role": "市场情绪分析师",
        "goal": "构建情绪指数，监控成交量、换手率、融资买入占比、期权 PCR、社交媒体热度",
        "backstory": "你是市场情绪监测专家，通过成交量、换手率、融资买入占比、"
                     "期权认沽认购比 (PCR)、社交媒体热度等多维度数据构建综合情绪指数，"
                     "能够识别市场极端情绪并提示反转机会。",
        "verbose": True,
        "enable_search": True,  # 启用搜索获取情绪数据
        "search_options": {
            "search_strategy": "agent",  # agent 策略
            "enable_source": True,
            "freshness": 3,  # 3 天内的舆情
        },
    },
    {
        "role": "事件驱动分析师",
        "goal": "实时抓取重要事件并评估其对相关 ETF 的短期影响",
        "backstory": "你是事件驱动策略专家，实时抓取财报发布、行业会议、"
                     "突发新闻、政策公告等重要事件，快速评估事件对相关 ETF 的"
                     "短期影响方向和幅度，捕捉事件驱动的交易机会。",
        "verbose": True,
        "enable_search": True,  # 启用搜索获取最新事件
        "search_options": {
            "search_strategy": "agent",  # agent 策略（多轮检索）
            "enable_source": True,
            "freshness": 1,  # 只看最新事件
        },
    },
    {
        "role": "跨市场分析师",
        "goal": "观察港股、美股、商品、债券市场表现，寻找联动机会或风险传导",
        "backstory": "你是全球市场联动专家，跟踪港股、美股、商品期货、"
                     "债券市场表现，善于发现跨市场套利机会和风险传导路径，"
                     "能够从全球视角给出 A 股 ETF 的投资建议。",
        "verbose": True,
        "enable_search": True,  # 启用搜索获取全球市场数据
        "search_options": {
            "search_strategy": "agent",  # agent 策略
            "enable_source": True,
            "freshness": 1,  # 只看最新行情
        },
    },
    {
        "role": "首席投资策略师",
        "goal": "整合所有信号，生成最终的投资方向和时机建议",
        "backstory": "你是首席投资策略师，拥有 20 年以上投资经验，"
                     "擅长综合宏观经济、行业景气、资金流向、技术面、情绪面、"
                     "事件驱动、跨市场等多维度信息，给出明确的 ETF 板块选择和"
                     "买卖点建议。你的建议以稳健著称，注重风险控制。",
        "verbose": True,
        "enable_search": False,  # 不需要搜索，只整合已有报告
    },
]


# ==================== Task 配置区 ====================

TASK_CONFIGS = [
    {
        "description": "解读国内最新宏观经济数据（GDP、CPI、PPI、PMI、社融等）和重大政策（货币政策、财政政策、产业政策），"
                     "判断当前市场整体风险偏好（高/中/低），识别主要政策驱动方向（如科技创新、消费升级、绿色能源等），"
                     "给出宏观层面的配置建议（如股票/债券/商品的大类资产配置比例）。",
        "expected_output": "宏观经济分析报告，包含：1)经济数据解读 2)政策方向判断 3)市场风险偏好评估 4)大类资产配置建议",
        "agent": None,
    },
    {
        "description": "跟踪国内主要行业（科技、消费、医药、金融、周期、制造等）的高频数据，"
                     "识别景气度向上（需求改善、价格上涨、库存下降）或触底反转（利空出尽、政策转向）的行业，"
                     "对每个行业给出景气度评分（1-5 分）和变化趋势（上升/持平/下降）。",
        "expected_output": "行业景气度跟踪报告，包含：1)各行业高频数据汇总 2)景气度评分排名 3)推荐关注的行业及理由",
        "agent": None,
    },
    {
        "description": "监测北向资金（沪股通 + 深股通）、主力资金、两融余额、ETF 申赎数据，"
                     "分析资金在行业（科技/消费/医药等）和风格（大盘/小盘、价值/成长）上的偏好，"
                     "识别资金持续净流入（3 日/5 日/10 日）的方向，提示大资金异动情况。",
        "expected_output": "资金流向监测报告，包含：1)北向资金流向 2)主力资金流向 3)两融数据 4)ETF 申赎数据 5)资金偏好分析",
        "agent": None,
    },
    {
        "description": "对主要宽基 ETF（沪深 300、中证 500、创业板等）和行业 ETF 计算常用技术指标，"
                     "包括 MA（5/10/20/60 日）、MACD、KDJ、RSI、BOLL 等，"
                     "识别当前趋势（上涨/下跌/震荡）、支撑位和阻力位、超买超卖信号，"
                     "对每个 ETF 给出技术面评分（1-5 分）和短期买卖信号。",
        "expected_output": "技术指标量化报告，包含：1)主要 ETF 技术指标汇总 2)趋势判断 3)支撑阻力位 4)买卖信号提示",
        "agent": None,
    },
    {
        "description": "监控市场情绪指标：成交量变化、换手率、融资买入占比、期权认沽认购比 (PCR)、"
                     "社交媒体（微博、雪球、股吧）热度，构建综合情绪指数（0-100），"
                     "当情绪指数处于极端值（<20 或>80）时提示反转机会，给出情绪面建议（乐观/中性/谨慎）。",
        "expected_output": "市场情绪分析报告，包含：1)各情绪指标数据 2)综合情绪指数 3)极端值提示 4)情绪面建议",
        "agent": None,
    },
    {
        "description": "实时抓取并分析重要事件：财报季业绩超预期/低于预期、重要行业会议、"
                     "突发新闻（政策/地缘/灾害）、公司公告（重组/减持/增持）等，"
                     "评估事件对相关 ETF 的短期影响（正面/负面/中性）和影响幅度（高/中/低），"
                     "给出事件驱动的交易建议（如业绩超预期可关注相关 ETF）。",
        "expected_output": "事件驱动分析报告，包含：1)重要事件汇总 2)事件影响评估 3)相关 ETF 推荐 4)交易时机建议",
        "agent": None,
    },
    {
        "description": "观察港股（恒生指数、恒生科技）、美股（标普 500、纳斯达克）、"
                     "商品（黄金、原油、铜）、债券（中美国债收益率）市场表现，"
                     "分析内外盘联动关系（如美股科技股对 A 股科技 ETF 的影响）、"
                     "风险传导路径（如美债收益率对成长股估值的影响），"
                     "寻找跨市场套利机会或风险提示。",
        "expected_output": "跨市场联动分析报告，包含：1)全球市场表现汇总 2)联动关系分析 3)风险传导评估 4)跨市场机会提示",
        "agent": None,
    },
    {
        "description": "整合以上所有分析报告（宏观、行业、资金、技术、情绪、事件、跨市场），"
                     "对主要 ETF 板块进行综合评分（1-5 分），"
                     "给出明确的投资方向（推荐/中性/回避）、具体 ETF 标的、"
                     "买卖点建议（如沪深 300ETF 可在 X 元以下分批建仓）、"
                     "仓位建议（如总仓位 6-7 成）、风险提示（如下行风险 Y%）。",
        "expected_output": "最终投资决策报告，包含：1)各维度信号汇总 2)ETF 板块综合评分 3)具体投资建议 4)风险提示",
        "agent": None,
    },
]


# ==================== 应用主逻辑 ====================

def create_agents():
    """创建所有 Agent"""
    agents = []
    for config in AGENT_CONFIGS:
        agent = Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            verbose=config["verbose"],
            enable_search=config.get("enable_search", True),  # 传递搜索设置
            search_options=config.get("search_options", None),  # 传递搜索高级选项
        )
        agents.append(agent)
        search_status = "启用" if config.get("enable_search", True) else "禁用"
        search_strategy = config.get("search_options", {}).get("search_strategy", "turbo") if config.get("enable_search", True) else "N/A"
        print(f"[Agent] 已创建：{config['role']} (搜索：{search_status}, 策略：{search_strategy})")
    return agents


def create_tasks(agents):
    """创建所有 Task 并绑定 Agent"""
    tasks = []
    for i, config in enumerate(TASK_CONFIGS):
        # 前 7 个任务分配给对应的专业分析师，最后一个决策任务分配给首席策略师
        if i < len(agents) - 1:
            config['agent'] = agents[i]
        else:
            config['agent'] = agents[-1]  # 最后一个 Agent 是首席策略师

        task = Task(
            description=config["description"],
            expected_output=config["expected_output"],
            agent=config['agent'],
        )
        tasks.append(task)
        print(f"[Task] 已创建：{config['description'][:40]}...")
    return tasks


def run_analysis():
    """运行分析主流程"""
    print("\n" + "=" * 70)
    print(" " * 20 + "国内 ETF 投资分析系统")
    print("=" * 70)

    # 获取 API 配置
    model = os.getenv('QWEN_MODEL', 'qwen3.5-plus')
    print(f"[模型] {model}")
    print(f"[分析维度] 7 个专业分析 + 1 个决策融合")

    # 创建 Agent
    print("\n[阶段 1] 创建分析师团队...")
    agents = create_agents()
    print(f"[完成] 共创建 {len(agents)} 名专业分析师")

    # 创建 Task
    print("\n[阶段 2] 定义分析任务...")
    tasks = create_tasks(agents)
    print(f"[完成] 共定义 {len(tasks)} 项分析任务")

    # 创建 Crew
    print("\n[阶段 3] 组建分析团队...")
    crew = Crew(
        agents=agents,
        tasks=tasks,
        verbose=True,
    )
    print(f"[完成] 团队组建完成：{crew}")

    # 执行任务
    print("\n" + "=" * 70)
    print("[执行] 开始 ETF 投资分析（激进模式）...")
    print("=" * 70)

    # 使用激进并行执行（无速率限制）
    # max_workers=7: 7 个独立分析任务同时执行
    # rate_limit=None: 不限制速率（可能触发 429，但速度最快）
    results = crew.kickoff_parallel(max_workers=7, rate_limit=None)
    
    # 统计 token 使用
    total_tokens = 0
    total_prompt_tokens = 0
    total_completion_tokens = 0
    for agent in agents:
        if hasattr(agent.llm, 'total_tokens'):
            total_tokens += agent.llm.total_tokens
            total_prompt_tokens += agent.llm.total_prompt_tokens
            total_completion_tokens += agent.llm.total_completion_tokens

    # 输出结果
    print("\n" + "=" * 70)
    print(" " * 25 + "分析结果汇总")
    print("=" * 70)

    task_names = [
        "宏观经济分析",
        "行业景气度跟踪",
        "资金流向监测",
        "技术指标量化",
        "市场情绪分析",
        "事件驱动捕捉",
        "跨市场联动",
        "投资决策建议"
    ]

    # 输出完整结果（不截断）
    for i, (name, result) in enumerate(zip(task_names, results), 1):
        print(f"\n{'='*70}")
        print(f"[{i}] {name}")
        print("=" * 70)
        # 处理可能的字典/列表格式结果
        if isinstance(result, list) and len(result) > 0:
            # DashScope MultiModalConversation 返回格式
            for item in result:
                if isinstance(item, dict) and 'text' in item:
                    # 移除可能的 emoji 字符（Windows GBK 不支持）
                    text = item['text']
                    text = text.replace('🔴', '[红圈]').replace('🟢', '[绿圈]')
                    text = text.replace('✅', '[OK]').replace('⚠️', '[警告]')
                    print(text.encode('gbk', errors='ignore').decode('gbk'))
                else:
                    print(str(item).encode('gbk', errors='ignore').decode('gbk'))
        elif isinstance(result, dict) and 'text' in result:
            print(result['text'].encode('gbk', errors='ignore').decode('gbk'))
        else:
            # 普通字符串
            print(str(result).encode('gbk', errors='ignore').decode('gbk'))

    # 返回结果和 token 统计
    token_stats = (total_tokens, total_prompt_tokens, total_completion_tokens)
    return results, token_stats


def main():
    """入口函数"""
    try:
        result_data = run_analysis()
        if result_data:
            results, token_stats = result_data
            print("\n" + "=" * 70)
            print("[完成] ETF 投资分析完成!")
            print("=" * 70)
            
            # 输出 token 统计
            if token_stats:
                total_tokens, total_prompt, total_completion = token_stats
                print(f"\n[Token 统计]")
                print(f"   - 输入 Token: {total_prompt:,}")
                print(f"   - 输出 Token: {total_completion:,}")
                print(f"   - 总计 Token: {total_tokens:,}")
                
                # 估算费用（qwen3.5-plus: 输入 0.002 元/千 tokens, 输出 0.006 元/千 tokens）
                # 搜索策略费用：agent 策略 4 元/1000 次
                input_cost = (total_prompt / 1000) * 0.002
                output_cost = (total_completion / 1000) * 0.006
                search_cost = 8 * 4 / 1000  # 8 个 agent，每个 1 次搜索
                total_cost = input_cost + output_cost + search_cost
                
                print(f"\n[费用估算]")
                print(f"   - 模型输入费用：{input_cost:.4f}元")
                print(f"   - 模型输出费用：{output_cost:.4f}元")
                print(f"   - 搜索策略费用：{search_cost:.4f}元 (agent 策略，4 元/千次)")
                print(f"   - 总计费用：{total_cost:.4f}元")
            
            print("\n[提示] 以上分析结果仅供参考，不构成投资建议。")
            print("       投资有风险，入市需谨慎。")
    except Exception as e:
        print(f"\n[错误] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
