import sqlite3
import os
import glob

from tests import loading, filesize, minvalue
from tests.errorcodes import LOADERR

from quaco_settings import DB_NAME, DIR_STRUCTURES, EXCLUSION_LIST

def run_tests(filename):
    total_errors = 0
    load_result, data = loading.run(filename)
    if load_result == LOADERR:
        # won't go ahead
        return load_result
    total_errors += filesize.run(filename)
    total_errors += minvalue.run(data)
    return total_errors


def inspect_files(filelist):
    con = sqlite3.connect(DB_NAME)
    with con:
        cur = con.cursor()
        i = 0
        for filename in filelist:
            cur.execute("select * from FileHist where name='{0}'".format(filename,))
            result = cur.fetchone()
            log = open('log.txt', 'a')
            if result:
                log.write("skipped" + filename + "\n")
            else:
                err = run_tests(filename)
                if err:
                    log.write("reproved" + filename + "\n")
                else:
                    log.write("approved" + filename + "\n")
                cur.execute("insert into FileHist(name, err, ack) values ('{0}',{1}, 0)".format(filename, str(err)))
            con.commit()
            log.close()
    print "finished exp"


def repo_crawler():
    return glob.glob(DIR_STRUCTURES['exp_root']) + glob.glob(DIR_STRUCTURES['cmp_root'])


def exp_crawler():
    exps = repo_crawler()
    for exp in exps:
        print "verifying", exp
        abort = False
        for exc in EXCLUSION_LIST:
            if exc in exp:
                print "aborting, excluded exp"
                abort = True
        if not abort:
            ocean = glob.glob(os.path.join(exp, DIR_STRUCTURES['exp_ocean']))
            #atmos = glob.glob(os.path.join(exp, DIR_STRUCTURES['exp_atmos']))
            print "total {0} files".format(len(ocean))
            inspect_files(ocean)
            #inspect_file(atmos)
        


if __name__ == "__main__":
    print "running inspector"
    exp_crawler()

