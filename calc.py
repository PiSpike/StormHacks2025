print("Enter Equation")
equation = input()
nums = []
ops = []
prev = 0
for i in range(len(equation)):
    if (equation[i].isnumeric()) == False:
        nums.append(equation[prev:i])
        ops.append(equation[i])
        prev = i+1

while "*" in ops or "/" in ops:
    for i in range(len(ops)):
        # print(len(ops))
        # print("i = " + str(i))

        if ops[i] == '*':
            nums[i] = float(nums[i]) * float(nums[i+1])
            ops.pop(i)
            nums.pop(i+1)
            break
        if ops[i] == '/':
            nums[i] = float(nums[i]) / float(nums[i+1])
            ops.pop(i)
            nums.pop(i+1)
            break
        # print(nums)
        # print(ops)

        
while "+" in ops or "-" in ops:
    for i in range(len(ops)):
        # print(len(ops))
        # print("i = :" + str(i))

        if ops[i] == '+':
            nums[i] = float(nums[i]) + float(nums[i+1])
            ops.pop(i)
            nums.pop(i+1)
            break
        if ops[i] == '-':
            nums[i] = float(nums[i]) - float(nums[i+1])
            ops.pop(i)
            nums.pop(i+1)
            break
        # print(nums)
        
    
print(nums)