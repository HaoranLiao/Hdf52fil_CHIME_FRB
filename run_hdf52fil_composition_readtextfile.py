import filterbank
import numpy as np
import h5py
import sys

DEBUG = False

Pol_Separate = False

header={'data_type': 1,
 'fch1': 800.0,              # central frequency (MHz) of the first channel in the spectrum array
 'foff': -0.4,                   # frequency offset (MHz) for each subsequent channel.
 'machine_id': 0,
 'nbits': 32,                # number of bits per sample (e.g. float32)
 'nchans': 1024,             # number of channels
 'nifs': 1,
 'source_name': 'CHIME_FRB',
 'telescope_id': 0,
 'tsamp': 0.001,             # sampling time in seconds
 'tstart': 50000.0}

input_txt = sys.argv[1]
with open(input_txt) as f:
    content = f.readlines()
content = [x.strip() for x in content]

hd = h5py.File(content[0])

header['nchans'] = hd.items()[1][1].shape[0]
header['fch1'] = hd.values()[0].values()[0][0]/(1e6)                                                                            # in MHz
header['foff'] = (hd.values()[0].values()[0][1]-hd.values()[0].values()[0][0])/(1e6)            # -24414.0625 / 1e6 in MHz
header['tstart'] = hd.values()[0].values()[2][0]
header['tsamp'] =  hd.values()[0].values()[2][1]-hd.values()[0].values()[2][0]

num_polzn = hd.values()[0].values()[1].shape[0]
if Pol_Separate:   
   for polzn in range(num_polzn):
		outFileName = 'compo_p%s.fil'%(str(polzn))
		fil = filterbank.create_filterbank_file(outFileName, header=header, nbits=32, verbose=DEBUG)
		for line in content:
			hd = h5py.File(line)
        	print(hd.filename)
        	data = hd.values()[1]
        	fil.append_spectra(np.transpose(np.squeeze(data[:,polzn,:])))
else:
	outFileName = 'compo_pall.fil'
	fil = filterbank.create_filterbank_file(outFileName, header=header, nbits=32, verbose=DEBUG)
	for polzn in range(num_polzn):
		for line in content:
			hd = h5py.File(line)
			print(hd.filename)
			data = hd.values()[1]
			fil.append_spectra(np.transpose(np.squeeze(data[:,polzn,:])))

fil.close()

hd.close()
