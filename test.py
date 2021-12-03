time = ' 33m 24s '
kok = time.split()
minutes = int(''.join(filter(str.isdigit, kok[0])))
seconds = int(''.join(filter(str.isdigit, kok[1])))
time = minutes*60+seconds
print(time)