startingusername = input('Input starting username: ').strip()
similaritythreshold = float(input('Input similarity threshold: ').strip())
degree = int(input('Input degree of separation: ').strip())
downloadmodel = input('In order to make this program work, it needs a RoBERTa language model (around 1.5 GB), are you okay with downloading this model? (y/n): ')
if downloadmodel.lower().strip() == 'y':
    model = SentenceTransformer('roberta-large-nli-stsb-mean-tokens')
else:
    print('Quiting program...')
    raise ValueError('Quitting program')
import os
import twint
import operator
from twittersixdegrees import makefollowinglistfor, getbio, makedatafolder, appendrowstolist, downloadfollowingsingleuser
import csv
from sentence_transformers import SentenceTransformer

from numba import jit
import numpy as np
@jit(nopython=True)
def cosine_similarity_numba(u:np.ndarray, v:np.ndarray):
    assert(u.shape[0] == v.shape[0])
    uv = 0
    uu = 0
    vv = 0
    for i in range(u.shape[0]):
        uv += u[i]*v[i]
        uu += u[i]*u[i]
        vv += v[i]*v[i]
    cos_theta = 1
    if uu!=0 and vv!=0:
        cos_theta = uv/np.sqrt(uu*vv)
    return cos_theta


def writetocsv(filename, values, header=None):
    if not os.path.exists(filename):
        header_added = False
    else:
        header_added = True

    if header == None:
        header = (len(values) * [''])
    if values == None:
        raise ValueError('''You might have forgotten to specify what to write in rows or the values are None.
        Here is an example of how the input should look like (this would be the second parameter in the function):
        writetocsv('filename.csv',
        [input_column_one, input_column_two, input_column_three],
        header=['column one', 'column two', 'column three'])''')
    with open(filename, mode='a') as csv_writer:
        csv_writer = csv.writer(csv_writer, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if not header_added:
            csv_writer.writerow(header)
        csv_writer.writerow(values)


def downloaduserbios(username, followinglist):
    if not os.path.exists('data/' + username + ' following users bio.csv'):
        for user in followinglist:
            userbio = getbio(user)
            writetocsv('data/' + username + ' following users bio.csv',
            [user, userbio],
            header=['username', 'bio']
            )
def makeresultsfolder():
    if not os.path.exists('results'):
        os.mkdir('results')

def getkey(dct,value):
     return [key for key in dct if (dct[key] == value)]
def getusersbiosandsimilarities(startingusername, startinguserbioembeddings):
    usersandbios = appendrowstolist('data/' + startingusername + ' following users bio.csv', [0,1], skipheader=True)

    usersandbiosdict = {}
    for user, bio in usersandbios:
        usersandbiosdict.update({user:bio})
    if not os.path.exists('data/' + startingusername + ' following users bio similarity.csv'):
        embeddingsforbios = model.encode(list(usersandbiosdict.values()))
        bios_and_similarities = {}
        for startingbioembedding in startinguserbioembeddings:
            for bio, embedding in zip(list(usersandbiosdict.values()), embeddingsforbios):
                bios_and_similarities.update({bio:abs(cosine_similarity_numba(startingbioembedding, embedding))})



        bios_and_similarities_sorted = dict(sorted(bios_and_similarities.items(), key=operator.itemgetter(1),reverse=True))

        users_similarities_bios = {}
        for bio, similarity in bios_and_similarities_sorted.items():
            users_similarities_bios.update({getkey(usersandbiosdict,bio)[0]:[similarity,bio]})
            print(getkey(usersandbiosdict,bio)[0],similarity)


        for user, bioandsimilarity in users_similarities_bios.items():

            similarity = bioandsimilarity[0]
            userbio = bioandsimilarity[1]

            writetocsv('data/' + startingusername + ' following users bio similarity.csv',
            [user, similarity, userbio],
            header=['username', 'similarity', 'user bio']
            )
    else:
        users_similarities_bios_list = appendrowstolist('data/' + startingusername + ' following users bio similarity.csv', [0,1,2], skipheader=True)
        users_similarities_bios = {}
        for user, similarity, bio in users_similarities_bios_list:
            users_similarities_bios.update({user:[float(similarity), bio]})
    return users_similarities_bios

#Start

makedatafolder()
makeresultsfolder()
startinguserfollowing = makefollowinglistfor(startingusername)

startinguserbio = getbio(startingusername)


startinguserbioembeddings =  model.encode([startinguserbio])



if degree == 1:
    downloaduserbios(startingusername, startinguserfollowing)
    users_similarities_bios = getusersbiosandsimilarities(startingusername, startinguserbioembeddings)

    for user, similarityandbio in users_similarities_bios.items():
        similarity = similarityandbio[0]
        bio = similarityandbio[1]
        writetocsv('results/' + 'Most similar users to ' + startingusername + ' First Degree.csv'
        [startingusername, startinguserbio, user, similarity, bio],
        header=['Starting Username', 'Starting Bio', 'User', 'Similarity', 'Bio'])

elif degree == 2:
    downloaduserbios(startingusername, startinguserfollowing)
    users_similarities_bios = getusersbiosandsimilarities(startingusername, startinguserbioembeddings)

    for userone, similarityandbio in users_similarities_bios.items():

        useronesimilarity = similarityandbio[0]
        useronebio = similarityandbio[1]
        if useronesimilarity >= similaritythreshold:
            downloadfollowingsingleuser(userone)
            useronefollowinglist = makefollowinglistfor(userone)
            downloaduserbios(userone, useronefollowinglist)
            userone_users_bios_similarities = getusersbiosandsimilarities(userone, startinguserbioembeddings)

            for usertwo, similarityandbio in userone_users_bios_similarities.items():
                usertwosimilarity = similarityandbio[0]
                usertwobio = similarityandbio[1]
                writetocsv('results/' + 'Most similar users to ' + startingusername + ' Second Degree.csv',
                [str(startingusername), str(startinguserbio), 'Following', str(userone), str(useronesimilarity), str(useronebio), 'Following',str(usertwo), str(usertwosimilarity),str(usertwobio)],
                header=['Starting Username', 'Starting Bio', '>', 'User 1', 'User 1 Similarity', 'User 1 Bio', '>','User 2', 'User 2 Similarity', 'User 2 Bio'])

#To do: Ponds, and Pond jumping through node co-existence and node path/tree traversal
