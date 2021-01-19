#!/usr/bin/env python3
import hashlib
from immudb.constants import *
from immudb.exceptions import *
import immudb.store

class InclusionProof:
    def __init__(self):
        self.leaf=None
        self.width=None
        self.terms=b''
        
class HTree:
    def __init__(self, maxWidth:int):
        if maxWidth<1:
            return
       
        self.maxWidth=maxWidth
        lw=1
        while lw<maxWidth:
            lw=lw<<1
        height=(maxWidth-1).bit_length()+1
        self.levels=[None]*height
        for l in range(0,height):
            self.levels[l]=[None]*(lw>>l)

    def BuildWith(self, digests:list[bytes]):
        if len(digests)>self.maxWidth:
            raise ErrMaxWidthExceeded
        if len(digests)==0:
            raise ErrIllegalArguments
        for i in range(0,len(digests)):
            leaf=LEAF_PREFIX+digests[i]
            self.levels[0][i]=hashlib.sha256(leaf).digest()
        l=0
        w=len(digests)
        while w>1:
            b=NODE_PREFIX
            wn=0
            i=0
            while i+1<w:
                b+=self.levels[l][i]+self.levels[l][i+1]
                self.levels[l+1][wn]=hashlib.sha256(b).digest()
                wn=wn+1
                i=i+2
            if w%2==1:
                self.levels[l+1][wn]=self.levels[l][w-1]
                wn=wn+1
        self.width=len(digests)
        self.root=self.levels[l][0]
    def InclusionProof(self, i):
        if i>=self.width:
            raise ErrIllegalArguments
        m=0
        n=self.width
        offset=0
        proof=InclusionProof()
        proof.leaf=i
        proof.width=self.width
        if self.width==1:
            return proof
        while true:
            d=(n-1).bit_length()
            k=1<<(d-1)
            if m<k:
                l,r=offset+k,offset+n-1
                n=k
            else:
                l,r=offset,offset+k-1
                m=m-k
                n=n-k
                offset=offset+k
            layer=(r-l).bit_length()
            index=l/(1<<layer)
            proof.terms=t+levels[layer][index]+proof.terms
            if n<1 or (n==1 and m==0):
                return proof
            
def InclusionProofFrom(iproof):
    h=InclusionProof()
    h.leaf=int(iproof.leaf)
    h.width=int(iproof.width)
    h.terms=immudb.store.DigestFrom(iproof.terms)
    return h
