from ... import DEV_ID, SD_ID, SUPPORT_ID, TIGERS_ID, WHITELIST_ID, lynx_client

xxx = {"DEV_ID", "SD_ID", "SUPPORT_ID", "WHITELIST_ID", "TIGERS_ID"}

zzz = list(set(DEV_ID) | set(SD_ID) | set(SUPPORT_ID) | set(WHITELIST_ID) | set(TIGERS_ID))

U_ABSURD = xxx.union(zzz)
