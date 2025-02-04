import argparse
import pyLCIO
import ROOT
from array import array
from math import sqrt

X, Y, Z = 0, 1, 2

VERTEX_COLLECTIONS = [
    "VertexBarrelCollection",
    "VertexEndcapCollection"
]
TRACKER_COLLECTIONS = [
    "InnerTrackerBarrelCollection",
    "InnerTrackerEndcapCollection",
    "OuterTrackerBarrelCollection",
    "OuterTrackerEndcapCollection"
]


def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", required=True, type=str, help="Input LCIO file")
    parser.add_argument("-o", required=True, help="Ouput ROOT file")
    parser.add_argument(
        "-n", required=False, type=int, help="Number of events to process"
    )
    return parser.parse_args()


def main():
    ops = options()
    print(f"Reading file {ops.i}")

    vxb_px, vxb_py, vxb_pz, vxb_pt, vxb_x, vxb_y, vxb_z, vxb_edep, vxb_eta, vxb_phi = array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d')
    vxe_px, vxe_py, vxe_pz, vxe_pt, vxe_x, vxe_y, vxe_z, vxe_edep, vxe_eta, vxe_phi = array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d')
    itb_px, itb_py, itb_pz, itb_pt, itb_x, itb_y, itb_z, itb_edep, itb_eta, itb_phi = array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d')
    ite_px, ite_py, ite_pz, ite_pt, ite_x, ite_y, ite_z, ite_edep, ite_eta, ite_phi = array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d')
    otb_px, otb_py, otb_pz, otb_pt, otb_x, otb_y, otb_z, otb_edep, otb_eta, otb_phi = array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d')
    ote_px, ote_py, ote_pz, ote_pt, ote_x, ote_y, ote_z, ote_edep, ote_eta, ote_phi = array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d'), array('d')

    reader = pyLCIO.IOIMPL.LCFactory.getInstance().createLCReader()
    reader.open(ops.i)

    for i_event, event in enumerate(reader):

        if ops.n is not None and i_event >= ops.n:
            break

        cols = {}
        for col in VERTEX_COLLECTIONS:
            cols[col] = get_collection(event, col)
        for col in TRACKER_COLLECTIONS:
            cols[col] = get_collection(event, col)

        for col_name in VERTEX_COLLECTIONS:
            for i_hit, hit in enumerate(cols[col_name]):
                position = hit.getPosition()
                momentum = hit.getMomentum()
                lvec = ROOT.TLorentzVector()
                lvec.SetPxPyPzE(momentum[X], momentum[Y], momentum[Z], sqrt(momentum[X]**2 + momentum[Y]**2 + momentum[Z]**2))

                if col_name == "VertexBarrelCollection":
                    vxb_px.append(momentum[X])
                    vxb_py.append(momentum[Y])
                    vxb_pz.append(momentum[Z])
                    vxb_pt.append(lvec.Pt())
                    vxb_x.append(position[X])
                    vxb_y.append(position[Y])
                    vxb_z.append(position[Z])
                    vxb_edep.append(hit.getEDep()*1000)
                    vxb_eta.append(lvec.Eta())
                    vxb_phi.append(lvec.Phi())

                else:
                    vxe_px.append(momentum[X])
                    vxe_py.append(momentum[Y])
                    vxe_pz.append(momentum[Z])
                    vxe_pt.append(lvec.Pt())
                    vxe_x.append(position[X])
                    vxe_y.append(position[Y])
                    vxe_z.append(position[Z])
                    vxe_edep.append(hit.getEDep()*1000)
                    vxe_eta.append(lvec.Eta())
                    vxe_phi.append(lvec.Phi())


        for col_name in TRACKER_COLLECTIONS:
            for i_hit, hit in enumerate(cols[col_name]):
                position = hit.getPosition()
                momentum = hit.getMomentum()
                lvec = ROOT.TLorentzVector()
                lvec.SetPxPyPzE(momentum[X], momentum[Y], momentum[Z], sqrt(momentum[X]**2 + momentum[Y]**2 + momentum[Z]**2))

                if col_name == "InnerTrackerBarrelCollection":
                    itb_px.append(momentum[X])
                    itb_py.append(momentum[Y])
                    itb_pz.append(momentum[Z])
                    itb_pt.append(lvec.Pt())
                    itb_x.append(position[X])
                    itb_y.append(position[Y])
                    itb_z.append(position[Z])
                    itb_edep.append(hit.getEDep()*1000)
                    itb_eta.append(lvec.Eta())
                    itb_phi.append(lvec.Phi())

                elif col_name == "InnerTrackerEndcapCollection":
                    ite_px.append(momentum[X])
                    ite_py.append(momentum[Y])
                    ite_pz.append(momentum[Z])
                    ite_pt.append(lvec.Pt())
                    ite_x.append(position[X])
                    ite_y.append(position[Y])
                    ite_z.append(position[Z])
                    ite_edep.append(hit.getEDep()*1000)
                    ite_eta.append(lvec.Eta())
                    ite_phi.append(lvec.Phi())

                elif col_name == "OuterTrackerBarrelCollection":
                    otb_px.append(momentum[X])
                    otb_py.append(momentum[Y])
                    otb_pz.append(momentum[Z])
                    otb_pt.append(lvec.Pt())
                    otb_x.append(position[X])
                    otb_y.append(position[Y])
                    otb_z.append(position[Z])
                    otb_edep.append(hit.getEDep()*1000)
                    otb_eta.append(lvec.Eta())
                    otb_phi.append(lvec.Phi())

                else:
                    ote_px.append(momentum[X])
                    ote_py.append(momentum[Y])
                    ote_pz.append(momentum[Z])
                    ote_pt.append(lvec.Pt())
                    ote_x.append(position[X])
                    ote_y.append(position[Y])
                    ote_z.append(position[Z])
                    ote_edep.append(hit.getEDep()*1000)
                    ote_eta.append(lvec.Eta())
                    ote_phi.append(lvec.Phi())


    root_file = ROOT.TFile(f"{ops.o}", "RECREATE")
    h_vxb_px = ROOT.TH1F("h_vxb_px", "Px of vertex barrel hits; Px [GeV]; Entries", 1000, -5, 5)
    h_vxb_py = ROOT.TH1F("h_vxb_py", "Py of vertex barrel hits; Py [GeV]; Entries", 1000, -5, 5)
    h_vxb_pz = ROOT.TH1F("h_vxb_pz", "Pz of vertex barrel hits; Pz [GeV]; Entries", 20000, -10000, 10000)
    h_vxb_edep = ROOT.TH1F("h_vxb_edep", "Energy deposition of vertex barrel hits; Energy [MeV]; Entries", 1000, 0, 1)
    h_vxb_x = ROOT.TH1F("h_vxb_x", "X of vertex barrel hits; X [mm]; Entries", 5000, -5000, 5000)
    h_vxb_y = ROOT.TH1F("h_vxb_y", "Y of vertex barrel hits; Y [mm]; Entries", 5000, -5000, 5000)
    h_vxb_z = ROOT.TH1F("h_vxb_z", "Z of vertex barrel hits; Z [mm]; Entries", 5000, -5000, 5000)
    h_vxb_phi = ROOT.TH1F("h_vxb_phi", "Phi of vertex barrel hits; Phi [radian]; Entries", 6400, -3.2, 3.2)
    h_vxb_eta = ROOT.TH1F("h_vxb_eta", "Eta of vertex barrel hits; Eta; Entries", 2000, -10, 10)
    h_vxb_pt = ROOT.TH1F("h_vxb_pt", "Pt of vertex barrel hits; Pt [GeV]; Entries", 1000, 0, 5)
    h_vxb_r_z = ROOT.TH2F("h_vxb_r_z", "R vs Z of vertex barrel hits; Z [mm]; R [mm]", 1000, -5000, 5000, 400, 0, 2000)
    h_vxb_r_phi = ROOT.TH2F("h_vxb_r_phi", "R vs Phi of vertex barrel hits; Phi [radians]; R [mm]", 6400, -3.2, 3.2, 400, 0, 2000)
    h_vxe_px = ROOT.TH1F("h_vxe_px", "Px of vertex endcap hits; Px [GeV]; Entries", 1000, -5, 5)
    h_vxe_py = ROOT.TH1F("h_vxe_py", "Py of vertex endcap hits; Py [GeV]; Entries", 1000, -5, 5)
    h_vxe_pz = ROOT.TH1F("h_vxe_pz", "Pz of vertex endcap hits; Pz [GeV]; Entries", 20000, -10000, 10000)
    h_vxe_edep = ROOT.TH1F("h_vxe_edep", "Energy deposition of vertex endcap hits; Energy [MeV]; Entries", 1000, 0, 1)
    h_vxe_x = ROOT.TH1F("h_vxe_x", "X of vertex endcap hits; X [mm]; Entries", 5000, -5000, 5000)
    h_vxe_y = ROOT.TH1F("h_vxe_y", "Y of vertex endcap hits; Y [mm]; Entries", 5000, -5000, 5000)
    h_vxe_z = ROOT.TH1F("h_vxe_z", "Z of vertex endcap hits; Z [mm]; Entries", 5000, -5000, 5000)
    h_vxe_phi = ROOT.TH1F("h_vxe_phi", "Phi of vertex endcap hits; Phi [radian]; Entries", 6400, -3.2, 3.2)
    h_vxe_eta = ROOT.TH1F("h_vxe_eta", "Eta of vertex endcap hits; Eta; Entries", 2000, -10, 10)
    h_vxe_pt = ROOT.TH1F("h_vxe_pt", "Pt of vertex endcap hits; Pt [GeV]; Entries", 1000, 0, 5)
    h_vxe_r_z = ROOT.TH2F("h_vxe_r_z", "R vs Z of vertex endcap hits; Z [mm]; R [mm]", 1000, -5000, 5000, 400, 0, 2000)
    h_vxe_r_phi = ROOT.TH2F("h_vxe_r_phi", "R vs Phi of vertex endcap hits; Phi [radians]; R [mm]", 6400, -3.2, 3.2, 400, 0, 2000)
    h_itb_px = ROOT.TH1F("h_itb_px", "Px of inner tracker barrel hits; Px [GeV]; Entries", 1000, -5, 5)
    h_itb_py = ROOT.TH1F("h_itb_py", "Py of inner tracker barrel hits; Py [GeV]; Entries", 1000, -5, 5)
    h_itb_pz = ROOT.TH1F("h_itb_pz", "Pz of inner tracker barrel hits; Pz [GeV]; Entries", 20000, -10000, 10000)
    h_itb_edep = ROOT.TH1F("h_itb_edep", "Energy deposition of inner tracker barrel hits; Energy [MeV]; Entries", 1000, 0, 1)
    h_itb_x = ROOT.TH1F("h_itb_x", "X of inner tracker barrel hits; X [mm]; Entries", 5000, -5000, 5000)
    h_itb_y = ROOT.TH1F("h_itb_y", "Y of inner tracker barrel hits; Y [mm]; Entries", 5000, -5000, 5000)
    h_itb_z = ROOT.TH1F("h_itb_z", "Z of inner tracker barrel hits; Z [mm]; Entries", 5000, -5000, 5000)
    h_itb_phi = ROOT.TH1F("h_itb_phi", "Phi of inner tracker barrel hits; Phi [radian]; Entries", 6400, -3.2, 3.2)
    h_itb_eta = ROOT.TH1F("h_itb_eta", "Eta of inner tracker barrel hits; Eta; Entries", 2000, -10, 10)
    h_itb_pt = ROOT.TH1F("h_itb_pt", "Pt of inner tracker barrel hits; Pt [GeV]; Entries", 1000, 0, 5)
    h_itb_r_z = ROOT.TH2F("h_itb_r_z", "R vs Z of inner tracker barrel hits; Z [mm]; R [mm]", 1000, -5000, 5000, 400, 0, 2000)
    h_itb_r_phi = ROOT.TH2F("h_itb_r_phi", "R vs Phi of inner tracker barrel hits; Phi [radians]; R [mm]", 6400, -3.2, 3.2, 400, 0, 2000)
    h_ite_px = ROOT.TH1F("h_ite_px", "Px of inner tracker endcap hits; Px [GeV]; Entries", 1000, -5, 5)
    h_ite_py = ROOT.TH1F("h_ite_py", "Py of inner tracker endcap hits; Py [GeV]; Entries", 1000, -5, 5)
    h_ite_pz = ROOT.TH1F("h_ite_pz", "Pz of inner tracker endcap hits; Pz [GeV]; Entries", 20000, -10000, 10000)
    h_ite_edep = ROOT.TH1F("h_ite_edep", "Energy deposition of inner tracker endcap hits; Energy [MeV]; Entries", 1000, 0, 1)
    h_ite_x = ROOT.TH1F("h_ite_x", "X of inner tracker endcap hits; X [mm]; Entries", 5000, -5000, 5000)
    h_ite_y = ROOT.TH1F("h_ite_y", "Y of inner tracker endcap hits; Y [mm]; Entries", 5000, -5000, 5000)
    h_ite_z = ROOT.TH1F("h_ite_z", "Z of inner tracker endcap hits; Z [mm]; Entries", 5000, -5000, 5000)
    h_ite_phi = ROOT.TH1F("h_ite_phi", "Phi of inner tracker endcap hits; Phi [radian]; Entries", 6400, -3.2, 3.2)
    h_ite_eta = ROOT.TH1F("h_ite_eta", "Eta of inner tracker endcap hits; Eta; Entries", 2000, -10, 10)
    h_ite_pt = ROOT.TH1F("h_ite_pt", "Pt of inner tracker endcap hits; Pt [GeV]; Entries", 1000, 0, 5)
    h_ite_r_z = ROOT.TH2F("h_ite_r_z", "R vs Z of inner tracker endcap hits; Z [mm]; R [mm]", 1000, -5000, 5000, 400, 0, 2000)
    h_ite_r_phi = ROOT.TH2F("h_ite_r_phi", "R vs Phi of inner tracker endcap hits; Phi [radians]; R [mm]", 6400, -3.2, 3.2, 400, 0, 2000)
    h_otb_px = ROOT.TH1F("h_otb_px", "Px of inner tracker barrel hits; Px [GeV]; Entries", 1000, -5, 5)
    h_otb_py = ROOT.TH1F("h_otb_py", "Py of inner tracker barrel hits; Py [GeV]; Entries", 1000, -5, 5)
    h_otb_pz = ROOT.TH1F("h_otb_pz", "Pz of inner tracker barrel hits; Pz [GeV]; Entries", 20000, -10000, 10000)
    h_otb_edep = ROOT.TH1F("h_otb_edep", "Energy deposition of inner tracker barrel hits; Energy [MeV]; Entries", 1000, 0, 1)
    h_otb_x = ROOT.TH1F("h_otb_x", "X of inner tracker barrel hits; X [mm]; Entries", 5000, -5000, 5000)
    h_otb_y = ROOT.TH1F("h_otb_y", "Y of inner tracker barrel hits; Y [mm]; Entries", 5000, -5000, 5000)
    h_otb_z = ROOT.TH1F("h_otb_z", "Z of inner tracker barrel hits; Z [mm]; Entries", 5000, -5000, 5000)
    h_otb_phi = ROOT.TH1F("h_otb_phi", "Phi of inner tracker barrel hits; Phi [radian]; Entries", 6400, -3.2, 3.2)
    h_otb_eta = ROOT.TH1F("h_otb_eta", "Eta of inner tracker barrel hits; Eta; Entries", 2000, -10, 10)
    h_otb_pt = ROOT.TH1F("h_otb_pt", "Pt of inner tracker barrel hits; Pt [GeV]; Entries", 1000, 0, 5)
    h_otb_r_z = ROOT.TH2F("h_otb_r_z", "R vs Z of outer tracker barrel hits; Z [mm]; R [mm]", 1000, -5000, 5000, 400, 0, 2000)
    h_otb_r_phi = ROOT.TH2F("h_otb_r_phi", "R vs Phi of outer tracker barrel hits; Phi [radians]; R [mm]", 6400, -3.2, 3.2, 400, 0, 2000)
    h_ote_px = ROOT.TH1F("h_ote_px", "Px of inner tracker endcap hits; Px [GeV]; Entries", 1000, -5, 5)
    h_ote_py = ROOT.TH1F("h_ote_py", "Py of inner tracker endcap hits; Py [GeV]; Entries", 1000, -5, 5)
    h_ote_pz = ROOT.TH1F("h_ote_pz", "Pz of inner tracker endcap hits; Pz [GeV]; Entries", 20000, -10000, 10000)
    h_ote_edep = ROOT.TH1F("h_ote_edep", "Energy deposition of inner tracker endcap hits; Energy [MeV]; Entries", 1000, 0, 1)
    h_ote_x = ROOT.TH1F("h_ote_x", "X of inner tracker endcap hits; X [mm]; Entries", 5000, -5000, 5000)
    h_ote_y = ROOT.TH1F("h_ote_y", "Y of inner tracker endcap hits; Y [mm]; Entries", 5000, -5000, 5000)
    h_ote_z = ROOT.TH1F("h_ote_z", "Z of inner tracker endcap hits; Z [mm]; Entries", 5000, -5000, 5000)
    h_ote_phi = ROOT.TH1F("h_ote_phi", "Phi of inner tracker endcap hits; Phi [radian]; Entries", 6400, -3.2, 3.2)
    h_ote_eta = ROOT.TH1F("h_ote_eta", "Eta of inner tracker endcap hits; Eta; Entries", 2000, -10, 10)
    h_ote_pt = ROOT.TH1F("h_ote_pt", "Pt of inner tracker endcap hits; Pt [GeV]; Entries", 1000, 0, 5)
    h_ote_r_z = ROOT.TH2F("h_ote_r_z", "R vs Z of outer tracker endcap hits; Z [mm]; R [mm]", 1000, -5000, 5000, 400, 0, 2000)
    h_ote_r_phi = ROOT.TH2F("h_ote_r_phi", "R vs Phi of outer tracker endcap hits; Phi [radians]; R [mm]", 6400, -3.2, 3.2, 400, 0, 2000)

    w = 2400
    
    for i in range(len(vxb_px)):
        h_vxb_px.Fill(vxb_px[i], w)
        h_vxb_py.Fill(vxb_py[i], w)
        h_vxb_pz.Fill(vxb_pz[i], w)
        h_vxb_edep.Fill(vxb_edep[i], w)
        h_vxb_x.Fill(vxb_x[i], w)
        h_vxb_y.Fill(vxb_y[i], w)
        h_vxb_z.Fill(vxb_z[i], w)
        h_vxb_pt.Fill(vxb_pt[i], w)
        h_vxb_eta.Fill(vxb_eta[i], w)
        h_vxb_phi.Fill(vxb_phi[i], w)
        h_vxb_r_z.Fill(vxb_z[i], sqrt(vxb_x[i]**2 + vxb_y[i]**2), w)
        h_vxb_r_phi.Fill(vxb_phi[i], sqrt(vxb_x[i]**2 + vxb_y[i]**2), w)
    for i in range(len(vxe_px)):
        h_vxe_px.Fill(vxe_px[i], w)
        h_vxe_py.Fill(vxe_py[i], w)
        h_vxe_pz.Fill(vxe_pz[i], w)
        h_vxe_edep.Fill(vxe_edep[i], w)
        h_vxe_x.Fill(vxe_x[i], w)
        h_vxe_y.Fill(vxe_y[i], w)
        h_vxe_z.Fill(vxe_z[i], w)
        h_vxe_pt.Fill(vxe_pt[i], w)
        h_vxe_eta.Fill(vxe_eta[i], w)
        h_vxe_phi.Fill(vxe_phi[i], w)
        h_vxe_r_z.Fill(vxe_z[i], sqrt(vxe_x[i]**2 + vxe_y[i]**2), w)
        h_vxe_r_phi.Fill(vxe_phi[i], sqrt(vxe_x[i]**2 + vxe_y[i]**2), w)
    for i in range(len(itb_px)):
        h_itb_px.Fill(itb_px[i], w)
        h_itb_py.Fill(itb_py[i], w)
        h_itb_pz.Fill(itb_pz[i], w)
        h_itb_edep.Fill(itb_edep[i], w)
        h_itb_x.Fill(itb_x[i], w)
        h_itb_y.Fill(itb_y[i], w)
        h_itb_z.Fill(itb_z[i], w)
        h_itb_pt.Fill(itb_pt[i], w)
        h_itb_eta.Fill(itb_eta[i], w)
        h_itb_phi.Fill(itb_phi[i], w)
        h_itb_r_z.Fill(itb_z[i], sqrt(itb_x[i]**2 + itb_y[i]**2), w)
        h_itb_r_phi.Fill(itb_phi[i], sqrt(itb_x[i]**2 + itb_y[i]**2), w)
    for i in range(len(ite_px)):
        h_ite_px.Fill(ite_px[i], w)
        h_ite_py.Fill(ite_py[i], w)
        h_ite_pz.Fill(ite_pz[i], w)
        h_ite_edep.Fill(ite_edep[i], w)
        h_ite_x.Fill(ite_x[i], w)
        h_ite_y.Fill(ite_y[i], w)
        h_ite_z.Fill(ite_z[i], w)
        h_ite_pt.Fill(ite_pt[i], w)
        h_ite_eta.Fill(ite_eta[i], w)
        h_ite_phi.Fill(ite_phi[i], w)
        h_ite_r_z.Fill(ite_z[i], sqrt(ite_x[i]**2 + ite_y[i]**2), w)
        h_ite_r_phi.Fill(ite_phi[i], sqrt(ite_x[i]**2 + ite_y[i]**2), w)
    for i in range(len(otb_px)):
        h_otb_px.Fill(otb_px[i], w)
        h_otb_py.Fill(otb_py[i], w)
        h_otb_pz.Fill(otb_pz[i], w)
        h_otb_edep.Fill(otb_edep[i], w)
        h_otb_x.Fill(otb_x[i], w)
        h_otb_y.Fill(otb_y[i], w)
        h_otb_z.Fill(otb_z[i], w)
        h_otb_pt.Fill(otb_pt[i], w)
        h_otb_eta.Fill(otb_eta[i], w)
        h_otb_phi.Fill(otb_phi[i], w)
        h_otb_r_z.Fill(otb_z[i], sqrt(otb_x[i]**2 + otb_y[i]**2), w)
        h_otb_r_phi.Fill(otb_phi[i], sqrt(otb_x[i]**2 + otb_y[i]**2), w)
    for i in range(len(ote_px)):
        h_ote_px.Fill(ote_px[i], w)
        h_ote_py.Fill(ote_py[i], w)
        h_ote_pz.Fill(ote_pz[i], w)
        h_ote_edep.Fill(ote_edep[i], w)
        h_ote_x.Fill(ote_x[i], w)
        h_ote_y.Fill(ote_y[i], w)
        h_ote_z.Fill(ote_z[i], w)
        h_ote_pt.Fill(ote_pt[i], w)
        h_ote_eta.Fill(ote_eta[i], w)
        h_ote_phi.Fill(ote_phi[i], w)
        h_ote_r_z.Fill(ote_z[i], sqrt(ote_x[i]**2 + ote_y[i]**2), w)
        h_ote_r_phi.Fill(ote_phi[i], sqrt(ote_x[i]**2 + ote_y[i]**2), w)

    root_file.Write()

                    
def get_collection(event, name):
    names = event.getCollectionNames()
    if name in names:
        return event.getCollection(name)
    return []


if __name__ == "__main__":
    main()
