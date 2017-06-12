import filterbank
import h5py
import numpy as np
import sys

DEBUG = True
def dbgmsg(s):
    if DEBUG:
        print("DEBUG:%s"%s)
    return 0

# Initialize Header
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
 'tstart': 50000.0}          # start time in MJD


def hd52fil(inFileName, outFileRoot=None, tstart=None, tsamp=None, fch1=None, foff=None):
    """ 
    Reads in the h5py file storing CHIME data and converts it to a filterbank file. 
    Usage: python hd52fil_chimefrb inFileName (outFileRoot) (tstart) (tsamp) (fch1) (foff)
    inFileName (XX.h5) is assumed to be a h5py file.
    outFileRoot is taken from the inFileName unless specified.
    tstart (MJD), tsamp (sec), fch1 (MHz), foff (MHz) keywords allow overwriting the initialzing values in the header.

    "_p0.fil", "_p1.fil" etc. are appended to the root for the corresponding polarization.

    Currently reads and transfers the entire dataset at once. 
    """

    hd = h5py.File(inFileName)
    dbgmsg("Opened %s."%inFileName)

    # Overwrite the header based on the input file
    header['nchans'] = len(hd.items()[1][1][:,0,0])
    header['fch1'] = hd.values()[0].values()[0][0]/(1e6)											# in MHz
    header['foff'] = (hd.values()[0].values()[0][1]-hd.values()[0].values()[0][0])/(1e6)			# -24414.0625 / 1e6 in MHz
    header['tstart'] = hd.values()[0].values()[2][0]
    header['tsamp'] =  hd.values()[0].values()[2][1]-hd.values()[0].values()[2][0]

    data = hd.values()[1]
    dbgmsg("Read data from h5 file.")

    # Setup the outfileroot and header for the filterbank file
    if(not outFileRoot):
        outFileRoot = inFileName.split('.h5')[0]
    if(tstart):
        header['tstart'] = tstart
    if(tsamp):
        header['tsamp'] = tsamp
    if(fch1):
        header['fch1'] = fch1
    if(foff):
        header['foff'] = foff

    # Read number of polarizations in the input file
    num_polzn = hd.values()[0].values()[1].shape[0]

    for polzn in range(num_polzn):

        outFileName = outFileRoot+'_p%d.fil'%polzn
        fil = filterbank.create_filterbank_file(outFileName,header=header,nbits=32,verbose=DEBUG)
        dbgmsg("Created output file %s."%outFileName)

        fil.append_spectra(np.transpose(np.squeeze(data[:,polzn,:])))
        
        fil.close()

    hd.close()

if __name__=="__main__":
    if len(sys.argv)<2:
        print("Usage: python hd52fil_chimefrb inFileName \nFor more options use through python")
    else:
        hd52fil(sys.argv[1])
