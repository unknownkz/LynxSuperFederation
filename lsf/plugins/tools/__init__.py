# Copyright © 2022 Unknown (The MIT License)
# All Rights Reserved
# @unknownkz
import numpy as zz
from base64 import b64decode
from ...database import users_sql as sql


LIST_NOSPAM = [
    -1001699144606,  # @kastaot
    -1001697659804,  # @LSF_SupportGroup
    -1001578266225,  # CTT
]

xa = [
    "LTEwMDE2OTkxNDQ2MDY=",
    "LTEwMDE2OTc2NTk4MDQ=",
    "LTEwMDE1NzgyNjYyMjU=",
]

v = []

for exam in xa:
    exam = b64decode(exam).decode("utf-8")
    for x in exam:
        v.append(x)

Weird = zz.array(v, dtype=str)
