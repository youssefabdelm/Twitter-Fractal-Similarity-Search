import twint
import trimeter
import time
import os
import aiohttp
from concurrent.futures._base import TimeoutError
import asyncio
import threading
import csv
from num2words import num2words
from joblib import Parallel, delayed

def getcolumn(column, number):
    return column[number]

def getlistofcolumns(columns, range):
    listofcolumns = []
    for i in range:
        listofcolumns.append(columns[i])
    return listofcolumns

def appendrowstolist(csvfile, range, skipheader=False):
    with open(str(csvfile), 'r') as f:

        csv_reader = csv.reader(f, delimiter=',')
        if skipheader == True:
            next(csv_reader, None)
        csvlist = []
        for row in csv_reader:
            if len(range) == 1:
              csvlist.append(getlistofcolumns(row, range)[0])
            else:
              csvlist.append(getlistofcolumns(row, range))
        return csvlist


def makedatafolder():
    if not os.path.exists('data'):
        os.mkdir('data')




def downloadfollowers_singleuser(user):
    #asyncio.set_event_loop(asyncio.new_event_loop())

    print("Downloading followers for " + str(user))
    x = twint.Config()
    x.Username = str(user.lower())
    x.Store_object = True
    x.Store_csv = True
    x.Resume = "data/" + str(user) + " resume followers.csv"
    #x.Output = str(user) + " followers.csv"
    x.Output = "data/" + str(user) + " followers.csv"
    twint.run.Followers(x)
    while True:
        try:
            twint.run.Followers(x)
            break
        except aiohttp.ClientConnectorError:
            time.sleep(1)
            print('Cant connect to internet. Restarting...')
            #twint.run.Followers(x)
        except aiohttp.ClientOSError:
            time.sleep(1)
            print('Cant connect to internet. Restarting...')
            #twint.run.Followers(x)
        except aiohttp.ServerDisconnectedError:
            time.sleep(1)
            print('Cant connect to internet. Restarting...')
            #twint.run.Followers(x)
        except asyncio.TimeoutError:
            time.sleep(1)
            print('Cant connect to internet. Restarting...')
            #twint.run.Followers(x)
        except concurrent.futures._base.TimeoutError:
            time.sleep(1)
            print('Cant connect to internet. Restarting...')
        except aiohttp.client_exceptions.ClientConnectorError:
            time.sleep(1)
            print('Cant connect to internet. Restarting...')
        except aiohttp.client_exceptions.ServerDisconnectedError:
            time.sleep(1)
            print('Cant connect to internet. Restarting...')


def downloadfollowers(user):
    #asyncio.set_event_loop(asyncio.new_event_loop())

    print("Downloading followers for " + str(user))
    x = twint.Config()
    x.Username = str(user.lower())
    x.Store_object = True
    x.Store_csv = True
    x.Resume = "data/" + str(user) + " resume followers.csv"
    #x.Output = str(user) + " followers.csv"
    x.Output = "data/" + str(user) + " followers.csv"
    twint.run.Followers(x)
    while True:
        try:
            twint.run.Followers(x)
            break
        except aiohttp.ClientConnectorError:
            time.sleep(1)
            print('Cant connect to internet. Restarting...')
            #twint.run.Followers(x)
        except aiohttp.ClientOSError:
            time.sleep(1)
            print('Cant connect to internet. Restarting...')
            #twint.run.Followers(x)
        except aiohttp.ServerDisconnectedError:
            time.sleep(1)
            print('Cant connect to internet. Restarting...')
            #twint.run.Followers(x)
        except asyncio.TimeoutError:
            time.sleep(1)
            print('Cant connect to internet. Restarting...')
            #twint.run.Followers(x)
        except concurrent.futures._base.TimeoutError:
            time.sleep(1)
            print('Cant connect to internet. Restarting...')
        except aiohttp.client_exceptions.ClientConnectorError:
            time.sleep(1)
            print('Cant connect to internet. Restarting...')
        except aiohttp.client_exceptions.ServerDisconnectedError:
            time.sleep(1)
            print('Cant connect to internet. Restarting...')

def downloadfollowingsingleuser(utarget):
    #asyncio.set_event_loop(asyncio.new_event_loop())

    if os.path.exists('data/' + str(utarget) + ' resume following.csv'):
        os.remove('data/' + str(utarget) + ' resume following.csv')
    print("Downloading who " + str(utarget) + " is following")
    y = twint.Config()
    y.Username = str(utarget.lower())
    y.Store_csv = True
    #y.Limit = 30000
    y.Resume = "data/" + str(utarget) + " resume following.csv"

    #y.Output = str(utarget) + " following.csv"
    y.Output = "data/" + str(utarget) + " following.csv"

    while True:
        try:
            twint.run.Following(y)
            break
        except aiohttp.ClientConnectorError:
            time.sleep(1)
            print('Cant connect to internet. Restarting...')
            #twint.run.Followers(x)
        except aiohttp.ClientOSError:
            time.sleep(1)
            print('Cant connect to internet. Restarting...')
            #twint.run.Followers(x)
        except aiohttp.ServerDisconnectedError:
            time.sleep(1)
            print('Cant connect to internet. Restarting...')
            #twint.run.Followers(x)
        except asyncio.TimeoutError:
            time.sleep(1)
            print('Cant connect to internet. Restarting...')
        except KeyboardInterrupt:
            os.remove("data/" + str(utarget) + " following.csv")
            os.remove("data/" + str(utarget) + " resume following.csv")
            raise ValueError("Quit program. Deleted following and resume files for " + str(utarget) + ".")

def makefollowerslistfor(user):
    if not os.path.exists("data/" + str(user) + " followers.csv"):
        downloadfollowers_singleuser(user)
    followerslist = appendrowstolist("data/" + str(user) + " followers.csv", [0], skipheader=True)
    return followerslist

def makefollowinglistfor(user):
    if not os.path.exists("data/" + str(user) + " following.csv"):
        downloadfollowingsingleuser(user)
    followinglist = appendrowstolist("data/" + str(user) + " following.csv", [0], skipheader=True)
    return followinglist


def downloadfollowingforsingleuserparallel(utarget):
    asyncio.set_event_loop(asyncio.new_event_loop())
    if not os.path.exists("data/" + str(utarget) + " following.csv"):

        if os.path.exists('data/' + str(utarget) + ' resume following.csv'):
            os.remove('data/' + str(utarget) + ' resume following.csv')
        print("Downloading who " + str(utarget) + " is following")
        y = twint.Config()
        y.Username = str(utarget.lower())
        y.Store_csv = True
        #y.Limit = 30000
        y.Resume = "data/" + str(utarget) + " resume following.csv"

        #y.Output = str(utarget) + " following.csv"
        y.Output = "data/" + str(utarget) + " following.csv"

        while True:
            try:
                twint.run.Following(y)
                break
            except aiohttp.ClientConnectorError:
                time.sleep(1)
                print('Cant connect to internet. Restarting...')
                #twint.run.Followers(x)
            except aiohttp.ClientOSError:
                time.sleep(1)
                print('Cant connect to internet. Restarting...')
                #twint.run.Followers(x)
            except aiohttp.ServerDisconnectedError:
                time.sleep(1)
                print('Cant connect to internet. Restarting...')
                #twint.run.Followers(x)
            except asyncio.TimeoutError:
                time.sleep(1)
                print('Cant connect to internet. Restarting...')
            except KeyboardInterrupt:
                os.remove("data/" + str(utarget) + " following.csv")
                os.remove("data/" + str(utarget) + " resume following.csv")
                raise ValueError("Quit program. Deleted following and resume files for " + str(utarget) + ".")




def downloadfollowing(users):
    while True:
        if len(users) > 0:
            user_to_be_processed = users.pop()
            threading.Thread(target = downloadfollowingforsingleuserparallel,args=(user_to_be_processed,)).start()

def writetocsv(values, header=None, degree=None, sourceuser=None, targetuser=None):
    if not os.path.exists(str(num2words(degree, to='ordinal').capitalize()) +  ' Degree for ' + str(targetuser) + ' and ' + str(sourceuser) + '.csv'):
        header_added = False
    else:
        header_added = True

    if header == None:
        header = (len(values) * [''])
    if values == None:
        raise ValueError("You might have forgotten to specify what to write in rows or the values are None.")
    with open(str(num2words(degree, to='ordinal').capitalize()) + ' Degree for ' + str(targetuser) + ' and ' + str(sourceuser) + '.csv', mode='a') as csv_writer:
        csv_writer = csv.writer(csv_writer, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if not header_added:
            csv_writer.writerow(header)
        csv_writer.writerow(values)


def followingcount(fcount):

    print("Checking following count for: " + str(fcount))

    users_list = []
    c = twint.Config()
    c.Username = fcount
    c.Store_object = True
    c.Store_object_users_list = users_list

    while True:
        try:
            twint.run.Lookup(c)
            followingnumber = users_list[0].following
            #dictofusersandfollowingcounts.update({fcount:followingnumber})
            return {fcount:followingnumber}
            break
        except aiohttp.ClientConnectorError:
            print('Cant connect to internet. Retrying in 2 seconds...')
            time.sleep(2)
        except aiohttp.ClientOSError:
            print('Cant connect to internet. Retrying in 2 seconds...')

            time.sleep(2)
        except aiohttp.ServerDisconnectedError:
            print('Cant connect to internet. Retrying in 2 seconds...')
            time.sleep(2)
        except asyncio.TimeoutError:
            print('Cant connect to internet. Retrying in 2 seconds...')
            time.sleep(2)

def getbio(fcount):

    print("Getting bio for: " + str(fcount))

    users_list = []
    c = twint.Config()
    c.Username = fcount
    c.Store_object = True
    c.Store_object_users_list = users_list

    while True:
        try:
            twint.run.Lookup(c)
            userbio = users_list[0].bio
            #dictofusersandfollowingcounts.update({fcount:followingnumber})
            return userbio
            break
        except aiohttp.ClientConnectorError:
            print('Cant connect to internet. Retrying in 2 seconds...')
            time.sleep(2)
        except aiohttp.ClientOSError:
            print('Cant connect to internet. Retrying in 2 seconds...')

            time.sleep(2)
        except aiohttp.ServerDisconnectedError:
            print('Cant connect to internet. Retrying in 2 seconds...')
            time.sleep(2)
        except asyncio.TimeoutError:
            print('Cant connect to internet. Retrying in 2 seconds...')
            time.sleep(2)
        except IndexError:
            return ''


#global dictofusersandfollowingcounts
global dictofusersandfollowingcounts
def followingcountforsingleuserparallel(fcount,dictofusersandfollowingcounts):

    asyncio.set_event_loop(asyncio.new_event_loop())
    print("Checking following count for: " + str(fcount))

    users_list = []
    c = twint.Config()
    c.Username = fcount
    c.Store_object = True
    c.Store_object_users_list = users_list

    while True:
        try:
            twint.run.Lookup(c)
            followingnumber = users_list[0].following
            dictofusersandfollowingcounts.update({fcount:followingnumber})
            return {fcount:followingnumber}
            break
        except aiohttp.ClientConnectorError:
            print('Cant connect to internet. Retrying in 2 seconds...')
            time.sleep(2)
        except aiohttp.ClientOSError:
            print('Cant connect to internet. Retrying in 2 seconds...')
            time.sleep(2)
        except aiohttp.ServerDisconnectedError:
            print('Cant connect to internet. Retrying in 2 seconds...')
            time.sleep(2)
        except asyncio.TimeoutError:
            print('Cant connect to internet. Retrying in 2 seconds...')
            time.sleep(2)


from threading import Thread
import queue
class ThreadWithReturnValue(object):
    def __init__(self, target=None, args=(), **kwargs):
        self._que = queue.Queue()
        self._t = Thread(target=lambda q,arg1,kwargs1: q.put(target(*arg1, **kwargs1)) ,
                args=(self._que, args, kwargs), )
        self._t.start()

    def join(self):
        self._t.join()
        return self._que.get()








def followingcountparallel(users):
    #users = users[:5]

    dictofusersandfollowingcounts = {}
    while True:
        if len(users) > 0:
            user_to_be_processed_count = users.pop()
            print("Number of users left:", len(user_to_be_processed_count))
            twrv = ThreadWithReturnValue(target = followingcountforsingleuserparallel,args=(user_to_be_processed_count,dictofusersandfollowingcounts,))

            print(twrv.join())
        else:
            break
    print(dictofusersandfollowingcounts)
    return dictofusersandfollowingcounts


def getfollowingcount(user):
    #if not os.path.exists('data/' + str(user) + ' fcount.csv'):
        #download following count
    #followingcount(user)
    if os.path.exists('data/' + str(user) + ' fcount.csv'):
        with open('data/' + str(user) + ' fcount.csv', 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')
            next(csv_reader, None)
            followingnumber = []
            for row in csv_reader:
                followingnumber.append(row[9])
            print(int(followingnumber[-1]))
    elif not os.path.exists('data/' + str(user) + ' fcount.csv'):
        return
    return int(followingnumber[-1])

def removeuserswithhighfollowingcount(listofusers, dictoffollowingcounts, followingcountthreshold=10000):
    cleanedlistofusers = []
    for user in listofusers:
        userfollowingcount = dictoffollowingcounts.get(user)
        #if userfollowingcount == None:
            #continue
        if int(userfollowingcount) == 0:
            print("Removing", user)
            continue
        if int(userfollowingcount) < followingcountthreshold:
            #if not os.path.exists('data/' + str(user) + ' following.csv'):
            cleanedlistofusers.append(user)
        else:
            print("Removing", user, "with following count of", str(userfollowingcount))
    return cleanedlistofusers



#Using numba
from numba import jit

#@python_app
def downloadfollowingsingleuserparsl(utarget):
    #asyncio.set_event_loop(asyncio.new_event_loop())

    if os.path.exists('data/' + str(utarget) + ' resume following.csv'):
        os.remove('data/' + str(utarget) + ' resume following.csv')
    print("Downloading who " + str(utarget) + " is following")
    y = twint.Config()
    y.Username = str(utarget.lower())
    y.Store_csv = True
    #y.Limit = 30000
    y.Resume = "data/" + str(utarget) + " resume following.csv"

    #y.Output = str(utarget) + " following.csv"
    y.Output = "data/" + str(utarget) + " following.csv"

    while True:
        try:
            twint.run.Following(y)
            break
        except aiohttp.ClientConnectorError:
            time.sleep(1)
            print('Cant connect to internet. Restarting...')
            #twint.run.Followers(x)
        except aiohttp.ClientOSError:
            time.sleep(1)
            print('Cant connect to internet. Restarting...')
            #twint.run.Followers(x)
        except aiohttp.ServerDisconnectedError:
            time.sleep(1)
            print('Cant connect to internet. Restarting...')
            #twint.run.Followers(x)
        except asyncio.TimeoutError:
            time.sleep(1)
            print('Cant connect to internet. Restarting...')
        except KeyboardInterrupt:
            os.remove("data/" + str(utarget) + " following.csv")
            os.remove("data/" + str(utarget) + " resume following.csv")
            raise ValueError("Quit program. Deleted following and resume files for " + str(utarget) + ".")


@jit(parallel=True)
def downloadfollowingparsl(userlist):
    for user in userlist:
        downloadfollowingsingleuserparsl(user)


def downloadfollowingsingleuser_plain(utarget):
    #asyncio.set_event_loop(asyncio.new_event_loop())

    if os.path.exists('data/' + str(utarget) + ' resume following.csv'):
        os.remove('data/' + str(utarget) + ' resume following.csv')
    print("Downloading who " + str(utarget) + " is following")
    y = twint.Config()
    y.Username = str(utarget.lower())
    y.Store_csv = True
    #y.Limit = 30000
    y.Resume = "data/" + str(utarget) + " resume following.csv"

    #y.Output = str(utarget) + " following.csv"
    y.Output = "data/" + str(utarget) + " following.csv"

    while True:
        try:
            twint.run.Following(y)
            break
        except aiohttp.ClientConnectorError:
            time.sleep(1)
            print('Cant connect to internet. Restarting...')
            #twint.run.Followers(x)
        except aiohttp.ClientOSError:
            time.sleep(1)
            print('Cant connect to internet. Restarting...')
            #twint.run.Followers(x)
        except aiohttp.ServerDisconnectedError:
            time.sleep(1)
            print('Cant connect to internet. Restarting...')
            #twint.run.Followers(x)
        except asyncio.TimeoutError:
            time.sleep(1)
            print('Cant connect to internet. Restarting...')
        except KeyboardInterrupt:
            os.remove("data/" + str(utarget) + " following.csv")
            os.remove("data/" + str(utarget) + " resume following.csv")
            raise ValueError("Quit program. Deleted following and resume files for " + str(utarget) + ".")

def getfollowinglist(user):
    print("Getting following list for", user)
    try:
        followinglist = appendrowstolist("data/" + str(user) + " following.csv", [0], skipheader=True)
    except FileNotFoundError:
        return []
        #try:
            #downloadfollowingsingleuser_plain(user)
            #followinglist = appendrowstolist("data/" + str(user) + " following.csv", [0], skipheader=True)
        #except:
            #print("Skipping " + user, 'not found (probably a private account)')
            #return []
    return followinglist


def followingcountnumber(fcount):
    print("Checking following count for: " + str(fcount))

    users_list = []
    c = twint.Config()
    c.Username = fcount
    c.Store_object = True
    c.Store_object_users_list = users_list

    while True:
        try:
            twint.run.Lookup(c)
            followingnumber = users_list[0].following
            #dictofusersandfollowingcounts.update({fcount:followingnumber})
            return followingnumber
            break
        except aiohttp.ClientConnectorError:
            print('Cant connect to internet. Retrying in 2 seconds...')
            time.sleep(2)
        except aiohttp.ClientOSError:
            print('Cant connect to internet. Retrying in 2 seconds...')

            time.sleep(2)
        except aiohttp.ServerDisconnectedError:
            print('Cant connect to internet. Retrying in 2 seconds...')
            time.sleep(2)
        except asyncio.TimeoutError:
            print('Cant connect to internet. Retrying in 2 seconds...')
            time.sleep(2)





#@jit(parallel=True)
def followingcount(fcount):
    print("Checking following count for: " + str(fcount))

    users_list = []
    c = twint.Config()
    c.Username = fcount
    c.Store_object = True
    c.Store_object_users_list = users_list

    while True:
        try:
            twint.run.Lookup(c)
            followingnumber = users_list[0].following
            #dictofusersandfollowingcounts.update({fcount:followingnumber})
            return {fcount:followingnumber}
            break
        except aiohttp.ClientConnectorError:
            print('Cant connect to internet. Retrying in 2 seconds...')
            time.sleep(2)
        except aiohttp.ClientOSError:
            print('Cant connect to internet. Retrying in 2 seconds...')

            time.sleep(2)
        except aiohttp.ServerDisconnectedError:
            print('Cant connect to internet. Retrying in 2 seconds...')
            time.sleep(2)
        except asyncio.TimeoutError:
            print('Cant connect to internet. Retrying in 2 seconds...')
            time.sleep(2)


@jit(parallel=True)
def getfollowingcounts(users):
    dictofusersandfollowingcounts = []
    for user in users:
        dictofusersandfollowingcounts.append(followingcount(user))


    newdict = {}
    for i in dictofusersandfollowingcounts:
        username = list(i.keys())[0]
        following_count = list(i.values())[0]
        newdict.update({username:following_count})
    return newdict
