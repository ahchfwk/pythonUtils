'''created by fwk
   2018/01/04
   to transform ccfinder prep file to an uniform style for simhash 
'''

def handle(filepath):
    f = open(filepath,'r')
    r = f.readlines()
    r = [x.split()[2] for x in r]
    result = open('handle.txt','w')
    count = 0
    for i in r:
        if i.startswith('(brace'):
            result.write('{')
        elif i.startswith(')brace'):
            result.write('}')
        elif i.startswith('(paren'):
            result.write('(')
        elif i.startswith(')paren'):
            result.write(')')
        elif i.startswith('(def_block'):
            result.write('start_block')
        elif i.startswith(')def_block'):
            result.write('end_block')
            result.write('\n')
        elif i.startswith('id'):
            if r[count-1] == 'r_class':
                result.write('class_name')
            elif r[count+1] == 'c_func':
                result.write('func_name')
            elif i.count('&'):
                result.write(i[3:].split('&')[0])
            else:
                result.write('id')
        elif i.startswith('suffix'):
            result.write(';')
        elif i.startswith('dot'):
            result.write('.')
        elif i.startswith('comma'):
            result.write(',')
        elif i.startswith('c_func'):
            pass
        elif i.startswith('r_class'):
            result.write('class')
        elif i.startswith('l_'):
            result.write(i[2:].split('|')[0]+'_text')
        elif i[1] == '_':
            result.write(i[2:])
        else:
            result.write(i)
        result.write(' ')
        count += 1


if __name__ == '__main__':
    handle('BucketAssigner.java.java.2_0_0_0.default.ccfxprep')
