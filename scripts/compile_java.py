#!/usr/bin/env python3
"""Compile Java snippets in isolated judge-like environments; does not claim Accepted."""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMPORTS = "import java.util.*;\nimport java.util.stream.*;\nimport java.math.*;\nimport java.util.function.*;\n"
STUBS = {
    "Problem": "abstract class Problem { public int commonSetBits(int x){throw new UnsupportedOperationException(\"judge API stub\");} public int commonBits(int x){throw new UnsupportedOperationException(\"judge API stub\");} }",
    "Node": "class Node { public int val; public Node prev, next; Node(){} Node(int v){val=v;} }",
    "TreeNode": "class TreeNode { int val; TreeNode left, right; TreeNode() {} TreeNode(int v) {val=v;} TreeNode(int v,TreeNode l,TreeNode r){val=v;left=l;right=r;} }",
    "ListNode": "class ListNode { int val; ListNode next; ListNode() {} ListNode(int v){val=v;} ListNode(int v,ListNode n){val=v;next=n;} }",
    "InfiniteStream": "abstract class InfiniteStream { public abstract int next(); }",
    "BigArray": "abstract class BigArray { public abstract int at(long index); public abstract long size(); }",
    "ArrayReader": "abstract class ArrayReader { public abstract int get(int i); public abstract int length(); public abstract int compareSub(int l,int r,int x,int y); public abstract int query(int a,int b,int c,int d); }",
    "Pair": "class Pair<K,V> { private final K key; private final V value; Pair(K k,V v){key=k;value=v;} public K getKey(){return key;} public V getValue(){return value;} public boolean equals(Object o){if(!(o instanceof Pair<?,?> p))return false;return Objects.equals(key,p.key)&&Objects.equals(value,p.value);}public int hashCode(){return Objects.hash(key,value);} }",
}


def compiler_command() -> list[str]:
    if shutil.which("javac"):
        return ["javac"]
    if shutil.which("java"):
        return ["java", "com.sun.tools.javac.Main"]
    raise RuntimeError("A JDK with javac is required")


def compile_file(path: Path, compiler: list[str]) -> tuple[str, str | None]:
    source = path.read_text(encoding="utf-8")
    declarations = re.sub(r"/\*.*?\*/|//[^\n]*", "", source, flags=re.DOTALL)
    supplements = []
    for name, code in STUBS.items():
        if re.search(r"\b" + name + r"\b", source) and not re.search(
            r"(?m)^\s*(?:public\s+)?(?:final\s+)?(?:class|record|interface)\s+" + name + r"\b", declarations
        ):
            supplements.append(code)
    public = re.search(r"(?m)^\s*public\s+(?:final\s+)?class\s+(\w+)", source)
    filename = (public.group(1) if public else "Solution") + ".java"
    with tempfile.TemporaryDirectory(prefix="leetcode-javac-") as tmp:
        work = Path(tmp)
        target = work / filename
        target.write_text(IMPORTS + source + "\n" + "\n".join(supplements) + "\n", encoding="utf-8")
        try:
            result = subprocess.run(compiler + ["-encoding", "UTF-8", "-d", str(work), str(target)],
                                    capture_output=True, text=True, timeout=60)
        except subprocess.TimeoutExpired:
            return str(path.relative_to(ROOT)), "compiler timed out"
        return str(path.relative_to(ROOT)), None if result.returncode == 0 else result.stderr[-5000:]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--new-only", action="store_true")
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args()
    files = sorted((ROOT / "problems").glob("*/java.java"))
    if args.new_only:
        def is_added(path: Path) -> bool:
            metadata = json.loads((path.parent / "metadata.json").read_text())
            return any("java" in metadata.get(key, {}) for key in ("additional_sources", "adapted_sources"))
        files = [p for p in files if is_added(p)]
    if not files:
        raise SystemExit("No Java files selected")
    compiler = compiler_command()
    failures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        for path, error in pool.map(lambda p: compile_file(p, compiler), files):
            if error:
                failures.append((path, error))
    print(f"Java compilation: {len(files) - len(failures)}/{len(files)} passed")
    for path, error in failures:
        print(f"ERROR {path}\n{error}")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
