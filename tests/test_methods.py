'''
# instantiate test
print(sep='\n', *attr_names.items())
pprint(attr_names)
# method generating test
print(
    print.values,
    print.red.values,
    print.red.bgcyan.values,
    sep='\n')
# print function running test
print(' ', sep=' - ', *range(10))
print.red(' ', sep=' - ', *range(10))
print.red.bgcyan(' ', sep=' - ', *range(10))

rec = []; rec.append(rec)
obj = ([0,1,{2:"3 33 333",4:{5, lambda:0}}],rec)
print.reverse(obj)
pprint.reverse(obj, indent=3, width=1)

# exception test
print.kkk
'''
