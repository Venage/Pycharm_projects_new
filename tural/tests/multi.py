import multiprocessing as mp
from multiprocessing import Pool

def xxx(a):
    return a+1

num = 10
a = [2,2,2,2,2,2,2,2,2,2]
b = list(range(1, num+1))




if __name__ == '__main__':
    with mp.Pool(mp.cpu_count() * 3) as p:
        pars = p.map_async(xxx, a)  #, callback=end_)
        print()
        p.close()
        p.join()



