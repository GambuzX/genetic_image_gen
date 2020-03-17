#!/bin/python
from random import *
import struct

def value(bits1, bits2):
    similar = 0
    for i in range(len(bits1)):
        if bits1[i] == bits2[i]:
            similar += 1
    return similar

def mutate(bits):
    cut = randrange(0, len(bits))
    return bits[:cut] + ('1' if bits[cut] == '0' else '0') + bits[cut+1:]

def reproduce(bits1, bits2):
    slice = randrange(1, len(bits1)-1)
    return bits1[:slice] + bits2[slice:]

def gen_random_population(size, genome_size):
    pop = []
    for i in range(size):
        genome = ""
        for j in range(genome_size):
            genome += "1" if random() >= 0.5 else "0"
        pop.append(genome)
    return pop

def roullete_select(population, val, target):

    choice = random()
    cumulative_values = []
    total = 0
    for pop in population:
        v = val(pop, target)
        total += v
        cumulative_values.append(total)
    for i in range(len(cumulative_values)):
        cumulative_values[i] = cumulative_values[i] * 1.0 / total

        if i == 0 and choice <= cumulative_values[i]:
            return population[i]

        if cumulative_values[i-1] < choice and choice <= cumulative_values[i]:
            return population[i]

    print("did not find")
    return population[0]

def select_best(population, value, target):
    max_i = 0
    max_val = value(population[0], target)
    for i in range(1, len(population)):
        v = value(population[i], target)
        if v > max_val:
            max_i = i
            max_val = v
    return population[max_i]

def write_image(bits, generation):
    f = open('generations/gen' + str(generation) + '.jpg', 'wb')
    bits = [bits[8*i: 8*(i+1)] for i in range(int(len(bits)/8))]
    bits = [int(i,2) for i in bits]
    for i in bits:
        f.write(bytes([i]))
    f.close()


def bin_from_hex(hex_val):
    return bin(int(hex_val, 16))[2:].zfill(8)

def get_bits(byte):
    return bin_from_hex(hex(int.from_bytes(byte, "little")))

target = ""
with open("original.jpg", "rb") as f:
    byte = f.read(1)
    target += get_bits(byte)
    while byte != b"":
        byte = f.read(1)
        target += get_bits(byte)

population_size = 100
generations = 100


print("[+] Generating initial population")
population = gen_random_population(population_size, len(target))
for g in range(generations):
    print("[+] Starting generation " + str(g+1))
    new_population = []
    for p in range(population_size):
        print("... %d\r" % (p+1), end="")
        
        x = roullete_select(population, value, target)
        y = roullete_select(population, value, target)
        child = reproduce(x,y)
        
        if randrange(0, 10000) == 1: 
            mutate(child)
        
        new_population.append(child)
    population = new_population
    print("[+] Selecting best option")
    best = select_best(population, value, target)
    write_image(best, g+1)
    