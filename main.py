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
# n = 11*23 # = 253
# t = 10
# z = 0x13 # (hex)

# compute 2^(2^t) (mod n)

LOGGING_FREQUENCY = 1000000   # log intermediate result every # iterations
PERSISTENT_DATA_FILE = "rivest_real.pkl"

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

def print_decoded_message(message, key):
    # # split z and the key (result) into bytes

    z_bytes = []
    z_temp = message
    while z_temp > 0:
        z_bytes.insert(0, (z_temp & 0xff))
        z_temp = z_temp >> 8

    key_bytes = []
    key_temp = key
    while key_temp > 0:
        key_bytes.insert(0, (key_temp & 0xff))
        key_temp = key_temp >> 8

    # repeat left to right
    # for i in range(len(z_bytes)):
    #     print(chr(z_bytes[i] ^ key_bytes[(i+0) % len(key_bytes)]), end='')

    # repeat right to left
    for i in range(len(z_bytes)):
        print(chr(z_bytes[i] ^ key_bytes[(i+(len(z_bytes) % len(key_bytes))) % len(key_bytes)]), end='')

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

print(f"2^(2^{t}) =")
print(f"{result}")
print()
print(f"{hex(z)} (z)")
print("XOR")
print(f"{result}")
print("=")
print(f"{hex(z ^ result)}")

# calculate result
decoded_int = z ^ result

# convert to hex
decoded_hex = hex(decoded_int)

# remove 0x
decoded_hex = decoded_hex[2:]

print()
print("Decoded message (hex)")
decoded_hex = f"0{decoded_hex}"

print(decoded_hex)

print_decoded_message(z, result)

print()

# Hint:
#
#          ¥
#         /|\
#        /*|O\
#       /*/|\*\
#      /X/O|*\X\
#     Ô   |X|   Ô
#         |X|
#    11111.....11111
#
# ?

# # Guess: binary number, size fixed, dots can be anything
# high_value = 31 << 10
# low_value = 31 << 0
#
# for i in range(32):
#     possible_solution = high_value + i << 5 + low_value
#     remainder = n % possible_solution
#     if remainder == 0:
#         print("Dots can be anything binary found a solution")
#         print(f"FOUND: {possible_solution}")
#         break
#
# # Guess: decimal number, size fixed, dots can be anything
# high_value = 111110000000000
# low_value = 11111
#
# for i in range(100000):
#     possible_solution = high_value + i * 100000 + low_value
#     remainder = n % possible_solution
#     if remainder == 0:
#         print("Dots can be anything decimal found a solution")
#         print(f"FOUND: {possible_solution}")
#         break
#
# # Guess: binary number, size not fixed, all 1's
# possible_solution = 1
# for i in range(1500):
#     possible_solution = possible_solution * 2 + 1
#     if possible_solution > n:
#         print("> n, all 1's binary")
#         break
#     remainder = n % possible_solution
#     if remainder == 0:
#         print("All 1's binary found a solution")
#         print(f"FOUND: {possible_solution}")
#         break

# Guess: decimal number, size not fixed, all 1's
possible_solution = 1
for i in range(1000):
    possible_solution = possible_solution * 10 + 1
    if possible_solution > n:
        print("> n, all 1's decimal")
        break
    remainder = n % possible_solution
    if remainder == 0:
        print("All 1's decimal found a solution")
        # print(f"FOUND: {possible_solution}")
        break


# # Guess: decimal number, size not fixed, dots can be anything
# low_value = 11111
# high_value = 11111
#
# for i in range(1, 10000):
#     mid_size = math.ceil(math.log(i, 10))
#     possible_solution = high_value * (10 ** (mid_size + 5)) + i * 100000 + low_value
#     if possible_solution > n:
#         print("> n, break")
#         break
#     remainder = n % possible_solution
#     if remainder == 0:
#         print("Dots can be anything and any length decimal found a solution")
#         print(f"FOUND: {possible_solution}")
#         break
#
# # Guess: binary number, size not fixed, dots can be anything
# low_value = 31
# high_value = 31
#
# for i in range(1, 1000):
#     mid_size = math.ceil(math.log(i, 2))
#     possible_solution = (high_value << (mid_size + 6)) + (i << 5) + low_value
#     if possible_solution > n:
#         print("> n, break")
#         break
#     remainder = n % possible_solution
#     if remainder == 0:
#         print("Dots can be anything and any length binary found a solution")
#         print(f"FOUND: {possible_solution}")
#         break


first_prime = possible_solution # 11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
second_prime = n // first_prime # 475420437734698220747368027166749382927701417016557193662268716376935476241

print("First (p)")
print(first_prime)
print("Second (q)")
print(second_prime)

# 360th Fibonacci Number
# https://www.thelearningpoint.net/home/mathematics/fibonacci-numbers/fibonacci-numbers-360th

# PART 2

# p and q are known now
p = first_prime
q = second_prime

# but we have new values for t and z
t = 3141592653589793238462643
z = 58583694967857719568672046116858120224587618119822340618189001678393102218990807349308131223453625414513065216230044608830114792473444339822430433495672836848863365341483999187599145505201721404441744151339962772300313013573392190161155464247385927218862457095824188667582050956487344938459381877043300282745011289126832899364508833467936092306093584864909509688669999145388591432781321752053405999394345306317914993220518080983260099633806700399939767499907138690819600153823804412797590316240733611918641828293702084954666972711281741458389444357833972630839408128310744847507844944761696605192126889452293654935399366931927954839785034003941300961561148148937701363614936970991356037672675983395684898670091207675028957490866500389269826055918567928748023929953853362527575068566100630559601797518146074255402807776217148901895395895983845293407127269514808717525674322790355008278506499517329564176094842813183918157463739481898267725974416620524683556065490867282379915014661274021423298819557221587907924881065620383297690634338473353478761759703291065204526874249023628608378886991185243349462684849457312737073483147877452061720402015684269111168981944011524065028034339399196714959004741367615317558248619741996258338710516379223517110014134978361977041153451014133478635871884602602308478477748161294891824891343752787887330947802489164462554570434341625489674243310872822832183966321759244474045474986797299377300746879511316207701505535353329091679861331911810917084115462395494963551325565035150785918022433068819329526239294677712024081816801835153560154914643824312628294706489884755571933971750261957494968858244391617645720892850997304675361034691766864143431112404205671011086125609361900386441447871525249543143943261111622418455247304206775617397436273596556421519654550716051935996873760345890982162397420797331982170363204508895913767070375635666660928272820102114055834572782405278221044530716725142240044619114884818622423953537402180955147012215990306509652166433075079485099368485966738305987936088166947544091867168141157522492473769047782409529280066874028714665160442029264003147130336830113146220131102110001505751271080800565722905191679055550071517712492882055567682302895481572806559418909127075437873983071736625291009957028681745322119521055624413599340807876738876082407365443466097028040221319339088426057605435652790090308574872115652960491285745519310318575189016168438477401894021500135459333372123726057144986497589980770308443104906973440068185199563122427336621840955522439265805994452287658461874434838791500159201489712716061481732901963949730360767585309807146129986938151096041446796068220374337571779703962451506690089756914765852982818150886107513673103338800955016288106770416093413695579157778512059303599937834046433367381472015754088776306371730309739701763576359450656378408683405026635849450544973075826696482059503706556196069755982390940124100102506620237295113332963084633597789784404375088026587973414605651455926822751494799521177832363631832811193618755925240921094854074408309003525245336252050040844615688377428566763924820853494256212699088238390580501327303997930160544110974323244627722709102467227791950805002779965049224605042216318155538578922953973981214684612043115194075286263923004463863920763649752905079830679171042572231101061933740627741023416341493617422647577008517114575486298291636259895086973930828682734097154997579692314448734841943336443316978648365852931198687933167136727021746134837830118101750306538487099731097211349110529643142266198476851786284338181703386931149136090353676631088277854944708222249159713108416057413771356069

# calculating 2^(2^t) (mod n) iteratively will be infeasible now, but we can take advantage of knowing
# the factorization of n!

# Note that z is longer now, so we need to repeat the key

# Hints: https://crypto.stanford.edu/~dabo/cs255/handouts/numth2.pdf

# If N = pq, then phi(N) = (p-1)(q-1) where pgi(n) denotes the number of elements in Z*_N
phi = (p-1) * (q-1)

print()
print(f"phi(N) = {phi}")

# a^phi(N) = 1 mod N, so 2^(2^t) = 1*1*...*1*2^(2^t mod phi(N))
t_mod = pow(2, t, phi)
print(f"t' = {t_mod}")

result = pow(2, t_mod, n)

print(f"2^t' =")
print(f"{result}")

print_decoded_message(z, result)

