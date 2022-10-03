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

def cut_find_histos(tree,h_jsz,h_met,h_je,h_jpt,h_dz,h_dB,h_mass,h_iD):
    for i in range(tree.GetEntries()):
        tree.GetEntry(i)
        if(tree.muontracks_size >=2):
            muons = pt.get_collection(tree, "muontracks")
            passing = 0
            for mi in range(len(muons)):
                if(tree.muontracks_dz[mi]<0.005 and tree.muontracks_dB[mi]<0.003 and tree.muontracks_isoDeposits[mi]<4):
                    for mj in range(len(muons)):
                        if(mi!=mj and tree.muontracks_dz[mj]<0.014 and tree.muontracks_dB[mj]<0.007 and tree.muontracks_isoDeposits[mj]<9):
                            passing = 1
                            s_mu = (muons[mi].p4+muons[mj].p4).M()
                            h_mass.Fill(s_mu)
            if(passing==1):
                #Taglio in distanza angolare jets-leptons + solo 2 jets più energetici
                jets = pt.get_collection(tree, "jets") 
                if(len(jets)>=2):
                    clean_jets = []             #jets con distanza angolare che ci piace
                    sel_j = []                  #solo i 2 più energetici di ogni clean_jets
                    for jj in range(len(jets)): #Selezione jets validi
                        dists=[]                #array di distanze angolari
                        for mm in range(len(muons)):
                            d = ROOT.TMath.Sqrt( ((muons[mm].eta - jets[jj].eta)*(muons[mm].eta - jets[jj].eta)) + ((muons[mm].phi - jets[jj].phi)*(muons[mm].phi -jets[jj].phi)) )
                            dists.append(d)
                        if(min(dists) > 0.4):           #imposizione distanza minima, solo se la minima è soperiroe a 0.4 vado avanti
                            clean_jets.append(jets[jj])
                    if(len(clean_jets)>1):              #non ha senso considerare l'evento se nella selezione resta un solo jet
                        for p in range(2):              #solo 2 per evento
                            sel_j.append(clean_jets[p]) #questi sono i jets che ci piacciono

                        h_jsz.Fill(tree.jets_size)
                        h_met.Fill(tree.met_pt[0])

                        for jet in range(len(sel_j)):
                            h_je.Fill(sel_j[jet].e)
                            h_jpt.Fill(sel_j[jet].pt)
                        for m in range(tree.muontracks_size):   #non ha senso considerare i casi dove ho jets non validi
                            h_dz.Fill(tree.muontracks_dz[m]) #quindi stampo i muoni solo se ho i jets validi
                            h_dB.Fill(tree.muontracks_dB[m]) #esattamente come ho stampato i jets solo dopo il tag & probe
                            h_iD.Fill(tree.muontracks_isoDeposits[m])
    return h_jsz,h_met,h_je,h_jpt,h_dz,h_dB,h_mass,h_iD

def cut_find_small(tree,h_met,h_je,h_jpt,h_mass):
    for i in range(tree.GetEntries()):
        tree.GetEntry(i)
        if(tree.muontracks_size >=2):
            muons = pt.get_collection(tree, "muontracks")
            passing = 0
            for mi in range(len(muons)):
                if(tree.muontracks_dz[mi]<0.014 and tree.muontracks_dB[mi]<0.007 and tree.muontracks_isoDeposits[mi]<9):
                    for mj in range(len(muons)):
                        if(mi!=mj and tree.muontracks_dz[mj]<0.014 and tree.muontracks_dB[mj]<0.007 and tree.muontracks_isoDeposits[mj]<9):
                            passing = 1
                            s_mu = (muons[mi].p4+muons[mj].p4).M()
                            h_mass.Fill(s_mu)
            if(passing==1):
                #Taglio in distanza angolare jets-leptons + solo 2 jets più energetici
                jets = pt.get_collection(tree, "jets") 
                if(len(jets)>=2):
                    clean_jets = []             #jets con distanza angolare che ci piace
                    sel_j = []                  #solo i 2 più energetici di ogni clean_jets
                    for jj in range(len(jets)): #Selezione jets validi
                        dists=[]                #array di distanze angolari
                        for mm in range(len(muons)):
                            d = ROOT.TMath.Sqrt( ((muons[mm].eta - jets[jj].eta)*(muons[mm].eta - jets[jj].eta)) + ((muons[mm].phi - jets[jj].phi)*(muons[mm].phi -jets[jj].phi)) )
                            dists.append(d)
                        if(min(dists) > 0.4):           #imposizione distanza minima, solo se la minima è soperiroe a 0.4 vado avanti
                            clean_jets.append(jets[jj])
                    if(len(clean_jets)>1):              #non ha senso considerare l'evento se nella selezione resta un solo jet
                        for p in range(2):              #solo 2 per evento
                            sel_j.append(clean_jets[p]) #questi sono i jets che ci piacciono

                        h_met.Fill(tree.met_pt[0])

                        for jet in range(len(sel_j)):
                            h_je.Fill(sel_j[jet].e)
                            h_jpt.Fill(sel_j[jet].pt)
    return h_met,h_je,h_jpt,h_mass

def cut_make(tree,h_met,h_je,h_jpt,h_mass):
    n_events=0
    for i in range(tree.GetEntries()):
        tree.GetEntry(i)
        if(tree.muontracks_size >=2):
            muons = pt.get_collection(tree, "muontracks")
            passing = 0
            for mi in range(len(muons)):
                if(tree.muontracks_dz[mi]<0.014 and tree.muontracks_dB[mi]<0.007 and tree.muontracks_isoDeposits[mi]<9):
                    for mj in range(len(muons)):
                        if(mi!=mj and tree.muontracks_dz[mj]<0.014 and tree.muontracks_dB[mj]<0.007 and tree.muontracks_isoDeposits[mj]<9):
                            passing = 1
                            s_mu = (muons[mi].p4+muons[mj].p4).M()
                            h_mass.Fill(s_mu)
            if(passing==1):
                #Taglio in distanza angolare jets-leptons + solo 2 jets più energetici
                jets = pt.get_collection(tree, "jets") 
                if(len(jets)>=2):
                    clean_jets = []             #jets con distanza angolare che ci piace
                    sel_j = []                  #solo i 2 più energetici di ogni clean_jets
                    for jj in range(len(jets)): #Selezione jets validi
                        dists=[]                #array di distanze angolari
                        for mm in range(len(muons)):
                            d = ROOT.TMath.Sqrt( ((muons[mm].eta - jets[jj].eta)*(muons[mm].eta - jets[jj].eta)) + ((muons[mm].phi - jets[jj].phi)*(muons[mm].phi -jets[jj].phi)) )
                            dists.append(d)
                        if(min(dists) > 0.4):           #imposizione distanza minima, solo se la minima è soperiroe a 0.4 vado avanti
                            clean_jets.append(jets[jj])
                    if(len(clean_jets)>1):              #non ha senso considerare l'evento se nella selezione resta un solo jet
                        for p in range(2):              #solo 2 per evento
                            sel_j.append(clean_jets[p]) #questi sono i jets che ci piacciono

                        if(tree.met_pt[0]>=35):
                            top = 0
                            if(sel_j[0].pt >= 45 and sel_j[1].pt >= 45 ):
                                top = 1
                            if(top == 1):
                                n_events = n_events + 1
                                h_met.Fill(tree.met_pt[0])
                                for jet in range(len(sel_j)):
                                    h_je.Fill(sel_j[jet].e)
                                    h_jpt.Fill(sel_j[jet].pt)
    n_jet = h_jpt.Integral()
    n_met = h_met.Integral()
    return h_met,h_je,h_jpt,h_mass, n_jet, n_met, n_events

def cut_make_revert(tree,h_met,h_je,h_jpt,h_mass):
    n_events=0
    for i in range(tree.GetEntries()):
        tree.GetEntry(i)
        if(tree.muontracks_size >=2):
            muons = pt.get_collection(tree, "muontracks")
            passing = 0
            for mi in range(len(muons)):
                if(tree.muontracks_dz[mi]<0.014 and tree.muontracks_dB[mi]<0.007 and tree.muontracks_isoDeposits[mi]<9):
                    for mj in range(len(muons)):
                        if(mi!=mj and tree.muontracks_dz[mj]<0.014 and tree.muontracks_dB[mj]<0.007 and tree.muontracks_isoDeposits[mj]<9):
                            passing = 1
                            s_mu = (muons[mi].p4+muons[mj].p4).M()
                            h_mass.Fill(s_mu)
            if(passing==0):
                #Taglio in distanza angolare jets-leptons + solo 2 jets più energetici
                jets = pt.get_collection(tree, "jets") 
                if(len(jets)>=2):
                    clean_jets = []             #jets con distanza angolare che ci piace
                    sel_j = []                  #solo i 2 più energetici di ogni clean_jets
                    for jj in range(len(jets)): #Selezione jets validi
                        dists=[]                #array di distanze angolari
                        for mm in range(len(muons)):
                            d = ROOT.TMath.Sqrt( ((muons[mm].eta - jets[jj].eta)*(muons[mm].eta - jets[jj].eta)) + ((muons[mm].phi - jets[jj].phi)*(muons[mm].phi -jets[jj].phi)) )
                            dists.append(d)
                        if(min(dists) > 0.4):           #imposizione distanza minima, solo se la minima è soperiroe a 0.4 vado avanti
                            clean_jets.append(jets[jj])
                    if(len(clean_jets)>1):              #non ha senso considerare l'evento se nella selezione resta un solo jet
                        for p in range(2):              #solo 2 per evento
                            sel_j.append(clean_jets[p]) #questi sono i jets che ci piacciono

                        if(tree.met_pt[0]>=35):
                            top = 0
                            if(sel_j[0].pt >= 45 and sel_j[1].pt >= 45 ):
                                top = 1
                            if(top == 1):
                                n_events = n_events + 1
                                h_met.Fill(tree.met_pt[0])
                                for jet in range(len(sel_j)):
                                    h_je.Fill(sel_j[jet].e)
                                    h_jpt.Fill(sel_j[jet].pt)
    n_jet = h_jpt.Integral()
    n_met = h_met.Integral()
    return h_met,h_je,h_jpt,h_mass, n_jet, n_met, n_events

def n4(var = "dy"):
    L = 3.1 # pb^-1
    sigma_dy = 3048 #pb
    sigma_tt = 17.48 #pb
    w_norm = 0
    if(var == "dy"):
        w_norm= 1/10000 * L * sigma_dy
    if(var == "tt"):
        w_norm = 1/5000 * L * sigma_tt

    return w_norm

"""def n4(n_jet, n_met, var = "dy"): #vecchia versione rotta
L = 3.1 # pb^-1
sigma_dy = 3048 #pb
sigma_tt = 17.48 #pb
w_norm_jet = 0
w_norm_met = 0
if(var == "dy"):
    w_norm_jet = 1/n_jet * L * sigma_dy
    w_norm_met = 1/n_met * L * sigma_dy
if(var == "tt"):
    w_norm_jet = 1/n_jet * L * sigma_tt
    w_norm_met = 1/n_met * L * sigma_tt

return w_norm_jet,w_norm_met"""