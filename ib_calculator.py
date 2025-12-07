#!/usr/bin/env python3
"""
Interactive Brokers Stock Cost and Profit Calculator
盈透证券股票成本与盈利计算器
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import List, Dict, Tuple


class IBStockCalculator:
    """Interactive Brokers股票成本和盈利计算器"""
    
    def __init__(self, commission_rate: float = 0.0035, min_commission: float = 0.35, 
                 max_commission_rate: float = 0.01):
        """
        初始化计算器
        
        Args:
            commission_rate: 佣金费率 (默认0.0035，即每股$0.0035)
            min_commission: 最低佣金 (默认$0.35)
            max_commission_rate: 最高佣金费率 (默认1%，即交易额的0.01)
        """
        self.commission_rate = Decimal(str(commission_rate))
        self.min_commission = Decimal(str(min_commission))
        self.max_commission_rate = Decimal(str(max_commission_rate))
    
    def calculate_commission(self, shares: int, price: float) -> Decimal:
        """
        计算IB佣金
        
        Args:
            shares: 股票数量
            price: 股票价格
            
        Returns:
            佣金金额
        """
        shares_dec = Decimal(str(shares))
        price_dec = Decimal(str(price))
        trade_value = shares_dec * price_dec
        
        # 计算基础佣金 (每股费率)
        commission = shares_dec * self.commission_rate
        
        # 应用最低佣金
        if commission < self.min_commission:
            commission = self.min_commission
        
        # 应用最高佣金限制 (交易额的1%)
        max_commission = trade_value * self.max_commission_rate
        if commission > max_commission:
            commission = max_commission
        
        return commission.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    def calculate_buy_cost(self, shares: int, price: float) -> Dict[str, Decimal]:
        """
        计算买入总成本
        
        Args:
            shares: 买入股数
            price: 买入价格
            
        Returns:
            包含详细成本信息的字典
        """
        shares_dec = Decimal(str(shares))
        price_dec = Decimal(str(price))
        
        stock_cost = shares_dec * price_dec
        commission = self.calculate_commission(shares, price)
        total_cost = stock_cost + commission
        avg_cost_per_share = (total_cost / shares_dec).quantize(
            Decimal('0.0001'), rounding=ROUND_HALF_UP
        )
        
        return {
            'shares': shares_dec,
            'price': price_dec,
            'stock_cost': stock_cost.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'commission': commission,
            'total_cost': total_cost.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'avg_cost_per_share': avg_cost_per_share
        }
    
    def calculate_sell_proceeds(self, shares: int, price: float) -> Dict[str, Decimal]:
        """
        计算卖出净收入
        
        Args:
            shares: 卖出股数
            price: 卖出价格
            
        Returns:
            包含详细收入信息的字典
        """
        shares_dec = Decimal(str(shares))
        price_dec = Decimal(str(price))
        
        gross_proceeds = shares_dec * price_dec
        commission = self.calculate_commission(shares, price)
        net_proceeds = gross_proceeds - commission
        avg_proceeds_per_share = (net_proceeds / shares_dec).quantize(
            Decimal('0.0001'), rounding=ROUND_HALF_UP
        )
        
        return {
            'shares': shares_dec,
            'price': price_dec,
            'gross_proceeds': gross_proceeds.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'commission': commission,
            'net_proceeds': net_proceeds.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'avg_proceeds_per_share': avg_proceeds_per_share
        }
    
    def calculate_profit(self, buy_shares: int, buy_price: float, 
                        sell_shares: int, sell_price: float) -> Dict[str, any]:
        """
        计算交易盈利
        
        Args:
            buy_shares: 买入股数
            buy_price: 买入价格
            sell_shares: 卖出股数
            sell_price: 卖出价格
            
        Returns:
            包含详细盈利信息的字典
        """
        if sell_shares > buy_shares:
            raise ValueError("卖出股数不能大于买入股数")
        
        buy_info = self.calculate_buy_cost(buy_shares, buy_price)
        sell_info = self.calculate_sell_proceeds(sell_shares, sell_price)
        
        # 计算这部分股票的成本
        cost_for_sold_shares = (buy_info['avg_cost_per_share'] * 
                               Decimal(str(sell_shares)))
        
        # 计算盈利
        profit = sell_info['net_proceeds'] - cost_for_sold_shares
        profit_percentage = ((profit / cost_for_sold_shares) * Decimal('100')).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
        
        # 计算剩余持仓
        remaining_shares = buy_shares - sell_shares
        remaining_cost = buy_info['total_cost'] - cost_for_sold_shares
        
        return {
            'buy_info': buy_info,
            'sell_info': sell_info,
            'cost_for_sold_shares': cost_for_sold_shares.quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            ),
            'profit': profit.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'profit_percentage': profit_percentage,
            'remaining_shares': remaining_shares,
            'remaining_cost': remaining_cost.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'remaining_avg_cost': buy_info['avg_cost_per_share'] if remaining_shares > 0 else Decimal('0')
        }
    
    def calculate_multiple_transactions(self, transactions: List[Dict]) -> Dict:
        """
        计算多笔交易的总成本和盈利
        
        Args:
            transactions: 交易列表，每个交易是一个字典，包含:
                - type: 'buy' 或 'sell'
                - shares: 股数
                - price: 价格
                
        Returns:
            包含总体信息的字典
        """
        total_shares = 0
        total_cost = Decimal('0')
        total_proceeds = Decimal('0')
        total_buy_commission = Decimal('0')
        total_sell_commission = Decimal('0')
        
        for trans in transactions:
            trans_type = trans['type']
            shares = trans['shares']
            price = trans['price']
            
            if trans_type == 'buy':
                buy_info = self.calculate_buy_cost(shares, price)
                total_shares += shares
                total_cost += buy_info['total_cost']
                total_buy_commission += buy_info['commission']
            elif trans_type == 'sell':
                if shares > total_shares:
                    raise ValueError(f"卖出股数 {shares} 超过持有股数 {total_shares}")
                sell_info = self.calculate_sell_proceeds(shares, price)
                total_shares -= shares
                total_proceeds += sell_info['net_proceeds']
                total_sell_commission += sell_info['commission']
        
        avg_cost_per_share = (total_cost / Decimal(str(sum(
            t['shares'] for t in transactions if t['type'] == 'buy'
        )))).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP) if any(
            t['type'] == 'buy' for t in transactions
        ) else Decimal('0')
        
        total_profit = total_proceeds - (avg_cost_per_share * Decimal(str(sum(
            t['shares'] for t in transactions if t['type'] == 'sell'
        ))))
        
        return {
            'remaining_shares': total_shares,
            'total_cost': total_cost.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'total_proceeds': total_proceeds.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'total_buy_commission': total_buy_commission.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'total_sell_commission': total_sell_commission.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'total_commission': (total_buy_commission + total_sell_commission).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            ),
            'avg_cost_per_share': avg_cost_per_share,
            'total_profit': total_profit.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            'profit_percentage': ((total_profit / (avg_cost_per_share * Decimal(str(sum(
                t['shares'] for t in transactions if t['type'] == 'sell'
            ))))) * Decimal('100')).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            ) if total_proceeds > 0 else Decimal('0')
        }


def print_transaction_summary(result: Dict):
    """打印交易摘要"""
    print("\n" + "="*60)
    print("交易摘要 / Transaction Summary")
    print("="*60)
    
    if 'buy_info' in result:
        print("\n【买入信息 / Buy Information】")
        buy = result['buy_info']
        print(f"  股数 Shares: {buy['shares']}")
        print(f"  价格 Price: ${buy['price']}")
        print(f"  股票成本 Stock Cost: ${buy['stock_cost']}")
        print(f"  佣金 Commission: ${buy['commission']}")
        print(f"  总成本 Total Cost: ${buy['total_cost']}")
        print(f"  平均成本/股 Avg Cost/Share: ${buy['avg_cost_per_share']}")
        
        print("\n【卖出信息 / Sell Information】")
        sell = result['sell_info']
        print(f"  股数 Shares: {sell['shares']}")
        print(f"  价格 Price: ${sell['price']}")
        print(f"  总收入 Gross Proceeds: ${sell['gross_proceeds']}")
        print(f"  佣金 Commission: ${sell['commission']}")
        print(f"  净收入 Net Proceeds: ${sell['net_proceeds']}")
        
        print("\n【盈利信息 / Profit Information】")
        print(f"  卖出股票成本 Cost for Sold Shares: ${result['cost_for_sold_shares']}")
        print(f"  盈利 Profit: ${result['profit']}")
        print(f"  盈利率 Profit %: {result['profit_percentage']}%")
        
        if result['remaining_shares'] > 0:
            print("\n【剩余持仓 / Remaining Position】")
            print(f"  剩余股数 Remaining Shares: {result['remaining_shares']}")
            print(f"  剩余成本 Remaining Cost: ${result['remaining_cost']}")
            print(f"  平均成本/股 Avg Cost/Share: ${result['remaining_avg_cost']}")
    else:
        print(f"\n剩余股数 Remaining Shares: {result['remaining_shares']}")
        print(f"总成本 Total Cost: ${result['total_cost']}")
        print(f"总收入 Total Proceeds: ${result['total_proceeds']}")
        print(f"买入佣金 Buy Commission: ${result['total_buy_commission']}")
        print(f"卖出佣金 Sell Commission: ${result['total_sell_commission']}")
        print(f"总佣金 Total Commission: ${result['total_commission']}")
        print(f"平均成本/股 Avg Cost/Share: ${result['avg_cost_per_share']}")
        print(f"总盈利 Total Profit: ${result['total_profit']}")
        print(f"盈利率 Profit %: {result['profit_percentage']}%")
    
    print("="*60 + "\n")


def main():
    """主程序 - 演示示例"""
    print("盈透证券股票成本与盈利计算器")
    print("Interactive Brokers Stock Cost and Profit Calculator\n")
    
    calculator = IBStockCalculator()
    
    # 示例 1: 简单的买入卖出
    print("\n示例 1: 买入100股@$150，卖出100股@$160")
    result1 = calculator.calculate_profit(
        buy_shares=100,
        buy_price=150.00,
        sell_shares=100,
        sell_price=160.00
    )
    print_transaction_summary(result1)
    
    # 示例 2: 部分卖出
    print("\n示例 2: 买入200股@$50，卖出100股@$55")
    result2 = calculator.calculate_profit(
        buy_shares=200,
        buy_price=50.00,
        sell_shares=100,
        sell_price=55.00
    )
    print_transaction_summary(result2)
    
    # 示例 3: 多笔交易
    print("\n示例 3: 多笔交易")
    transactions = [
        {'type': 'buy', 'shares': 100, 'price': 50.00},
        {'type': 'buy', 'shares': 50, 'price': 52.00},
        {'type': 'sell', 'shares': 80, 'price': 55.00},
        {'type': 'sell', 'shares': 30, 'price': 57.00},
    ]
    result3 = calculator.calculate_multiple_transactions(transactions)
    print_transaction_summary(result3)


if __name__ == "__main__":
    main()
