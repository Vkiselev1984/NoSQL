local key = ARGV[1]
local value = tonumber(ARGV[2])
local sqrt_value = math.sqrt(value)
redis.call('SET', key, sqrt_value)
return sqrt_value