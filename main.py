# XMAS-Crypto-Puzzle
# Inspired by Ronald L. Rivest. December 22, 2021.
# More info: http://people.csail.mit.edu/rivest/lcs35-puzzle-description.txt

# Puzzle parameters
n = 5282449308163313563859644746297215365863349077961746596247430181965949736011111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111058286618029477975472514663648138957452477620331493645148636809291451613751

t = 9999999996

z = 668982906662259241898499065103473245960164961956379608176477385568916730412708940627183786580130305413916213903107370821687807114455622233129065284523542286660747383208859057005014109901179025180585657310560580373893562272798582372082139636432607739424027324558809706621124173160967213211956896669859138626558962483744668579313732058599658824157337817420528373805887095539165385293563750768

import time
import timeit
import pickle
import os.path
import math

# Replace actual parameters with small values for testing
n = 11*23 # = 253
t = 10
z = 0x13 # (hex)

# compute 2^(2^t) (mod n)

LOGGING_FREQUENCY = 1000000   # log intermediate result every # iterations
PERSISTENT_DATA_FILE = "rivest_real_test.pkl"

def save_data(result, i, total_time):
    data = {"result": result, "i": i, "total_time": total_time}
    file = open(PERSISTENT_DATA_FILE, 'wb')
    pickle.dump(data, file)
    file.close()


def load_data():
    file = open(PERSISTENT_DATA_FILE, 'rb')
    data = pickle.load(file)
    file.close()
    return data["result"], data["i"], data["total_time"]

# Create data file if not exists
if not os.path.isfile(PERSISTENT_DATA_FILE):
    # initial data
    save_data(2, 0, 0)

# Load data to (re)start
result, start_i, time_offset = load_data()

# Current start time
start_time = timeit.default_timer()

logging_count = 0

# taking larger steps speeds up the algorithm, but when making steps too large it slows down again
# optimum seems te be around 8
STEP = 8
power_of_two = 2**STEP
for i in range(start_i, t, STEP):
    # correct power for final step
    if i + STEP >= t:
        power_of_two = 2**(t - i)

    result = pow(result, power_of_two, n)

    # Log and save data
    logging_count += STEP # addition is less expensive than modulo
    if logging_count > LOGGING_FREQUENCY or i + STEP >= t:
        logging_count = 0
        print(f"-----------------------------------------------------")
        print(f"t = {i+STEP}, intermediate result = {result}")
        stop_time = timeit.default_timer()
        total_time = time_offset + stop_time - start_time
        print(f"progress = {i / t * 100: .2f}%, current running time = {stop_time - start_time: .2f}s, total time = {total_time: .2f}s")

        save_data(result, i+STEP, total_time) # increase i, to restart at next iteration with current result

print(f"2^(2^{t}) = {result}")
print(f"{hex(z)} (z) XOR {result} = {hex(z ^ result)}")

decoded_int = z ^ result

byte_size = math.ceil(math.log(decoded_int,2) / 8)

bytes_val = decoded_int.to_bytes(byte_size, 'big')

print("Message: ", bytes_val.decode("utf-8") )

