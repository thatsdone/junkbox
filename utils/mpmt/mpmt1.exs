#!/usr/bin/elixir
#
# mpmt1.exs: Elixir version of mpmt1.py
#
# License:
#   Apache License, Version 2.0
# History:
#   * 2022/04/16 v0.1 Initial version
# Author:
#   Masanori Itoh <masanori.itoh@gmail.com>
# TODO:
#   * Show PID not reference at process termination time.
#
defmodule Mpmt1 do

  def busy_worker(idx, time_left) do
    IO.inspect("busy_worker: started. idx = #{idx} time_left = #{time_left}")
    now = :os.system_time(:millisecond)
    busy_loop(now, time_left)
  end

  def busy_loop(current, time_left) when time_left > 0 do
    now = :os.system_time(:millisecond)
    busy_loop(now, time_left - (now - current) / 1000.0)
  end

  def busy_loop(_current, time_left) do
    IO.inspect("busy_worker: expired. time_left = #{time_left}")
  end

end

#
# main routine
#
p = OptionParser.parse(System.argv,
  switches: [num_context: :integer, duration: :float],
  aliases: [n: :num_context, d: :duration]
)
num_context = Keyword.get(elem(p, 0), :num_context, 2)
duration = Keyword.get(elem(p, 0), :duration, 5.0)
IO.inspect("mpmt1.exs: num_context = #{num_context} duration = #{duration}")


pid_list = Enum.map(Enum.to_list(1..num_context),
  fn x ->
    spawn(Mpmt1, :busy_worker, [x, duration])
  end
)

ref_list = Enum.map(pid_list,
  fn x ->
    Process.monitor(x)
  end
)

for ref <- ref_list do
    receive do
      {:DOWN, ^ref, _, _, _} ->
	IO.inspect("#{inspect(ref)} finished.")
    end
end
