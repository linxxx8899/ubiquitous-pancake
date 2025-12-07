#!/usr/bin/env python3
"""
使用示例 / Usage Examples
"""

from ib_calculator import IBStockCalculator, print_transaction_summary


def example_1_simple_buy():
    """示例1: 简单买入"""
    print("\n" + "="*60)
    print("示例1: 简单买入 / Example 1: Simple Buy")
    print("="*60)
    
    calculator = IBStockCalculator()
    result = calculator.calculate_buy_cost(shares=100, price=150.00)
    
    print(f"\n买入 100股 @ $150.00")
    print(f"股票成本: ${result['stock_cost']}")
    print(f"佣金: ${result['commission']}")
    print(f"总成本: ${result['total_cost']}")
    print(f"平均成本/股: ${result['avg_cost_per_share']}")


def example_2_simple_sell():
    """示例2: 简单卖出"""
    print("\n" + "="*60)
    print("示例2: 简单卖出 / Example 2: Simple Sell")
    print("="*60)
    
    calculator = IBStockCalculator()
    result = calculator.calculate_sell_proceeds(shares=100, price=160.00)
    
    print(f"\n卖出 100股 @ $160.00")
    print(f"总收入: ${result['gross_proceeds']}")
    print(f"佣金: ${result['commission']}")
    print(f"净收入: ${result['net_proceeds']}")
    print(f"平均收入/股: ${result['avg_proceeds_per_share']}")


def example_3_profit_calculation():
    """示例3: 盈利计算"""
    print("\n" + "="*60)
    print("示例3: 盈利计算 / Example 3: Profit Calculation")
    print("="*60)
    
    calculator = IBStockCalculator()
    result = calculator.calculate_profit(
        buy_shares=100,
        buy_price=150.00,
        sell_shares=100,
        sell_price=160.00
    )
    
    print_transaction_summary(result)


def example_4_partial_sell():
    """示例4: 部分卖出"""
    print("\n" + "="*60)
    print("示例4: 部分卖出 / Example 4: Partial Sell")
    print("="*60)
    
    calculator = IBStockCalculator()
    result = calculator.calculate_profit(
        buy_shares=200,
        buy_price=50.00,
        sell_shares=100,
        sell_price=55.00
    )
    
    print_transaction_summary(result)


def example_5_multiple_transactions():
    """示例5: 多笔交易"""
    print("\n" + "="*60)
    print("示例5: 多笔交易 / Example 5: Multiple Transactions")
    print("="*60)
    
    calculator = IBStockCalculator()
    
    transactions = [
        {'type': 'buy', 'shares': 100, 'price': 50.00},
        {'type': 'buy', 'shares': 50, 'price': 52.00},
        {'type': 'sell', 'shares': 80, 'price': 55.00},
        {'type': 'sell', 'shares': 30, 'price': 57.00},
    ]
    
    print("\n交易记录:")
    for i, trans in enumerate(transactions, 1):
        trans_type = "买入" if trans['type'] == 'buy' else "卖出"
        print(f"{i}. {trans_type} {trans['shares']}股 @ ${trans['price']}")
    
    result = calculator.calculate_multiple_transactions(transactions)
    print_transaction_summary(result)


def example_6_real_scenario():
    """示例6: 真实场景 - 分批买入卖出"""
    print("\n" + "="*60)
    print("示例6: 真实场景 - 分批建仓和减仓")
    print("Example 6: Real Scenario - Gradual Position Building")
    print("="*60)
    
    calculator = IBStockCalculator()
    
    # 模拟真实的交易场景
    transactions = [
        # 第一批建仓
        {'type': 'buy', 'shares': 50, 'price': 100.00},
        # 加仓
        {'type': 'buy', 'shares': 30, 'price': 98.00},
        # 继续加仓
        {'type': 'buy', 'shares': 20, 'price': 95.00},
        # 部分获利了结
        {'type': 'sell', 'shares': 40, 'price': 105.00},
        # 继续减仓
        {'type': 'sell', 'shares': 30, 'price': 108.00},
    ]
    
    print("\n📈 交易历史:")
    for i, trans in enumerate(transactions, 1):
        trans_type = "🟢 买入" if trans['type'] == 'buy' else "🔴 卖出"
        print(f"{i}. {trans_type} {trans['shares']}股 @ ${trans['price']}")
    
    result = calculator.calculate_multiple_transactions(transactions)
    
    print("\n" + "="*60)
    print("最终结果 / Final Results")
    print("="*60)
    print(f"\n💼 剩余持仓: {result['remaining_shares']}股")
    print(f"💰 总投入成本: ${result['total_cost']}")
    print(f"💵 已获利收入: ${result['total_proceeds']}")
    print(f"📊 平均成本/股: ${result['avg_cost_per_share']}")
    print(f"🎯 已实现盈利: ${result['total_profit']}")
    print(f"📈 盈利率: {result['profit_percentage']}%")
    print(f"💸 总佣金支出: ${result['total_commission']}")


def example_7_commission_comparison():
    """示例7: 不同交易规模的佣金对比"""
    print("\n" + "="*60)
    print("示例7: 佣金对比 / Example 7: Commission Comparison")
    print("="*60)
    
    calculator = IBStockCalculator()
    
    test_cases = [
        (10, 10.00),    # 小额交易
        (100, 10.00),   # 中等交易
        (500, 10.00),   # 较大交易
        (10000, 10.00), # 大额交易（触发1%上限）
    ]
    
    print("\n不同规模交易的佣金对比:")
    print(f"{'股数':<10} {'价格':<10} {'交易额':<12} {'佣金':<10} {'佣金率':<10}")
    print("-" * 60)
    
    for shares, price in test_cases:
        trade_value = shares * price
        commission = calculator.calculate_commission(shares, price)
        commission_rate = (float(commission) / trade_value * 100)
        
        print(f"{shares:<10} ${price:<9.2f} ${trade_value:<11.2f} "
              f"${float(commission):<9.2f} {commission_rate:<9.4f}%")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("盈透证券股票计算器 - 使用示例")
    print("IB Stock Calculator - Usage Examples")
    print("="*60)
    
    # 运行所有示例
    example_1_simple_buy()
    example_2_simple_sell()
    example_3_profit_calculation()
    example_4_partial_sell()
    example_5_multiple_transactions()
    example_6_real_scenario()
    example_7_commission_comparison()
    
    print("\n" + "="*60)
    print("所有示例运行完毕！")
    print("All examples completed!")
    print("="*60 + "\n")
