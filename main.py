import threading
import random
import queue

# Constants
LOWER_NUM = 1
UPPER_NUM = 10000
BUFFER_SIZE = 100
MAX_COUNT = 10000

# Global buffer (stack)
buffer = queue.LifoQueue(BUFFER_SIZE)

# Lock for writing to files
file_lock = threading.Lock()

# Event for notifying the consumers that the producer has finished producing
done = threading.Event()

def producer():
    with open('all.txt', 'w') as f:
        for _ in range(MAX_COUNT):
            num = random.randint(LOWER_NUM, UPPER_NUM)
            f.write(str(num) + '\n')
            buffer.put(num)
    # Signal that the producer is done
    done.set()

def consumer_odd():
    with open('odd.txt', 'w') as f:
        while not done.is_set() or not buffer.empty():
            num = buffer.queue[-1]  # Peek at the top of the stack
            if num % 2 != 0:
                with file_lock:
                    f.write(str(num) + '\n')
                buffer.get()  # Remove the number from the buffer

def consumer_even():
    with open('even.txt', 'w') as f:
        while not done.is_set() or not buffer.empty():
            num = buffer.queue[-1]  # Peek at the top of the stack
            if num % 2 == 0:
                with file_lock:
                    f.write(str(num) + '\n')
                buffer.get()  # Remove the number from the buffer

# Create threads
producer_thread = threading.Thread(target=producer)
consumer_odd_thread = threading.Thread(target=consumer_odd)
consumer_even_thread = threading.Thread(target=consumer_even)

# Start threads
producer_thread.start()
consumer_odd_thread.start()
consumer_even_thread.start()

# Wait for all threads to complete
producer_thread.join()
consumer_odd_thread.join()
consumer_even_thread.join()
