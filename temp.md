## 0.bitcount

Bug detail: 在運算消除n中的1時，應該用and運算卻用成xor，造成原本應該能消掉1的步驟變成n只能保持不變，導致while迴圈無限循環

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def bitcount(n):
    count = 0
    while n:
        n ^= n - 1 # The bug is here
        count += 1
    return count
```

## 1.breadth_first_search

Bug detail: 在while迴圈的判斷式中，應該使用while queue讓佇列數量為0時脫離迴圈卻錯用為while True，導致迴圈無限循環無法停止

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
from collections import deque as Queue

def breadth_first_search(startnode, goalnode):
    queue = Queue()
    queue.append(startnode)

    nodesseen = set()
    nodesseen.add(startnode)

    while True: # The bug is here
        node = queue.popleft()

        if node is goalnode:
            return True
        else:
            queue.extend(node for node in node.successors if node not in nodesseen)
            nodesseen.update(node.successors)

    return False
```

## 2.bucketsort

Bug detail: 在for迴圈中把遍歷的目標誤用為原本的陣列arr，而非標記陣列中元素數量的count，然而不可能構造一個跟count一樣的arr，導致全部出錯

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def bucketsort(arr, k):
    counts = [0] * k
    for x in arr:
        counts[x] += 1

    sorted_arr = []
    for i, count in enumerate(arr): # The bug is here
        sorted_arr.extend([i] * count)

    return sorted_arr
```

## 3.depth_first_search

Bug detail: 在向深處搜尋時，沒有紀錄已經造訪過的節點，導致除馬上找到goalnode以外的狀況遞迴都無法停止

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def depth_first_search(startnode, goalnode):
    nodesvisited = set()

    def search_from(node):
        if node in nodesvisited:
            return False
        elif node is goalnode:
            return True
        else:
            return any( # The bug is here
                search_from(nextnode) for nextnode in node.successors
            )

    return search_from(startnode)
```

## 4.detect_cycle

Bug detail: 在判斷終止情況時，沒有處理hare也是空值的狀況，只有處理hare的後繼是空值的狀況，導致hare剛好是空值時會觸發AttributeError

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def detect_cycle(node):
    hare = tortoise = node

    while True:
        if hare.successor is None: # The bug is here
            return False

        tortoise = tortoise.successor
        hare = hare.successor.successor

        if hare is tortoise:
            return True
```

## 5.find_first_in_sorted

Bug detail: 在whlie判斷式中，錯誤考慮了lo==hi的狀況，導致如目標不在陣列中的情況會無窮迴圈

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def find_first_in_sorted(arr, x):
    lo = 0
    hi = len(arr)

    while lo <= hi: # The bug is here
        mid = (lo + hi) // 2

        if x == arr[mid] and (mid == 0 or x != arr[mid - 1]):
            return mid

        elif x <= arr[mid]:
            hi = mid

        else:
            lo = mid + 1

    return -1
```

## 6.find_in_sorted

Bug detail: 在目標大於中點時，新陣列起始序號mid沒有+1，導致邊緣情況遞迴不會停止

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def find_in_sorted(arr, x):
    def binsearch(start, end):
        if start == end:
            return -1
        mid = start + (end - start) // 2
        if x < arr[mid]:
            return binsearch(start, mid)
        elif x > arr[mid]:
            return binsearch(mid, end) # The bug is here
        else:
            return mid

    return binsearch(0, len(arr))
```

## 7.flatten

Bug detail: 在遞回的終止條件回傳時，對於不是list的輸入依舊使用遞迴，導致大部分輸出不是預期的格式

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def flatten(arr):
    for x in arr:
        if isinstance(x, list):
            for y in flatten(x):
                yield y
        else:
            yield flatten(x) # The bug is here
```

## 8.gcd

Bug detail: 在遞迴呼叫時，沒有交換數字的位置，使得b的位置始終保持不變，導致除b=0外的情況外遞迴不會停止

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(a % b, b) # The bug is here
```

## 9.get_factors

Bug detail: 在輸入是質數時僅回傳空陣列而非包含數字本身的陣列，造成輸出總是少了最後一個數，導致質數的分解出錯且遞迴的影響除1以外的所有輸入

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def get_factors(n):
    if n == 1:
        return []

    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return [i] + get_factors(n // i)

    return [] # The bug is here
```

## 10.hanoi

Bug detail: 在步驟二中的交換把end寫成helper，使func無法交換到最後目標上，導致height=0之外的情況只能給出錯誤答案

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def hanoi(height, start=1, end=3):
    steps = []
    if height > 0:
        helper = ({1, 2, 3} - {start} - {end}).pop()
        steps.extend(hanoi(height - 1, start, helper))
        steps.append((start, helper)) # The bug is here
        steps.extend(hanoi(height - 1, helper, end))

    return steps
```

## 11.is_valid_parenthesization

Bug detail: 在遍歷完字串後直接回傳True而沒有考慮到depth大於1時仍非合法的狀況，造成輸出偏向true，導致最後depth大於1的輸入皆會出錯

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def is_valid_parenthesization(parens):
    depth = 0
    for paren in parens:
        if paren == '(':
            depth += 1
        else:
            depth -= 1
            if depth < 0:
                return False

    return True # The bug is here
```

## 12.kheapsort

Bug detail: 在遍歷陣列時沒有排除已經在heap中的元素，造成輸出比輸入多出3個元素且排序失效，導致除了k為0以外的輸入皆會產生錯誤

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def kheapsort(arr, k):
    import heapq

    heap = arr[:k]
    heapq.heapify(heap)

    for x in arr: # The bug is here
        yield heapq.heappushpop(heap, x)

    while heap:
        yield heapq.heappop(heap)
```

## 13.knapsack

Bug detail: 在寫動態規劃的陣列時，沒有考慮到weight剛好等於容納上限的狀況，造成輸出比預期小一點，導致輸出內有機會觸發該類邊緣狀況時輸出錯誤答案

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def knapsack(capacity, items):
    from collections import defaultdict
    memo = defaultdict(int)

    for i in range(1, len(items) + 1):
        weight, value = items[i - 1]

        for j in range(1, capacity + 1):
            memo[i, j] = memo[i - 1, j]

            if weight < j: # The bug is here
                memo[i, j] = max(
                    memo[i, j],
                    value + memo[i - 1, j - weight]
                )

    return memo[len(items), capacity]
```

## 14.kth

Bug detail: 在處理到k存在於大於pivot的陣列above時，遞迴呼叫沒有將k的輸入根據num_lessoreq重置，導致在該類狀況中k總是代表超過陣列的位置觸發IndexError

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def kth(arr, k):
    pivot = arr[0]
    below = [x for x in arr if x < pivot]
    above = [x for x in arr if x > pivot]

    num_less = len(below)
    num_lessoreq = len(arr) - len(above)

    if k < num_less:
        return kth(below, k)
    elif k >= num_lessoreq:
        return kth(above, k) # The bug is here
    else:
        return pivot
```

## 15.lcs_length

Bug detail: 在動態規劃陣列計算中，子問題的選擇時j沒有減一，造成動態規劃只會在一個維度中取值，導致除了答案小於1以外的輸入皆會出錯

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def lcs_length(s, t):
    from collections import Counter

    dp = Counter()

    for i in range(len(s)):
        for j in range(len(t)):
            if s[i] == t[j]:
                dp[i, j] = dp[i - 1, j] + 1 # The bug is here

    return max(dp.values()) if dp else 0
```

## 16.levenshtein

Bug detail: 在兩個字串首字相同的情況下，在遞迴式前錯誤的+1，由於兩字一致所以對於結果的影響應該是0而非1，導致除空字串以外的輸入皆會出錯

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def levenshtein(source, target):
    if source == '' or target == '':
        return len(source) or len(target)

    elif source[0] == target[0]:
        return 1 + levenshtein(source[1:], target[1:]) # The bug is here

    else:
        return 1 + min(
            levenshtein(source,     target[1:]),
            levenshtein(source[1:], target[1:]),
            levenshtein(source[1:], target)
        )
```

## 17.lis

Bug detail: 在更改longest變數時，缺少了max函數判斷新數值是否比原本長，導致在初期就找到答案的情況會在後期被更新為錯誤答案

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def lis(arr):
    ends = {}
    longest = 0

    for i, val in enumerate(arr):

        prefix_lengths = [j for j in range(1, longest + 1) if arr[ends[j]] < val]

        length = max(prefix_lengths) if prefix_lengths else 0

        if length == longest or val < arr[ends[length + 1]]:
            ends[length + 1] = i
            longest = length + 1 # The bug is here

    return longest
```

## 18.longest_common_subsequence

Bug detail: 在兩字串首字一致呼叫遞迴式的情況下，字串b沒有移除首字便直接輸入，導致不斷重複比較輸出錯誤答案

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def longest_common_subsequence(a, b):
    if not a or not b:
        return ''

    elif a[0] == b[0]:
        return a[0] + longest_common_subsequence(a[1:], b) # The bug is here

    else:
        return max(
            longest_common_subsequence(a, b[1:]),
            longest_common_subsequence(a[1:], b),
            key=len
        )
```

## 19.max_sublist_sum

Bug detail: 在更改max_ending_here時，沒有加上max函數，造成計算總是考慮到整個list而沒有歸零機制，導致只能處理答案是整個list相加或sublist在前期出現的狀況

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def max_sublist_sum(arr):
    max_ending_here = 0
    max_so_far = 0

    for x in arr:
        max_ending_here = max_ending_here + x # The bug is here
        max_so_far = max(max_so_far, max_ending_here)

    return max_so_far
```

## 20.mergesort

Bug detail: 在遞迴的終止狀況判斷中，沒有考慮到只有一個元素時也無法切為左右兩個陣列，導致遞迴無法停止

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def mergesort(arr):
    def merge(left, right):
        result = []
        i = 0
        j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:] or right[j:])
        return result

    if len(arr) == 0: # The bug is here
        return arr
    else:
        middle = len(arr) // 2
        left = mergesort(arr[:middle])
        right = mergesort(arr[middle:])
        return merge(left, right)
```

## 21.minimum_spanning_tree

Bug detail: 在更新group_by_node變數時，誤用update函數在for loop中更新set引發RuntimeError，導致幾乎所有輸入都無法運行

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def minimum_spanning_tree(weight_by_edge):
    group_by_node = {}
    mst_edges = set()

    for edge in sorted(weight_by_edge, key=weight_by_edge.__getitem__):
        u, v = edge
        if group_by_node.setdefault(u, {u}) != group_by_node.setdefault(v, {v}):
            mst_edges.add(edge)
            group_by_node[u].update(group_by_node[v])
            for node in group_by_node[v]:
                group_by_node[node].update(group_by_node[u]) # The bug is here

    return mst_edges
```

## 22.next_palindrome

Bug detail: 在如999這類需要進位的輸入而進入最後一個進位處理邏輯時，沒有將原始位數-1造成回傳結果多一位，導致類似邊緣情況的輸入無法獲得正確輸出

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def next_palindrome(digit_list):
    high_mid = len(digit_list) // 2
    low_mid = (len(digit_list) - 1) // 2
    while high_mid < len(digit_list) and low_mid >= 0:
        if digit_list[high_mid] == 9:
            digit_list[high_mid] = 0
            digit_list[low_mid] = 0
            high_mid += 1
            low_mid -= 1
        else:
            digit_list[high_mid] += 1
            if low_mid != high_mid:
                digit_list[low_mid] += 1
            return digit_list
    return [1] + (len(digit_list)) * [0] + [1] # The bug is here
```

## 23.next_permutation

Bug detail: 在檢查首元素要置換為哪個元素時，將首元素索引i和比較元素索引j錯誤的置換，導致所有輸出都是錯誤或直接輸出空值

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def next_permutation(perm):
    for i in range(len(perm) - 2, -1, -1):
        if perm[i] < perm[i + 1]:
            for j in range(len(perm) - 1, i, -1):
                if perm[j] < perm[i]: # The bug is here
                    next_perm = list(perm)
                    next_perm[i], next_perm[j] = perm[j], perm[i]
                    next_perm[i + 1:] = reversed(next_perm[i + 1:])
                    return next_perm
```

## 24.pascal

Bug detail: 在控制三角形底邊數量的for loop參數時，缺少將r+1造成底邊長度少一，導致輸出的三角形或者缺少最後一排或者訪問前一排最後元素時觸發IndexError

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def pascal(n):
    rows = [[1]]
    for r in range(1, n):
        row = []
        for c in range(0, r): # The bug is here
            upleft = rows[r - 1][c - 1] if c > 0 else 0
            upright = rows[r - 1][c] if c < r else 0
            row.append(upleft + upright)
        rows.append(row)

    return rows
```

## 25.possible_change

Bug detail: 在處理邊界狀況時，缺少處理硬幣沒有輸入的邊界狀況，導致沒有輸入硬幣種類時由於無法unpack coins變數觸發ValueError

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def possible_change(coins, total):
    if total == 0:
        return 1
    if total < 0: # The bug is here
        return 0

    first, *rest = coins
    return possible_change(coins, total - first) + possible_change(rest, total)
```

## 26.powerset

Bug detail: 在遞迴的回傳值中沒有把rest_subsets也加入，造成每次遞迴都不存在空集合，導致所有輸出都只會輸出輸入陣列本身所以都是錯誤的

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def powerset(arr):
    if arr:
        first, *rest = arr 
        rest_subsets = powerset(rest)
        return [[first] + subset for subset in rest_subsets] # The bug is here
    else:
        return [[]]
```

## 27.quicksort

Bug detail: 在建立比pivot大的元素組成的陣列時，沒有將和pivot相等的元素包含進去，導致在排序有和pivot相等元素的陣列時會缺少這些元素

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def quicksort(arr):
    if not arr:
        return []

    pivot = arr[0]
    lesser = quicksort([x for x in arr[1:] if x < pivot])
    greater = quicksort([x for x in arr[1:] if x > pivot]) # The bug is here
    return lesser + [pivot] + greater
```

## 28.reverse_linked_list

Bug detail: 在置換node的successor時，沒有將node賦值給prevnode，造成prevnode一直是空值且所有node的新successor都是空值，導致除了輸入空值外的所有情況都會錯誤

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def reverse_linked_list(node):
    prevnode = None
    while node:
        nextnode = node.successor
        node.successor = prevnode
        node = nextnode # The bug is here
    return prevnode
```

## 29.rpn_eval

Bug detail: 在運算並放回stack時，忽略了stack中第一個pop的元素是擺在運算式後的元素，導致運算不符合交換律的輸入時皆會錯誤

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def rpn_eval(tokens):
    def op(symbol, a, b):
        return {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b
        }[symbol](a, b)

    stack = []

    for token in tokens:
        if isinstance(token, float):
            stack.append(token)
        else:
            a = stack.pop()
            b = stack.pop()
            stack.append(
                op(token, a, b) # The bug is here
            )

    return stack.pop()
```

## 30.shortest_path_length

Bug detail: 在動態規劃更新節點距離時，沒有加上起點到前一節點的距離，導致除了起點終點相同和起點終點不可達等特殊情況以外的輸入都無法獲得正確結果

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
from heapq import *

def shortest_path_length(length_by_edge, startnode, goalnode):
    unvisited_nodes = [] 
    heappush(unvisited_nodes, (0, startnode))
    visited_nodes = set()

    while len(unvisited_nodes) > 0:
        distance, node = heappop(unvisited_nodes)
        if node is goalnode:
            return distance

        visited_nodes.add(node)

        for nextnode in node.successors:
            if nextnode in visited_nodes:
                continue

            insert_or_update(unvisited_nodes,
                (min(
                    get(unvisited_nodes, nextnode) or float('inf'),
                    get(unvisited_nodes, nextnode) + length_by_edge[node, nextnode] # The bug is here
                ),
                nextnode)
            )

    return float('inf')


def get(node_heap, wanted_node):
    for dist, node in node_heap:
        if node == wanted_node:
            return dist
    return 0

def insert_or_update(node_heap, dist_node):
    dist, node = dist_node
    for i, tpl in enumerate(node_heap):
        a, b = tpl
        if b == node:
            node_heap[i] = dist_node 
            return None

    heappush(node_heap, dist_node)
    return None
```

## 31.shortest_path_lengths

Bug detail: 在計算以k為中繼連結ij的距離時，將i到k、k到j誤寫為i到k、j到k，導致非無向圖結構的輸入結果皆會出錯

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
from collections import defaultdict

def shortest_path_lengths(n, length_by_edge):
    length_by_path = defaultdict(lambda: float('inf'))
    length_by_path.update({(i, i): 0 for i in range(n)})
    length_by_path.update(length_by_edge)

    for k in range(n):
        for i in range(n):
            for j in range(n):
                length_by_path[i, j] = min(
                    length_by_path[i, j],
                    length_by_path[i, k] + length_by_path[j, k] # The bug is here
                )

    return length_by_path
```

## 32.shortest_paths

Bug detail: 在動態規劃weight_by_node變數時，誤寫為weight_by_edge，造成最後回傳的結果跟初始化的一樣，導致除了所有節點都無法到達以外的情況皆輸出錯誤

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def shortest_paths(source, weight_by_edge):
    weight_by_node = {
        v: float('inf') for u, v in weight_by_edge
    }
    weight_by_node[source] = 0

    for i in range(len(weight_by_node) - 1):
        for (u, v), weight in weight_by_edge.items():
            weight_by_edge[u, v] = min( # The bug is here
                weight_by_node[u] + weight,
                weight_by_node[v]
            )

    return weight_by_node
```

## 33.shunting_yard

Bug detail: 在處理到運算符的時候沒有將運算符放進opstack中，造成rpntokens沒有任何運算符，導致有運算符的輸入皆會出錯

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def shunting_yard(tokens):
    precedence = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2
    }

    rpntokens = []
    opstack = []
    for token in tokens:
        if isinstance(token, int):
            rpntokens.append(token)
        else:
            while opstack and precedence[token] <= precedence[opstack[-1]]:
                rpntokens.append(opstack.pop())
 # The bug is here
    while opstack:
        rpntokens.append(opstack.pop())

    return rpntokens
```

## 34.sieve

Bug detail: 在判斷n是否不被所有質數整除時，寫成了是否存在質數不能整除n，由於始終不存在質數用於判斷，導致除了max=1以外的狀況全部出錯

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def sieve(max):
    primes = []
    for n in range(2, max + 1):
        if any(n % p > 0 for p in primes): # The bug is here
            primes.append(n)
    return primes
```

## 35.sqrt

Bug detail: 在誤差計算時，忘記把approx平方，造成誤差計算的是x跟根號x的差，導致除了x=1或epsilon很大的情況外計算都不會停下

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def sqrt(x, epsilon):
    approx = x / 2
    while abs(x - approx) > epsilon: # The bug is here
        approx = 0.5 * (approx + x / approx)
    return approx
```

## 36.subsequences

Bug detail: 在處理k=0時的回傳時，缺少包含一個空陣列，造成遞迴的最後一層長度為0並且淺層呼叫也都為0，導致除了k非零且a>b的情況外的輸入皆會出錯

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def subsequences(a, b, k):
    if k == 0:
        return [] # The bug is here

    ret = []
    for i in range(a, b + 1 - k):
        ret.extend(
            [i] + rest for rest in subsequences(i + 1, b, k - 1)
        )

    return ret
```

## 37.to_base

Bug detail: 在結果計算時，先計算出的是低位的結果，但是字串拼接時錯置了result跟新位的位置，造成得到的結果都是相反的，導致除迴文數外的結果都是錯誤的

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
import string
def to_base(num, b):
    result = ''
    alphabet = string.digits + string.ascii_uppercase
    while num > 0:
        i = num % b
        num = num // b
        result = result + alphabet[i] # The bug is here
    return result
```

## 38.topological_ordering

Bug detail: 在判斷節點能否排進ordered_nodes時，把incoming寫成outgoing，造成除了沒有incoming節點的初始節點外沒有節點能被排序進來，導致輸入有邊圖皆會出錯

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def topological_ordering(nodes):
    ordered_nodes = [node for node in nodes if not node.incoming_nodes]

    for node in ordered_nodes:
        for nextnode in node.outgoing_nodes:
            if set(ordered_nodes).issuperset(nextnode.outgoing_nodes) and nextnode not in ordered_nodes: # The bug is here
                ordered_nodes.append(nextnode)

    return ordered_nodes
```

## 39.wrap

Bug detail: 在回傳前缺少append text，造成回傳結果缺少最後一段，導致空值以外的輸入結果皆會出錯

### Prompt
Fix the bug in the following code. The bug is on the line commented below:
```python=
def wrap(text, cols):
    lines = []
    while len(text) > cols:
        end = text.rfind(' ', 0, cols + 1)
        if end == -1:
            end = cols
        line, text = text[:end], text[end:]
        lines.append(line)
 # The bug is here
    return lines
```

