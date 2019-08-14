ofn = "cities1.txt"
outfile = open(ofn,'a+', encoding='utf-8')
with open('cities.txt', 'r', encoding='utf-8') as f:
    city_list = f.readlines()
    lines = []
    for eachline in city_list:
        lines_list = list(filter(lambda ch: ch not in '\t\n0123456789', eachline))
        line = ''.join(lines_list)
        lines.append(line)
lines_str = '\n'.join(lines)
outfile.write(lines_str)
outfile.close()