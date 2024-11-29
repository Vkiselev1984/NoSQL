# Work with RedisDB

Let's install and run MongoDB with docker via WSL:

```Terminal
kiselev@terminal:wsl
sudo docker run --name redis-container -d -p 6379:6379 redis
sudo docker exec -it redis-container redis-cli
```

Let's start with a simple command and set the key + value:

```Terminal
redis-cli
127.0.0.1:6379> SET mykey "Hello, Redis!"
OK
127.0.0.1:6379> get mykey
"Hello, Redis!"
```

In Redis, the maximum key size is 512 MB (megabytes). This means that you can use keys up to 512 MB long, which is quite large for most applications.

Storing user attributes in Redis is a common scenario, and Redis is great for this because of its speed and ease of working with data. We can use hashes to store user attributes because they allow us to store related data under a single key.

Let's create a hash called "users" and store some user attributes:

```Terminal
127.0.0.1:6379>HSET user:1000 name "Alice" age 30 email "alice@example.com"
```

To get all attributes of a user, use the HGETALL command:

```Terminal
127.0.0.1:6379>HGETALL user:1000
```

![hgetall](/Redis/img/Redis_hgetall_db.png)

If you want to get just the username, use the HGET command:

```Terminal
127.0.0.1:6379>HGET user:1000 name
```

If you need to update the user's age, you can use HSET again:

```Terminal
127.0.0.1:6379>HSET user:1000 age 31
```

To remove an attribute, such as email, use the HDEL command:

```Terminal
127.0.0.1:6379>HDEL user:1000 email
```

Great! Let's move on and look at some additional operations and scenarios related to storing user attributes in Redis. We can also look at using other Redis data structures for more complex scenarios.

- Storing Multiple Users

If you have multiple users, you can use a similar approach to storing their attributes. For example, let's add another user:

```Terminal
127.0.0.1:6379>HSET user:1001 name "Bob" age 35 email "bob@example.com"
```

Now we have two users: Alice and Bob.

To get a list of all users, we can use keys with a pattern. For example, to get all user keys, we can use the KEYS command (note that using KEYS is not recommended in a production environment due to its impact on performance):

```Terminal
127.0.0.1:6379>KEYS user:*
```

We can use lists to store the history of user actions. For example, if you want to store the latest user actions, you can do the following:

```Terminal
LPUSH user:1000:actions "Logged in"
LPUSH user:1000:actions "Viewed profile"
LPUSH user:1000:actions "Updated email"
```

To get the latest user actions, use the LRANGE command:

```Terminal
127.0.0.1:6379>LRANGE user:actions:1000 0 -1
```

If you want to store user roles, you can use sets. For example, let's add roles for a user:

```Terminal
SADD user:1000:roles "admin"
SADD user:1000:roles "editor"
```

To get all roles for a user, use the SMEMBERS command:

```Terminal
127.0.0.1:6379>SMEMBERS user:1000:roles:admin
```

If you need to delete a user and all of their data, you can use the DEL command to delete all associated keys. For example:

```Terminal
127.0.0.1:6379>DEL user:1000
127.0.0.1:6379>DEL user:1000:actions
127.0.0.1:6379>DEL user:1000:roles
```

If you want to append data to an existing value in Redis, you can do so using the APPEND command, which allows you to append a string to a key value. This is especially useful when you want to store additional information without overwriting the existing value.

```Terminal
127.0.0.1:6379>APPEND mykey ", Redis!"
127.0.0.1:6379> GET mykey
"Hello, Redis!, Redis!"
```

Using the APPEND command in Redis can be useful in various scenarios where you need to append data to existing string values. Here are a few examples where this can be especially useful:

1. Logging

   If you are logging events or actions, you can use APPEND to add new entries to an existing row. For example, if you have a key for storing user logs, you can add new events:

```Terminal
127.0.0.1:6379>SET user:1000:logs "Log entry 1"
127.0.0.1:6379>APPEND user:1000:logs "Log entry 2"
127.0.0.1:6379>APPEND user:1000:logs "Log entry 3"
```

2. Auditing

   If you're collecting data from multiple sources and want to store it in a single key, APPEND can help. For example, if you're collecting product reviews, you can append new reviews to an existing value:

```Terminal
APPEND product:123:reviews "Great product! "
APPEND product:123:reviews "Would buy again! "
```

3. Forming Strings

   If you need to form strings on the fly, such as to create messages or notifications, APPEND can be useful. For example, you can create messages for users:

```Terminal
SET message "Hello, "
APPEND message "Alice! "
APPEND message "Welcome to our service."
```

4. Storing temporary data

   If you want to store temporary data that will be updated, such as timestamps or statuses, APPEND can help you add new values:

```Terminal
APPEND session:userid123 "Activity at 10:00 AM; "
APPEND session:userid123 "Activity at 10:05 AM; "
```

5. Keeping track of changes

   If you want to track changes to your data, you can use APPEND to add new values ​​to existing ones. For example, if you have a field to store the history of changes to user attributes:

```Terminal
APPEND user:1000:history "Changed email from old@example.com to new@example.com; "
APPEND user:1000:history "Updated age from 30 to 31; "
```

## TTL (Time To Live)

If you want user data to be automatically deleted after a certain amount of time, you can set a time to live (TTL) for the key:

```Terminal
EXPIRE user:1000 3600
```

Use the TTL command to find out how much time is left before a key expires:

```Terminal
127.0.0.1:6379>TTL user:1000
```

![ttl](/Redis/img/Redis_TTL.png)

TTL (Time To Live) in Redis can be very useful in various scenarios, especially when you are working with temporary data, caching or user sessions. Let's look at some real-world examples where TTL can come in handy.

### Example 1: Caching data

Suppose you have a web application that frequently queries data from a database, such as product information. To reduce the load on the database and speed up response times, you can cache the query results in Redis with a set TTL.

1. Caching the query result

   When a user requests product information, you first check if the data is in the Redis cache:

```Terminal
127.0.0.1:6379>GET product:123
```

2. If data is missing

   If data is not found, you query the database, get the data, and store it in Redis with a TTL:

```Terminal
127.0.0.1:6379>SET product:123 "Product Data" EX 3600
```

3. If the data is there

   If the data is already in the cache, you simply return it to the user, which is much faster than querying the database.

### Example 2: User Sessions

When users log in to your application, you can store session information in Redis. By setting a TTL on the session key, you can automatically remove old or inactive sessions.

1. Creating a Session

   When a user logs in, you create a session and store it in Redis:

```Terminal
127.0.0.1:6379>SET session:userid123 "session_data" EX 1800
```

2. Session Check

   On every request from the user, you check if the session exists:

```Terminal
127.0.0.1:6379>GET session:userid123
```

3. Automatic deletion

   If a user is inactive for 30 minutes, the session is automatically deleted from Redis, which helps with resource management and security.

### Example 3: Temporary notifications

You can use TTL for timed notifications or messages that should disappear after a certain amount of time.

1. Sending a notification

   When you send a notification to a user, you can store it in Redis with a TTL:

```Terminal
127.0.0.1:6379>SET notification:userid123 "You have a new message!" EX 300
```

2. Checking for notifications

   When checking for notifications, you can simply query Redis:

```Terminal
127.0.0.1:6379>GET notification:userid123
```

3. Automatic deletion

The notification will be automatically deleted after 5 minutes if the user does not read it.

## Increment and Decrement Commands

In Redis, the increment and decrement commands allow you to easily increase or decrease numeric values ​​stored under specific keys. These commands are very useful for working with counters, ratings, statistics, and other numeric data.

- INCR: Increments the key by 1.
- INCRBY: Increments the key by the given number.
- DECR: Decrements the key by 1.
- DECRBY: Decrements the key by the given number.

1. Increment

   Create and increment:

```Terminal
127.0.0.1:6379>SET counter 10
127.0.0.1:6379>INCR counter
```

After executing the INCR counter command, the value of the counter key will become 11.

2. Decrement

- Creation and decrement:

```Terminal
127.0.0.1:6379>SET counter 10
127.0.0.1:6379>DECR counter
```

After executing the DECR counter command, the value of the counter key will become 9.

- Decrement by a given number:

```Terminal
127.0.0.1:6379>SET counter 10
127.0.0.1:6379>DECRBY counter 5
```

After executing the DECRBY counter 5 command, the value of the counter key will become 5.

## Type of data

So, we already found out in the [introduction](/introduction.md) that in Redis you can store not only a string as a value, but also a more complex structure.

### Example

For example, let's create a data structure for managing projects, tasks and users.

#### Data Structure

1. Projects: Each project will be stored as a hash with attributes like title, description, and status.
2. Tasks: Each task will be stored as a hash associated with a project, with attributes like title, description, status, and priority.
3. Users: Each user will be stored as a hash with attributes like name and email.
4. Association between tasks and users: We will use sets to store the users assigned to each task.

#### Creating structure

1. Creating users

```Terminal
HSET user:1 name "Alice" email "alice@example.com"
HSET user:2 name "Bob" email "bob@example.com"
HSET user:3 name "Charlie" email "charlie@example.com"
```

2. Creating projects

```Terminal
HSET project:101 name "Project Alpha" description "Description of Project Alpha" status "active"
HSET project:102 name "Project Beta" description "Description of Project Beta" status "active"
HSET project:103 name "Project Gamma" description "Description of Project Gamma" status "active"
```

3. Creating tasks

```Terminal
HSET task:201 name "Task 1" description "Description of Task 1" status "in progress" priority "high"
HSET task:202 name "Task 2" description "Description of Task 2" status "not started" priority "medium"
HSET task:203 name "Task 3" description "Description of Task 3" status "completed" priority "low"
```

4. Creating association between tasks and users

To link tasks to projects, we can use lists. For example, let's add tasks to the Alpha project:

```Terminal
LPUSH project:101:tasks 201
LPUSH project:101:tasks 202
```

And let's add a task to the Beta project:

```Terminal
LPUSH project:102:tasks 203
```

5. Query the association between tasks and users:

```Terminal
SADD task:201:assigned_users 1
SADD task:202:assigned_users 2
SADD task:203:assigned_users 3
```

To get information about a project, you can use the HGETALL command:

```Terminal
HGETALL project:101
```

To get all tasks associated with the Alpha project, you can use the LRANGE command:

```Terminal
LRANGE project:101:tasks 0 -1
```

To get information about a task, you can use the HGETALL command:

```Terminal
HGETALL task:201
```

To get all users assigned to a task, you can use the SMEMBERS command:

```Terminal
SMEMBERS task:201:assigned_users
```

We have created a complex data structure in Redis to manage projects, tasks and users. This structure allows you to easily organize data and access information about projects, tasks and assigned users.

## Lua scripting

Redis doesn't have a built-in command that lets you get all the information about a project, its associated tasks, and assigned users in a single command. However, you can use Lua scripts to accomplish this task in a single command. Lua scripts allow you to perform multiple Redis operations in a single call, which can greatly simplify the process of getting the combined output.

Let's create a Lua script that will get information about a project, its associated tasks, and assigned users.

```Lua
local project_id = ARGV[1]

local project_info = redis.call('HGETALL', 'project:' .. project_id)


local task_ids = redis.call('LRANGE', 'project:' .. project_id .. ':tasks', 0, -1)

local tasks_info = {}

for _, task_id in ipairs(task_ids) do
    local task = {}
    task.info = redis.call('HGETALL', 'task:' .. task_id)
    task.assigned_users = redis.call('SMEMBERS', 'task:' .. task_id .. ':assigned_users')
    table.insert(tasks_info, task)
end

return {project_info, tasks_info}
```

Let's save this script on the local machine and copy it to the container.

Find out the name of the container:

```Terminal
docker ps
```

Copy the file into the container:

```Terminal
docker cp Redis/project_info.lua d4ffca51a43c:/usr/local/bin/project_info.lua
```

Now you can use the Lua script to get information about a project, its associated tasks, and assigned users:

```Terminal
sudo docker exec -it d4ffca51a43c redis-cli --eval /usr/local/bin/project_info.lua , 101
```

![Lua script](/Redis/img/Redis_Lua_script.png)

The Lua script takes the project ID as an argument and returns the project information and the list of tasks associated with the project.

The Lua script uses the HGETALL command to get the project information and the LRANGE command to get the list of tasks.

The SMEMBERS command is used to get the list of assigned users for each task.

## Pub/Sub

Pub/Sub is a communication pattern used in messaging systems that allows for the separation of message senders (publishers) and message receivers (subscribers). This approach is widely used in a variety of applications, including messaging systems, notifications, distributed systems, and more.

### Main components of Pub/Sub

- Publisher:

This is the component that sends messages. The publisher does not know who the subscriber is and does not care how many subscribers there are to its messages.

- Subscriber:

This is the component that subscribes to specific messages or channels. The subscriber receives messages that match its subscription.

- Channel:

This is the logical entity that subscribers subscribe to and through which publishers send messages. Channels can be created for different topics or categories of messages.

### How Pub/Sub Works

- Subscription:

A subscriber registers for a specific channel or topic. After that, he starts receiving messages sent to this channel.

- Publishing:

A publisher sends messages to a specific channel. All subscribers registered to this channel receive these messages.

- Asynchrony:

Publishing and subscribing happen asynchronously, which allows the publisher and subscriber to work independently of each other.

### Example

Let's create a small Python project that implements the Pub/Sub pattern using the redis-py library to interact with Redis. This project will consist of two parts: a publisher and a subscriber.

We have prepared the files:

- [publisher.py](/Redis/pubsub_example/publisher.py)
- [subscriber.py](/Redis/pubsub_example/subscriber.py)
- [Dockerfile](/Redis/pubsub_example/Dockerfile)
- [Docker-compose.yml](/Redis/pubsub_example/Docker-compose.yml)
- [Dockerfile.publisher](/Redis/pubsub_example/Dockerfile.publisher)
- [Dockerfile.subscriber](/Redis/pubsub_example/Dockerfile.subscriber)

Let's start by building the publisher:

```Terminal
sudo docker-compose up --build
```

The publisher will connect to Redis and send a message to the channel.

```Terminal
sudo docker-compose up --build publisher
```

The subscriber will connect to Redis and subscribe to the channel.

```Terminal
sudo docker-compose up --build subscriber
```

Now you can send a message to the publisher. The subscriber will receive the message and print it to the console.

![Pub/Sub example](/Redis/img/Redis_pub_sub.png)
![Pub example](/Redis/img/Redis_pub.png)
![Sub example](/Redis/img/Redis_sub.png)

In our Python code interpretation, we added commands for the subscriber that allow you to query the status or view subscriptions using commands.

![Pub/Sub commands](/Redis/img/Redis_sub_commands.png)

## Conclusion

Let's consolidate the knowledge we've gained

### Task 1

Practical work objective:

- Learn how to perform simple queries in Redis.

What needs to be done

- Write a sequence of commands for Redis:
- Create an index key with the value “index precalculated content”.
- Check if the index key exists in the database.
- Find out how long the index key will exist.
- Cancel the scheduled deletion of the index key.

What is assessed

- Correct sequence of commands.

![Task 1](/Redis/img/Redis_task_one.png)

- SET: Sets the value for the specified key. If the key already exists, its value will be overwritten.
- EXISTS: Checks if the specified key already exists in the database. Returns 1 if the key exists and 0 if it does not.
- TTL: Returns the remaining lifetime of the key in seconds. If the key does not have a lifetime set, returns -1.
- PERSIST: Removes the lifetime of the key, making it permanent. If the key does not have a lifetime, the command will not change it.

### Task 2

Practical work objective:

- Learn how to work with data structures in Redis.

What needs to be done
Write a sequence of commands for Redis:

- Create a data structure in Redis with the ratings key to store the following technology rating values: mysql — 10, postgresql — 20, mongodb — 30, redis — 40.
- Increase the mysql rating value by 15 using the same key.
- Remove the element with the maximum value from the structure.
- Display the ranking for mysql.

What is assessed

- Correct sequence of commands.

![Task 2](/Redis/img/Redis_task_two.png)

- Create a hash:

```Terminal
localhost:6379>HSET ratings mysql 10 postgresql 20 mongodb 30 redis 40
```

- Increase ratings:

```Terminal
localhost:6379>HINCRBY ratings mysql 15
```

- Get all values:

```Terminal
localhost:6379>HGETALL ratings
```

- Remove the item with the maximum value (e.g. redis):

```Terminal
localhost:6379>HDEL ratings redis
```

- Get all values ​​again and determine the location for mysql:

```Terminal
localhost:6379>HGETALL ratings
```

### Task 3

Practical work objective:

- Learn how to work with the Pub/Sub mechanism in Redis.

What needs to be done

- Write two commands for the Redis DBMS:
- Subscribe to all events published in channels starting with events.
- Publish a message in the events101 channel with the text “Hello there”.

What is assessed

- Correct sequence of commands.

![Task 3](/Redis/img/Redis_task_three.png)

1. Open the first client for subscription

```Redis
localhost:6379>redis-cli -h localhost -p 6379
```

Subscribe using the command:

```Redis
localhost:6379>PSUBSCRIBE events*
```

2. Open the second client for subscription and connect to the same server. Publish a message on the events101 channel with the text “Hello there”:

```Redis
localhost:6379>redis-cli -h localhost -p 6379
```

```Redis
localhost:6379>PUBLISH events101 "Hello there"
```

### Task 4

Practical work objective:

- Learn how to work with stored functions in Redis.

What needs to be done

- Save a function in Redis that takes a key and a value and stores the square root of the value under the specified key.

What is assessed

- Correct query.

The [Lua](/Redis/square.lua) script will take two arguments: a key and a value, calculate the square root of the value, and store the result under the specified key.

```Terminal
redis-cli -h localhost -p 6379 SCRIPT LOAD "local key = ARGV[1]; local value = tonumber(ARGV[2]); local sqrt_value = math.sqrt(value); redis.call('SET', key, sqrt_value); return sqrt_value;"
```

```Terminal
redis-cli -h localhost -p 6379 EVALSHA 83279e2d164f777a0c213ed649d33537166bd8de 0 my_key 25
```
