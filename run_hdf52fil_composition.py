import filterbank
import numpy as np
import h5py

DEBUG = False

header={'data_type': 1,
 'fch1': 800.0,              # central frequency (MHz) of the first channel in the spectrum array
 'foff': -0.4,          	 # frequency offset (MHz) for each subsequent channel.
 'machine_id': 0,
 'nbits': 32,                # number of bits per sample (e.g. float32)
 'nchans': 1024,             # number of channels
 'nifs': 1,
 'source_name': 'CHIME_FRB',
 'telescope_id': 0,
 'tsamp': 0.001,             # sampling time in seconds
 'tstart': 50000.0} 

hd = h5py.File('00000000.h5')

header['nchans'] = len(hd.items()[1][1][:,0,0])
header['fch1'] = hd.values()[0].values()[0][0]/(1e6)										# in MHz
header['foff'] = (hd.values()[0].values()[0][1]-hd.values()[0].values()[0][0])/(1e6)		# -24414.0625 / 1e6 in MHz
header['tstart'] = hd.values()[0].values()[2][0]
header['tsamp'] =  hd.values()[0].values()[2][1]-hd.values()[0].values()[2][0]

n = 50

outFileName = 'composition_0_%s.fil'%n
fil = filterbank.create_filterbank_file(outFileName, header=header, nbits=32, verbose=DEBUG)

for i in range(n):
    if i<10:
        hd = h5py.File('0000000%i.h5'%i)
    elif i<100:
        hd = h5py.File('000000%i.h5'%i)
    elif i<1000:
        hd = h5py.File('00000%i.h5'%i)
    elif i<10000:
        hd = h5py.File('0000%i.h5'%i)
    print(hd.filename)
    data = hd.values()[1]
    fil.append_spectra(np.transpose(np.squeeze(data[:,0,:])))

fil.close()

hd.close()
