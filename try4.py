import math

table = []

for i in range(8):
    part = []
    for y in range(8):
        part.append((i * 7) + i + y)
    table.append(part)

table2 = []

for i in range(8):
    p = []
    for part in table:
        p.append(part[i])
    table2.append(p)

table3 = []

for i in range(15):
    p = []
    r = range(i + 1)
    y = 0
    t = i
    if i >= 8:
        r = range(i - (2 * (i - 8)) - 1)
        t = i - (2 * (i - 8)) - 1
    for x in r:
        xM = x
        minus = t - y
        if i >= 8:
            xM = x + 1 + i - 8
            minus = (t - y) + (1 * (i - 8))
        p.append(table[minus][-1 - xM])
        y += 1
    table3.append(p)

table3.pop(0)
table3.pop(-1)

table4 = []

for i in range(15):
    p = []
    r = range(i + 1)
    y = 0
    t = i
    if i >= 8:
        r = range(i - (2 * (i - 8)) - 1)
        t = i - (2 * (i - 8)) - 1
    for x in r:
        xM = x
        minus = t - y
        if i >= 8:
            xM = x + 1 + i - 8
            minus = (t - y) + (1 * (i - 8))
        p.append(table[minus][xM])
        y += 1
    table4.append(p)

table4.pop(0)
table4.pop(-1)

table5 = []

for line in table:
    for l in line:
        indexL = ((l / 8) - math.floor(l / 8))*8
        listB = [l - 6, l + 6, l - 10, l + 10, l - 15, l + 15, l - 17, l + 17]

        for b in listB.copy():
            indexB = ((b / 8) - math.floor(b/8))*8

            if b < 0:
                listB.remove(b)
            elif b > 63:
                listB.remove(b)
            elif indexB > indexL + 2:
                listB.remove(b)
            elif indexB < indexL - 2:
                listB.remove(b)

        table5.append(listB)


tables = [table, table2, table3, table4, table5]


for i in table:
    print(i)

for i in table2:
    print(i)

for i in table3:
    print(i)

for i in table4:
    print(i)

for i in table5:
    print(i)
