from fastapi import FastAPI, HTTPException
from redis.asyncio import Redis 
import time
import uuid
app = FastAPI()

r = Redis(host="redis", port=6379, decode_responses=True)

# @app.get('/')
# async def read_root():
#     user_id = 'test_user'
#     hits = await r.incr(user_id)
    
#     if hits == 1:
#         await r.expire(user_id, 60)
        
#     if hits > 5:
#         raise HTTPException(status_code=429, detail="Too many requests")
        
#     return {"message": "trying it out", "request_counts": hits}

@app.get('/advanced')
async def read_advanced():
    user_id='test_user'
    now=time.time()
    window_size=60
    limit=5
    request_id=str(uuid.uuid4())
    pipe=r.pipeline() 
    pipe.zremrangebyscore(user_id, 0, now - window_size)
    pipe.zadd(user_id,{request_id:now})
    pipe.zcard(user_id)
    pipe.expire(user_id,window_size)
    _, _ , count, _ =await pipe.execute()
    if count>limit:
        raise HTTPException(status_code=429, detail="Rate Limit Exceeded (Sliding Window)")
    return {"message": "Success", "current_count": count}
    