"""
Test to verify pytest assertion rewriting works
"""
import asyncio

async def test_assertion_rewriting():
    """Test with a failing assertion to verify we get good error messages"""
    x = 10
    y = 20
    await asyncio.sleep(0.001)
    # This should fail with a detailed message showing x and y values
    assert x == y
