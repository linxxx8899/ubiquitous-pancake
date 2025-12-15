#!/usr/bin/env python3
"""
儿童概率解谜游戏 | Probability Puzzles for Kids

提供多种概率相关的互动游戏，帮助儿童理解概率概念。
Provides various interactive probability games to help children understand probability concepts.
"""

import random
from typing import Dict, List, Tuple, Optional


class MontyHallGame:
    """
    三门问题游戏 | Monty Hall Problem Game
    
    经典的概率悖论游戏，展示条件概率的反直觉特性。
    A classic probability paradox that demonstrates counter-intuitive properties of conditional probability.
    """
    
    def __init__(self):
        self.doors = [1, 2, 3]
        self.car_door = None
        self.player_choice = None
        self.opened_door = None
        
    def new_game(self) -> Dict:
        """开始新游戏 | Start a new game"""
        self.car_door = random.choice(self.doors)
        self.player_choice = None
        self.opened_door = None
        return {
            'message': '三扇门中有一扇门后有汽车，另外两扇门后是山羊。请选择一扇门！',
            'message_en': 'Behind one of three doors is a car, behind the other two are goats. Choose a door!',
            'doors': self.doors
        }
    
    def make_choice(self, choice: int) -> Dict:
        """玩家做出初始选择 | Player makes initial choice"""
        if choice not in self.doors:
            raise ValueError("选择必须是1, 2, 或3 | Choice must be 1, 2, or 3")
        
        self.player_choice = choice
        
        # 主持人打开一扇有山羊的门 | Host opens a door with a goat
        available_doors = [d for d in self.doors if d != self.car_door and d != self.player_choice]
        self.opened_door = random.choice(available_doors)
        
        remaining_doors = [d for d in self.doors if d != self.opened_door]
        
        return {
            'player_choice': self.player_choice,
            'opened_door': self.opened_door,
            'remaining_doors': remaining_doors,
            'message': f'主持人打开了门{self.opened_door}，里面是山羊！你要换门吗？',
            'message_en': f'The host opened door {self.opened_door}, revealing a goat! Do you want to switch?'
        }
    
    def final_decision(self, switch: bool) -> Dict:
        """最终决定是否换门 | Final decision to switch or not"""
        if self.player_choice is None or self.opened_door is None:
            raise ValueError("游戏尚未开始 | Game not started")
        
        if switch:
            final_choice = [d for d in self.doors if d != self.player_choice and d != self.opened_door][0]
        else:
            final_choice = self.player_choice
        
        won = final_choice == self.car_door
        
        return {
            'switched': switch,
            'final_choice': final_choice,
            'car_door': self.car_door,
            'won': won,
            'message': f'汽车在门{self.car_door}！你{"赢了" if won else "输了"}！',
            'message_en': f'The car was behind door {self.car_door}! You {"won" if won else "lost"}!'
        }


class NumberGuessingGame:
    """
    猜数字游戏 | Number Guessing Game
    
    通过反馈缩小范围，理解信息熵和概率推断。
    Understand information entropy and probability inference by narrowing down the range.
    """
    
    def __init__(self, min_num: int = 1, max_num: int = 100):
        self.min_num = min_num
        self.max_num = max_num
        self.target = None
        self.guesses = []
        self.max_attempts = None
        
    def new_game(self, difficulty: str = 'medium') -> Dict:
        """开始新游戏 | Start a new game"""
        self.target = random.randint(self.min_num, self.max_num)
        self.guesses = []
        
        # 根据难度设置尝试次数 | Set max attempts based on difficulty
        difficulty_settings = {
            'easy': int((self.max_num - self.min_num).bit_length() + 5),
            'medium': int((self.max_num - self.min_num).bit_length() + 2),
            'hard': int((self.max_num - self.min_num).bit_length())
        }
        self.max_attempts = difficulty_settings.get(difficulty, difficulty_settings['medium'])
        
        return {
            'min_num': self.min_num,
            'max_num': self.max_num,
            'max_attempts': self.max_attempts,
            'message': f'我想了一个{self.min_num}到{self.max_num}之间的数字，你有{self.max_attempts}次机会猜！',
            'message_en': f'I\'m thinking of a number between {self.min_num} and {self.max_num}. You have {self.max_attempts} attempts!'
        }
    
    def make_guess(self, guess: int) -> Dict:
        """做出一次猜测 | Make a guess"""
        if guess < self.min_num or guess > self.max_num:
            raise ValueError(f"猜测必须在{self.min_num}到{self.max_num}之间 | Guess must be between {self.min_num} and {self.max_num}")
        
        self.guesses.append(guess)
        attempts_left = self.max_attempts - len(self.guesses)
        
        if guess == self.target:
            return {
                'guess': guess,
                'result': 'correct',
                'attempts_used': len(self.guesses),
                'message': f'恭喜！你用{len(self.guesses)}次就猜对了！',
                'message_en': f'Congratulations! You guessed it in {len(self.guesses)} attempts!',
                'game_over': True,
                'won': True
            }
        elif attempts_left == 0:
            return {
                'guess': guess,
                'result': 'too_high' if guess > self.target else 'too_low',
                'target': self.target,
                'attempts_used': len(self.guesses),
                'message': f'很遗憾，次数用完了！答案是{self.target}。',
                'message_en': f'Sorry, you\'re out of attempts! The answer was {self.target}.',
                'game_over': True,
                'won': False
            }
        else:
            result = 'too_high' if guess > self.target else 'too_low'
            hint = '太大了' if result == 'too_high' else '太小了'
            hint_en = 'Too high' if result == 'too_high' else 'Too low'
            
            return {
                'guess': guess,
                'result': result,
                'attempts_left': attempts_left,
                'message': f'{hint}！还有{attempts_left}次机会。',
                'message_en': f'{hint_en}! {attempts_left} attempts left.',
                'game_over': False
            }


class ProbabilityRaceGame:
    """
    概率赛道游戏 | Probability Race Game
    
    通过计算期望值选择最优路径。
    Choose optimal paths by calculating expected values.
    """
    
    def __init__(self):
        self.current_position = 0
        self.target_position = 10
        self.path_history = []
        
    def new_game(self, target: int = 10) -> Dict:
        """开始新游戏 | Start a new game"""
        self.current_position = 0
        self.target_position = target
        self.path_history = []
        
        return {
            'current_position': self.current_position,
            'target_position': self.target_position,
            'message': f'从起点到达{self.target_position}点即可获胜！每个路口都要做出选择。',
            'message_en': f'Reach position {self.target_position} to win! Make choices at each junction.'
        }
    
    def get_paths(self) -> Dict:
        """获取当前可选路径 | Get available paths"""
        if self.current_position >= self.target_position:
            return {
                'game_over': True,
                'message': '恭喜到达终点！',
                'message_en': 'Congratulations, you reached the finish!'
            }
        
        # 生成随机路径选项 | Generate random path options
        paths = []
        
        # 安全路径：小步前进，100%成功 | Safe path: small step, 100% success
        safe_distance = random.randint(1, 2)
        paths.append({
            'id': 'safe',
            'name': '安全路径 | Safe Path',
            'distance': safe_distance,
            'success_rate': 1.0,
            'expected_value': safe_distance,
            'description': f'稳步前进{safe_distance}步 (100%成功)',
            'description_en': f'Steadily advance {safe_distance} steps (100% success)'
        })
        
        # 冒险路径：大步前进，有风险 | Risky path: big step, has risk
        risky_distance = random.randint(3, 5)
        risky_success_rate = round(random.uniform(0.5, 0.7), 2)
        paths.append({
            'id': 'risky',
            'name': '冒险路径 | Risky Path',
            'distance': risky_distance,
            'success_rate': risky_success_rate,
            'expected_value': round(risky_distance * risky_success_rate, 2),
            'description': f'前进{risky_distance}步 ({int(risky_success_rate*100)}%成功，失败则后退1步)',
            'description_en': f'Advance {risky_distance} steps ({int(risky_success_rate*100)}% success, -1 step if fail)'
        })
        
        # 平衡路径：中等距离，中等风险 | Balanced path: medium distance, medium risk
        balanced_distance = random.randint(2, 3)
        balanced_success_rate = round(random.uniform(0.75, 0.9), 2)
        paths.append({
            'id': 'balanced',
            'name': '平衡路径 | Balanced Path',
            'distance': balanced_distance,
            'success_rate': balanced_success_rate,
            'expected_value': round(balanced_distance * balanced_success_rate, 2),
            'description': f'前进{balanced_distance}步 ({int(balanced_success_rate*100)}%成功)',
            'description_en': f'Advance {balanced_distance} steps ({int(balanced_success_rate*100)}% success)'
        })
        
        return {
            'current_position': self.current_position,
            'target_position': self.target_position,
            'paths': paths,
            'game_over': False
        }
    
    def choose_path(self, path_id: str, paths: List[Dict]) -> Dict:
        """选择一条路径 | Choose a path"""
        selected_path = next((p for p in paths if p['id'] == path_id), None)
        if not selected_path:
            raise ValueError("无效的路径选择 | Invalid path choice")
        
        # 根据成功率判断是否成功 | Determine success based on success rate
        success = random.random() < selected_path['success_rate']
        
        old_position = self.current_position
        if success:
            self.current_position += selected_path['distance']
            message = f'成功前进{selected_path["distance"]}步！'
            message_en = f'Successfully advanced {selected_path["distance"]} steps!'
        else:
            penalty = -1 if path_id == 'risky' else 0
            self.current_position = max(0, self.current_position + penalty)
            message = f'失败了！{" 后退1步" if penalty else ""}'
            message_en = f'Failed!{" Moved back 1 step" if penalty else ""}'
        
        self.path_history.append({
            'path': path_id,
            'success': success,
            'old_position': old_position,
            'new_position': self.current_position
        })
        
        game_over = self.current_position >= self.target_position
        
        return {
            'path_chosen': path_id,
            'success': success,
            'old_position': old_position,
            'current_position': self.current_position,
            'message': message,
            'message_en': message_en,
            'game_over': game_over
        }


class SlotMachineSimulator:
    """
    老虎机模拟器 | Slot Machine Simulator
    
    展示独立事件和大数定律，纯数学教育目的。
    Demonstrates independent events and law of large numbers, for educational purposes only.
    """
    
    def __init__(self):
        self.symbols = ['🍎', '🍌', '⭐', '🍒', '🔔']
        self.probabilities = [0.35, 0.25, 0.20, 0.15, 0.05]
        self.reels = 3
        self.spin_history = []
        
    def get_symbol_probabilities(self) -> Dict:
        """获取符号概率 | Get symbol probabilities"""
        return {
            'symbols': self.symbols,
            'probabilities': self.probabilities,
            'description': '每个符号出现的概率',
            'description_en': 'Probability of each symbol appearing'
        }
    
    def spin(self) -> Dict:
        """转动老虎机 | Spin the slot machine"""
        result = []
        for _ in range(self.reels):
            symbol = random.choices(self.symbols, weights=self.probabilities, k=1)[0]
            result.append(symbol)
        
        # 判断是否中奖 | Check if won
        all_same = len(set(result)) == 1
        two_same = len(set(result)) == 2
        
        if all_same:
            win_type = 'jackpot'
            message = f'大奖！三个{result[0]}！'
            message_en = f'Jackpot! Three {result[0]}!'
        elif two_same:
            win_type = 'small_win'
            message = '小奖！两个相同！'
            message_en = 'Small win! Two matching!'
        else:
            win_type = 'no_win'
            message = '未中奖，再试一次！'
            message_en = 'No win, try again!'
        
        self.spin_history.append({
            'result': result,
            'win_type': win_type
        })
        
        return {
            'result': result,
            'win_type': win_type,
            'message': message,
            'message_en': message_en,
            'total_spins': len(self.spin_history)
        }
    
    def get_statistics(self) -> Dict:
        """获取统计数据 | Get statistics"""
        if not self.spin_history:
            return {
                'total_spins': 0,
                'message': '还没有转动记录',
                'message_en': 'No spins yet'
            }
        
        # 统计每个符号出现的次数 | Count symbol occurrences
        symbol_counts = {symbol: 0 for symbol in self.symbols}
        total_symbols = 0
        
        for spin in self.spin_history:
            for symbol in spin['result']:
                symbol_counts[symbol] += 1
                total_symbols += 1
        
        # 计算实际频率 | Calculate actual frequencies
        symbol_frequencies = {
            symbol: round(count / total_symbols, 3) if total_symbols > 0 else 0
            for symbol, count in symbol_counts.items()
        }
        
        # 统计中奖类型 | Count win types
        win_types = {'jackpot': 0, 'small_win': 0, 'no_win': 0}
        for spin in self.spin_history:
            win_types[spin['win_type']] += 1
        
        return {
            'total_spins': len(self.spin_history),
            'total_symbols': total_symbols,
            'symbol_counts': symbol_counts,
            'symbol_frequencies': symbol_frequencies,
            'expected_probabilities': dict(zip(self.symbols, self.probabilities)),
            'win_types': win_types,
            'message': f'已转动{len(self.spin_history)}次',
            'message_en': f'{len(self.spin_history)} spins completed'
        }


def demo_monty_hall():
    """演示三门问题 | Demonstrate Monty Hall Problem"""
    print("=" * 60)
    print("三门问题演示 | Monty Hall Problem Demo")
    print("=" * 60)
    
    game = MontyHallGame()
    
    # 模拟1000次游戏，统计换门和不换门的胜率
    switch_wins = 0
    stay_wins = 0
    trials = 1000
    
    for _ in range(trials):
        game.new_game()
        game.make_choice(1)  # 总是选择门1
        
        # 换门策略
        result = game.final_decision(switch=True)
        if result['won']:
            switch_wins += 1
        
        # 不换门策略
        game.new_game()
        game.make_choice(1)
        result = game.final_decision(switch=False)
        if result['won']:
            stay_wins += 1
    
    print(f"\n模拟{trials}次游戏的结果 | Results from {trials} simulations:")
    print(f"换门策略胜率 | Switch strategy win rate: {switch_wins/trials*100:.1f}%")
    print(f"不换策略胜率 | Stay strategy win rate: {stay_wins/trials*100:.1f}%")
    print(f"\n结论：换门策略的胜率约为2/3！")
    print(f"Conclusion: Switching has approximately 2/3 win rate!\n")


def demo_number_guessing():
    """演示猜数字游戏 | Demonstrate Number Guessing Game"""
    print("=" * 60)
    print("猜数字游戏演示 | Number Guessing Game Demo")
    print("=" * 60)
    
    game = NumberGuessingGame(1, 100)
    info = game.new_game('medium')
    print(f"\n{info['message']}")
    print(f"{info['message_en']}\n")
    
    # 使用二分查找策略 | Use binary search strategy
    low, high = 1, 100
    while True:
        guess = (low + high) // 2
        result = game.make_guess(guess)
        print(f"猜测 | Guess: {guess} - {result['message']}")
        
        if result['game_over']:
            break
        
        if result['result'] == 'too_high':
            high = guess - 1
        else:
            low = guess + 1


def demo_probability_race():
    """演示概率赛道游戏 | Demonstrate Probability Race Game"""
    print("=" * 60)
    print("概率赛道游戏演示 | Probability Race Game Demo")
    print("=" * 60)
    
    game = ProbabilityRaceGame()
    info = game.new_game(10)
    print(f"\n{info['message']}\n")
    
    while True:
        paths_info = game.get_paths()
        if paths_info['game_over']:
            print(f"\n{paths_info['message']}")
            break
        
        print(f"\n当前位置 | Current position: {paths_info['current_position']}/{paths_info['target_position']}")
        print("可选路径 | Available paths:")
        for path in paths_info['paths']:
            print(f"  {path['name']}: {path['description']}")
            print(f"    期望值 | Expected value: {path['expected_value']}")
        
        # 选择期望值最高的路径 | Choose path with highest expected value
        best_path = max(paths_info['paths'], key=lambda p: p['expected_value'])
        result = game.choose_path(best_path['id'], paths_info['paths'])
        print(f"\n选择了 | Chose: {best_path['name']}")
        print(f"{result['message']}")


def demo_slot_machine():
    """演示老虎机模拟器 | Demonstrate Slot Machine Simulator"""
    print("=" * 60)
    print("老虎机模拟器演示 | Slot Machine Simulator Demo")
    print("=" * 60)
    
    simulator = SlotMachineSimulator()
    probs = simulator.get_symbol_probabilities()
    
    print(f"\n符号概率 | Symbol probabilities:")
    for symbol, prob in zip(probs['symbols'], probs['probabilities']):
        print(f"  {symbol}: {prob*100:.0f}%")
    
    print(f"\n模拟100次转动 | Simulating 100 spins...")
    for _ in range(100):
        simulator.spin()
    
    stats = simulator.get_statistics()
    print(f"\n统计结果 | Statistics:")
    print(f"总转动次数 | Total spins: {stats['total_spins']}")
    print(f"\n实际频率 vs 期望概率 | Actual frequency vs Expected probability:")
    for symbol in simulator.symbols:
        actual = stats['symbol_frequencies'][symbol]
        expected = stats['expected_probabilities'][symbol]
        print(f"  {symbol}: {actual*100:.1f}% (期望 | expected: {expected*100:.0f}%)")
    
    print(f"\n中奖统计 | Win statistics:")
    print(f"  大奖 | Jackpot: {stats['win_types']['jackpot']}")
    print(f"  小奖 | Small win: {stats['win_types']['small_win']}")
    print(f"  未中奖 | No win: {stats['win_types']['no_win']}")


if __name__ == '__main__':
    print("\n儿童概率解谜游戏演示")
    print("Probability Puzzles for Kids Demo")
    print("\n")
    
    demo_monty_hall()
    print("\n")
    
    demo_number_guessing()
    print("\n")
    
    demo_probability_race()
    print("\n")
    
    demo_slot_machine()
