x=input("Stop after: ")
number=int(x)
for number in range(1, 9):
  if number == 3:
    continue
  if number > 9:
    break
  print(number)
print("done")
