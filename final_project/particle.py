import ROOT
class particle:
    def __init__ (self, pt, eta, phi, e, charge, flavor):
        self.pt=pt
        self.eta=eta
        self.phi=phi
        self.e=e
        self.charge=charge
        self.flavor=flavor
        self.p4=ROOT.TLorentzVector()
        self.p4.SetPtEtaPhiE(pt,eta,phi,e)

def eff(ns,np):
    rs=np/ns 
    n_ps=np*rs
    es=n_ps/ns
    return es

def get_particle(tree="tree", var="muontracks", index=0):
    flav_dict={"muontracks":13, "electrons":11}
    p=particle(getattr(tree,var+"_pt")[index],
               getattr(tree,var+"_eta")[index],
               getattr(tree,var+"_phi")[index],
               getattr(tree,var+"_e")[index],
               getattr(tree,var+"_charge")[index] if hasattr(tree,var+"_charge") else  0,
               -1*getattr(tree,var+"_charge")[index]*(flav_dict[var]) if hasattr(tree,var+"_charge") else 0)
    return p

def get_collection(tree="tree", var="muontracks"):
    particles=[get_particle(tree,var,i) for i in range (getattr(tree,var+"_size"))]
    return particles

def two_hist(c,h1,h2):
    c=ROOT.TCanvas()
    h1.Scale(1/h1.Integral())
    h2.Scale(1/h2.Integral())
    c.Draw()
    h1.SetLineColor(ROOT.kRed)
    h2.Draw("hist")
    h1.Draw("SAME,hist")
    return c,h1,h2

def plot_part_mass(file, tree, var="muontracks"):
    file.cd()
    are_os = lambda x,y: x.charge*y.charge<0
    are_ss = lambda x,y: x.charge*y.charge>0
    c2=ROOT.TCanvas("Masses")
    h_mass_os=ROOT.TH1F("h_mass_os",("Mass of "+var+" os"),100,0,150)
    h_mass_ss=ROOT.TH1F("h_mass_ss",("Mass of "+var+" ss"),100,0,150)
    for i in range(tree.GetEntries()):
        tree.GetEntry(i)
        part=get_collection(tree,var) 
        
        for mi in range(len(part)):
            for mj in range(mi):
                if(are_os(part[mi],part[mj])):
                    h_mass_os.Fill((part[mi].p4+part[mj].p4).M())
                else:
                    h_mass_ss.Fill((part[mi].p4+part[mj].p4).M())
    c2.Draw()
    h_mass_os.Draw()
    h_mass_ss.SetLineColor(ROOT.kRed)
    h_mass_ss.Draw("same")
    c2.SetLogy()
    #c2.SaveAs("masses_"+var+".JPG")
    return c2, h_mass_os, h_mass_ss


def mass_z_range(file, tree, var="muontracks_chi2", n_bin=100, min=0, max=100 ,os=0): #Funzione che fa il confronto fra tutte le particelle e quelle con la massa nel range desiderato (range che deve essere tale da avere eventi prompt)
    # var è il nome della caratteristica che voglio vedere: ad esempio muontracks_chi2
    # is os=0 I don't distinguish OS and SS, is os==1 I do it
        
    if(os==0):
        if(var == "muontracks_chi2"):
            file.cd()
            c=ROOT.TCanvas()
            h_all = ROOT.TH1F(var,var, n_bin,min,max)
            h_cut = ROOT.TH1F(var,var, n_bin,min,max)
            for i in range(tree.GetEntries()):
                tree.GetEntry(i)
                muons = get_collection(tree, "muontracks")
                for mi in range(len(muons)):
                    chi2 = tree.muontracks_chi2[mi]
                    h_all.Fill(chi2)
                    for mj in range(mi):
                        s = (muons[mi].p4 + muons[mj].p4).M()
                        if(s>80 and s<100):
                            h_cut.Fill(tree.muontracks_chi2[mj])
            c.Draw()
            h_cut.SetLineColor(ROOT.kRed)
            h_cut.Scale(1/h_cut.Integral())
            h_cut.Draw("hist")
            h_all.SetLineColor(ROOT.kBlue)
            h_all.Scale(1/h_all.Integral())
            h_all.Draw("SAME,hist")
            return c, h_cut, h_all
        if(var == "muontracks_dz"):
            file.cd()
            c=ROOT.TCanvas()
            h_all = ROOT.TH1F(var,var, n_bin,min,max)
            h_cut = ROOT.TH1F(var,var, n_bin,min,max)
            for i in range(tree.GetEntries()):
                tree.GetEntry(i)
                muons = get_collection(tree, "muontracks")
                for mi in range(len(muons)):
                    dz = tree.muontracks_dz[mi]
                    h_all.Fill(dz)
                    for mj in range(mi):
                        s = (muons[mi].p4 + muons[mj].p4).M()
                        if(s>80 and s<100):
                            h_cut.Fill(tree.muontracks_dz[mj])
            c.Draw()
            h_cut.SetLineColor(ROOT.kRed)
            h_cut.Scale(1/h_cut.Integral())
            h_cut.Draw("hist")
            h_all.SetLineColor(ROOT.kBlue)
            h_all.Scale(1/h_all.Integral())
            h_all.Draw("SAME,hist")
            return c, h_cut, h_all
        if(var == "muontracks_dB"):
            file.cd()
            c=ROOT.TCanvas()
            h_all = ROOT.TH1F(var,var, n_bin,min,max)
            h_cut = ROOT.TH1F(var,var, n_bin,min,max)
            for i in range(tree.GetEntries()):
                tree.GetEntry(i)
                muons = get_collection(tree, "muontracks")
                for mi in range(len(muons)):
                    dB = tree.muontracks_dB[mi]
                    h_all.Fill(dB)
                    for mj in range(mi):
                        s = (muons[mi].p4 + muons[mj].p4).M()
                        if(s>80 and s<100):
                            h_cut.Fill(tree.muontracks_dB[mj])
            c.Draw()
            h_cut.SetLineColor(ROOT.kRed)
            h_cut.Scale(1/h_cut.Integral())
            h_cut.Draw("hist")
            h_all.SetLineColor(ROOT.kBlue)
            h_all.Scale(1/h_all.Integral())
            h_all.Draw("SAME,hist")
            return c, h_cut, h_all
        if(var == "muontracks_isoDeposits"):
            file.cd()
            c=ROOT.TCanvas()
            h_all = ROOT.TH1F(var,var, n_bin,min,max)
            h_cut = ROOT.TH1F(var,var, n_bin,min,max)
            for i in range(tree.GetEntries()):
                tree.GetEntry(i)
                muons = get_collection(tree, "muontracks")
                for mi in range(len(muons)):
                    isoDeposits = tree.muontracks_isoDeposits[mi]
                    h_all.Fill(isoDeposits)
                    for mj in range(mi):
                        s = (muons[mi].p4 + muons[mj].p4).M()
                        if(s>80 and s<100):
                            h_cut.Fill(tree.muontracks_isoDeposits[mj])
            c.Draw()
            h_cut.SetLineColor(ROOT.kRed)
            h_cut.Scale(1/h_cut.Integral())
            h_cut.Draw("hist")
            h_all.SetLineColor(ROOT.kBlue)
            h_all.Scale(1/h_all.Integral())
            h_all.Draw("SAME,hist")
            return c, h_cut, h_all
    if(os==1):
        print("Selecting only OS muons in the mass range")
        are_os = lambda x,y: x.charge*y.charge<0
        if(var == "muontracks_chi2"):
            file.cd()
            c=ROOT.TCanvas()
            h_all = ROOT.TH1F(var,var, n_bin,min,max)
            h_cut = ROOT.TH1F(var,var, n_bin,min,max)
            for i in range(tree.GetEntries()):
                tree.GetEntry(i)
                muons = get_collection(tree, "muontracks")
                for mi in range(len(muons)):
                    chi2 = tree.muontracks_chi2[mi]
                    h_all.Fill(chi2)
                    for mj in range(mi):
                        s = (muons[mi].p4 + muons[mj].p4).M()
                        if(s>80 and s<100):
                            if(are_os(muons[mi],muons[mj])):
                                h_cut.Fill(tree.muontracks_chi2[mj])
            c.Draw()
            h_cut.SetLineColor(ROOT.kRed)
            h_cut.Scale(1/h_cut.Integral())
            h_cut.Draw("hist")
            h_all.SetLineColor(ROOT.kBlue)
            h_all.Scale(1/h_all.Integral())
            h_all.Draw("SAME,hist")
            return c, h_cut, h_all
        if(var == "muontracks_dz"):
            file.cd()
            c=ROOT.TCanvas()
            h_all = ROOT.TH1F(var,var, n_bin,min,max)
            h_cut = ROOT.TH1F(var,var, n_bin,min,max)
            for i in range(tree.GetEntries()):
                tree.GetEntry(i)
                muons = get_collection(tree, "muontracks")
                for mi in range(len(muons)):
                    dz = tree.muontracks_dz[mi]
                    h_all.Fill(dz)
                    for mj in range(mi):
                        s = (muons[mi].p4 + muons[mj].p4).M()
                        if(s>80 and s<100):
                            if(are_os(muons[mi],muons[mj])):
                                h_cut.Fill(tree.muontracks_dz[mj])
            c.Draw()
            h_cut.SetLineColor(ROOT.kRed)
            h_cut.Scale(1/h_cut.Integral())
            h_cut.Draw("hist")
            h_all.SetLineColor(ROOT.kBlue)
            h_all.Scale(1/h_all.Integral())
            h_all.Draw("SAME,hist")
            return c, h_cut, h_all
        if(var == "muontracks_dB"):
            file.cd()
            c=ROOT.TCanvas()
            h_all = ROOT.TH1F(var,var, n_bin,min,max)
            h_cut = ROOT.TH1F(var,var, n_bin,min,max)
            for i in range(tree.GetEntries()):
                tree.GetEntry(i)
                muons = get_collection(tree, "muontracks")
                for mi in range(len(muons)):
                    dB = tree.muontracks_dB[mi]
                    h_all.Fill(dB)
                    for mj in range(mi):
                        s = (muons[mi].p4 + muons[mj].p4).M()
                        if(s>80 and s<100):
                            if(are_os(muons[mi],muons[mj])):
                                h_cut.Fill(tree.muontracks_dB[mj])
            c.Draw()
            h_cut.SetLineColor(ROOT.kRed)
            h_cut.Scale(1/h_cut.Integral())
            h_cut.Draw("hist")
            h_all.SetLineColor(ROOT.kBlue)
            h_all.Scale(1/h_all.Integral())
            h_all.Draw("SAME,hist")
            return c, h_cut, h_all
        if(var == "muontracks_isoDeposits"):
            file.cd()
            c=ROOT.TCanvas()
            h_all = ROOT.TH1F(var,var, n_bin,min,max)
            h_cut = ROOT.TH1F(var,var, n_bin,min,max)
            for i in range(tree.GetEntries()):
                tree.GetEntry(i)
                muons = get_collection(tree, "muontracks")
                for mi in range(len(muons)):
                    isoDeposits = tree.muontracks_isoDeposits[mi]
                    h_all.Fill(isoDeposits)
                    for mj in range(mi):
                        s = (muons[mi].p4 + muons[mj].p4).M()
                        if(s>80 and s<100):
                            if(are_os(muons[mi],muons[mj])):
                                h_cut.Fill(tree.muontracks_isoDeposits[mj])
            c.Draw()
            h_cut.SetLineColor(ROOT.kRed)
            h_cut.Scale(1/h_cut.Integral())
            h_cut.Draw("hist")
            h_all.SetLineColor(ROOT.kBlue)
            h_all.Scale(1/h_all.Integral())
            h_all.Draw("SAME,hist")
            return c, h_cut, h_all    
    if(os==2):
        print("Selecting only OS muons in the mass range")
        are_os = lambda x,y: x.charge*y.charge<0
        if(var == "muontracks_chi2"):
            file.cd()
            c=ROOT.TCanvas()
            h_ss = ROOT.TH1F(var,var, n_bin,min,max)
            h_os = ROOT.TH1F(var,var, n_bin,min,max)
            for i in range(tree.GetEntries()):
                tree.GetEntry(i)
                muons = get_collection(tree, "muontracks")
                for mi in range(len(muons)):
                    for mj in range(mi):
                        if(are_os(muons[mi],muons[mj])):
                            s = (muons[mi].p4 + muons[mj].p4).M()
                            if(s>80 and s<100):
                                h_os.Fill(tree.muontracks_chi2[mj])
                        else:
                            h_ss.Fill(tree.muontracks_chi2[mj])
            c.Draw()
            h_os.SetLineColor(ROOT.kRed)
            h_os.Scale(1/h_os.Integral())
            h_os.Draw("hist")
            h_ss.SetLineColor(ROOT.kBlue)
            h_ss.Scale(1/h_ss.Integral())
            h_ss.Draw("SAME,hist")
            return c, h_os, h_ss
        if(var == "muontracks_dz"):
            file.cd()
            c=ROOT.TCanvas()
            h_ss = ROOT.TH1F(var,var, n_bin,min,max)
            h_os = ROOT.TH1F(var,var, n_bin,min,max)
            for i in range(tree.GetEntries()):
                tree.GetEntry(i)
                muons = get_collection(tree, "muontracks")
                for mi in range(len(muons)):
                    for mj in range(mi):
                        if(are_os(muons[mi],muons[mj])):
                            s = (muons[mi].p4 + muons[mj].p4).M()
                            if(s>80 and s<100):
                                h_os.Fill(tree.muontracks_dz[mj])
                        else:
                            h_ss.Fill(tree.muontracks_dz[mj])
            c.Draw()
            h_os.SetLineColor(ROOT.kRed)
            h_os.Scale(1/h_os.Integral())
            h_os.Draw("hist")
            h_ss.SetLineColor(ROOT.kBlue)
            h_ss.Scale(1/h_ss.Integral())
            h_ss.Draw("SAME,hist")
            return c, h_os, h_ss
        if(var == "muontracks_dB"):
            file.cd()
            c=ROOT.TCanvas()
            h_ss = ROOT.TH1F(var,var, n_bin,min,max)
            h_os = ROOT.TH1F(var,var, n_bin,min,max)
            for i in range(tree.GetEntries()):
                tree.GetEntry(i)
                muons = get_collection(tree, "muontracks")
                for mi in range(len(muons)):
                    for mj in range(mi):
                        if(are_os(muons[mi],muons[mj])):
                            s = (muons[mi].p4 + muons[mj].p4).M()
                            if(s>80 and s<100):
                                h_os.Fill(tree.muontracks_dB[mj])
                        else:
                            h_ss.Fill(tree.muontracks_dB[mj])
            c.Draw()
            h_os.SetLineColor(ROOT.kRed)
            h_os.Scale(1/h_os.Integral())
            h_os.Draw("hist")
            h_ss.SetLineColor(ROOT.kBlue)
            h_ss.Scale(1/h_ss.Integral())
            h_ss.Draw("SAME,hist")
            return c, h_os, h_ss
        if(var == "muontracks_isoDeposits"):
            file.cd()
            c=ROOT.TCanvas()
            h_ss = ROOT.TH1F(var,var, n_bin,min,max)
            h_os = ROOT.TH1F(var,var, n_bin,min,max)
            for i in range(tree.GetEntries()):
                tree.GetEntry(i)
                muons = get_collection(tree, "muontracks")
                for mi in range(len(muons)):
                    for mj in range(mi):
                        if(are_os(muons[mi],muons[mj])):
                            s = (muons[mi].p4 + muons[mj].p4).M()
                            if(s>80 and s<100):
                                h_os.Fill(tree.muontracks_isoDeposits[mj])
                        else:
                            h_ss.Fill(tree.muontracks_isoDeposits[mj])
            c.Draw()
            h_os.SetLineColor(ROOT.kRed)
            h_os.Scale(1/h_os.Integral())
            h_os.Draw("hist")
            h_ss.SetLineColor(ROOT.kBlue)
            h_ss.Scale(1/h_ss.Integral())
            h_ss.Draw("SAME,hist")
            return c, h_os, h_ss