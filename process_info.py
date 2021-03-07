import psutil
print(psutil.pids())
p=psutil.Process(11432)
print(p)
print(p.name(),p.memory_info())
print(p.memory_full_info())
print(p.threads())
print(p.cmdline())