def subset_sums(a, n, b,n1):
  bits=[]
  total1 = 1 << n1
 
  for i1 in range(total1):
      Sum1 = 0
      for j1 in range(n1):
          if ((i1 & (1 << j1)) != 0):
              Sum1 += b[j1]
      bits.append(Sum1)
     

  total = 1 << n
  print(bits)
  for i in range(total):
      Sum = 0
 
      for j in range(n):
          if ((i & (1 << j)) != 0):
           Sum += a[j]
 
      print(Sum, "", end = "")
      for x in range(1,total1):
         if bits[x] == Sum:
            return i,x;




a=list(map(int,input().split()))

b=list(map(int,input().split()))
n = len(a)
n1 = len(b)

a_ind,b_ind = subset_sums(a, n, b, n1);

a_nums=[]
b_nums=[]

for j in range(n):
          if ((a_ind & (1 << j)) != 0):
           a_nums.append(a[j])

for j in range(n1):
          if ((b_ind & (1 << j)) != 0):
           b_nums.append(b[j])

print(a_nums)
print(b_nums)
