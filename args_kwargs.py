list_ = ['one', 'two', 'three', 'four', 'five']
dic_ = {1:'one', 2:'two', 3:'three', 4:'four', 5:'five'}

def test(a, b, *args, **kwargs):
    print(a, b, *args, **kwargs)

test(1, 2, list_, dic_)