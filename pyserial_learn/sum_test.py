# coding=utf8
# 列出列表内，和等于sum，的元素的组合
# 每个元素可重复使用，组合使用的元素个数不限
# 例a=[1,3,5],sum=10 result=[[1*10],[5*2],[3*m,5*n,1*k]]

# 分析
# a0,a1,,,an的使用个数N0,N1,,Ni,,Nn<=sum/ai
# sum_result = 0
# sum_i = 0
# sum_j = 0
# sum_k = 0

# sum = 10  # 目标和
# a = [ 1, 3, 5]  # 元素
# N = [10, 3, 2]  # 每个元素使用的最多个数
# for i in range(10+1):
#     # print "i:", i
#     if i*1 > 10:
#         break
#     for j in range(3+1):
#         # print "j:", j
#         for k in range(2+1):
#             # print "k:", k
#             if i*1+j*3+k*5 == sum:
#                 print "result", i, j, k  # 打印每个元素使用的个数

sum_result = 0
sum_i = 0
sum_j = 0
sum_k = 0

sum = 10  # 目标和
a = [1, 3, 5]  # 元素
N = []  # 每个元素被使用的最大个数
num = []  # 每个元素被使用的个数
for ai in a:
    N.append(sum/ai)

print N

for i in a:
    line_num = a.index(i)
    for j in range(N[line_num]+1):
        print j