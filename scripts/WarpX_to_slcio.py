#!/usr/bin/env python
"""This script converts a WarpX beam-beam interaction output file to an SLCIO file with LCIO::MCParticle instances"""

import os
import argparse
import numpy as np
from openpmd_viewer import OpenPMDTimeSeries
from scipy.constants import c, e
from math import sqrt
from pdb import set_trace as br
from array import array
from pyLCIO import UTIL, EVENT, IMPL, IO, IOIMPL
import random
import math
import ROOT

parser = argparse.ArgumentParser(description='Convert WarpX simulation output to SLCIO file with MCParticles')
parser.add_argument('--inputDir', metavar='FILE_IN', help='Input directory with WarpX simulation output', type=str)
parser.add_argument('--outputDir', metavar='FILE_OUT', help='Output directory with SLCIO files')
parser.add_argument('-c', '--comment', metavar='TEXT',  help='Comment to be added to the header', type=str)
parser.add_argument('-n', '--numParticlesPerFile',  help='Number of particles per file', type=int, default=-1)
parser.add_argument('-f', '--filterGenParticles', help='Filter gen MC particles', action='store_true', default=False)

args = parser.parse_args()

def extract_macroparticles_data(species_name):
    """
    Returns 4 numpy arrays, with one element per macroparticle:
    - the momentum in x, y, z (in units eV/c)
    - the weight (unitless), i.e. how many physical particles are represented by this macroparticle
    """
    x_list = []
    y_list = []
    z_list = []
    px_list = []
    py_list = []
    pz_list = []
    m_list = []
    q_list = []
    t_list = []

    # Loop through the files that contain particles collected at the edges and in the box
    for folder_name in [
        '/diags/bound/particles_at_xlo',
        '/diags/bound/particles_at_xhi',
        '/diags/bound/particles_at_ylo',
        '/diags/bound/particles_at_yhi',
        '/diags/trajs',        
        ]:
        ts = OpenPMDTimeSeries(f"{args.inputDir}" + folder_name)
        x, y, z, px, py, pz, m, q = ts.get_particle( ['x', 'y', 'z', 'ux', 'uy', 'uz', 'mass', 'charge'], 
            iteration=ts.iterations[-1], species=species_name )

        t = [0]*len(x)
        x_list.append(x)
        y_list.append(y)
        z_list.append(z)
        px_list.append(px)
        py_list.append(py)
        pz_list.append(pz)
        q_list.append(q)
        m_list.append(m)
        t_list.append(t)
        
    # Concatenate list of particles from all files
    x_all = np.concatenate( x_list )
    y_all = np.concatenate( y_list )
    z_all = np.concatenate( z_list )
    px_all = np.concatenate( px_list )
    py_all = np.concatenate( py_list )
    pz_all = np.concatenate( pz_list )
    t_all = np.concatenate( t_list )
    q_all = np.concatenate( q_list)
    m_all = np.concatenate( m_list)

    # Convert momenta to eV/c
    if m[0] != 0:
        # First convert from unitless to kg.m.s-1
        conversion_factor = m[0]*c
    else:
        # For photons, i.e. m=0, the momenta are already in kg.m.s-1
        conversion_factor = 1.
    # Then convert to eV/c
    conversion_factor *= c/e
    px_all *= conversion_factor/1e9
    py_all *= conversion_factor/1e9
    pz_all *= conversion_factor/1e9
    q_all *= 1/e
    m_all *= c**2/(e*1e9)
    
    return x_all, y_all, z_all, px_all, py_all, pz_all, q_all, m_all, t_all

def calc_energy(px,py,pz,m):
    e = sqrt((px**2 + py**2 + pz**2) + (m**2))

    return e

def openLCIO(fileName, wrt):
    # Write a RunHeader
    run = IMPL.LCRunHeaderImpl()
    run.setRunNumber(0)
    # Initialize the LCIO file writer                                                                                                                                                
    wrt = IOIMPL.LCFactory.getInstance().createLCWriter()
    wrt.open(fileName, EVENT.LCIO.WRITE_NEW)
    wrt.writeRunHeader(run)

    return wrt

def lcioEvt(col, evt):
    col = None
    evt = None
    col = IMPL.LCCollectionVec(EVENT.LCIO.MCPARTICLE)
    evt = IMPL.LCEventImpl()
    evt.setEventNumber(0)
    evt.addCollection(col, 'MCParticle')

    return col, evt

def main():

    if not os.path.isdir(args.inputDir):
        print(f"Directory does not exist: {inputDir}. Please check the input again.")

    if not os.path.exists(args.outputDir):
        os.makedirs(args.outputDir)
        print(f"Directory '{args.outputDir}' created.")
    else:
        for filename in os.listdir(args.outputDir):
            file_path = os.path.join(args.outputDir, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")            

    #define list of species with their PDGID as the key value
    dict_species = {'ele1':11, 'ele2':11, 'pos1':-11, 'pos2':-11, 'pho1':22, 'pho2':22}

    countFiles = 0
    col = None
    evt = None
    col, evt = lcioEvt(col, evt)
    # Initialize the LCIO file writer
    wrt = IOIMPL.LCFactory.getInstance().createLCWriter()
    filePath = ""
    
    if args.numParticlesPerFile<0:
        filePath = os.path.join(args.outputDir, "out.slcio")
    else:
        filePath = os.path.join(args.outputDir, f"out_{countFiles}.slcio")

    print(f"Creating file {filePath}")
    wrt = openLCIO(filePath, wrt)
        
    for sp, pid in dict_species.items():
        x, y, z, px, py, pz, q, m, t = extract_macroparticles_data(sp)

        for i in range(0,len(x)):
            lvec = ROOT.TLorentzVector()
            lvec.SetPxPyPzE(px[i],py[i],pz[i],calc_energy(px[i],py[i],pz[i],m[i]))
            
            # Creating the particle with original parameters
            particle = IMPL.MCParticleImpl()
            particle.setPDG(pid)
            particle.setGeneratorStatus(1)
            particle.setTime(t[i])
            particle.setMass(m[i])
            particle.setCharge(q[i])
            pos = np.array([x[i], y[i], z[i]])
            particle.setVertex(pos)
            mom = np.array([px[i], py[i], pz[i]])
            particle.setMomentum(mom)

            # Adding particle to the collection
            if args.filterGenParticles:
                if pid==22 and abs(lvec.Eta())<5:
                    col.addElement(particle)
                if abs(pid)==11 and lvec.Pt()>0.01:
                    col.addElement(particle)
            else:
                col.addElement(particle)
                
            if col.getNumberOfElements()>0 and col.getNumberOfElements()%args.numParticlesPerFile==0 and args.numParticlesPerFile>0:
                print(f'Wrote {col.getNumberOfElements()} particles')
                wrt.writeEvent(evt)
                wrt.close()
                countFiles += 1
                filePath = os.path.join(args.outputDir, f"out_{countFiles}.slcio")
                print(f"Creating file {filePath}")
                col, evt = lcioEvt(col, evt)
                wrt = openLCIO(filePath, wrt)

    wrt.writeEvent(evt)
    wrt.close()

if __name__ == "__main__":
    main()
