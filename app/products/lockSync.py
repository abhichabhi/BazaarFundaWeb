from multiprocessing.pool import ThreadPool
pool = ThreadPool(processes=1)
def getProductIdResults(func, productID ):
    async_result = pool.apply_async(func, args = (productID,)) # tuple of args for foo
    return async_result.get()