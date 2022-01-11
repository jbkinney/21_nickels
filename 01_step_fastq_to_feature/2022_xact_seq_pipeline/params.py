import sys
import os
import pandas as pd
import numpy as np
import re
import glob
from pandas.api.types import is_string_dtype
from typing import Optional, Dict, Tuple, List
import time

# User options
illumina_run_dir = '../fastq'
metadata_file = './metadata.xlsx'
tmp_dir = 'tmp'
interm_dir = 'intermediate'
reads_per_split = int(1E6)
clean_intermediate = True
make_split_files = True
make_features_files = True
merge_feature = True
clean_tmp = True
use_cluster = True
