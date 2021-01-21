import numpy as np
import adios2

fileName = "steps_int32.bp"
total_steps = 100

#write data
with adios2.open(fileName, "w") as fh:
    for i in range(total_steps):
        fh.write("step", np.array([i], dtype=np.int32), [1], [0], [1])
        fh.end_step()
        print("written {}".format(i))

#read from n to the end
from_n = 20
adios = adios2.ADIOS()
ioReadBP = adios.DeclareIO("hellopy")

f = ioReadBP.Open(fileName, adios2.Mode.Read)
total_steps = f.Steps()
print(total_steps)
var = ioReadBP.InquireVariable("step")
var.SetStepSelection([from_n, total_steps - from_n])
data = np.zeros(total_steps - from_n, dtype=np.int32)
f.Get(var, data, adios2.Mode.Sync)
print(data)
