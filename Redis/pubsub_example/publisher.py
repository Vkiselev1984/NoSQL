import redis

redis_client = redis.StrictRedis(host='redis', port=6379, decode_responses=True)

def publish_message():
    redis_client.set('publisher_status', 'active')
    print("Publisher started. Status set to active.")

    while True:
        message = input("Enter message to send (or 'exit' to exit): ")
        if message.lower() == 'exit':
            break
        redis_client.publish('my_channel', message)
        redis_client.lpush('published_messages', message)
        print(f"Published: {message}")
    redis_client.set('publisher_status', 'inactive')
    print("Publisher stopped. Status set to inactive.")

if __name__ == "__main__":
    publish_message()