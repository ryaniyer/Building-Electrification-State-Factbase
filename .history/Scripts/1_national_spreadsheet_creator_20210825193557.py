import time
start_time = time.time()
from Scripts import eia_national
from Scripts import eia_state
from Scripts import epa_nei
from Scripts import tessum
from Scripts import acs_housing
from Scripts import economic_data

import pandas as pd
import os
import shutil

restart_national = False
restart_national_natgas = False
restart_national_air_quality = False