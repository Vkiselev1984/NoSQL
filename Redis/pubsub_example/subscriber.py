import redis
import threading
import os

redis_client = redis.StrictRedis(host='redis', port=6379, decode_responses=True)

subscribed_channels = ['my_channel']

def message_handler(message):
    print(f"Received: {message['data']}")

def subscribe():
    pubsub = redis_client.pubsub()
    pubsub.subscribe(**{subscribed_channels[0]: message_handler})
    print("Subscriber started. Waiting for messages...")
    pubsub.run_in_thread(sleep_time=0.001)

def show_help():
    print("Available commands:")
    print("- exit: Exit the subscriber.")
    print("- status: Show the current status of the subscriber.")
    print("- list: List all published messages.")
    print("- subscriptions: Show subscribed channels.")
    print("- send admin: Send a message to the admin.")
    print("- history: Show message history.")
    print("- delete <index>: Delete a message by index.")
    print("- clear: Clear the terminal screen.")
    print("- help: Show this help message.")

def command_interface():
    show_help()
    while True:
        command = input("Enter command (or 'exit' to quit): ").strip()
        print(f"Received command: {command}")
        if command.lower() == 'exit':
            print("Exiting subscriber...")
            break
        elif command.lower() == 'status':
            redis_client.set('subscriber_status', 'active')
            status = redis_client.get('subscriber_status')
            print(f"Subscriber status: {status}")
        elif command.lower() == 'list':
            messages = redis_client.lrange('published_messages', 0, -1)
            print("Published messages:")
            for msg in messages:
                print(msg)
        elif command.lower() == 'subscriptions':
            print("Subscribed channels:")
            for channel in subscribed_channels:
                print(channel)
        elif command.lower() == 'send admin':
            admin_message = input("Enter message to send to admin: ")
            redis_client.publish('admin_channel', admin_message)
            print(f"Message sent to admin: {admin_message}")
        elif command.lower() == 'history':
            messages = redis_client.lrange('published_messages', 0, -1)
            print("Message history:")
            for idx, msg in enumerate(messages):
                print(f"{idx}: {msg}")
        elif command.lower().startswith('delete '):
            try:
                index = int(command.split()[1])
                messages = redis_client.lrange('published_messages', 0, -1)
                if 0 <= index < len(messages):
                    redis_client.lrem('published_messages', 1, messages[index])
                    print(f"Message deleted: {messages[index]}")
                else:
                    print("Invalid index. Please enter a valid message index.")
            except (ValueError, IndexError):
                print("Invalid command. Use 'delete <index>' to delete a message.")
        elif command.lower() == 'clear':
            os.system('cls' if os.name == 'nt' else 'clear')
        elif command.lower() == 'help':
            show_help()
        else:
            print("Unknown command. Type 'help' for a list of commands.")

if __name__ == "__main__":
    threading.Thread(target=subscribe).start()
    command_interface()