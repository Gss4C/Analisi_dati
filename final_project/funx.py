import ROOT
import particle as pt

def eff(ns,np):
    rs=np/ns 
    n_ps=np*rs
    es=n_ps/ns
    return es

def two_hist(h1,h2):
    h1.Scale(1/h1.Integral())
    h2.Scale(1/h2.Integral())
    h1.SetLineColor(ROOT.kRed)
    """h2.Draw("hist")
    h1.Draw("SAME,hist")"""
    return h1,h2

#def n_histos():

def histos_cut(dytr,h_jsz,h_met,h_je,h_jpt,h_dz,h_dB,h_pt,h_iD):
    for k in range(dytr.GetEntries()):
        dytr.GetEntry(k)
        if(dytr.muontracks_size >=2):
            muons = pt.get_collection(dytr, "muontracks")
            passing = 0
            for mi in range(len(muons)):
                if(dytr.muontracks_dz[mi]<0.005 and dytr.muontracks_dB[mi]<0.003 and dytr.muontracks_isoDeposits[mi]<4): #Taglio del tag
                    for mj in range(len(muons)):
                        if(mi!=mj and dytr.muontracks_dz[mj]<0.014 and dytr.muontracks_dB[mj]<0.007 and dytr.muontracks_isoDeposits[mj]<9): 
                            passing = 1
            if(passing==1):
                h_jsz.Fill(dytr.jets_size)
                h_met.Fill(dytr.met_pt[0])
                for jet in range(dytr.jets_size):
                    h_je.Fill(dytr.jets_e[jet])
                    h_jpt.Fill(dytr.jets_pt[jet])
                for m in range(dytr.muontracks_size):
                    h_dz.Fill(dytr.muontracks_dz[m])
                    h_dB.Fill(dytr.muontracks_dB[m])
                    h_pt.Fill(dytr.muontracks_pt[m])
                for z in range(dytr.muontracks_size):
                    h_iD.Fill(dytr.muontracks_isoDeposits[m])

    return h_jsz,h_met,h_je,h_jpt,h_dz,h_dB,h_pt,h_iD