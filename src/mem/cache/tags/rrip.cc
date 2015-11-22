/* UT Austin
 * EE460N 2015 Fall, Grad Lab
 * Authors: Chi-Wen Cheng, Hung-Ming Hsu
 */

/**
 * @file
 * Definitions of a RRIP tag store.
 */

#include "debug/CacheRepl.hh"
#include "mem/cache/tags/rrip.hh"
#include "mem/cache/base.hh"

RRIP::RRIP(const Params *p)
    : BaseSetAssoc(p)
{
    RRIP_bit = 2;
    int total_blks = numSets * assoc;
    RRPV_M1 = (2<<(RRIP_bit-1))-1;
    RRPV_M2 = (2<<(RRIP_bit-1))-2;
    RRPV_array = new int(total_blks);
    for(int i=0;i<total_blks;i++)
        RRPV_array[i] = RRPV_M1;
}

BaseSetAssoc::BlkType*
RRIP::accessBlock(Addr addr, bool is_secure, Cycles &lat, int master_id)
{
    BlkType *blk = BaseSetAssoc::accessBlock(addr, is_secure, lat, master_id);
    if(blk!=NULL){
        int set = blk->set;
        setRRPV(set,hit);
        DPRINTF(CacheRepl, "set %x: moving blk %x (%s) to MRU\n",
                blk->set, regenerateBlkAddr(blk->tag, blk->set),
                is_secure ? "s" : "ns");
    }
/*    
    if (blk != NULL) {
        // move this block to head of the MRU list
        sets[blk->set].moveToHead(blk);
        DPRINTF(CacheRepl, "set %x: moving blk %x (%s) to MRU\n",
                blk->set, regenerateBlkAddr(blk->tag, blk->set),
                is_secure ? "s" : "ns");
    }
*/
    return blk;
}

BaseSetAssoc::BlkType*
RRIP::findVictim(Addr addr) const
{
    int set = extractSet(addr);
    // grab a replacement candidate
    // BlkType *blk = sets[set].blks[assoc - 1];
    setRRPV(set,miss);
    BlkType *blk = getVictim(set);
    if (blk->isValid()) {
        DPRINTF(CacheRepl, "set %x: selecting blk %x for replacement\n",
                set, regenerateBlkAddr(blk->tag, set));
    }

    return blk;
}

void
RRIP::insertBlock(PacketPtr pkt, BlkType *blk)
{
    BaseSetAssoc::insertBlock(pkt, blk);

    int set = extractSet(pkt->getAddr());
    //sets[set].moveToHead(blk);
    setRRPV(set,insert);
}

void
RRIP::invalidate(BlkType *blk)
{
    BaseSetAssoc::invalidate(blk);

    // should be evicted before valid blocks
    int set = blk->set;
    //sets[set].moveToTail(blk);
    setRRPV(set,invalidate);
}

void setRRPV(Addr addr, int type, bool is_secure){
    Addr tag = extractTag(addr);
    int set = extractSet(addr);
    int way_id;
    BlkType *tmp = sets[set].findBlk(tag, is_secure, way_id);
    switch(type){
        case hit:
            RRPV_array[set*assoc+way_id]=0;
            break;
        case miss:
            int done=0;
            while(!done){
                for(int i=0;i<assoc;i++)
                    if(RRPV_array[set*assoc+i]==RRPV_M1){
                        done = 1;
                        break;
                    }
                if(done) break;
                for(int i=0;i<assoc;i++)
                    RRPV_array[set*assoc+i]++;
            }
            break;
        case insert:
            RRPV_array[set*assoc+way_id]=RRPV_M2;
            break;
        case inval:
            RRPV_array[set*assoc+way_id]=RRPV_M1;
            break;
        default:
            printf("fall in traps\n");
            break;
    }
}

BlkType* getVictim(int n_set){
    int index=0;
    BlkType* tmp;
    while(index<assoc)
    {
        if(RRPV_array[n_set*assoc+index]==RRPV_M1)
        {
            tmp = sets[n_set].blks[index];
            break;   
        }
        index++;
    }
    return tmp;
}

RRIP*
RRIPParams::create()
{
    return new RRIP(this);
}
