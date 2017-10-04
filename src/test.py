candidate = 0
count = 0
for value in []:
  if count == 0:
    candidate = value
  if candidate == value:
    count += 1
  else:
    count -= 1

print(candidate)