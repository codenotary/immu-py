import pytest
import immudb.client
from random import randint
import grpc._channel

class TestHistory:
        
    def test_history(self):
        try:
            a = immudb.client.ImmudbClient("localhost:3322")
            a.login("immudb","immudb")
        except grpc._channel._InactiveRpcError as e:
            pytest.skip("Cannot reach immudb server")
        key="history_{:04d}".format(randint(0,9999))
        values=[]
        for i in range(0,10):
            v="value_{:04d}".format(randint(0,9999))
            a.safeSet(key.encode('ascii'),v.encode('ascii'))
            values.append(v)
            
        hh=a.history(key.encode('ascii'),0,99,immudb.client.NEWEST_FIRST)
        assert(len(hh)==10)
        for i in range(0,10):
            assert(hh[i].value==values[9-i].encode('ascii'))
        
        idx=0
        for i in range(0,10):
           hh=a.history(key.encode('ascii'),idx,1,immudb.client.OLDEST_FIRST)
           assert(len(hh)>0)
           assert(hh[0].value==values[i].encode('ascii'))
           idx=hh[0].index
