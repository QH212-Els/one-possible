# 留学生生活サポート Multi-Agent System

这是一个完整可运行的 Python 项目，包含三个 Agent 功能：

1. 日语消息回复 Agent
2. 消费法律小助手 Agent
3. 兼职排班与收入管理 Agent

项目不需要安装第三方库，也不需要 API Key。只要电脑有 Python，就可以直接运行。

---

## 1. 项目解决的核心痛点

在日本生活的留学生经常会遇到三类问题：

### 1. 日语沟通困难

收到学校、打工、面试、房东或快递相关的日语消息时，虽然能看懂大概意思，但不知道如何自然、礼貌地回复。

### 2. 消费和合同问题难判断

遇到退货、取消、租房、打工工资、合同纠纷时，不知道问题大概属于哪一类，也不知道下一步应该找谁咨询。

### 3. 打工时间和收入不好管理

留学生需要同时考虑课程、排班、收入和每周工时限制。如果没有工具辅助，容易出现排班冲突、打工时间过长或收入估算不清楚的问题。

---

## 2. 核心逻辑流

本项目采用多 Agent 协同方式，每个功能都由多个 Agent 分步骤完成，而不是直接给出结果。

---

# 功能一：日语消息回复 Agent

## 核心逻辑流

用户输入日语消息和自己想表达的意思后，系统按以下流程处理：

输入消息  
→ SceneAgent 判断场景  
→ IntentionAgent 判断对方意图  
→ InformationAgent 提取重要信息  
→ ReplyAgent 生成三种回复  
→ CheckAgent 检查敬语和遗漏信息  
→ 输出结果

## 包含的 Agent

- SceneAgent：判断是面试、学校、打工、租房、快递还是日常沟通
- IntentionAgent：判断对方是否要求确认、提交资料、前往某地等
- InformationAgent：提取时间、履历书、身分证、地址等重要信息
- ReplyAgent：生成简洁版、礼貌版、自然版回复
- CheckAgent：检查敬语、感谢表达和信息遗漏

---

# 功能二：消费法律小助手 Agent

## 核心逻辑流

用户输入遇到的消费或生活问题后，系统按以下流程处理：

输入问题  
→ LawCategoryAgent 判断问题类型  
→ RelatedLawAgent 匹配相关制度  
→ RiskAgent 判断风险程度  
→ ExplanationAgent 用简单语言说明  
→ ActionAgent 给出下一步建议  
→ 输出结果

## 包含的 Agent

- LawCategoryAgent：判断问题属于购物退货、クーリング・オフ、租房、打工劳动条件或消费者合同纠纷
- RelatedLawAgent：匹配可能相关的制度，例如消費者契約法、労働基準法、賃貸借契約等
- RiskAgent：粗略判断问题紧急程度
- ExplanationAgent：用留学生容易理解的语言说明
- ActionAgent：建议保存证据、不要立刻付款、咨询消费者中心或学校等

## 注意

这个功能不是律师，不提供正式法律意见，只是帮助留学生整理问题和判断咨询方向。

---

# 功能三：兼职排班与收入管理 Agent

## 核心逻辑流

用户输入时薪、预计每周工时、课程时间和排班时间后，系统按以下流程处理：

输入数据  
→ InputConvertAgent 转换数字  
→ IncomeAgent 计算预计周收入和月收入  
→ WorkHourLimitAgent 判断是否接近或超过每周28小时  
→ ScheduleConflictAgent 判断课程和排班是否可能冲突  
→ AdviceAgent 给出建议  
→ 输出结果

## 包含的 Agent

- InputConvertAgent：把用户输入的时薪和工时转换为数字
- IncomeAgent：计算预计收入
- WorkHourLimitAgent：检查是否接近或超过28小时
- ScheduleConflictAgent：检查课程日期和排班日期是否重合
- AdviceAgent：给出学习和打工平衡建议

---

## 3. 是否包含长链推理

包含。

本项目不是输入后直接输出一句话，而是分成多个步骤进行判断。例如消费法律小助手会先判断问题类型，再判断相关制度和风险，最后才给出说明和行动建议。

这种流程属于基础版长链推理，逻辑清楚，也方便以后接入大语言模型 API。

---

## 4. 是否包含多 Agent 协同

包含。

每个功能都由多个 Agent 协作完成，并由对应的 System 类统一调度：

- JapaneseReplyAgentSystem
- ConsumerLawAgentSystem
- WorkShiftAgentSystem

主程序 main.py 提供统一入口，让用户选择不同功能。

---

## 5. 项目结构

```text
student_life_agent/
├── main.py
├── japanese_reply_agent.py
├── consumer_law_agent.py
├── work_shift_agent.py
└── README.md
```

---

## 6. 运行方法

进入项目文件夹：

```bash
cd student_life_agent
```

运行：

```bash
python main.py
```

Mac 或部分电脑可以使用：

```bash
python3 main.py
```

---

## 7. 使用示例

### 日语消息回复 Agent 输入示例

```text
明日の16時から面接を行いますので、履歴書を持参してお越しください。ご確認よろしくお願いいたします。
```

用户想表达：

```text
确认可以去，并表示感谢
```

### 消费法律小助手 Agent 输入示例

```text
我在网上买了商品，但是收到后发现和说明不一样，想取消订单。
```

### 兼职排班与收入管理 Agent 输入示例

时薪：

```text
1200
```

本周打工时间：

```text
26
```

课程说明：

```text
周一周五15点下课，周三17点下课
```

排班说明：

```text
周三18-22点，周六10-18点
```

---

## 8. token plan / 赠金额度的使用说明

如果之后接入真实大语言模型 API，token plan 或赠金额度可以用于：

1. 分析更长的日语邮件和短信
2. 进行更自然的敬语修改
3. 判断更复杂的消费法律问题
4. 根据真实课程表生成更准确的排班建议
5. 支持多轮对话修改和长链推理
6. 让不同 Agent 之间传递更详细的分析结果

预期成果是帮助留学生更快处理生活、学习和打工中的常见问题，提高日语沟通效率，减少误会，并更合理地安排打工时间。
