"""
数据结构与算法 - 阶段作业 01 自动化测试 Harness (Python 3.10+)

包含：
1. 随机数据生成器 (Random Data Generator)
2. 经典排序算法实现 (Bubble, Insertion, Merge, Quick, Quick-3Way)
3. 对拍校验引擎 (Stress Testing Engine)
4. 高精度性能 Benchmark 评估器 (Benchmark Evaluator)
"""

import sys
import time
import random

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class DataGenerator:
    @staticmethod
    def generate_random(n: int, min_val: int = -10000, max_val: int = 10000) -> list[int]:
        return [random.randint(min_val, max_val) for _ in range(n)]

    @staticmethod
    def generate_nearly_sorted(n: int, swap_count: int = 5) -> list[int]:
        arr = list(range(n))
        for _ in range(swap_count):
            i, j = random.randint(0, n - 1), random.randint(0, n - 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr

    @staticmethod
    def generate_reversed(n: int) -> list[int]:
        return list(range(n, 0, -1))

    @staticmethod
    def generate_many_duplicates(n: int, num_distinct: int = 5) -> list[int]:
        choices = [random.randint(1, 100) for _ in range(num_distinct)]
        return [random.choice(choices) for _ in range(n)]


class SortAlgorithms:
    @staticmethod
    def bubble_sort(arr: list[int]) -> list[int]:
        a = list(arr)
        n = len(a)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if a[j] > a[j + 1]:
                    a[j], a[j + 1] = a[j + 1], a[j]
                    swapped = True
            if not swapped:
                break
        return a

    @staticmethod
    def insertion_sort(arr: list[int]) -> list[int]:
        a = list(arr)
        for i in range(1, len(a)):
            key = a[i]
            j = i - 1
            while j >= 0 and a[j] > key:
                a[j + 1] = a[j]
                j -= 1
            a[j + 1] = key
        return a

    @staticmethod
    def merge_sort(arr: list[int]) -> list[int]:
        if len(arr) <= 1:
            return list(arr)
        mid = len(arr) // 2
        left = SortAlgorithms.merge_sort(arr[:mid])
        right = SortAlgorithms.merge_sort(arr[mid:])
        
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    @staticmethod
    def quick_sort_3way(arr: list[int]) -> list[int]:
        a = list(arr)
        def _quick_sort(low: int, high: int):
            if low >= high:
                return
            lt = low
            gt = high
            pivot = a[low]
            i = low + 1
            while i <= gt:
                if a[i] < pivot:
                    a[lt], a[i] = a[i], a[lt]
                    lt += 1
                    i += 1
                elif a[i] > pivot:
                    a[i], a[gt] = a[gt], a[i]
                    gt -= 1
                else:
                    i += 1
            _quick_sort(low, lt - 1)
            _quick_sort(gt + 1, high)
        _quick_sort(0, len(a) - 1)
        return a


class StressTester:
    @staticmethod
    def run_stress_test(num_trials: int = 50, max_n: int = 200) -> bool:
        print(f"正在进行对拍测试 ({num_trials} 次独立随机实验, Max N={max_n})...")
        for trial in range(1, num_trials + 1):
            n = random.randint(0, max_n)
            data_type = random.choice(["random", "nearly_sorted", "reversed", "duplicates"])
            
            if data_type == "random":
                test_input = DataGenerator.generate_random(n)
            elif data_type == "nearly_sorted":
                test_input = DataGenerator.generate_nearly_sorted(n)
            elif data_type == "reversed":
                test_input = DataGenerator.generate_reversed(n)
            else:
                test_input = DataGenerator.generate_many_duplicates(n)

            expected = sorted(test_input)
            
            m_res = SortAlgorithms.merge_sort(test_input)
            q_res = SortAlgorithms.quick_sort_3way(test_input)
            
            if m_res != expected or q_res != expected:
                print(f"[FAIL] 对拍发现错误！试验 #{trial}, 类型: {data_type}, N={n}")
                return False
            
            if n <= 100:
                b_res = SortAlgorithms.bubble_sort(test_input)
                i_res = SortAlgorithms.insertion_sort(test_input)
                if b_res != expected or i_res != expected:
                    print(f"[FAIL] 基础排序在试验 #{trial} 发现错误！")
                    return False

        print("[OK] 所有对拍测试用例 100% 验证通过！")
        return True


class BenchmarkEngine:
    @staticmethod
    def run_benchmark():
        print("\n" + "="*50)
        print("    数据结构与算法 - 排序算法 Benchmark 耗时表 (秒)")
        print("="*50)
        sizes = [100, 1000, 5000]
        header = f"{'规模 (N)':<10} | {'Bubble':<10} | {'Insertion':<10} | {'Merge':<10} | {'Quick-3Way':<10}"
        print(header)
        print("-" * len(header))

        for n in sizes:
            data = DataGenerator.generate_random(n)

            t_b = "-"
            if n <= 1000:
                t0 = time.perf_counter()
                SortAlgorithms.bubble_sort(data)
                t_b = f"{time.perf_counter() - t0:.5f}s"

            t_i = "-"
            if n <= 1000:
                t0 = time.perf_counter()
                SortAlgorithms.insertion_sort(data)
                t_i = f"{time.perf_counter() - t0:.5f}s"

            t0 = time.perf_counter()
            SortAlgorithms.merge_sort(data)
            t_m = f"{time.perf_counter() - t0:.5f}s"

            t0 = time.perf_counter()
            SortAlgorithms.quick_sort_3way(data)
            t_q = f"{time.perf_counter() - t0:.5f}s"

            print(f"{n:<10} | {t_b:<10} | {t_i:<10} | {t_m:<10} | {t_q:<10}")

        print("="*50 + "\n")


if __name__ == "__main__":
    if StressTester.run_stress_test():
        BenchmarkEngine.run_benchmark()
