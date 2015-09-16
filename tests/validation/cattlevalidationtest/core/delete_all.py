#!/usr/bin/env python

import cattle
DEFAULT_TIMEOUT = 45


def main():
    client = cattle.from_env()
    print format(client)
    env = client.list_environment()
    print format(env)
    delete_all(client, [env])

def delete_all(client, items):
    wait_for = []
    for i in items:
        client.delete(i)
        wait_for.append(client.reload(i))
    wait_all_success(client, items, timeout=180)


def wait_all_success(client, items, timeout=DEFAULT_TIMEOUT):
    result = []
    for item in items:
        item = client.wait_success(item, timeout=timeout)
        result.append(item)

    return result


if __name__ == '__main__':
    main()


# l = client.list_container(removed_null=True)
# print format(l)
# while l is not None:
#     for c in l:
#         print format(c)
#         try:
#             if c.state == 'stopped':
#                 print 'Deleting', c.id
#                 client.delete(c)
#             else:
#                 print 'Stopping', c.id
#                 c.stop(remove=True)
#         except:
#             pass
#
#     try:
#         l = l.next()
#     except:
#         l = None
