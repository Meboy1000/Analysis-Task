import pandas as pd
import h5py
import numpy as np
import matplotlib.pyplot as plt
import time

file_name = "Final_Analysis\chunk2.hdf5"
csv_file = "Final_Analysis\chunk2.csv"

# extracts part of seismogramp between p and s arrival, pads, and returns fourier transform of that
def transform(array, psample, ssample):
    array = array[psample: min(ssample, psample+200)]
    avg = np.average(np.abs(array))
    mul = 50/avg
    array = array * mul
    pad = int((400 - len(array))/2)
    array = np.pad(array, (pad,), 'constant', constant_values=0)
    if (len(array) < 400):
        xtras = 400 - len(array)
        for x in range(xtras):
            array = np.append(array, 0)
    results = np.fft.fft(array)
    freq = np.fft.fftfreq(array.shape[-1])
    paired = [results, freq]
    return paired

# gets median and standard deviation of each frequency amplitude
def arrs_to_avg(array, freq):
    data =[]
    for i in range(400):
        real_arr = []
        imag_arr = []
        for element in array:
            real_arr.append(element.real[i])
            imag_arr.append(element.imag[i])
        data.append([[np.median(real_arr), np.std(real_arr)], [np.median(imag_arr), np.std(imag_arr)], freq[i]])
    return data

# reading the csv file into a dataframe:
df = pd.read_csv(csv_file)
print(f'total events in csv file: {len(df)}')
dtfl = h5py.File(file_name, 'r')

receivers = df["receiver_code"].value_counts().index.to_list()

receiver_data = []

for code in receivers:
    t1 = time.perf_counter()
    tdf = df[(df.receiver_code == code)]
    print(f'total events selected: {len(tdf)}')
    print(tdf)

    # making a list of trace names for the selected data
    ev_list = tdf['trace_name'].to_list()

    # prepare arrays for extracted data
    xfreqs = []
    yfreqs = []
    zfreqs = []
    # retrieving selected waveforms from the hdf5 file: 
    freq = []
    for c, evi in enumerate(ev_list):
        t1 = time.perf_counter()
        dataset = dtfl.get('data/'+str(evi)) 
        # waveforms, 3 channels: first row: E channel, second row: N channel, third row: Z channel 
        data = np.array(dataset)
        xarray = data[:,0]
        yarray = data[:,1]
        zarray = data[:,2]

        # p wave arrival sample and s wave arrival sample indices
        psample = int(dataset.attrs['p_arrival_sample'])
        ssample = int(dataset.attrs['s_arrival_sample'])

        xfreqs.append(transform(xarray, psample, ssample)[0])
        yfreqs.append(transform(yarray, psample, ssample)[0])
        zfreqs.append(transform(zarray, psample, ssample)[0])

        if len(freq) == 0:
            freq = transform(xarray, psample, ssample)[1]

    xdata = arrs_to_avg(xfreqs, freq)
    ydata = arrs_to_avg(yfreqs, freq)
    zdata = arrs_to_avg(zfreqs, freq)
    xplot = []
    for thing in xdata:
        xplot.append(abs(thing[0][0]))
    receiver_data.append([code, xdata, ydata, zdata])
    fig = plt.figure()
    ax = fig.add_subplot(111)         
    plt.plot(xplot)
    plt.rcParams["figure.figsize"] = (8, 5)
    legend_properties = {'weight':'bold'}    
    plt.tight_layout()
    ymin, ymax = ax.get_ylim()
    ax.set_xticklabels([])
    plt.show()
    t2 = time.perf_counter()
    print("time:", t2-t1) 
print(receiver_data)
