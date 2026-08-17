#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROBLEMS = ROOT / "problems"
EXTRA_PROBLEMS = (3000, 3001, 3002, 3005, 3010)

FILES = {
    "c": "c.c",
    "dart": "dart.dart",
    "elixir": "elixir.ex",
    "erlang": "erlang.erl",
    "kotlin": "kotlin.kt",
    "php": "php.php",
    "racket": "racket.rkt",
    "ruby": "ruby.rb",
    "scala": "scala.scala",
    "swift": "swift.swift",
    "javascript": "javascript.js",
    "csharp": "csharp.cs",
    "rust": "rust.rs",
}


def check_runtime(command: str) -> None:
    if shutil.which(command) is None:
        raise RuntimeError(f"required runtime/compiler not found: {command}")


def run(command: list[str], cwd: Path, timeout: int = 90) -> None:
    proc = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"command failed ({proc.returncode}): {' '.join(command)}\n{proc.stdout}"
        )


def residual_variants() -> list[tuple[int, str, Path]]:
    variants = []
    for number in EXTRA_PROBLEMS:
        problem = PROBLEMS / str(number)
        metadata = json.loads((problem / "metadata.json").read_text(encoding="utf-8"))
        statuses = metadata.get("languages", {})
        for language, filename in FILES.items():
            path = problem / filename
            if not path.exists():
                continue
            status = statuses.get(language)
            if status != "imported-unverified":
                variants.append((number, language, path))
    return variants


def c_harness(number: int, source: str) -> str:
    tests = {
        3000: r'''
int main(void) {
    { int a[]={9,3}, b[]={8,6}; int* d[]={a,b}; int cols[]={2,2}; if(areaOfMaxDiagonal(d,2,cols)!=48) return 1; }
    { int a[]={4,7}, b[]={1,8}; int* d[]={a,b}; int cols[]={2,2}; if(areaOfMaxDiagonal(d,2,cols)!=28) return 2; }
    { int a[]={2,6}, b[]={5,5}; int* d[]={a,b}; int cols[]={2,2}; if(areaOfMaxDiagonal(d,2,cols)!=25) return 3; }
    return 0;
}
''',
        3001: r'''
int main(void) {
    if(minMovesToCaptureTheQueen(1,1,8,8,1,8)!=1) return 1;
    if(minMovesToCaptureTheQueen(1,1,1,4,1,8)!=2) return 2;
    if(minMovesToCaptureTheQueen(2,3,1,1,4,4)!=1) return 3;
    if(minMovesToCaptureTheQueen(2,2,1,1,4,4)!=2) return 4;
    return 0;
}
''',
        3002: r'''
int main(void) {
    { int a[]={1,2,1,2}, b[]={1,1,1,1}; if(maximumSetSize(a,4,b,4)!=2) return 1; }
    { int a[]={1,2,3,4}, b[]={5,6,7,8}; if(maximumSetSize(a,4,b,4)!=4) return 2; }
    { int a[]={1,2,3,4}, b[]={3,4,5,6}; if(maximumSetSize(a,4,b,4)!=4) return 3; }
    return 0;
}
''',
        3005: r'''
int main(void) {
    { int a[]={1,2,2,3,1,4}; if(maxFrequencyElements(a,6)!=4) return 1; }
    { int a[]={1,2,3,4,5}; if(maxFrequencyElements(a,5)!=5) return 2; }
    { int a[]={7,7,7}; if(maxFrequencyElements(a,3)!=3) return 3; }
    return 0;
}
''',
        3010: r'''
int main(void) {
    { int a[]={1,2,3,12}; if(minimumCost(a,4)!=6) return 1; }
    { int a[]={5,4,3,2,1}; if(minimumCost(a,5)!=8) return 2; }
    { int a[]={10,10,1,10,2}; if(minimumCost(a,5)!=13) return 3; }
    return 0;
}
''',
    }
    return "#include <stdio.h>\n#include <stdlib.h>\n#include <limits.h>\n" + source + tests[number]


def javascript_harness(number: int, source: str) -> str:
    exprs = {
        3000: [
            "areaOfMaxDiagonal([[9,3],[8,6]]) === 48",
            "areaOfMaxDiagonal([[4,7],[1,8]]) === 28",
            "areaOfMaxDiagonal([[2,6],[5,5]]) === 25",
        ],
        3001: [
            "minMovesToCaptureTheQueen(1,1,8,8,1,8) === 1",
            "minMovesToCaptureTheQueen(1,1,1,4,1,8) === 2",
            "minMovesToCaptureTheQueen(2,3,1,1,4,4) === 1",
            "minMovesToCaptureTheQueen(2,2,1,1,4,4) === 2",
        ],
        3002: [
            "maximumSetSize([1,2,1,2],[1,1,1,1]) === 2",
            "maximumSetSize([1,2,3,4],[5,6,7,8]) === 4",
            "maximumSetSize([1,2,3,4],[3,4,5,6]) === 4",
        ],
        3005: [
            "maxFrequencyElements([1,2,2,3,1,4]) === 4",
            "maxFrequencyElements([1,2,3,4,5]) === 5",
            "maxFrequencyElements([7,7,7]) === 3",
        ],
        3010: [
            "minimumCost([1,2,3,12]) === 6",
            "minimumCost([5,4,3,2,1]) === 8",
            "minimumCost([10,10,1,10,2]) === 13",
        ],
    }
    checks = "\n".join(f"if (!({e})) throw new Error('failed: {e}');" for e in exprs[number])
    return source + "\n" + checks + "\n"


def ruby_harness(number: int, source: str) -> str:
    calls = {
        3000: [
            "area_of_max_diagonal([[9,3],[8,6]]) == 48",
            "area_of_max_diagonal([[4,7],[1,8]]) == 28",
            "area_of_max_diagonal([[2,6],[5,5]]) == 25",
        ],
        3001: [
            "min_moves_to_capture_the_queen(1,1,8,8,1,8) == 1",
            "min_moves_to_capture_the_queen(1,1,1,4,1,8) == 2",
            "min_moves_to_capture_the_queen(2,3,1,1,4,4) == 1",
            "min_moves_to_capture_the_queen(2,2,1,1,4,4) == 2",
        ],
        3002: [
            "maximum_set_size([1,2,1,2],[1,1,1,1]) == 2",
            "maximum_set_size([1,2,3,4],[5,6,7,8]) == 4",
            "maximum_set_size([1,2,3,4],[3,4,5,6]) == 4",
        ],
        3005: [
            "max_frequency_elements([1,2,2,3,1,4]) == 4",
            "max_frequency_elements([1,2,3,4,5]) == 5",
            "max_frequency_elements([7,7,7]) == 3",
        ],
        3010: [
            "minimum_cost([1,2,3,12]) == 6",
            "minimum_cost([5,4,3,2,1]) == 8",
            "minimum_cost([10,10,1,10,2]) == 13",
        ],
    }
    return source + "\n" + "\n".join(f"raise 'failed' unless {x}" for x in calls[number]) + "\n"


def php_harness(number: int, source: str) -> str:
    source = source.strip()
    if source.endswith("?>"):
        source = source[:-2].rstrip()
    calls = {
        3000: ["$s->areaOfMaxDiagonal([[9,3],[8,6]]) === 48", "$s->areaOfMaxDiagonal([[4,7],[1,8]]) === 28", "$s->areaOfMaxDiagonal([[2,6],[5,5]]) === 25"],
        3001: ["$s->minMovesToCaptureTheQueen(1,1,8,8,1,8) === 1", "$s->minMovesToCaptureTheQueen(1,1,1,4,1,8) === 2", "$s->minMovesToCaptureTheQueen(2,3,1,1,4,4) === 1", "$s->minMovesToCaptureTheQueen(2,2,1,1,4,4) === 2"],
        3002: ["$s->maximumSetSize([1,2,1,2],[1,1,1,1]) === 2", "$s->maximumSetSize([1,2,3,4],[5,6,7,8]) === 4", "$s->maximumSetSize([1,2,3,4],[3,4,5,6]) === 4"],
        3005: ["$s->maxFrequencyElements([1,2,2,3,1,4]) === 4", "$s->maxFrequencyElements([1,2,3,4,5]) === 5", "$s->maxFrequencyElements([7,7,7]) === 3"],
        3010: ["$s->minimumCost([1,2,3,12]) === 6", "$s->minimumCost([5,4,3,2,1]) === 8", "$s->minimumCost([10,10,1,10,2]) === 13"],
    }
    checks = "\n".join(f"if (!({x})) {{ throw new Exception('failed'); }}" for x in calls[number])
    return source + "\n$s = new Solution();\n" + checks + "\n?>\n"


def rust_harness(number: int, source: str) -> str:
    calls = {
        3000: ["Solution::area_of_max_diagonal(vec![vec![9,3],vec![8,6]]) == 48", "Solution::area_of_max_diagonal(vec![vec![4,7],vec![1,8]]) == 28", "Solution::area_of_max_diagonal(vec![vec![2,6],vec![5,5]]) == 25"],
        3001: ["Solution::min_moves_to_capture_the_queen(1,1,8,8,1,8) == 1", "Solution::min_moves_to_capture_the_queen(1,1,1,4,1,8) == 2", "Solution::min_moves_to_capture_the_queen(2,3,1,1,4,4) == 1", "Solution::min_moves_to_capture_the_queen(2,2,1,1,4,4) == 2"],
        3002: ["Solution::maximum_set_size(vec![1,2,1,2],vec![1,1,1,1]) == 2", "Solution::maximum_set_size(vec![1,2,3,4],vec![5,6,7,8]) == 4", "Solution::maximum_set_size(vec![1,2,3,4],vec![3,4,5,6]) == 4"],
        3005: ["Solution::max_frequency_elements(vec![1,2,2,3,1,4]) == 4", "Solution::max_frequency_elements(vec![1,2,3,4,5]) == 5", "Solution::max_frequency_elements(vec![7,7,7]) == 3"],
        3010: ["Solution::minimum_cost(vec![1,2,3,12]) == 6", "Solution::minimum_cost(vec![5,4,3,2,1]) == 8", "Solution::minimum_cost(vec![10,10,1,10,2]) == 13"],
    }
    checks = "\n".join(f"assert!({x});" for x in calls[number])
    return "struct Solution;\n" + source + f"\nfn main() {{\n{checks}\n}}\n"


def kotlin_harness(number: int, source: str) -> str:
    calls = {
        3000: ["s.areaOfMaxDiagonal(arrayOf(intArrayOf(9,3),intArrayOf(8,6))) == 48", "s.areaOfMaxDiagonal(arrayOf(intArrayOf(4,7),intArrayOf(1,8))) == 28", "s.areaOfMaxDiagonal(arrayOf(intArrayOf(2,6),intArrayOf(5,5))) == 25"],
        3001: ["s.minMovesToCaptureTheQueen(1,1,8,8,1,8) == 1", "s.minMovesToCaptureTheQueen(1,1,1,4,1,8) == 2", "s.minMovesToCaptureTheQueen(2,3,1,1,4,4) == 1", "s.minMovesToCaptureTheQueen(2,2,1,1,4,4) == 2"],
        3002: ["s.maximumSetSize(intArrayOf(1,2,1,2),intArrayOf(1,1,1,1)) == 2", "s.maximumSetSize(intArrayOf(1,2,3,4),intArrayOf(5,6,7,8)) == 4", "s.maximumSetSize(intArrayOf(1,2,3,4),intArrayOf(3,4,5,6)) == 4"],
        3005: ["s.maxFrequencyElements(intArrayOf(1,2,2,3,1,4)) == 4", "s.maxFrequencyElements(intArrayOf(1,2,3,4,5)) == 5", "s.maxFrequencyElements(intArrayOf(7,7,7)) == 3"],
        3010: ["s.minimumCost(intArrayOf(1,2,3,12)) == 6", "s.minimumCost(intArrayOf(5,4,3,2,1)) == 8", "s.minimumCost(intArrayOf(10,10,1,10,2)) == 13"],
    }
    checks = "\n".join(f"check({x})" for x in calls[number])
    return source + f"\nfun main() {{\nval s = Solution()\n{checks}\n}}\n"


def scala_harness(number: int, source: str) -> str:
    calls = {
        3000: ["Solution.areaOfMaxDiagonal(Array(Array(9,3),Array(8,6))) == 48", "Solution.areaOfMaxDiagonal(Array(Array(4,7),Array(1,8))) == 28", "Solution.areaOfMaxDiagonal(Array(Array(2,6),Array(5,5))) == 25"],
        3001: ["Solution.minMovesToCaptureTheQueen(1,1,8,8,1,8) == 1", "Solution.minMovesToCaptureTheQueen(1,1,1,4,1,8) == 2", "Solution.minMovesToCaptureTheQueen(2,3,1,1,4,4) == 1", "Solution.minMovesToCaptureTheQueen(2,2,1,1,4,4) == 2"],
        3002: ["Solution.maximumSetSize(Array(1,2,1,2),Array(1,1,1,1)) == 2", "Solution.maximumSetSize(Array(1,2,3,4),Array(5,6,7,8)) == 4", "Solution.maximumSetSize(Array(1,2,3,4),Array(3,4,5,6)) == 4"],
        3005: ["Solution.maxFrequencyElements(Array(1,2,2,3,1,4)) == 4", "Solution.maxFrequencyElements(Array(1,2,3,4,5)) == 5", "Solution.maxFrequencyElements(Array(7,7,7)) == 3"],
        3010: ["Solution.minimumCost(Array(1,2,3,12)) == 6", "Solution.minimumCost(Array(5,4,3,2,1)) == 8", "Solution.minimumCost(Array(10,10,1,10,2)) == 13"],
    }
    checks = "\n".join(f"assert({x})" for x in calls[number])
    return source + f"\nobject ExtraTest extends App {{\n{checks}\n}}\n"


def swift_harness(number: int, source: str) -> str:
    calls = {
        3000: ["s.areaOfMaxDiagonal([[9,3],[8,6]]) == 48", "s.areaOfMaxDiagonal([[4,7],[1,8]]) == 28", "s.areaOfMaxDiagonal([[2,6],[5,5]]) == 25"],
        3001: ["s.minMovesToCaptureTheQueen(1,1,8,8,1,8) == 1", "s.minMovesToCaptureTheQueen(1,1,1,4,1,8) == 2", "s.minMovesToCaptureTheQueen(2,3,1,1,4,4) == 1", "s.minMovesToCaptureTheQueen(2,2,1,1,4,4) == 2"],
        3002: ["s.maximumSetSize([1,2,1,2],[1,1,1,1]) == 2", "s.maximumSetSize([1,2,3,4],[5,6,7,8]) == 4", "s.maximumSetSize([1,2,3,4],[3,4,5,6]) == 4"],
        3005: ["s.maxFrequencyElements([1,2,2,3,1,4]) == 4", "s.maxFrequencyElements([1,2,3,4,5]) == 5", "s.maxFrequencyElements([7,7,7]) == 3"],
        3010: ["s.minimumCost([1,2,3,12]) == 6", "s.minimumCost([5,4,3,2,1]) == 8", "s.minimumCost([10,10,1,10,2]) == 13"],
    }
    checks = "\n".join(f"precondition({x})" for x in calls[number])
    return source + f"\nlet s = Solution()\n{checks}\n"


def dart_harness(number: int, source: str) -> str:
    calls = {
        3000: ["s.areaOfMaxDiagonal([[9,3],[8,6]]) == 48", "s.areaOfMaxDiagonal([[4,7],[1,8]]) == 28", "s.areaOfMaxDiagonal([[2,6],[5,5]]) == 25"],
        3001: ["s.minMovesToCaptureTheQueen(1,1,8,8,1,8) == 1", "s.minMovesToCaptureTheQueen(1,1,1,4,1,8) == 2", "s.minMovesToCaptureTheQueen(2,3,1,1,4,4) == 1", "s.minMovesToCaptureTheQueen(2,2,1,1,4,4) == 2"],
        3002: ["s.maximumSetSize([1,2,1,2],[1,1,1,1]) == 2", "s.maximumSetSize([1,2,3,4],[5,6,7,8]) == 4", "s.maximumSetSize([1,2,3,4],[3,4,5,6]) == 4"],
        3005: ["s.maxFrequencyElements([1,2,2,3,1,4]) == 4", "s.maxFrequencyElements([1,2,3,4,5]) == 5", "s.maxFrequencyElements([7,7,7]) == 3"],
        3010: ["s.minimumCost([1,2,3,12]) == 6", "s.minimumCost([5,4,3,2,1]) == 8", "s.minimumCost([10,10,1,10,2]) == 13"],
    }
    checks = "\n".join(f"if (!({x})) throw StateError('failed');" for x in calls[number])
    return source + f"\nvoid main() {{\nfinal s = Solution();\n{checks}\n}}\n"


def csharp_harness(number: int, source: str) -> str:
    calls = {
        3000: ["s.AreaOfMaxDiagonal(new int[][] { new[]{9,3}, new[]{8,6} }) == 48", "s.AreaOfMaxDiagonal(new int[][] { new[]{4,7}, new[]{1,8} }) == 28", "s.AreaOfMaxDiagonal(new int[][] { new[]{2,6}, new[]{5,5} }) == 25"],
        3001: ["s.MinMovesToCaptureTheQueen(1,1,8,8,1,8) == 1", "s.MinMovesToCaptureTheQueen(1,1,1,4,1,8) == 2", "s.MinMovesToCaptureTheQueen(2,3,1,1,4,4) == 1", "s.MinMovesToCaptureTheQueen(2,2,1,1,4,4) == 2"],
        3002: ["s.MaximumSetSize(new[]{1,2,1,2},new[]{1,1,1,1}) == 2", "s.MaximumSetSize(new[]{1,2,3,4},new[]{5,6,7,8}) == 4", "s.MaximumSetSize(new[]{1,2,3,4},new[]{3,4,5,6}) == 4"],
        3005: ["s.MaxFrequencyElements(new[]{1,2,2,3,1,4}) == 4", "s.MaxFrequencyElements(new[]{1,2,3,4,5}) == 5", "s.MaxFrequencyElements(new[]{7,7,7}) == 3"],
        3010: ["s.MinimumCost(new[]{1,2,3,12}) == 6", "s.MinimumCost(new[]{5,4,3,2,1}) == 8", "s.MinimumCost(new[]{10,10,1,10,2}) == 13"],
    }
    checks = "\n".join(f"if (!({x})) throw new Exception(\"failed\");" for x in calls[number])
    return "using System;\nusing System.Collections.Generic;\nusing System.Linq;\n" + source + f"\npublic static class Program {{ public static void Main() {{ var s = new Solution(); {checks} }} }}\n"


def racket_harness(number: int, source: str) -> str:
    calls = {
        3000: ["(= (area-of-max-diagonal '((9 3) (8 6))) 48)", "(= (area-of-max-diagonal '((4 7) (1 8))) 28)", "(= (area-of-max-diagonal '((2 6) (5 5))) 25)"],
        3001: ["(= (min-moves-to-capture-the-queen 1 1 8 8 1 8) 1)", "(= (min-moves-to-capture-the-queen 1 1 1 4 1 8) 2)", "(= (min-moves-to-capture-the-queen 2 3 1 1 4 4) 1)", "(= (min-moves-to-capture-the-queen 2 2 1 1 4 4) 2)"],
        3002: ["(= (maximum-set-size '(1 2 1 2) '(1 1 1 1)) 2)", "(= (maximum-set-size '(1 2 3 4) '(5 6 7 8)) 4)", "(= (maximum-set-size '(1 2 3 4) '(3 4 5 6)) 4)"],
        3005: ["(= (max-frequency-elements '(1 2 2 3 1 4)) 4)", "(= (max-frequency-elements '(1 2 3 4 5)) 5)", "(= (max-frequency-elements '(7 7 7)) 3)"],
        3010: ["(= (minimum-cost '(1 2 3 12)) 6)", "(= (minimum-cost '(5 4 3 2 1)) 8)", "(= (minimum-cost '(10 10 1 10 2)) 13)"],
    }
    checks = "\n".join(f"(unless {x} (error 'functional-test \"failed\"))" for x in calls[number])
    return "#lang racket\n" + source + "\n" + checks + "\n"


def elixir_harness(number: int, source: str) -> str:
    calls = {
        3000: ["Solution.area_of_max_diagonal([[9,3],[8,6]]) == 48", "Solution.area_of_max_diagonal([[4,7],[1,8]]) == 28", "Solution.area_of_max_diagonal([[2,6],[5,5]]) == 25"],
        3001: ["Solution.min_moves_to_capture_the_queen(1,1,8,8,1,8) == 1", "Solution.min_moves_to_capture_the_queen(1,1,1,4,1,8) == 2", "Solution.min_moves_to_capture_the_queen(2,3,1,1,4,4) == 1", "Solution.min_moves_to_capture_the_queen(2,2,1,1,4,4) == 2"],
        3002: ["Solution.maximum_set_size([1,2,1,2],[1,1,1,1]) == 2", "Solution.maximum_set_size([1,2,3,4],[5,6,7,8]) == 4", "Solution.maximum_set_size([1,2,3,4],[3,4,5,6]) == 4"],
        3005: ["Solution.max_frequency_elements([1,2,2,3,1,4]) == 4", "Solution.max_frequency_elements([1,2,3,4,5]) == 5", "Solution.max_frequency_elements([7,7,7]) == 3"],
        3010: ["Solution.minimum_cost([1,2,3,12]) == 6", "Solution.minimum_cost([5,4,3,2,1]) == 8", "Solution.minimum_cost([10,10,1,10,2]) == 13"],
    }
    checks = "\n".join(f"unless {x}, do: raise(\"failed\")" for x in calls[number])
    return source + "\n" + checks + "\n"


def erlang_harness(number: int, source: str) -> str:
    fn = {3000:"area_of_max_diagonal",3001:"min_moves_to_capture_the_queen",3002:"maximum_set_size",3005:"max_frequency_elements",3010:"minimum_cost"}[number]
    calls = {
        3000: ["48 = area_of_max_diagonal([[9,3],[8,6]])", "28 = area_of_max_diagonal([[4,7],[1,8]])", "25 = area_of_max_diagonal([[2,6],[5,5]])"],
        3001: ["1 = min_moves_to_capture_the_queen(1,1,8,8,1,8)", "2 = min_moves_to_capture_the_queen(1,1,1,4,1,8)", "1 = min_moves_to_capture_the_queen(2,3,1,1,4,4)", "2 = min_moves_to_capture_the_queen(2,2,1,1,4,4)"],
        3002: ["2 = maximum_set_size([1,2,1,2],[1,1,1,1])", "4 = maximum_set_size([1,2,3,4],[5,6,7,8])", "4 = maximum_set_size([1,2,3,4],[3,4,5,6])"],
        3005: ["4 = max_frequency_elements([1,2,2,3,1,4])", "5 = max_frequency_elements([1,2,3,4,5])", "3 = max_frequency_elements([7,7,7])"],
        3010: ["6 = minimum_cost([1,2,3,12])", "8 = minimum_cost([5,4,3,2,1])", "13 = minimum_cost([10,10,1,10,2])"],
    }
    body = ",\n    ".join(calls[number]) + ",\n    ok."
    return f"-module(extra_test).\n-export([main/0]).\n" + source + f"\nmain() ->\n    {body}\n"


def execute_variant(number: int, language: str, path: Path, work: Path) -> None:
    source = path.read_text(encoding="utf-8", errors="replace")
    if language == "c":
        check_runtime("gcc")
        test = work / "test.c"; test.write_text(c_harness(number, source), encoding="utf-8")
        run(["gcc","-std=c11","-O2","test.c","-o","test"], work); run([str(work / "test")], work)
    elif language == "javascript":
        check_runtime("node")
        test=work/"test.js"; test.write_text(javascript_harness(number, source), encoding="utf-8"); run(["node","test.js"], work)
    elif language == "ruby":
        check_runtime("ruby")
        test=work/"test.rb"; test.write_text(ruby_harness(number, source), encoding="utf-8"); run(["ruby","test.rb"], work)
    elif language == "php":
        check_runtime("php")
        test=work/"test.php"; test.write_text(php_harness(number, source), encoding="utf-8"); run(["php","test.php"], work)
    elif language == "rust":
        check_runtime("rustc")
        test=work/"test.rs"; test.write_text(rust_harness(number, source), encoding="utf-8"); run(["rustc","-O","test.rs","-o","test"], work); run([str(work/"test")], work)
    elif language == "kotlin":
        check_runtime("kotlinc"); check_runtime("java")
        test=work/"Test.kt"; test.write_text(kotlin_harness(number, source), encoding="utf-8"); run(["kotlinc","Test.kt","-include-runtime","-d","test.jar"], work); run(["java","-jar","test.jar"], work)
    elif language == "scala":
        check_runtime("scalac"); check_runtime("scala")
        test=work/"ExtraTest.scala"; test.write_text(scala_harness(number, source), encoding="utf-8"); run(["scalac","ExtraTest.scala"], work); run(["scala","ExtraTest"], work)
    elif language == "swift":
        check_runtime("swiftc")
        test=work/"main.swift"; test.write_text(swift_harness(number, source), encoding="utf-8"); run(["swiftc","main.swift","-o","test"], work); run([str(work/"test")], work)
    elif language == "dart":
        check_runtime("dart")
        test=work/"test.dart"; test.write_text(dart_harness(number, source), encoding="utf-8"); run(["dart","run","test.dart"], work)
    elif language == "csharp":
        check_runtime("mcs"); check_runtime("mono")
        test=work/"test.cs"; test.write_text(csharp_harness(number, source), encoding="utf-8"); run(["mcs","-optimize+","test.cs","-out:test.exe"], work); run(["mono","test.exe"], work)
    elif language == "racket":
        check_runtime("racket")
        test=work/"test.rkt"; test.write_text(racket_harness(number, source), encoding="utf-8"); run(["racket","test.rkt"], work)
    elif language == "elixir":
        check_runtime("elixir")
        test=work/"test.exs"; test.write_text(elixir_harness(number, source), encoding="utf-8"); run(["elixir","test.exs"], work)
    elif language == "erlang":
        check_runtime("erlc"); check_runtime("erl")
        test=work/"extra_test.erl"; test.write_text(erlang_harness(number, source), encoding="utf-8"); run(["erlc","extra_test.erl"], work); run(["erl","-noshell","-s","extra_test","main","-s","init","stop"], work)
    else:
        raise RuntimeError(f"unsupported extra language: {language}")


def main() -> None:
    variants = residual_variants()
    if len(variants) != 58:
        raise SystemExit(f"Expected 58 residual extra variants, found {len(variants)}. Update verification scope intentionally.")

    passed = Counter()
    failures = []
    with tempfile.TemporaryDirectory(prefix="leetcode-extra-tests-") as tmp:
        base = Path(tmp)
        for number, language, path in variants:
            work = base / f"{number}-{language}"
            work.mkdir(parents=True)
            try:
                execute_variant(number, language, path, work)
                passed[language] += 1
                print(f"PASS {number}/{language}")
            except Exception as exc:
                failures.append((number, language, str(exc)))
                print(f"FAIL {number}/{language}: {exc}", file=sys.stderr)

    print(f"Functional extra-variant tests passed: {sum(passed.values())}/{len(variants)}")
    for language, count in sorted(passed.items(), key=lambda item: (-item[1], item[0])):
        print(f"  {language}: {count}")

    report = [
        "# Functional verification of extra variants",
        "",
        f"- Residual manually-authored/translated variants tested: **{len(variants)}**",
        f"- Passed: **{sum(passed.values())}**",
        f"- Failed: **{len(failures)}**",
        "",
        "Each variant is compiled/executed in its own language runtime against deterministic behavioral test cases for its LeetCode problem.",
        "",
        "## Passed by language",
        "",
    ]
    for language, count in sorted(passed.items(), key=lambda item: (-item[1], item[0])):
        report.append(f"- {language}: {count}")
    if failures:
        report.extend(["", "## Failures", ""])
        for number, language, detail in failures:
            report.append(f"- {number}/{language}: `{detail.splitlines()[0]}`")
    (ROOT / "EXTRA_VARIANT_VERIFICATION.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
