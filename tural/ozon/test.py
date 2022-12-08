import multiprocessing as mp


products = [5,10]

def data_parsing(a, yyy):
    print(a+yyy)

p = mp.Pool(processes=10)

def pars_mult(product,yyy):
    data_parsing(product, yyy)


xxx = [4,5]
p.map(pars_mult, args=(products,[i for i in range(len(xxx))]))