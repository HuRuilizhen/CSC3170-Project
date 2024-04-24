from copy import deepcopy
import os, io, csv, math, random
import numpy as np
from tqdm import tqdm
import os
import shutil
import argparse
from collections import defaultdict
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('bert-base-nli-mean-tokens')

csv_path = "/mnt/petrelfs/wangyuancheng/CSC3170/course_list.csv"

with open(csv_path, 'r') as csvfile:
    files = list(csv.DictReader(csvfile))

save_path = "/mnt/petrelfs/wangyuancheng/CSC3170/embedding"

tmp = defaultdict()

for i in tqdm(range(0, len(files))):
    course_title = files[i]['Name']
    course_name = files[i]['Subject'] + files[i]['Number']

    if course_name in tmp.keys():
        continue
    
    tmp[course_name] = True

    ceph_dir = f"{save_path}/{course_name}.npy"

    sentence_embeddings = model.encode(course_title)

    np.save(ceph_dir, sentence_embeddings)