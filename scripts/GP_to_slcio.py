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

def calcPz(xangle, yangle, E):
    pz = E/(math.sqrt(1 + xangle**2 + yangle**2))
    return pz

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

    countFiles = 0
    col = None
    evt = None
    col, evt = lcioEvt(col, evt)
    # Initialize the LCIO file writer
    wrt = IOIMPL.LCFactory.getInstance().createLCWriter()
    filePath = ""
    wrt = openLCIO(filePath, wrt)
    
    """
    if args.numParticlesPerFile<0:
        filePath = os.path.join(args.outputDir, "out.slcio")
    else:
        filePath = os.path.join(args.outputDir, f"out_IP_{countFiles}.slcio")
 
    print(f"Creating file {filePath}")
    wrt = openLCIO(filePath, wrt)

    #incoherent pairs
    data = np.loadtxt(args.inputDir + '/pairs.dat')
    #more details on the format of these secondary output files here - https://trac.lal.in2p3.fr/GuineaPig/wiki/SecondariesFormat
    E = data[:,0] #GeV, negative for positrons and positive for electrons
    x = data[:,4] #nm 
    y = data[:,5] #nm
    z = data[:,6] #nm
    beta_x = data[:,1] #normalized velocity in x-dir (vx/c = px/E)
    beta_y = data[:,2] #normalized velocity in y-dir (vy/c = py/E)
    beta_z = data[:,3] #normalized velocity in z-dir (vz/c = pz/E)
    m_e = 0.000511 #mass of electron in GeV

    for i in range(0,len(x)):
        lvec = ROOT.TLorentzVector()
        if E[i]>0:
            lvec.SetPxPyPzE(beta_x[i]*E[i],beta_y[i]*E[i],beta_z[i]*E[i],E[i])
        else:
          lvec.SetPxPyPzE(beta_x[i]*E[i]*-1,beta_y[i]*E[i]*-1,beta_z[i]*E[i]*-1,E[i]*-1)  
            
        # Creating the particle with original parameters
        particle = IMPL.MCParticleImpl()
        if E[i]>0:
            particle.setPDG(11)
            particle.setCharge(-1)
            mom = np.array([beta_x[i]*E[i],beta_y[i]*E[i],beta_z[i]*E[i]])
        else:
            particle.setPDG(-11)
            particle.setCharge(1)
            mom = np.array([beta_x[i]*E[i]*-1,beta_y[i]*E[i]*-1,beta_z[i]*E[i]*-1])
        particle.setGeneratorStatus(1)
        particle.setMass(m_e)
        pos = np.array([x[i], y[i], z[i]])
        particle.setVertex(pos)
        particle.setMomentum(mom)

        # Adding particle to the collection
        if args.filterGenParticles:
            if lvec.Pt()>0.01 and abs(lvec.Eta())<2.5:
                col.addElement(particle)
        else:
            col.addElement(particle)
                
        if col.getNumberOfElements()>0 and col.getNumberOfElements()%args.numParticlesPerFile==0 and args.numParticlesPerFile>0:
            print(f'Wrote {col.getNumberOfElements()} particles')
            wrt.writeEvent(evt)
            wrt.close()
            countFiles += 1
            filePath = os.path.join(args.outputDir, f"out_IP_{countFiles}.slcio")
            print(f"Creating file {filePath}")
            col, evt = lcioEvt(col, evt)
            wrt = openLCIO(filePath, wrt)
    """
    
    out_file = args.outputDir+"/hist_CP.root"
    hstfile = ROOT.TFile(out_file, "RECREATE")
    h_px = ROOT.TH1F("CP_px",";px [GeV] ;Entries", 1000, -5000, 5000)
    h_py = ROOT.TH1F("CP_py",";py [GeV] ;Entries", 1000, -5000, 5000)
    h_pz = ROOT.TH1F("CP_pz",";pz [GeV] ;Entries", 1000, -5000, 5000)
    h_pt = ROOT.TH1F("CP_pt",";pt [GeV] ;Entries", 1000, 0, 1000)
    h_energy = ROOT.TH1F("CP_E",";E [GeV] ;Entries", 1000, 0, 10000)
    h_energy_np = ROOT.TH1F("CP_E_np",";E [GeV] ;Entries", 1000, 0, 10000)
    h_eta = ROOT.TH1F("CP_eta",";Eta;Entries", 5000, -2.5, 2.5)
    h_phi = ROOT.TH1F("CP_phi",";Phi [rad] ;Entries", 6400, -3.2, 3.2)

    if args.numParticlesPerFile>0:
        wrt.writeEvent(evt)
        wrt.close()
        countFiles = 0
        filePath = os.path.join(args.outputDir, f"out_CP_{countFiles}.slcio")
        print(f"Creating file {filePath}")
        wrt = openLCIO(filePath, wrt)

    #coherent pairs
    data = np.loadtxt(args.inputDir + '/coh1.dat')
    ncoh1 = len(data)
    data = np.vstack((data,np.loadtxt(args.inputDir + '/coh2.dat')))
    E = data[:,0] #GeV, negative for positrons and positive for electrons
    x = data[:,1]*1000 #nm
    y = data[:,2]*1000 #nm
    z = data[:,3]*1000 #nm
    xrad = data[:,4]/1000000 #angle w.r.t. z-axis in x-z plane i.e. px/pz in radians
    yrad = data[:,5]/1000000 #angle w.r.t. z-axis in y-z plane i.e. py/pz in radians
    m_e = 0.000511 #mass of electron in GeV

    for i in range(0,len(x)):
        lvec = ROOT.TLorentzVector()
        if E[i]>0: #electron
            pz = calcPz(xrad[i],yrad[i],E[i])
            if i>=ncoh1: #CP produced from Beam-1
                pz = pz*-1
            lvec.SetPxPyPzE(xrad[i]*pz,yrad[i]*pz,pz,E[i])
            h_energy_np.Fill(E[i])
        else:
            pz = calcPz(xrad[i],yrad[i],-1*E[i])
            if i>=ncoh1: #CP produced from Beam-2
                pz = pz*-1
            lvec.SetPxPyPzE(xrad[i]*pz,yrad[i]*pz,pz,-1*E[i])
            h_energy_np.Fill(-1*E[i])

        h_px.Fill(lvec.Px())
        h_py.Fill(lvec.Py())
        h_pz.Fill(lvec.Pz())
        h_energy.Fill(lvec.E())
        h_pt.Fill(lvec.Pt())
        h_phi.Fill(lvec.Phi())
        h_eta.Fill(lvec.Eta())

	# Creating the particle with original parameters
        particle = IMPL.MCParticleImpl()
        if E[i]>0:
            particle.setPDG(11)
            particle.setCharge(-1)
        else:
            particle.setPDG(-11)
            particle.setCharge(1)
        particle.setGeneratorStatus(1)
        particle.setMass(m_e)
        pos = np.array([x[i], y[i], z[i]])
        particle.setVertex(pos)
        mom = np.array([xrad[i]*pz,yrad[i]*pz,pz])
        particle.setMomentum(mom)
        
        # Adding particle to the collection
        if args.filterGenParticles:
            if lvec.Pt()>0.01 and abs(lvec.Eta())<2.5:
                col.addElement(particle)
        else:
            col.addElement(particle)
        
        if col.getNumberOfElements()>0 and col.getNumberOfElements()%args.numParticlesPerFile==0 and args.numParticlesPerFile>0:
            print(f'Wrote {col.getNumberOfElements()} particles')
            wrt.writeEvent(evt)
            wrt.close()
            countFiles += 1
            filePath = os.path.join(args.outputDir, f"out_CP_{countFiles}.slcio")
            print(f"Creating file {filePath}")
            col, evt = lcioEvt(col, evt)
            wrt = openLCIO(filePath, wrt)

    wrt.writeEvent(evt)
    wrt.close()

    h_px.Write()
    h_py.Write()
    h_pz.Write()
    h_pt.Write()
    h_eta.Write()
    h_phi.Write()
    h_energy_np.Write()
    h_energy.Write()
    hstfile.Close()


if __name__ == "__main__":
    main()
