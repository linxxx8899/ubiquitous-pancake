#!/usr/bin/env python3
"""
概率游戏测试脚本 | Probability Games Test Script

快速测试所有游戏的基本功能。
Quick test of all game basic functions.
"""

from probability_games import (
    MontyHallGame,
    NumberGuessingGame,
    ProbabilityRaceGame,
    SlotMachineSimulator
)


def test_monty_hall():
    """测试三门问题 | Test Monty Hall Problem"""
    print("Testing MontyHallGame...")
    game = MontyHallGame()
    
    # 测试新游戏
    result = game.new_game()
    assert 'message' in result
    assert 'doors' in result
    
    # 测试选择门
    result = game.make_choice(1)
    assert 'player_choice' in result
    assert 'opened_door' in result
    
    # 测试最终决定
    result = game.final_decision(True)
    assert 'won' in result
    assert 'car_door' in result
    
    print("✓ MontyHallGame passed all tests")


def test_number_guessing():
    """测试猜数字游戏 | Test Number Guessing Game"""
    print("Testing NumberGuessingGame...")
    game = NumberGuessingGame(1, 100)
    
    # 测试新游戏
    result = game.new_game('medium')
    assert 'max_attempts' in result
    assert result['max_attempts'] > 0
    
    # 测试猜测
    result = game.make_guess(50)
    assert 'result' in result
    assert result['result'] in ['correct', 'too_high', 'too_low']
    
    print("✓ NumberGuessingGame passed all tests")


def test_probability_race():
    """测试概率赛道游戏 | Test Probability Race Game"""
    print("Testing ProbabilityRaceGame...")
    game = ProbabilityRaceGame()
    
    # 测试新游戏
    result = game.new_game(10)
    assert 'current_position' in result
    assert result['current_position'] == 0
    
    # 测试获取路径
    result = game.get_paths()
    assert 'paths' in result
    assert len(result['paths']) > 0
    
    # 测试选择路径
    paths = result['paths']
    result = game.choose_path(paths[0]['id'], paths)
    assert 'current_position' in result
    
    print("✓ ProbabilityRaceGame passed all tests")


def test_slot_machine():
    """测试老虎机模拟器 | Test Slot Machine Simulator"""
    print("Testing SlotMachineSimulator...")
    simulator = SlotMachineSimulator()
    
    # 测试获取符号概率
    result = simulator.get_symbol_probabilities()
    assert 'symbols' in result
    assert 'probabilities' in result
    assert len(result['symbols']) == len(result['probabilities'])
    
    # 测试转动
    result = simulator.spin()
    assert 'result' in result
    assert 'win_type' in result
    assert len(result['result']) == 3
    
    # 测试统计
    result = simulator.get_statistics()
    assert 'total_spins' in result
    assert result['total_spins'] > 0
    
    print("✓ SlotMachineSimulator passed all tests")


def test_all_games():
    """运行所有测试 | Run all tests"""
    print("=" * 60)
    print("概率游戏测试 | Probability Games Tests")
    print("=" * 60)
    print()
    
    try:
        test_monty_hall()
        test_number_guessing()
        test_probability_race()
        test_slot_machine()
        
        print()
        print("=" * 60)
        print("✅ 所有测试通过！All tests passed!")
        print("=" * 60)
        return True
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ 测试失败！Test failed: {e}")
        print("=" * 60)
        return False


if __name__ == '__main__':
    success = test_all_games()
    exit(0 if success else 1)
