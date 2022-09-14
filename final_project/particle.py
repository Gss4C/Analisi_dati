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

def mass_z_range(tree, var="muontracks", os = 0): #Funzione che fa il confronto fra tutte le particelle e quelle con la massa nel range desiderato (range che deve essere tale da avere eventi prompt)
    # var è il nome della caratteristica che voglio vedere: ad esempio muontracks_chi2
    # se os=0 non faccio distinzione fra os e ss, altrimenti sì
    if(os==0):
        
    if(os==1):
    else:
        print("Error: os parameter shoud be a 0-1 boolean")
