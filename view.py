from Core import *
import argparse

# _______________________________________________________________________________________ ||
parser = argparse.ArgumentParser()
parser.add_argument("--inputPath",action="store")
parser.add_argument("--verbose",action="store_true")
option = parser.parse_args()

# _______________________________________________________________________________________ ||
# Read account record
reader = PaymentReader("Reader")
reader.readTextFile(option.inputPath)

for payment in reader.dict["payments"]:
    print "-"*60
    print payment
print "-"*60
