import sqlite3
import os
import glob

from tests import filesize

from quaco_settings import DB_NAME, DIR_STRUCTURES

def run_tests(filename):
    total_errors = 0
    total_errors += filesize.run(filename)
    return total_errors


def inspect_file(filename):
    con = sqlite3.connect(DB_NAME)
    with con:
        cur = con.cursor()
        cur.execute("select * from FileHist where name='{0}'".format(filename,))
        result = cur.fetchone()
        if result:        
            #file already verified
            pass
        else:
            err = run_tests(filename)
            cur.execute("insert into FileHist(name, err) values ('{0}',{1})".format(filename, str(err)))
        return


def repo_crawler():
    return glob.glob(DIR_STRUCTURES['exp_root']) 
    #return glob.glob(DIR_STRUCTURES['exp_root']) + glob.glob(DIR_STRUCTURES['cmp_root'])


def exp_crawler():
    exps = repo_crawler()
    for exp in exps:
        ocean = glob.glob(os.path.join(exp, DIR_STRUCTURES['exp_ocean']))
        atmos = glob.glob(os.path.join(exp, DIR_STRUCTURES['exp_atmos']))
        for oc in ocean:
            inspect_file(oc)
        for at in atmos:
            inspect_file(at)
        


if __name__ == "__main__":
    print "running inspector"
    exp_crawler()

