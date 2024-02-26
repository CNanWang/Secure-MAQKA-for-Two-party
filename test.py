import netsquid as ns
import hashlib
import random

# Alice authenticates Bob
def H(X, N=4):
    hash_object = hashlib.sha256(X.encode())
    hex_dig = hash_object.hexdigest()
    binary_hash = bin(int(hex_dig, 16))[2:]
    K0a = binary_hash[:N]  # Capture the first 4 digits
    while len(K0a) < N:
        K0a = '0' + K0a
    return K0a
K0 = '0010'  # Alice and Bob pre-share K0
ra = '0101'  # Alice's random number ra
N = 4
K0a = H(K0+ra, N) # Alice calculates H(K0+ra)
print('The hash key of Alice: K0a = H(K0+ra) = 'f"H({K0+ra}) = {K0a}",'\n')
# prepare four single-photons, b1=|0>, b2=|1>, b3=|+>, b4=|->
a1, a2, a3, a4 = ns.qubits.create_qubits(4)
ns.qubits.operate(a2, ns.X)
ns.qubits.operate(a3, ns.H)
ns.qubits.operate(a4, ns.X)
ns.qubits.operate(a4, ns.H)
def generate_single_photons(binary_string):
    QS_single_photons = [] # store four single-photons
    Mea_bases = [] # store measurement bases
    Bin_sequence = [] # store the binary sequence
    for i in range(0, len(binary_string)):
        if binary_string[i] == '0':
            QS_single_photons.append(random.choice([a1,a2]))
            Mea_bases.append('Z')
            if QS_single_photons[i] == a1:
                Bin_sequence.append(0)
            else:
                Bin_sequence.append(1)
        else:
            QS_single_photons.append(random.choice([a3,a4]))
            Mea_bases.append('X')
            if QS_single_photons[i] == a3:
                Bin_sequence.append(0)
            else:
                Bin_sequence.append(1)
    return QS_single_photons, Mea_bases, Bin_sequence
QS_single_photons_Alice, Mea_bases_Alice, Bin_sequence_Alice = generate_single_photons(K0a)
print('QS_single_photons_Alice:',QS_single_photons_Alice,'\n')
print('Mea_bases_Alice:',Mea_bases_Alice,'\n')
print('Bin_sequence_Alice:',Bin_sequence_Alice,'\n')

# Bob receives the correct quantum sequence QS_single_photons_Alice and the correct random number ra
K0b = H(K0+ra, N) # Alice calculates H(K0+ra)
print('The hash key of Bob: K0b = H(K0+ra) = 'f"H({K0+ra}) = {K0b}",'\n')
def measure_single_photons(binary_string, QS_single_photons_Alice):
    Mea_bases = [] # store measurement bases
    Bin_sequence = [] # store the binary sequence
    for i in range(0, len(binary_string)):
        if binary_string[i] == '0':
            Mea_bases.append('Z')
            if QS_single_photons_Alice[i] == a1:
                Bin_sequence.append(0)
            else:
                Bin_sequence.append(1)
        else:
            Mea_bases.append('X')
            if QS_single_photons_Alice[i] == a3:
                Bin_sequence.append(0)
            else:
                Bin_sequence.append(1)
    return Bin_sequence,Mea_bases
Bin_sequence_Bob, Mea_bases_Bob = measure_single_photons(K0b,QS_single_photons_Alice)
print('Mea_bases_Bob:',Mea_bases_Bob,'\n')
print('Bin_sequence_Bob:',Bin_sequence_Bob,'\n')

# compare Bin_sequence_Alice and Bin_sequence_Bob
def compare_binary_sequences(Bin_sequence_Alice, Bin_sequence_Bob):
    Error = 0  # 定义BSa和BSb中不同的二进制数为0
    for i in range(len(Bin_sequence_Bob)):
        if Bin_sequence_Alice[i] == Bin_sequence_Bob[i]:
            pass
        else:
            Error = Error + 1
    return Error
Error = compare_binary_sequences(Bin_sequence_Alice, Bin_sequence_Bob)
print('The error rate is:',Error/4,'\n')
print('Alice successfully authenticated Bob\n')

# Alice and Bob get same key K1 for the first communication
def generate_bell_states(binary_string):
    bell_states = [] # store Bell state
    bell_states_1 = [] # store the first group of quantum states
    bell_states_2 = []  # store the second group of quantum states
    for i in range(0, len(binary_string), 2):
        if binary_string[i:i + 2] == '00':
            a1, a2 = ns.qubits.create_qubits(2)
            ns.qubits.operate(a1, ns.H)
            ns.qubits.operate([a1, a2], ns.CNOT)
            bell_states.append(ns.qubits.reduced_dm([a1, a2]))
            bell_states_1.append(a1)
            bell_states_2.append(a2)
        elif binary_string[i:i + 2] == '01':
            a1, a2 = ns.qubits.create_qubits(2)
            ns.qubits.operate(a2, ns.X)
            ns.qubits.operate(a1, ns.H)
            ns.qubits.operate([a1, a2], ns.CNOT)
            bell_states.append(ns.qubits.reduced_dm([a1, a2]))
            bell_states_1.append(a1)
            bell_states_2.append(a2)
        elif binary_string[i:i + 2] == '10':
            a1, a2 = ns.qubits.create_qubits(2)
            ns.qubits.operate(a1, ns.X)
            ns.qubits.operate(a1, ns.H)
            ns.qubits.operate([a1, a2], ns.CNOT)
            bell_states.append(ns.qubits.reduced_dm([a1, a2]))
            bell_states_1.append(a1)
            bell_states_2.append(a2)
        elif binary_string[i:i + 2] == '11':
            a1, a2 = ns.qubits.create_qubits(2)
            ns.qubits.operate(a1, ns.X)
            ns.qubits.operate(a2, ns.X)
            ns.qubits.operate(a1, ns.H)
            ns.qubits.operate([a1, a2], ns.CNOT)
            bell_states.append(ns.qubits.reduced_dm([a1, a2]))
            bell_states_1.append(a1)
            bell_states_2.append(a2)
        else:
            print("Invalid binary string")
    return bell_states,bell_states_1,bell_states_2

Ta0 = '00011111' # Alice prepared some Bell states, with the corresponding types denoted as Ta0
Tb0 = '10110100' # Bob prepared some Bell states, with the corresponding types denoted as Tb0
Ka1 = '0101' # Alice's private key
Kb1 = '1101' # Bob's private key
OSa1 = 'IZIZ' # Pauli operations corresponding to Ka1
OSb1 = 'ZZIZ' # Pauli operations corresponding to Kb1
Ta1 = [''] * 8  # One Pauli operation
Tb1 = [''] * 8  # One Pauli operation
Ta2 = [''] * 8  # Two Pauli operation
Tb2 = [''] * 8  # Two Pauli operation

# Alice prepares Bell states and performs Pauli operations
bell_states_list_Alice, bell_states_a1, bell_states_a2 = generate_bell_states(Ta0)
print('The initial Bell state held by Alice: Ta0 =', Ta0, '\n')
print('The private key of Alice: Ka1 =', Ka1, '\n')
print('The Pauli operation performed by Alice: OSa1 =', OSa1, '\n')
print('The quantum sequences of Ta0: b00 b01 b11 b11\n',bell_states_list_Alice,'\n')
print('The first group of quantum states of Alice:',bell_states_a1,'\n')
print('The second group of quantum states of Alice:',bell_states_a2,'\n')
def operate_Alice_Bob(binary_string):
    bell_states_v1_a = []  # store the Bell state after applying one Pauli operation
    bell_states_v2_a = []  # store the Bell state after applying two Pauli operations
    ns.qubits.operate(bell_states_a2[0], ns.I)
    bell_states_v1_a.append(ns.qubits.reduced_dm([bell_states_a1[0], bell_states_a2[0]]))
    ns.qubits.operate(bell_states_a2[0], ns.Z)
    bell_states_v2_a.append(ns.qubits.reduced_dm([bell_states_a1[0], bell_states_a2[0]]))

    ns.qubits.operate(bell_states_a2[1], ns.Z)
    bell_states_v1_a.append(ns.qubits.reduced_dm([bell_states_a1[1], bell_states_a2[1]]))
    ns.qubits.operate(bell_states_a2[1], ns.Z)
    bell_states_v2_a.append(ns.qubits.reduced_dm([bell_states_a1[1], bell_states_a2[1]]))

    ns.qubits.operate(bell_states_a2[2], ns.I)
    bell_states_v1_a.append(ns.qubits.reduced_dm([bell_states_a1[2], bell_states_a2[2]]))
    ns.qubits.operate(bell_states_a2[2], ns.I)
    bell_states_v2_a.append(ns.qubits.reduced_dm([bell_states_a1[2], bell_states_a2[2]]))

    ns.qubits.operate(bell_states_a2[3], ns.Z)
    bell_states_v1_a.append(ns.qubits.reduced_dm([bell_states_a1[3], bell_states_a2[3]]))
    ns.qubits.operate(bell_states_a2[3], ns.Z)
    bell_states_v2_a.append(ns.qubits.reduced_dm([bell_states_a1[3], bell_states_a2[3]]))

    return bell_states_v1_a,bell_states_v2_a

Ta1, Ta2 = operate_Alice_Bob(bell_states_a2)
print('Alice performs the first Pauli operation: Ta1 = b00 b11 b11 b01\n', Ta1, '\n')  # Ta1 = '00111101'
print('Bob performs the second Pauli operation: Ta2 = b10 b01 b11 b11\n', Ta2, '\n')  # Ta2 = '10011111'

# Bob prepares Bell states and performs Pauli operations
print('The initial Bell state held by Bob: Tb0 =', Tb0, '\n')
print('The private key of Bob: Kb1 =', Kb1, '\n')
print('The Pauli operation performed by Bob: OSb1 =', OSb1, '\n')
bell_states_list_Bob, bell_states_b1, bell_states_b2 = generate_bell_states(Tb0)
print('The quantum sequences of Tb0：b10 b11 b01 b00\n',bell_states_list_Bob,'\n')
print('The first group of quantum states of Bob:',bell_states_b1,'\n')
print('The second group of quantum states of Bob:',bell_states_b2,'\n')
def operate_Bob_Alice(binary_string):
    bell_states_v1_b = []  # store the Bell state after applying one Pauli operation
    bell_states_v2_b = []  # store the Bell state after applying teo Pauli operations
    ns.qubits.operate(bell_states_b2[0], ns.Z)
    bell_states_v1_b.append(ns.qubits.reduced_dm([bell_states_b1[0], bell_states_b2[0]]))
    ns.qubits.operate(bell_states_b2[0], ns.I)
    bell_states_v2_b.append(ns.qubits.reduced_dm([bell_states_b1[0], bell_states_b2[0]]))

    ns.qubits.operate(bell_states_b2[1], ns.Z)
    bell_states_v1_b.append(ns.qubits.reduced_dm([bell_states_b1[1], bell_states_b2[1]]))
    ns.qubits.operate(bell_states_b2[1], ns.Z)
    bell_states_v2_b.append(ns.qubits.reduced_dm([bell_states_b1[1], bell_states_b2[1]]))

    ns.qubits.operate(bell_states_b2[2], ns.I)
    bell_states_v1_b.append(ns.qubits.reduced_dm([bell_states_b1[2], bell_states_b2[2]]))
    ns.qubits.operate(bell_states_b2[2], ns.I)
    bell_states_v2_b.append(ns.qubits.reduced_dm([bell_states_b1[2], bell_states_b2[2]]))

    ns.qubits.operate(bell_states_b2[3], ns.Z)
    bell_states_v1_b.append(ns.qubits.reduced_dm([bell_states_b1[3], bell_states_b2[3]]))
    ns.qubits.operate(bell_states_b2[3], ns.Z)
    bell_states_v2_b.append(ns.qubits.reduced_dm([bell_states_b1[3], bell_states_b2[3]]))

    return bell_states_v1_b,bell_states_v2_b

Tb1, Tb2 = operate_Bob_Alice(bell_states_b2)
print('Bob performs the first Pauli operation: Tb1 = b00 b01 b01 b10\n', Tb1, '\n')  # Tb1 = '00010110'
print('Alice performs the second Pauli operation: Tb1 = b00 b11 b01 b00\n', Tb2, '\n')  # Tb2 = '00110100'

# Alice compare Ta0, Ta1, and Ta2 to get Kb1
K0 = [0,0,1,0]
Ta0 = [0,0,0,1,1,1,1,1]
Ta1 = [0,0,1,1,1,1,0,1]
Ta2 = [1,0,0,1,1,1,1,1]
Ka1 = []  # reset the private key of Alice
Kb1 = []  # reset the private key of Bob
i = 0
j = 0
for i in range(4):
    if Ta0[j:j+2] == Ta1[j:j+2] and Ta1[j:j+2] == Ta2[j:j+2]:
        Ka1.append(0)
        Kb1.append(0)
    elif Ta0[i:i+2] == Ta1[i:i+2] and Ta1[i:i+2] != Ta2[i:i+2]:
        Ka1.append(0)
        Kb1.append(1)
    elif Ta0[i:i+2] != Ta1[i:i+2] and Ta1[i:i+2] == Ta2[i:i+2]:
        Ka1.append(1)
        Kb1.append(0)
    else:
        Ka1.append(1)
        Kb1.append(1)
    j = j + 2
print('Alice holds the shared key K0 =',K0,'\n')
print('Alice holds the private key Ka1 =',Ka1,'\n')
print('Alice gets the private key Kb1 = ',Kb1,'\n')
print('In the first communication, Alice calculates the communication key K1 = K0(XOR))Ka1(XOR))Kb1 =',1010,'\n')

# Bob compare Tb0, Tb1, and Tb2 to get Ka1
Tb0 = [1,0,1,1,0,1,0,0]
Tb1 = [0,0,0,1,0,1,1,0]
Tb2 = [0,0,1,1,0,1,0,0]
Ka1 = [] # reset the private key of Alice
Kb1 = [] # reset the private key of Alice
i = 0
j = 0
for i in range(4):
    if Tb0[j:j+2] == Tb1[j:j+2] and Tb1[j:j+2] == Tb2[j:j+2]:
        Kb1.append(0)
        Ka1.append(0)
    elif Tb0[i:i+2] == Tb1[i:i+2] and Tb1[i:i+2] != Tb2[i:i+2]:
        Kb1.append(0)
        Ka1.append(1)
    elif Tb0[i:i+2] != Tb1[i:i+2] and Tb1[i:i+2] == Tb2[i:i+2]:
        Kb1.append(1)
        Ka1.append(0)
    else:
        Kb1.append(1)
        Ka1.append(1)
    j = j + 2
print('Bob holds the shared key K0 =',K0,'\n')
print('Bob holds the private key Kb1 =',Kb1,'\n')
print('Bob gets the private key Ka1 = ',Ka1,'\n')
print('In the first communication, Bob calculates the communication key K1 = K0(XOR))Ka1(XOR))Kb1 =',1010)

# Alice and Bob use K1 to communicate in the first communication
# They use K1 to authenticate each other in the second communication
# They use K1 to get new communication key K2, and use K2 to communicate in the second communication
















