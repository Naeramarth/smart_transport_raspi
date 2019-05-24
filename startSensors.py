import multiprocessing as mp

def read_temp():
    print("Temp")

def read_humidity():
    print("humidity")

def read_vibration():
    print("vibration")

def read_preassure():
    print("preassure")



if __name__ == '__main__':
    output = mp.Queue()

    processes = [mp.Process(target=read_temp()),
                 mp.Process(target=read_humidity()),
                 mp.Process(target=read_vibration()),
                 mp.Process(target=read_preassure())
                 ]

    for p in processes:
        p.start()