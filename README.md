# 盈透证券股票成本与盈利计算器
# Interactive Brokers Stock Cost and Profit Calculator

一个简单易用的工具，用于计算盈透证券（Interactive Brokers）的股票交易成本、佣金和盈利。

A simple and user-friendly tool for calculating Interactive Brokers stock trading costs, commissions, and profits.

## 功能特性 Features

### 股票计算器 Stock Calculator
- ✅ **简单计算** - 单笔买入或卖出交易计算
- ✅ **盈利计算** - 完整的买卖盈利分析
- ✅ **多笔交易** - 支持多笔交易的累计计算
- ✅ **自动佣金计算** - 按照IB的佣金规则自动计算
- ✅ **双语界面** - 中英文双语支持
- ✅ **响应式设计** - 支持桌面和移动设备

### 🎲 儿童概率解谜游戏 Probability Puzzles for Kids (NEW!)
- 🚪 **三门问题** - 经典概率悖论，学习条件概率
- 🔢 **猜数字游戏** - 通过反馈缩小范围，理解信息熵
- 🏁 **概率赛道** - 计算期望值，做出最优决策
- 🎰 **概率模拟器** - 观察大数定律，理解随机性

## IB佣金规则 IB Commission Rules

- **每股佣金**: $0.0035 per share
- **最低佣金**: $0.35 minimum per order
- **最高佣金**: 交易额的1% (1% of trade value maximum)

## 使用方法 Usage

### 股票计算器 Stock Calculator

#### 方法一：网页版 Web Version

直接在浏览器中打开 `index.html` 文件即可使用。

Simply open `index.html` in your web browser.

```bash
# 使用默认浏览器打开
open index.html  # macOS
xdg-open index.html  # Linux
start index.html  # Windows
```

#### 方法二：Python版 Python Version

运行Python脚本查看示例或进行自定义计算。

Run the Python script to see examples or perform custom calculations.

```bash
# 运行示例
python3 ib_calculator.py

# 或在Python代码中使用
from ib_calculator import IBStockCalculator

calculator = IBStockCalculator()

# 计算买入成本
buy_info = calculator.calculate_buy_cost(shares=100, price=150.00)
print(f"总成本: ${buy_info['total_cost']}")

# 计算盈利
profit_info = calculator.calculate_profit(
    buy_shares=100,
    buy_price=150.00,
    sell_shares=100,
    sell_price=160.00
)
print(f"盈利: ${profit_info['profit']}")
print(f"盈利率: {profit_info['profit_percentage']}%")
```

### 🎲 儿童概率解谜游戏 Probability Puzzles for Kids

#### 网页版 Web Version

打开 `probability_puzzles.html` 即可体验互动游戏。

Open `probability_puzzles.html` to experience interactive games.

```bash
# 使用默认浏览器打开
open probability_puzzles.html  # macOS
xdg-open probability_puzzles.html  # Linux
start probability_puzzles.html  # Windows
```

#### Python版 Python Version

运行Python脚本查看游戏演示和概率统计。

Run the Python script to see game demos and probability statistics.

```bash
# 运行所有游戏的演示
python3 probability_games.py

# 运行使用示例
python3 probability_example.py

# 或在Python代码中使用
from probability_games import MontyHallGame, NumberGuessingGame

# 三门问题游戏
game = MontyHallGame()
game.new_game()
game.make_choice(1)
result = game.final_decision(switch=True)
print(f"你{'赢了' if result['won'] else '输了'}!")

# 猜数字游戏
guessing_game = NumberGuessingGame(1, 100)
guessing_game.new_game('medium')
result = guessing_game.make_guess(50)
print(result['message'])
```

## 计算示例 Examples

### 示例1：简单买入 Simple Buy

```python
买入 100股 @ $150.00
股票成本: $15,000.00
佣金: $0.35 (最低佣金)
总成本: $15,000.35
平均成本/股: $150.0035
```

### 示例2：盈利计算 Profit Calculation

```python
买入: 100股 @ $150.00
卖出: 100股 @ $160.00

买入总成本: $15,000.35
卖出净收入: $15,999.65
盈利: $999.30
盈利率: 6.66%
```

### 示例3：多笔交易 Multiple Transactions

```python
交易1: 买入 100股 @ $50.00
交易2: 买入 50股 @ $52.00
交易3: 卖出 80股 @ $55.00
交易4: 卖出 30股 @ $57.00

剩余股数: 40
总盈利: $498.76
```

## 功能说明 Function Description

### Python API

#### `calculate_buy_cost(shares, price)`
计算买入交易的总成本，包括佣金。

Calculate the total cost of a buy transaction, including commission.

**参数 Parameters:**
- `shares`: 买入股数 (number of shares)
- `price`: 买入价格 (buy price)

**返回 Returns:**
包含以下字段的字典：
- `stock_cost`: 股票成本
- `commission`: 佣金
- `total_cost`: 总成本
- `avg_cost_per_share`: 平均成本/股

#### `calculate_sell_proceeds(shares, price)`
计算卖出交易的净收入，扣除佣金。

Calculate the net proceeds from a sell transaction, minus commission.

**参数 Parameters:**
- `shares`: 卖出股数 (number of shares)
- `price`: 卖出价格 (sell price)

**返回 Returns:**
包含以下字段的字典：
- `gross_proceeds`: 总收入
- `commission`: 佣金
- `net_proceeds`: 净收入
- `avg_proceeds_per_share`: 平均收入/股

#### `calculate_profit(buy_shares, buy_price, sell_shares, sell_price)`
计算完整的交易盈利分析。

Calculate complete trade profit analysis.

**参数 Parameters:**
- `buy_shares`: 买入股数
- `buy_price`: 买入价格
- `sell_shares`: 卖出股数
- `sell_price`: 卖出价格

**返回 Returns:**
包含买入信息、卖出信息、盈利信息和剩余持仓的完整字典。

#### `calculate_multiple_transactions(transactions)`
计算多笔交易的总计。

Calculate totals for multiple transactions.

**参数 Parameters:**
- `transactions`: 交易列表，每个交易包含 `type`, `shares`, `price`

**返回 Returns:**
包含总计信息的字典。

## 技术栈 Tech Stack

- **Python**: 使用Decimal进行精确计算
- **HTML/CSS/JavaScript**: 响应式Web界面
- **无依赖**: 纯原生实现，无需安装额外包

## 概率游戏说明 Probability Games Guide

### 为什么要学习概率？Why Learn Probability?

概率是理解不确定世界的重要工具，通过游戏化的方式学习概率，可以：
- 🧠 培养逻辑思维和分析能力 Develop logical thinking and analytical skills
- 🎯 理解决策中的风险和收益 Understand risk and reward in decision making
- 📊 学会用数学方法解决实际问题 Learn to solve real problems with mathematics
- 🎮 在趣味中掌握抽象的数学概念 Master abstract math concepts through fun

Probability is an important tool for understanding an uncertain world. Learning probability through games helps:
- Develop logical thinking and analytical skills
- Understand risk and reward in decision making
- Learn to solve real problems with mathematics
- Master abstract math concepts through fun and engagement

### 🚪 三门问题 Monty Hall Problem

经典的概率悖论游戏，展示条件概率的反直觉特性。

A classic probability paradox demonstrating counter-intuitive properties of conditional probability.

**教学价值 Educational Value:**
- 理解条件概率 Understanding conditional probability
- 学习在新信息下更新决策 Learning to update decisions with new information
- 挑战直觉思维 Challenging intuitive thinking

**玩法 How to Play:**
1. 选择三扇门中的一扇 Choose one of three doors
2. 主持人打开一扇有山羊的门 Host opens a door with a goat
3. 决定是否换门 Decide whether to switch
4. 观察结果并理解为什么换门胜率更高 Observe results and understand why switching has higher win rate

### 🔢 猜数字游戏 Number Guessing Game

通过反馈缩小范围，理解信息熵和二分查找。

Narrow down the range through feedback, understand information entropy and binary search.

**教学价值 Educational Value:**
- 理解信息熵的概念 Understanding information entropy
- 学习二分查找策略 Learning binary search strategy
- 训练逻辑推理能力 Training logical reasoning

**玩法 How to Play:**
1. 选择难度级别 Choose difficulty level
2. 根据"太大"或"太小"的提示调整猜测 Adjust guesses based on "too high" or "too low" hints
3. 在有限次数内猜中数字 Guess the number within limited attempts

### 🏁 概率赛道 Probability Race

计算期望值，选择最优路径到达终点。

Calculate expected values and choose optimal paths to reach the finish line.

**教学价值 Educational Value:**
- 理解期望值的概念 Understanding expected value
- 学习风险与收益权衡 Learning risk-reward tradeoffs
- 应用概率进行决策 Applying probability to decision making

**玩法 How to Play:**
1. 在每个路口选择一条路径 Choose a path at each junction
2. 每条路径有不同的距离和成功率 Each path has different distance and success rate
3. 计算期望值选择最优策略 Calculate expected values to choose optimal strategy

### 🎰 概率模拟器 Probability Simulator

观察大数定律，理解长期频率趋近于理论概率。

Observe the law of large numbers, understand how long-term frequency approaches theoretical probability.

**教学价值 Educational Value:**
- 理解独立事件 Understanding independent events
- 观察大数定律 Observing law of large numbers
- 区分理论概率和实际频率 Distinguishing theoretical probability from actual frequency

**玩法 How to Play:**
1. 查看每个符号的理论概率 View theoretical probability of each symbol
2. 多次转动观察结果 Spin multiple times and observe results
3. 比较实际频率和理论概率 Compare actual frequency with theoretical probability

## 文件结构 File Structure

```
.
├── ib_calculator.py         # Python股票计算器核心
├── index.html               # 股票计算器Web界面
├── example.py               # 股票计算器示例
├── probability_games.py     # Python概率游戏核心
├── probability_puzzles.html # 概率游戏Web界面
├── probability_example.py   # 概率游戏使用示例
└── README.md               # 文档
```

## 注意事项 Notes

1. 本计算器仅计算基础交易佣金，不包括：
   - SEC费用
   - FINRA交易活动费
   - 市场数据费用
   - 其他可能的费用

2. 佣金规则基于IB美股固定价格方案，实际费用可能因账户类型和市场不同而异。

3. 本工具仅供参考，实际交易请以IB官方账单为准。

---

1. This calculator only computes basic trading commissions, excluding:
   - SEC fees
   - FINRA Trading Activity Fee
   - Market data fees
   - Other potential fees

2. Commission rules are based on IB's US Stock Fixed pricing plan. Actual fees may vary by account type and market.

3. This tool is for reference only. Always refer to official IB statements for actual trading costs.

## 贡献 Contributing

欢迎提交问题和改进建议！

Issues and improvement suggestions are welcome!

## 许可证 License

MIT License

## 免责声明 Disclaimer

本工具仅供教育和参考目的。使用本工具不构成投资建议。交易有风险，投资需谨慎。

This tool is for educational and reference purposes only. Using this tool does not constitute investment advice. Trading involves risks.
