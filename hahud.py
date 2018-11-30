import hashlib
import os

from cache import *
from datamodels import *
from htmlgenerator import *
from hahu_processor import *
from dao import *

query1 = query("Celica", "https://www.hasznaltauto.hu/talalatilista/PDNG2VC3V2NTAEG5RNLRAIDJKLT3GUVF7OJS3ICJDGEOGMMONSBW5OGK3Y5QNGTCFZPYZTUZY6MYOAKZ4TZMXSZMS5BEHQGGHICRP3GFTGYUYCR7UBAXUQQX5QEO3JIAJIOS6M36KOXMFAF6Q4FPYIGOK64ZXE7UBQJ3RUVIGYTNSSJB2YGHYLUZQMKNROJSRG5WYEJR5ROZ7K5WICQ3ZAZT3WMEPCTM7QPKK2GAIH5UOAJJX7QZBR2OQFWLXQLRZUVTVJA3A25UDPZ3W676CHXAB2ZSF3VFM2ITZC4PZLHFR5WGCY6S3QL77WYGBB56UPQGGDKWS7W4MYVH6WMH66KXJ4QUYGLQDJFFKROXQJRYUU5UPYZGCKZETIMRNHA5JZDTDRIE6XUPYHLJWUMOZOKTBANSW6ZTZHFFRMCWXUFGSIQWL3Z6LBFAZU5FGQRFVFMG7R2XA7WRHGVUAIIMDQYGOEDHTEC7NK5K64IPJJTJHHKHHOP6YIW2YVSO7I55T7WIGOF73DQATXNQNXIHL3S3T4UZOHRHM7QEKW256LCRQWHV2QIXV7COOFHTYY2CGNMB3ZLH4OR6H4OHQ5SSBQD4KK55TWL2H5UD4OV5YR7URIN4VXK6OEWMDBCUEHM4GXLJO4BFJCBGEDPK7DAFVNME7GUDKKIDFPLYBZQR6USBLRWHQGXFPA5W5WZV64R4E72I7FPY323PMZU5NWJCZPB7Z2A62E35LFN5OAEZITIXD6Q36AV73D56LZ7QDXGONTGQ")
query2 = query("Tiburon", "https://www.hasznaltauto.hu/talalatilista/PDNG2VCZR2RTAEF5RNHRBSGS3XHOOSBDZVH25ABKINARYLYV3EDHK2HF5ZOQMJUD5F6FC6VPSZLYWANZFXSVPECFFGCYNCBNPECSP3GFSGYUFCRQUBCXHBZO2IEO3JAASM5Z4ZX4UJ6I2EKDB42YIQI4Z5ZDGJ7JDE3OAK5LLRFLFEKCVQM7QXBSPMU3B42VCZ3XURNEWBTX3LXKYDCOUCW6OZRR4KMK6H5SMRILD3OF6BKGQULQ4ZPKCQGLSFY4246KGR3TYFEC72DH472BXLQRVYYCXYS6DILMTM7YKPJYYFKPNTI5GEX424HQX5QYHIJUHKWB5KFM2WHMPU66MX6BG5JQQUYWXSDEVVLTZSQUZRQH4NKKGMJTWFS6F4BBU2EKQ3S5XCRFTLIFPPXBHYULQU6ZS3DBFRL2WXWFHQIUW2HYNZRNI5U5FGR3EVBMW7RZWA3XQ43K6AGGYCG2EOEC3TFS6NK5264AKJMLZEXJGXKO6Y3NTW6J3YSXWN6ZPNYXZMGBMO4KA26RO77EPHZZS6PSMZ7AGWJ256C6FSWHV2QMA36ES4KPHRRYG5RATXSBPY4T4PY2OZ3FEHBHYUE33GMUEGBUT6OF5YQHFFKKART5F3AYEUJUVCRSOS5BQKZYCLBI2UYB3H4XKNFZQT22DNSWDZI22HPJFHVMYL4DJUHXNLIOJ3X5SLRTSYNYVXCPPZHIIKPNULAL56HXHIF3MOUBV4RNDCNSS6U37YC7YRX7UOH4ON4NO5WGO")

queries = [query1, query2]			
	
numchanges = 0
for query in queries:
	hash = hashlib.md5(query.url.encode('utf-8')).hexdigest()[:6]
	dirpath = os.getcwd() + "/data_" + query.name.strip() + "_" + hash
	
	results = fetch_results_from_query(query)
			
	newdb = setupNewDB(dirpath)
	insertResults(newdb, results)
		
	print("... ", end="")
	
	changes = findChanges(dirpath, results)
			
	if len(changes) is not 0:
		generateDelta(dirpath, changes, results)
		numchanges += len(changes)
	
	print("done. ", end='')
	if len(changes) is not 0:
		print(str(len(changes)) + " change(s)")
	else:
		print("")
	
	newdb.close()
	archiveDatabase(dirpath)

if os.path.isfile(os.getcwd()+"/menu.html"):
	os.remove(os.getcwd()+"/menu.html")
	
print("Generating main view...", end='')
generateMenu()
print(" all done.\n\n")