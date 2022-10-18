import hashlib
import multiprocessing
from itertools import product
import msvcrt
import time
import os

hashlist = ['1']
print("hello world")

working = True
commonpath = "hash.txt"
alphabet = 'abcdefghijklmnopqrstuvwxyz'
keys = ('h', 'H', 'р', 'Р', 'l', 'L', 'д', 'Д', 'q', 'Q', 'й', 'Й')
hash_messages = ["Выгрузить хеши из файла", "Ввести значения хешей с клавиатуры"]
brute_messages = ["Запустить однопоточный перебор", "Запустить параллельный перебор"]


def encode(string):
    return string.encode('UTF-8')


def decode(string):
    return string.decode("UTF-8")


def extractFromFile(path):
    hashes = []
    file = open(path, "r")
    hashes = file.read().split()
    file.close()
    return hashes


def GetHashFromColsole():
    hashes = []
    os.system("cls")
    print("Введите значения хешей. Закончите ввод пустой строкой")
    while True:
        stringhash = input()
        if stringhash == '':
            break
        hashes.append(stringhash)
    return hashes


def StraightBruteForce():
    start = time.time()
    for chars in product(alphabet, repeat=5):
        word = '{0}{1}{2}{3}{4}'
        word = (word.format(*chars))
        password = hashlib.sha256(encode(word))
        decoded = password.hexdigest()
        if decoded in hashlist:
            print("word", word, "was hashed as:", decoded)
            hashlist.remove(decoded)
            if len(hashlist) == 0:
                break
    print(f'На прямой перебор затрачено {time.time() - start:.5f} секунд')


def ParallelBruteForce(start: int):
    global hashlist
    hashes = hashlist[:]
    print(hashes)
    for chars in product('abcdefghijklmnopqrstuvwxyz', repeat=4):
        part2 = '{0}{1}{2}{3}'
        part2 = (part2.format(*chars))
        word = chr(start) + part2
        password = hashlib.sha256(word.encode("utf-8"))
        decoded = password.hexdigest()
        if decoded in hashes:
            print("word", word, "was hashed as:", decoded)
    return 0


def start():
    global hashlist
    hashlist = extractFromFile(commonpath)
    with multiprocessing.Pool(processes=26) as p:
        print(hashlist)
        p.map(ParallelBruteForce, range(97, 97 + 26))


def ChasingMenu(msgbox):
    os.system("cls")
    size = len(msgbox)
    choosen = 0
    key = chr(0)
    while ord(key) != 13:
        os.system("cls")
        for i in range(size):
            print(str(i + 1) + ". " + msgbox[i], end=(' <-\n' if choosen == i else '\n'))
        key = msvcrt.getch()
        if (ord(key)) == ord('s') and choosen + 1 <= size - 1:
            choosen += 1
        elif (ord(key) == ord('w')) and choosen - 1 >= 0:
            choosen -= 1
        elif ord(key) == 13:
            break
    return choosen


def menu():
    choosen = ChasingMenu(hash_messages)
    if choosen == 1:
        GetHashFromColsole()
    elif choosen == 0:
        extractFromFile(commonpath)
    brutetype = ChasingMenu(brute_messages)
    os.system("cls")
    if brutetype == 0:
        print("Запуск прямого перебора...")
        StraightBruteForce()
    elif brutetype == 1:
        print("Запуск многопоточного перебора...")
        start()
    return


if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')
    start()