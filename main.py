# XMAS-Crypto-Puzzle
# Inspired by Ronald L. Rivest. December 22, 2021.
# More info: http://people.csail.mit.edu/rivest/lcs35-puzzle-description.txt

# Puzzle parameters
n = 5282449308163313563859644746297215365863349077961746596247430181965949736011111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111058286618029477975472514663648138957452477620331493645148636809291451613751

t = 9999999996

z = 668982906662259241898499065103473245960164961956379608176477385568916730412708940627183786580130305413916213903107370821687807114455622233129065284523542286660747383208859057005014109901179025180585657310560580373893562272798582372082139636432607739424027324558809706621124173160967213211956896669859138626558962483744668579313732058599658824157337817420528373805887095539165385293563750768

import time
import pickle
import os.path

# Replace actual parameters with small values for testing
n = 11*23 # = 253
t = 10
z = 0x13 # (hex)

# compute 2^(2^t) (mod n)

LOGGING_FREQUENCY = 2   # log intermediate result every # iterations
PERSISTENT_DATA_FILE = "rivest.pkl"


def save_data(result, i):
    data = {"result": result, "i": i}
    file = open(PERSISTENT_DATA_FILE, 'wb')
    pickle.dump(data, file)
    file.close()


def load_data():
    file = open(PERSISTENT_DATA_FILE, 'rb')
    data = pickle.load(file)
    file.close()
    return data["result"], data["i"]

# Create data file if not exists
if not os.path.isfile(PERSISTENT_DATA_FILE):
    # initial data
    save_data(2, 0)

result, start_i = load_data()

logging_count = 0
for i in range(start_i, t):
    result = pow(result, 2, n)

    time.sleep(1)

    logging_count += 1 # addition is less expensive than modulo
    if logging_count == LOGGING_FREQUENCY:
        logging_count = 0
        print(f"-----------------------------------------------------")
        print(f"t = {i+1}, intermediate result = {result}")
        print(f"progress = {int((i/t)*10000)/100}%")
        save_data(result, i+1) # increase i, to restart at next iteration with current result

print(f"2^(2^{t}) = {result}")
print(f"{hex(z)} (z) XOR {result} = {hex(z ^ result)}")

