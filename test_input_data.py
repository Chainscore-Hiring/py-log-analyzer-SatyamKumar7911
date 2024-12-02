import asyncio
from coordinator import Coordinator
from worker import Worker

async def main():
    # Initialize Coordinator
    coordinator = Coordinator(port=8000)
    asyncio.create_task(coordinator.start())
    
    # Start Worker Nodes
    worker1 = Worker('alice', 'http://localhost:8000')
    worker2 = Worker('bob', 'http://localhost:8000')
    worker3 = Worker('charlie', 'http://localhost:8000')
    
    # Simulate worker nodes processing the log file
    tasks = [
        worker1.start('test_vectors/sample_logs.txt', 0, 100),
        worker2.start('test_vectors/sample_logs.txt', 100, 100),
        worker3.start('test_vectors/sample_logs.txt', 200, 100),
    ]
    
    # Measure processing speed and monitor memory usage
    start_time = asyncio.get_event_loop().time()
    await asyncio.gather(*tasks)
    end_time = asyncio.get_event_loop().time()
    
    print(f"Processing speed: {end_time - start_time:.2f} seconds")
    
    # Simulate worker failure
    await worker2.report_health()  # This should fail and the coordinator should handle reassignment
    
    # Get metrics from the coordinator
    metrics = coordinator.get_current_metrics()
    print(metrics)

asyncio.run(main())
