def format(filepath):
    f = open(filepath, 'r')
    newtext = []
    tem = ''
    for line in f.readlines():
        if len(line) < 2:
            if len(tem) > 2:
                newtext.append(tem)
                tem = ''
            newtext.append(line)
        else:
            tem = tem.strip() +' '+ line

    f.close()

    f = file('uuu2.txt', 'w')
    f.writelines(newtext)
    f.close()

if __name__ == '__main__':
    format('ui2code.pdf.txt')