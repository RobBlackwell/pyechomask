# -*- coding: utf-8 -*-
"""
.. :module:: masks
    :synopsis: Contains standardised mask methods
              
              Method format:
 
                def [mask-type]_[unique-name](*args):
                    '''
                    :param [name]: [desc]
                    :type  [name]: [type]
                    
                                   ...
                
                    desc: [description]
                    
                    defined by [initials of developer]
                    
                    status: [status(dev,test or product)]
                    
                    '''
                    [code...]
                    return mask
                
             

             mask-type can be 'binary' (0 or 1), 'flag'(range of ints) 
             or 'cont' (continuous: values range from 0-1)
             
             for binary masks: 1 = signal; 0 = noise

| Developed by: Roland Proud (RP) <rp43@st-andrews.ac.uk> 
|               Pelagic Ecology Research Group, University of St Andrews
| Contributors:
|
| Maintained by:
| Modification History:      
|
"""

## import packages
import numpy as np

################################################################## background noise

## Add function to reader module
## background noise is already removed from PERGobjects

################################################################## signal masks 

def binary_threshold(Sv,threshold):
    '''
    :param Sv: gridded Sv values (dB re 1m^-1)
    :type  Sv: numpy.array
    
    :param threshold: threshold-value (dB re 1m^-1)
    :type  threshold: float

    desc: generate threshold mask
    
    defined by RP
    
    status: product
    
    '''
    ## create mask grid
    mask = np.zeros(Sv.shape).astype(int)
    
    ## apply threshold
    mask[Sv > threshold] = 1
            
    return mask

## detect aggregates/SSLs

################################################################### noise masks

## transmit pulse and near-field

def binary_pulse(Sv,noise_level = -999):
    '''
    :param Sv: gridded Sv values (dB re 1m^-1)               
    :type  Sv: numpy.array
    
    :param noise_level: level of background noise (db re 1m^-1)
    :type  noise_level: float

    desc: generate pulse mask, mask pulse and surface noise
    
    defined by RP
    
    status: dev
    
    '''
    ## create mask grid
    mask = np.ones(Sv.shape).astype(int)
    
    ## mask pulse and signal up to first noise sample   
    samples,pings = Sv.shape
    for p in range(pings):
        idx           = np.where(Sv[:,p] <= noise_level)[0][0]
        mask[0:idx,p] = 0
         
    return mask


## surface (bubbles/airation)

## seabed

## false-bottom

## dropped ping/attenuated signal

## transient noise/noise spike

## impulse/interference - regular discrete pulses of sound from external source

def mask_impulse_noise(Sv, threshold):
    mask = np.ones(Sv.shape).astype(int)

    samples,pings = Sv.shape

    for sample in range(1, samples-1):
        for ping in range(0, pings):
            
            a = Sv[sample-1, ping]
            b = Sv[sample, ping]
            c = Sv[sample+1, ping]

            if (b - a > threshold) & (b - c > threshold):
                mask[sample, ping] = 0

    return mask


## lowered instrument (CTD etc.)







































