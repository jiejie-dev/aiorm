import time

from norm.query.query_base import Query
from norm.query.query_compiler import MySQLQueryCompiler
from sample.norm_bench import DemoUser


def main():
    t1 = time.time()
    for index in range(1000):
        query = Query(DemoUser).select().where(DemoUser.name == 'lujiejie')
        compiler = MySQLQueryCompiler()
        rs = compiler.compile(query)
        assert rs is not None
    t2 = time.time()
    print("{}".format(t2 - t1))


if __name__ == '__main__':
    main()
