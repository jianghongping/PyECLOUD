import sys
sys.path.append('../../../')

import numpy as np

input_fol = "../../testing/tests_buildup/LHC_ArcDipReal_450GeV_sey1.70_2.5e11ppb_bl_1.00ns/" 

import PyECLOUD.parse_beam_file as pbf

# bp = pbf.beam_descr_from_fil(input_fol+'/beam.beam', 1., 1., 1., 1.)

# 
sigmaz = 1.000000e-09/4.*299792458.
t_offs = 2.5e-9
filling_pattern = 1*(30*[1.]+5*[0])

b_spac = 25e-9

Dt = 2.500000e-11
t_end=1e-9;

# Parameters of the non-unif 
Dt_coarse = 4*Dt
refine_fact = 4.
t_start_refine = 0.
t_end_refine = 5e-9

ppb_vect = np.atleast_1d(np.float_(np.array(filling_pattern)))
sigmaz_vect = 0*ppb_vect+sigmaz

N_slots=len(ppb_vect)
t = np.arange(0.,N_slots*b_spac+t_end+2*Dt, Dt);

t_coarse = np.arange(0.,N_slots*b_spac+t_end+2*Dt, Dt_coarse);

t_fine_add_single = []

for i_step, t_step in enumerate(t_coarse):
	if t_step > t_end_refine:
		break

	if t_step>=t_start_refine:
		t_fine_add_single+=list(np.linspace(t_step, t_step+Dt_coarse, refine_fact+1)[1:-1])
t_fine_add_single = np.array(t_fine_add_single)

t_fine_add = []
for ii in range(0,N_slots): 
	t_fine_add += list(t_fine_add_single + b_spac*ii)

t_nunif = np.array(sorted(list(t_coarse)+t_fine_add))

c=299792458.;
zz=c*t;
val=0.*t;





for ii in range(0,N_slots):
    if np.mod(ii, N_slots/20)==0:
        print ('Beam profile generation %.0f'%(float(ii)/ float(N_slots)*100)+"""%""")

    ppb  =  ppb_vect[ii]
    sigmaz = sigmaz_vect[ii]
    if sigmaz>0:
        z0=c*(t_offs+ii*b_spac);
        mask_to_be_updated= (np.abs(zz-z0)<(10.*sigmaz))


        val[mask_to_be_updated]=val[mask_to_be_updated]+ppb/(sigmaz*np.sqrt(2*np.pi))*\
           np.exp(-(zz[mask_to_be_updated]-z0)*(zz[mask_to_be_updated]-z0)/(2*sigmaz*sigmaz));


val_nunif = np.interp(t_nunif, t, val)

import matplotlib.pyplot as plt
plt.close('all')
plt.figure(1)
plt.plot(t, val)
plt.plot(t_nunif, val_nunif, '.g')
plt.show()