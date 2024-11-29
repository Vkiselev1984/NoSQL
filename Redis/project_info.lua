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