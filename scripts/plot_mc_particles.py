import argparse
import pyLCIO
import ROOT
from array import array
import os

X, Y, Z = 0, 1, 2


def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", required=True, help="Input LCIO file")
    parser.add_argument("-o", required=True, help="Ouput ROOT file")
    parser.add_argument(
        "-n", required=False, type=int, help="Number of events to process"
    )
    return parser.parse_args()


def main():

    args = options()

    if not os.path.isdir(args.i):
        raise FileNotFoundError(f"Directory does not exist: {args.i}. Please check the input again.")


    ele_px, ele_py, ele_pz, ele_energy, ele_vx, ele_vy, ele_vz, ele_phi, ele_eta, ele_pt = array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d')
    pos_px, pos_py, pos_pz, pos_energy, pos_vx, pos_vy, pos_vz, pos_phi, pos_eta, pos_pt = array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d')
    pho_px, pho_py, pho_pz, pho_energy, pho_vx, pho_vy, pho_vz, pho_phi, pho_eta, pho_pt = array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d')

    reader = pyLCIO.IOIMPL.LCFactory.getInstance().createLCReader()

    for filename in os.listdir(args.i):
        filePath = os.path.join(args.i, filename)
        reader.open(filePath)
        print(f"Reading file {filePath}")
        
        for i_event, event in enumerate(reader):

            if args.n is not None and i_event >= args.n:
                break

            names = event.getCollectionNames()
            if "MCParticle" not in names:
                raise Exception(f"No MCParticle collection found in event {i_event}")

            mcparticles = event.getCollection("MCParticle")
            for i_mcparticle, mcparticle in enumerate(mcparticles):
                momentum = mcparticle.getMomentum()
                vertex = mcparticle.getVertex()
                lvec = ROOT.TLorentzVector()
                lvec.SetPxPyPzE(momentum[X], momentum[Y], momentum[Z], mcparticle.getEnergy())
                
                if mcparticle.getPDG()==11:
                    ele_px.append(momentum[X])
                    ele_py.append(momentum[Y])
                    ele_pz.append(momentum[Z])
                    ele_energy.append(mcparticle.getEnergy())
                    ele_vx.append(vertex[X]*1e6)
                    ele_vy.append(vertex[Y]*1e6)
                    ele_vz.append(vertex[Z]*1e6)
                    ele_phi.append(lvec.Phi())
                    ele_eta.append(lvec.Eta())
                    ele_pt.append(lvec.Pt())
                    
                if mcparticle.getPDG()==-11:
                    pos_px.append(momentum[X])
                    pos_py.append(momentum[Y])
                    pos_pz.append(momentum[Z])
                    pos_energy.append(mcparticle.getEnergy())
                    pos_vx.append(vertex[X]*1e6)
                    pos_vy.append(vertex[Y]*1e6)
                    pos_vz.append(vertex[Z]*1e6)
                    pos_phi.append(lvec.Phi())
                    pos_eta.append(lvec.Eta())
                    pos_pt.append(lvec.Pt())

                if mcparticle.getPDG()==22:
                    pho_px.append(momentum[X])
                    pho_py.append(momentum[Y])
                    pho_pz.append(momentum[Z])
                    pho_energy.append(mcparticle.getEnergy())
                    pho_vx.append(vertex[X]*1e6)
                    pho_vy.append(vertex[Y]*1e6)
                    pho_vz.append(vertex[Z]*1e6)
                    pho_phi.append(lvec.Phi())
                    pho_eta.append(lvec.Eta())
                    pho_pt.append(lvec.Pt())


    print("All collections read, creating and filling the histograms now.")
    
    root_file = ROOT.TFile(f"{args.o}", "RECREATE")
    h_ele_px = ROOT.TH1F("h_ele_px", "Px of electrons; Px [GeV/c]; Entries", 1000, -5, 5)
    h_ele_py = ROOT.TH1F("h_ele_py", "Py of electrons; Py [GeV/c]; Entries", 1000, -5, 5)
    h_ele_pz = ROOT.TH1F("h_ele_pz", "Pz of electrons; Pz [GeV/c]; Entries", 20000, -10000, 10000)
    h_ele_energy = ROOT.TH1F("h_ele_energy", "Energy of electrons; Energy [GeV/c^2]; Entries", 1000, 0, 10000)
    h_ele_vx = ROOT.TH1F("h_ele_vx", "Vx of electrons; Vx [um]; Entries", 5000, -1, 1)
    h_ele_vy = ROOT.TH1F("h_ele_vy", "Vy of electrons; Vy [um]; Entries", 5000, -1, 1)
    h_ele_vz = ROOT.TH1F("h_ele_vz", "Vz of electrons; Vz [um]; Entries", 10000, -500, 500)
    h_ele_phi = ROOT.TH1F("h_ele_phi", "Phi of electrons; Phi [radian]; Entries", 6400, -3.2, 3.2)
    h_ele_eta = ROOT.TH1F("h_ele_eta", "Eta of electrons; Eta; Entries", 2000, -10, 10)
    h_ele_pt = ROOT.TH1F("h_ele_pt", "Pt of electrons; Pt [GeV/c]; Entries", 1000, 0, 5)

    h_pos_px = ROOT.TH1F("h_pos_px", "Px of positrons; Px [GeV/c]; Entries", 1000, -5, 5)
    h_pos_py = ROOT.TH1F("h_pos_py", "Py of positrons; Py [GeV/c]; Entries", 1000, -5, 5)
    h_pos_pz = ROOT.TH1F("h_pos_pz", "Pz of positrons; Pz [GeV/c]; Entries", 20000, -10000, 10000)
    h_pos_energy = ROOT.TH1F("h_pos_energy", "Energy of positrons; Energy [GeV/c^2]; Entries", 1000, 0, 10000)
    h_pos_vx = ROOT.TH1F("h_pos_vx", "Vx of positrons; Vx [um]; Entries", 5000, -1, 1)
    h_pos_vy = ROOT.TH1F("h_pos_vy", "Vy of positrons; Vy [um]; Entries", 5000, -1, 1)
    h_pos_vz = ROOT.TH1F("h_pos_vz", "Vz of positrons; Vz [um]; Entries", 10000, -500, 500)
    h_pos_phi = ROOT.TH1F("h_pos_phi", "Phi of positrons; Phi [radian]; Entries", 6400, -3.2, 3.2)
    h_pos_eta = ROOT.TH1F("h_pos_eta", "Eta of positrons; Eta; Entries", 2000, -10, 10)
    h_pos_pt = ROOT.TH1F("h_pos_pt", "Pt of positrons; Pt [GeV/c]; Entries", 1000, 0, 5)

    h_pho_px = ROOT.TH1F("h_pho_px", "Px of photons; Px [GeV/c]; Entries", 10000, -5, 5)
    h_pho_py = ROOT.TH1F("h_pho_py", "Py of photons; Py [GeV/c]; Entries", 10000, -5, 5)
    h_pho_pz = ROOT.TH1F("h_pho_pz", "Pz of photons; Pz [GeV/c]; Entries", 20000, -10000, 10000)
    h_pho_energy = ROOT.TH1F("h_pho_energy", "Energy of photons; Energy [GeV/c^2]; Entries", 1000, 0, 10000)
    h_pho_vx = ROOT.TH1F("h_pho_vx", "Vx of photons; Vx [um]; Entries", 5000, -1, 1)
    h_pho_vy = ROOT.TH1F("h_pho_vy", "Vy of photons; Vy [um]; Entries", 5000, -1, 1)
    h_pho_vz = ROOT.TH1F("h_pho_vz", "Vz of photons; Vz [um]; Entries", 10000, -500, 500)
    h_pho_phi = ROOT.TH1F("h_pho_phi", "Phi of photons; Phi [radian]; Entries", 6400, -3.2, 3.2)
    h_pho_eta = ROOT.TH1F("h_pho_eta", "Eta of photons; Eta; Entries", 2000, -10, 10)
    h_pho_pt = ROOT.TH1F("h_pho_pt", "Pt of photons; Pt [GeV/c]; Entries", 1000, 0, 5)

    w = 2400
    
    for i in range(len(ele_px)):
        h_ele_px.Fill(ele_px[i], w)
        h_ele_py.Fill(ele_py[i], w)
        h_ele_pz.Fill(ele_pz[i], w)
        h_ele_energy.Fill(ele_energy[i], w)
        h_ele_vx.Fill(ele_vx[i], w)
        h_ele_vy.Fill(ele_vy[i], w)
        h_ele_vz.Fill(ele_vz[i], w)
        h_ele_pt.Fill(ele_pt[i], w)
        h_ele_eta.Fill(ele_eta[i], w)
        h_ele_phi.Fill(ele_phi[i], w)

    for i in range(len(pos_px)):
        h_pos_px.Fill(pos_px[i], w)
        h_pos_py.Fill(pos_py[i], w)
        h_pos_pz.Fill(pos_pz[i], w)
        h_pos_energy.Fill(pos_energy[i], w)
        h_pos_vx.Fill(pos_vx[i], w)
        h_pos_vy.Fill(pos_vy[i], w)
        h_pos_vz.Fill(pos_vz[i], w)
        h_pos_pt.Fill(pos_pt[i], w)
        h_pos_eta.Fill(pos_eta[i], w)
        h_pos_phi.Fill(pos_phi[i], w)

    for i in range(len(pho_px)):
        h_pho_px.Fill(pho_px[i], w)
        h_pho_py.Fill(pho_py[i], w)
        h_pho_pz.Fill(pho_pz[i], w)
        h_pho_energy.Fill(pho_energy[i], w)
        h_pho_vx.Fill(pho_vx[i], w)
        h_pho_vy.Fill(pho_vy[i], w)
        h_pho_vz.Fill(pho_vz[i], w)
        h_pho_pt.Fill(pho_pt[i], w)
        h_pho_eta.Fill(pho_eta[i], w)
        h_pho_phi.Fill(pho_phi[i], w)

    root_file.Write()

if __name__ == "__main__":
    main()
