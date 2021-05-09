def find_left(arr):
    #  this will contain all the elements to the left of the current element if it is greater than it  
    lstack = [1] #2,3,4,5
    output = [] #0,0, 2,3,0
 # 3,8, 4,2 ,9
    for ind in range(1, len(arr)-1):
        while lstack and arr[lstack[-1]-1] <= arr[ind]:
            # if the new value is greater then pop
            lstack.pop()
        left = lstack[-1] if lstack else 0
        lstack.append(ind+1)
        output.append(left)
    
    return output


def find_right(arr):
    arr_len = len(arr)
    rstack = []
    output = [0]
    for ind in range(1,len(arr)-1):
        while rstack and arr[rstack[-1]-1] <= arr[ind]:
            # if the new value is greater then pop
            rstack.pop()
        right = arr_len - rstack[-1] + 1 if rstack else 0
        rstack.append(ind+1)
        output.append(right)
    return output[::-1]

def solve(arr):
    res = 0

    left = find_left(arr)
    right = find_right(arr[::-1])

    for el in zip(left, right):
        res = max(res, el[0]*el[1])
        
    return res


arr = [5,4,3,4,5]
print(solve(arr))