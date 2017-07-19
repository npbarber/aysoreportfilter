#!/usr/bin/python

import argparse

# process volunteer certs report from eayso
# process player certs report from eayso

def parse_args():
    parser = argparse.ArgumentParser(description='ayso reporter')
    parser.add_argument('-m', help='master file', required=True)
    parser.add_argument('-f', help='names to filter on', required=True)
    parser.add_argument('--type', help='vol or player', required=True)
    return parser.parse_args()


def get_file_handle(filename):
    return open(filename)


def read_file(filename):
    with open(filename) as fh:
        data = [l.lower().strip() for l in fh.readlines()]
    return data


def get_next_line(file_handle):
    for line in file_handle:
        line = line.strip('"\r\n')
        line = line.strip('\r\n')
        yield line.split('","')


class VolunteerProcessor(object):

    def __call__(self, file_handle, filter_names):
        res = []

        for l in get_next_line(file_handle):
            details = {
                'div': l[1],
                'id': l[18],
                'fname': l[4],
                'lname': l[5],
                'email': l[11],
                'cell': l[13],
                'bg_status': l[15],
                'verify_status': l[16],
            }
            name = '%s %s' % (l[4], l[5])
            if name.lower() not in filter_names:
                continue
            res.append('%(div)s\t%(id)s\t%(fname)s\t%(lname)s\t%(email)s\t%(cell)s\t%(bg_status)s\t%(verify_status)s' % details)
        return res


class PlayerProcessor(object):

    def __init__(self):
        pass

    def __call__(self, file_handle, filter_names):
        res = []

        for l in get_next_line(file_handle):
            try:
                fname = l[4]
                lname = l[5]
                name = '%s %s' % (fname, lname)
                details = {
                    'id': l[23],
                    'fname': fname,
                    'lname': lname,
                    'home': l[13],
                    'email': l[11],
                    'prim_fname': l[2],
                    'prim_lname': l[3],
                }
            except IndexError:
                continue
            if name.lower() not in filter_names:
                continue
            res.append(
                    '%(id)s\t%(fname)s\t%(lname)s\t%(home)s\t%(email)s\t'
                    '%(prim_fname)s\t%(prim_lname)s' % details)
        return res


def get_processor(type):
    return {
        'vol': VolunteerProcessor,
        'player': PlayerProcessor
    }.get(type)


def output(results):
    for r in results:
        print r

def main():
    args = parse_args()
    master_handle = get_file_handle(args.m)
    filter_names = read_file(args.f)
    processor = get_processor(args.type)()
    results = processor(master_handle, filter_names)
    output(results)

if __name__ == '__main__':
    main()
