--
-- mpmt1.lua: A Lua version of mpmt1.py
--  dispatcher portion is based on:
--    https://www.lua.org/pil/9.4.html
--
-- License:
--   Apache License, Version 2.0
-- History:
--   * 2022/01/02 v0.1 Initial version
-- Author:
--   Masanori Itoh <masanori.itoh@gmail.com>
-- Note:

-- TOTO:
--   * Explore getopt

function busy_worker(id, duration)
    print(string.format("busy_worker: id: %d duration: %d", id, duration))
    local count = 0
    local ts_save = os.clock()
    while true do
       ts = os.clock()
       if (ts - ts_save) >= duration then
         print(string.format("Expired! %f / %d", ts - ts_save, count))
         break
       end
       count = count + 1
       coroutine.yield(1)
    end
end

--
--
--
num_context = 4
duration = 10
mode = 'c'

-- uses 'lua-posix'
-- local getopt = require "posix.unistd".getopt
-- local last_index = 1
-- for r, optarg, optind in getopt(arg, 'n:d:m:h') do
--   if r == '?' then
--     return print('Unsupported option', arg[optind -1])
--   end
--   last_index = optind
--   if r == 'h' then
--     print '-h      print this help text'
--     print '-n ARG  number of context'
--     print '-d ARG  duration'
--     print '-d ARG  mode (t: thread, p: process'
--   elseif r == 'n' then
--     num_context = optarg
--   elseif r == 'd' then
--     duration = optarg
--   elseif r == 'm' then
--       mode = optarg
--    end
-- end


print(string.format("num_context: %d duration: %d mode: %s",
                                  num_context, duration, mode))

threads = {}
for i = 1, num_context, 1 do
  print(string.format("Creating a coroutine i = %d", i))
  local th = coroutine.create(
      function()
--         print("calling busy_worker()")
         busy_worker(i, duration)
        end
  )
  coroutine.resume(th)
--  print(coroutine.status(th))
  table.insert(threads, th)
end


-- print(#threads)

-- dispatcher routine
while true do
--  local n = table.getn(threads)
  local n = #threads
  if n == 0 then break end
  for i = 1, n do
    local status, res = coroutine.resume(threads[i])
    if not res then
      table.remove(threads, i)
      break
    end
  end
end


-- print(string.format("busy_worker: %d", busy_worker(num_context, duration)))
