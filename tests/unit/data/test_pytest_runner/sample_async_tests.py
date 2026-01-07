"""
Sample async tests for pytest runner validation
"""
import asyncio

async def test_simple_pass():
    """A simple test that passes"""
    await asyncio.sleep(0.001)
    assert True

async def test_with_computation():
    """A test that does some computation"""
    result = 0
    for i in range(10):
        result += i
        await asyncio.sleep(0.0001)
    assert result == 45

async def test_another_pass():
    """Another passing test"""
    value = "hello"
    await asyncio.sleep(0.001)
    assert value == "hello"
    assert len(value) == 5
