"""Download flags of top 20 countries by population

ThreadPoolExecutor version

Sample run::

    $ python3 flags_threadpool.py
    BD retrieved.
    EG retrieved.
    CN retrieved.
    ...
    PH retrieved.
    US retrieved.
    IR retrieved.
    20 flags downloaded in 0.93s

"""
# BEGIN FLAGS_THREADPOOL
from concurrent import futures
import sys
from flags import save_flag, get_flag, show, main  # <1>

MAX_WORKERS = 20  # <2>


def download_one(cc,name):  # <3>
    image = get_flag(cc)
    show(cc)
    print(name,end=' ') # 只是为了显示传参数
    sys.stdout.flush()
    save_flag(image, cc.lower() + '.gif')

    return cc


def download_many(cc_list):
    workers = min(MAX_WORKERS, len(cc_list))  # <4>
    with futures.ThreadPoolExecutor(workers) as executor:  # <5>
        res = executor.map(download_one, sorted(cc_list),sorted(cc_list))  # <6>

    # return len(list(res))  # <7>


if __name__ == '__main__':
    main(download_many)  # <8>
# END FLAGS_THREADPOOL
