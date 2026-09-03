#!/usr/bin/env python3
"""Deterministic differential tests for the 48 Java adaptations; not judge acceptance.

Compiles each Solution in isolation and compares it with its source-backed C++
implementation. Selected problems also have independent small-input oracles.
No network, repository writes, or third-party Python packages are required.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import itertools
import json
import math
import os
import random
import re
import subprocess
import tempfile
from pathlib import Path

from compile_java import compiler_command

ROOT = Path(__file__).resolve().parents[1]
IDS = (3526,3595,3632,3656,3735,3802,3901,3911,3916,3920,3922,3923,
       3924,3927,3928,3929,3930,3933,3934,3938,3939,3943,3944,3947,
       3948,3949,3952,3953,3956,3957,3962,3966,3967,3970,3971,3972,
       3973,3980,3981,3984,3985,3988,3989,3990,3994,3995,3998,3999)


def cases(number: int, repeats: int = 48) -> list[list]:
    rng = random.Random(number)
    out = []
    for _ in range(repeats):
        n = rng.randint(2, 10)
        arr = lambda size=n, lo=1, hi=20: [rng.randint(lo, hi) for _ in range(size)]
        text = lambda size=n, alphabet="01": "".join(rng.choice(alphabet) for _ in range(size))
        tree = lambda: [[i, rng.randrange(i)] for i in range(1, n)]
        if number == 3526:
            queries = []
            for _ in range(20):
                kind = rng.randint(1, 3); left = rng.randrange(n)
                queries.append([kind, left, rng.randint(0, 100) if kind == 1 else rng.randint(left, n-1)])
            a = [arr(lo=0, hi=100), queries]
        elif number == 3595:
            values = rng.sample(range(-100, 101), n)
            nums = values[:1] + [values[1]] * 2 + list(itertools.chain.from_iterable([v]*3 for v in values[2:]))
            rng.shuffle(nums); a = [nums]
        elif number == 3632: a = [arr(lo=0, hi=63), rng.randint(0, 100)]
        elif number == 3656: a = [arr(lo=0, hi=n)]
        elif number == 3735: a = [text(alphabet="abcde")]
        elif number == 3802: a = [n, arr(size=rng.randint(2, 8), lo=1, hi=15)]
        elif number == 3901: a = [arr(hi=30), rng.randint(1, 7), [[rng.randrange(n), rng.randint(1, 30)] for _ in range(12)]]
        elif number == 3911:
            nums = sorted(rng.sample(range(1, 100), n)); queries = []
            for _ in range(12):
                left = rng.randrange(n); queries.append([left, rng.randint(left, n-1), rng.randint(1, 100)])
            a = [nums, queries]
        elif number == 3916:
            left = rng.randint(1, 10); a = [n, left, left + rng.randint(0, 30)]
        elif number == 3920: a = [arr(lo=0, hi=n)]
        elif number == 3922: a = [text()]
        elif number == 3923: a = [[arr(size=3, lo=0, hi=6) for _ in range(rng.randint(1, 8))], arr(size=3, lo=0, hi=6)]
        elif number == 3924:
            edges = [e + [rng.randint(1, 30)] for e in tree() if rng.random() < .8]
            a = [n, edges, rng.randrange(n), rng.randrange(n), rng.randrange(n)]
        elif number == 3927: a = [arr(hi=50)]
        elif number == 3928: a = [n, arr(hi=100), [e+[rng.randint(1, 20),rng.randint(1, 5)] for e in tree()]]
        elif number == 3929: a = [arr(hi=10), rng.randint(1, n)]
        elif number == 3930: a = [arr(lo=0), rng.randint(1, 100), [[rng.randint(0, 50), rng.randint(1, n+i+1)] for i in range(12)]]
        elif number == 3933:
            width = rng.randint(1,8)
            a = [[arr(size=width, lo=0, hi=4) for _ in range(rng.randint(1,10))]]
        elif number == 3934: a = [arr(lo=-3, hi=3)]
        elif number == 3938: a = [[arr(size=5, lo=-20, hi=20) for _ in range(n)]]
        elif number == 3939: a = [[-1]+[rng.randrange(i) for i in range(1,n)], arr(hi=20), rng.randint(1, 7)]
        elif number == 3943:
            queries = []
            for _ in range(20):
                left = rng.randrange(n)
                queries.append([1,left,rng.randint(left,n-1),rng.randint(1,10)] if rng.random()<.5 else [2,rng.randint(1,100)])
            a = [arr(size=5), arr(), queries]
        elif number == 3944: a = [arr(hi=100), rng.randint(2, 15)]
        elif number == 3947: a = [[[rng.randint(1,30), rng.randint(1,20)] for _ in range(n)], rng.randint(1,200)]
        elif number == 3948: a = [arr(lo=0, hi=n)]
        elif number == 3949: a = [tree(), arr(lo=-20,hi=20), rng.randint(1,n)]
        elif number == 3952: a = [arr(hi=100), text()]
        elif number == 3953: a = [arr(hi=50), rng.randint(1,50)]
        elif number in (3956,3957):
            lower = rng.randint(1,n); a = [arr(lo=-20,hi=20), rng.randint(1,n), lower, rng.randint(lower,n)]
        elif number == 3962: a = [arr(lo=-20,hi=20), rng.randint(0,n)]
        elif number == 3966:
            left = rng.randint(0,1000); a = [left, left+rng.randint(0,2000), rng.randint(0,9)]
        elif number == 3967: a = [n, tree(), arr(hi=50)]
        elif number == 3970:
            edges = [[u,v,rng.randint(1,30)] for u in range(n) for v in range(n) if u!=v and rng.random()<.2]
            a = [n, edges, text(alphabet="abc"), rng.randint(1,5)]
        elif number == 3971: a = [arr(hi=100), arr(hi=15), rng.randint(1,100)]
        elif number == 3972: a = [arr(hi=100), rng.randint(1,9)]
        elif number == 3973: a = [n,[-1]+[rng.randrange(i) for i in range(1,n)], [arr(size=3,lo=0,hi=10) for _ in range(n)], [[rng.randrange(n),rng.randrange(2),rng.randrange(n),rng.randrange(2)] for _ in range(12)]]
        elif number == 3980: a = [text(),text()]
        elif number == 3981: a = [text(size=4,alphabet="ab"),text(size=4,alphabet="ab"),text(size=rng.randint(1,8),alphabet="ab")]
        elif number == 3984: a = [arr(hi=100)]
        elif number == 3985: a = [arr(hi=4)]
        elif number == 3988: a = [rng.randint(1,7),rng.randint(1,7),rng.randint(1,4)]
        elif number == 3989: a = [[arr(size=8,lo=-20,hi=20) for _ in range(n)], rng.randint(0,30)]
        elif number == 3990: a = [rng.randint(1,10000)]
        elif number == 3994:
            low = rng.randint(1,30); a = [arr(hi=50),low,rng.randint(low,50)]
        elif number == 3995:
            rules = []
            for _ in range(12):
                length=rng.randint(1,n); rules.append([text(size=length,alphabet="ab*"),text(size=length,alphabet="ab")])
            a = [text(alphabet="ab"),text(alphabet="ab"),rules,arr(size=len(rules),lo=0,hi=10)]
        elif number == 3998: a = [text(),[text(alphabet="01?") for _ in range(15)]]
        elif number == 3999: a = [[text(size=rng.randint(1,8),alphabet="abc") for _ in range(15)]]
        else: raise ValueError(number)
        out.append(a)
    return out


def oracle(number: int, args: list):
    """Return an independent small-input result, or None for differential-only tests."""
    if number == 3526:
        nums, queries = args; nums=nums[:]; answer=[]
        for kind,left,right in queries:
            if kind==1: nums[left]=right
            elif kind==3: nums[left:right+1]=nums[left:right+1][::-1]
            else:
                value=0
                for x in nums[left:right+1]: value ^= x
                answer.append(value)
        return answer
    if number == 3632:
        nums,k=args; answer=0
        for i in range(len(nums)):
            value=0
            for x in nums[i:]: value ^= x; answer += value>=k
        return answer
    if number == 3656:
        degrees=args[0][:]
        while degrees:
            degrees.sort(reverse=True); degree=degrees.pop(0)
            if degree<0 or degree>len(degrees): return False
            for i in range(degree): degrees[i]-=1
        return True
    if number == 3735:
        s=args[0]; return min([s]+[s[:i][::-1]+s[i:] for i in range(1,len(s)+1)]+[s[:i]+s[i:][::-1] for i in range(len(s))])
    if number == 3802:
        n,limits=args
        return sum(first<=limits[i] and n-first<=limits[j] for first in range(1,n) for i in range(len(limits)) for j in range(len(limits)) if i!=j)
    if number == 3901:
        nums,p,queries=args; nums=nums[:]; answer=0
        for index,value in queries:
            nums[index]=value
            answer += any(math.gcd(*(nums[i] for i in range(len(nums)) if mask>>i&1))==p for mask in range(1,(1<<len(nums))-1))
        return answer
    if number == 3911:
        nums,queries=args; answer=[]
        for left,right,k in queries:
            excluded=set(nums[left:right+1]); value=0
            while k:
                value+=2; k-=value not in excluded
            answer.append(value)
        return answer
    if number == 3927:
        nums=args[0]; return sum(min(d for d in nums if x%d==0) for x in nums)
    if number == 3929:
        nums,k=args; n=len(nums); prefix=list(itertools.accumulate(nums,initial=0)); dp=[0]+[10**30]*n
        for _ in range(k):
            dp=[10**30]+[min(dp[j]+(prefix[i]-prefix[j])*(prefix[i]-prefix[j]+1)//2 for j in range(i)) for i in range(1,n+1)]
        return dp[n]
    if number == 3933:
        matrix=args[0]; n=len(matrix); m=len(matrix[0]); answer=0
        for r in range(n):
            for c in range(m):
                x=matrix[r][c]
                if x and all(matrix[i][j]<=x for i in range(max(0,r-x),min(n,r+x+1)) for j in range(max(0,c-x),min(m,c+x+1)) if not(abs(i-r)==x and abs(j-c)==x)):
                    answer+=1
        return answer
    if number == 3934:
        nums=args[0]
        for length in range(1,len(nums)+1):
            windows=[tuple(nums[i:i+length]) for i in range(len(nums)-length+1)]
            if any(windows.count(w)==1 for w in windows): return length
    if number == 3939:
        parent,nums,k=args
        return sum(sum(nums[i] for i in range(len(nums)) if mask>>i&1)%k==0 and all(not(mask>>i&1 and mask>>parent[i]&1) for i in range(1,len(nums))) for mask in range(1,1<<len(nums)))
    if number == 3944:
        nums,k=args
        cost=lambda parity,target:sum(min((x-target)%k,(target-x)%k) for x in nums[parity::2])
        return min(cost(0,a)+cost(1,b) for a in range(k) for b in range(k) if a!=b)
    if number in (3956,3957):
        nums,m,lower,upper=args; n=len(nums); prefix=list(itertools.accumulate(nums,initial=0)); best=-10**30
        dp=[0]*(n+1)
        for _ in range(min(m,n//lower)):
            next_dp=[-10**30]*(n+1)
            for i in range(1,n+1):
                next_dp[i]=next_dp[i-1]
                for length in range(lower,min(upper,i)+1): next_dp[i]=max(next_dp[i],dp[i-length]+prefix[i]-prefix[i-length])
            dp=next_dp; best=max(best,dp[n])
        return best
    if number == 3966:
        left,right,k=args
        return sum(all(abs(int(a)-int(b))<=k for a,b in zip(str(x),str(x)[1:])) for x in range(left,right+1))
    if number == 3971:
        values,decay,m=args
        return sum(sorted([x for v,d in zip(values,decay) for x in range(v,0,-d)],reverse=True)[:m])%1_000_000_007
    if number == 3972:
        nums,x=args; digit=str(x)
        return sum(str(sum(nums[i:j])).startswith(digit) and str(sum(nums[i:j])).endswith(digit) for i in range(len(nums)) for j in range(i+1,len(nums)+1))
    if number == 3985:
        nums=args[0]
        return max(sum(nums[i:j]) for i in range(len(nums)) for j in range(i+1,len(nums)+1) if nums[i:j]==nums[i:j][::-1])
    if number == 3989:
        grid,limit=args; n=len(grid[0]); dp=[1]*n
        for i in range(n):
            for j in range(i):
                if all(abs(row[i]-row[j])<=limit for row in grid): dp[i]=max(dp[i],dp[j]+1)
        return max(dp)
    if number == 3994:
        nums,a,b=args; classes=[0 if x<a else 1 if x<=b else 2 for x in nums]
        return sum(classes[i]>classes[j] for i in range(len(nums)) for j in range(i+1,len(nums)))
    return None


def first_cpp_solution(source: str) -> tuple[str, str, list[str]]:
    match=re.search(r"\bclass Solution\s*\{",source)
    if not match: raise ValueError("Missing C++ Solution")
    depth=1; end=match.end()
    while depth:
        depth += (source[end]=='{')-(source[end]=='}'); end+=1
    selected=source[:end]+";\n"
    method=re.search(r"public:\s*([\w<> ]+)\s+(\w+)\(([^)]*)\)\s*\{",source[match.end():end])
    if not method: raise ValueError("Missing C++ public method")
    types=[re.sub(r"\s+\w+$","",p.strip()).replace("&","").strip() for p in method.group(3).split(",")]
    return selected,method.group(2),types


def literal(value, type_name: str, java: bool) -> str:
    if type_name.startswith("vector<"):
        inner=type_name[7:-1]
        body="{"+",".join(literal(x,inner,java) for x in value)+"}"
        return "new "+java_type(type_name)+body if java else body
    if type_name=="string": return json.dumps(value)
    return str(value)+("L" if java and type_name=="long long" else "")


def java_type(type_name: str) -> str:
    if type_name.startswith("vector<"): return java_type(type_name[7:-1])+"[]"
    return {"string":"String","long long":"long","int":"int","bool":"boolean"}[type_name]


CPP_OUTPUT = r'''
template<class T> void emit(const vector<T>&);
template<class T> void emit(const T& value) { cout << value; }
void emit(const string& value) { cout << quoted(value); }
template<class T> void emit(const vector<T>& values) {
    cout << '['; bool first=true;
    for (auto value:values) { if(!first) cout<<','; first=false; emit(value); }
    cout << ']';
}
'''
JAVA_OUTPUT = r'''
class Main {
    static String encode(Object value) {
        if(value==null) return "null";
        if(value instanceof String) return "\""+value+"\"";
        List<String> parts=new ArrayList<>();
        if(value.getClass().isArray()) {
            for(int i=0;i<java.lang.reflect.Array.getLength(value);i++)
                parts.add(encode(java.lang.reflect.Array.get(value,i)));
        } else if(value instanceof Iterable<?>) {
            for(Object x:(Iterable<?>)value) parts.add(encode(x));
        } else return value.toString();
        return "["+String.join(",",parts)+"]";
    }
'''


def run_problem(number: int, repeats: int) -> tuple[int, int, int]:
    directory=ROOT/"problems"/str(number)
    cpp,method,types=first_cpp_solution((directory/"cpp.cpp").read_text())
    inputs=cases(number,repeats)
    cpp_cases=[]; java_cases=[]
    for case in inputs:
        declarations="".join(f"{t} a{i}={literal(v,t,False)};" for i,(t,v) in enumerate(zip(types,case)))
        names=",".join(f"a{i}" for i in range(len(types)))
        cpp_cases.append("{"+declarations+f"Solution s; emit(s.{method}({names}));cout<<'\\n';"+"}")
        arguments=",".join(literal(v,t,True) for t,v in zip(types,case))
        java_cases.append(f"System.out.println(encode(new Solution().{method}({arguments}))); ")
    with tempfile.TemporaryDirectory(prefix=f"leetcode-java-{number}-") as tmp:
        work=Path(tmp)
        (work/"main.cpp").write_text("#include <bits/stdc++.h>\nusing namespace std;\n"+cpp+CPP_OUTPUT+"int main(){"+"\n".join(cpp_cases)+"}\n")
        # Split generated Java methods to avoid the JVM's 64 KiB bytecode limit.
        chunks=[java_cases[i:i+10] for i in range(0,len(java_cases),10)]
        methods="\n".join(f"static void part{i}(){{"+"\n".join(chunk)+"}" for i,chunk in enumerate(chunks))
        main="public static void main(String[] args){"+"".join(f"part{i}();" for i in range(len(chunks)))+"}}"
        (work/"Main.java").write_text("import java.util.*;\n"+(directory/"java.java").read_text()+JAVA_OUTPUT+methods+main)
        def run(command, timeout=90):
            result=subprocess.run(command,cwd=work,capture_output=True,text=True,timeout=timeout)
            if result.returncode: raise RuntimeError(f"#{number}: {command[0]} failed\n{result.stderr[-5000:]}")
            return result.stdout
        flags = ["-O1", "-g", "-fsanitize=address,undefined", "-fno-omit-frame-pointer"] if os.environ.get("LEETCODE_CPP_SANITIZERS") else ["-O2"]
        run(["g++","-std=c++20",*flags,"main.cpp","-o","reference"])
        run(compiler_command()+["-encoding","UTF-8","Main.java"])
        reference=[json.loads(line) for line in run([str(work/"reference")]).splitlines()]
        actual=[json.loads(line) for line in run(["java","-Xmx512m","-cp",str(work),"Main"]).splitlines()]
    if len(reference)!=len(inputs) or len(actual)!=len(inputs): raise AssertionError(f"#{number}: missing output")
    independent=0
    for index,(args,expected,got) in enumerate(zip(inputs,reference,actual)):
        if expected!=got: raise AssertionError(f"#{number} case {index}: {args!r}; C++={expected!r}, Java={got!r}")
        other=oracle(number,args)
        if other is not None:
            independent+=1
            if got!=other: raise AssertionError(f"#{number} case {index}: {args!r}; oracle={other!r}, Java={got!r}")
    return number,len(inputs),independent


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ids",nargs="+",type=int,default=IDS)
    parser.add_argument("--cases",type=int,default=48)
    parser.add_argument("--jobs",type=int,default=4)
    args=parser.parse_args(); total=independent=0; failures=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1,args.jobs)) as pool:
        futures={pool.submit(run_problem,i,args.cases):i for i in args.ids}
        for future in concurrent.futures.as_completed(futures):
            number=futures[future]
            try:
                _,count,oracles=future.result(); total+=count; independent+=oracles
                print(f"PASS {number}: {count} differential, {oracles} independent",flush=True)
            except Exception as exc:
                failures.append(number); print(f"FAIL {number}: {exc}",flush=True)
    print(f"Java translation regression: {len(args.ids)-len(failures)}/{len(args.ids)} implementations, {total} cases, {independent} independent-oracle checks")
    if failures: raise SystemExit(1)


if __name__=="__main__":
    main()
