#!/usr/bin/env python3
"""
概率游戏使用示例 | Probability Games Usage Examples

展示如何使用各个概率游戏类。
Demonstrates how to use each probability game class.
"""

from probability_games import (
    MontyHallGame, 
    NumberGuessingGame, 
    ProbabilityRaceGame, 
    SlotMachineSimulator
)


def example_monty_hall():
    """三门问题示例 | Monty Hall Example"""
    print("=" * 60)
    print("示例1: 三门问题 | Example 1: Monty Hall Problem")
    print("=" * 60)
    
    game = MontyHallGame()
    
    # 开始新游戏
    info = game.new_game()
    print(f"\n{info['message']}")
    
    # 玩家选择门1
    choice_result = game.make_choice(1)
    print(f"\n{choice_result['message']}")
    
    # 决定换门
    final_result = game.final_decision(switch=True)
    print(f"\n{final_result['message']}")
    print(f"最终选择: 门{final_result['final_choice']}")
    print(f"结果: {'🎉 赢了!' if final_result['won'] else '😢 输了'}")


def example_number_guessing():
    """猜数字游戏示例 | Number Guessing Example"""
    print("\n\n" + "=" * 60)
    print("示例2: 猜数字游戏 | Example 2: Number Guessing Game")
    print("=" * 60)
    
    game = NumberGuessingGame(1, 100)
    
    # 开始新游戏（中等难度）
    info = game.new_game('medium')
    print(f"\n{info['message']}")
    
    # 模拟几次猜测
    guesses = [50, 75, 62]
    for guess in guesses:
        result = game.make_guess(guess)
        print(f"\n猜测 {guess}: {result['message']}")
        if result.get('game_over'):
            break


def example_probability_race():
    """概率赛道游戏示例 | Probability Race Example"""
    print("\n\n" + "=" * 60)
    print("示例3: 概率赛道游戏 | Example 3: Probability Race Game")
    print("=" * 60)
    
    game = ProbabilityRaceGame()
    
    # 开始新游戏
    info = game.new_game(10)
    print(f"\n{info['message']}")
    
    # 游戏循环
    step = 0
    while step < 5:  # 限制步数以便演示
        paths_info = game.get_paths()
        if paths_info['game_over']:
            print(f"\n{paths_info['message']}")
            break
        
        print(f"\n--- 步骤 {step + 1} ---")
        print(f"当前位置: {paths_info['current_position']}/{paths_info['target_position']}")
        
        # 选择期望值最高的路径
        best_path = max(paths_info['paths'], key=lambda p: p['expected_value'])
        print(f"可选路径:")
        for path in paths_info['paths']:
            marker = "👉" if path['id'] == best_path['id'] else "  "
            print(f"{marker} {path['name']}: 期望值={path['expected_value']:.2f}")
        
        # 执行选择
        result = game.choose_path(best_path['id'], paths_info['paths'])
        print(f"选择了: {best_path['name']}")
        print(f"结果: {result['message']}")
        
        step += 1


def example_slot_machine():
    """老虎机模拟器示例 | Slot Machine Simulator Example"""
    print("\n\n" + "=" * 60)
    print("示例4: 老虎机模拟器 | Example 4: Slot Machine Simulator")
    print("=" * 60)
    
    simulator = SlotMachineSimulator()
    
    # 显示符号概率
    probs = simulator.get_symbol_probabilities()
    print(f"\n{probs['description']}:")
    for symbol, prob in zip(probs['symbols'], probs['probabilities']):
        print(f"  {symbol}: {prob*100:.0f}%")
    
    # 转动20次
    print(f"\n转动20次...")
    for i in range(20):
        result = simulator.spin()
        if result['win_type'] != 'no_win':
            print(f"第{i+1}次: {' '.join(result['result'])} - {result['message']}")
    
    # 显示统计
    stats = simulator.get_statistics()
    print(f"\n统计结果:")
    print(f"总转动次数: {stats['total_spins']}")
    print(f"\n符号频率 (实际 vs 期望):")
    for symbol in simulator.symbols:
        actual = stats['symbol_frequencies'][symbol]
        expected = stats['expected_probabilities'][symbol]
        diff = abs(actual - expected)
        print(f"  {symbol}: {actual*100:.1f}% vs {expected*100:.0f}% (差异: {diff*100:.1f}%)")


def example_interactive_monty_hall():
    """交互式三门问题 | Interactive Monty Hall"""
    print("\n\n" + "=" * 60)
    print("交互式示例: 三门问题 | Interactive Example: Monty Hall")
    print("=" * 60)
    print("\n让我们来玩一局三门问题！")
    
    game = MontyHallGame()
    info = game.new_game()
    print(f"\n{info['message']}")
    print("门: 1, 2, 3")
    
    try:
        # 玩家选择
        choice = int(input("\n请输入你的选择 (1-3): "))
        if choice not in [1, 2, 3]:
            print("无效选择，使用门1")
            choice = 1
    except:
        print("无效输入，使用门1")
        choice = 1
    
    choice_result = game.make_choice(choice)
    print(f"\n{choice_result['message']}")
    print(f"剩余的门: {choice_result['remaining_doors']}")
    
    try:
        # 决定是否换门
        switch_input = input("\n你要换门吗? (y/n): ").lower()
        switch = switch_input in ['y', 'yes', '是', 'Y']
    except:
        switch = True
        print("默认换门")
    
    final_result = game.final_decision(switch)
    print(f"\n{'='*60}")
    print(final_result['message'])
    print(f"{'='*60}")


if __name__ == '__main__':
    print("\n🎲 概率游戏使用示例")
    print("Probability Games Usage Examples\n")
    
    # 运行所有示例
    example_monty_hall()
    example_number_guessing()
    example_probability_race()
    example_slot_machine()
    
    # 交互式示例（可选）
    print("\n\n" + "=" * 60)
    try:
        play = input("\n想要玩一局交互式三门问题吗? (y/n): ").lower()
        if play in ['y', 'yes', '是', 'Y']:
            example_interactive_monty_hall()
    except:
        print("跳过交互式示例")
    
    print("\n\n✅ 所有示例完成！")
    print("✅ All examples completed!")
    print("\n提示: 打开 probability_puzzles.html 体验完整的网页版游戏！")
    print("Tip: Open probability_puzzles.html to experience the full web version!")
