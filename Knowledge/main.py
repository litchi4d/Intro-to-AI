from logic import *
harry = Symbol("Harry")
rain = Symbol("Rain")
dumboldore = Symbol("Dumboldore")
sen = And(rain,dumboldore)
print(sen.formula())
