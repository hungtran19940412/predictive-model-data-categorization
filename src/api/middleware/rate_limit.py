import logging
from aioredis import Redis
from fastapi import HTTPException, Depends
from typing import Optional
import asyncio

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.redis = Redis(host='localhost', port=6379)
        logger.info(f"Initialized RateLimiter with {requests_per_minute} requests per minute")

    async def check_rate_limit(self, user_id: str) -> bool:
        """Check if user has exceeded rate limit"""
        try:
            key = f"rate_limit:{user_id}"
            current = await self.redis.incr(key)
            
            if current == 1:
                await self.redis.expire(key, 60)
            
            if current > self.requests_per_minute:
                logger.warning(f"Rate limit exceeded for user {user_id}")
                return False
                
            return True
        except Exception as e:
            logger.error(f"Rate limiting error: {e}")
            raise HTTPException(status_code=500, detail="Rate limiting service unavailable")

async def get_rate_limiter() -> RateLimiter:
    """Dependency to get rate limiter instance"""
    return RateLimiter()

if __name__ == "__main__":
    import asyncio
    logging.basicConfig(level=logging.INFO)
    
    async def test_rate_limiter():
        limiter = RateLimiter(requests_per_minute=2)
        user_id = "testuser"
        
        for i in range(3):
            allowed = await limiter.check_rate_limit(user_id)
            print(f"Request {i+1}: {'Allowed' if allowed else 'Denied'}")
            await asyncio.sleep(1)
    
    asyncio.run(test_rate_limiter())