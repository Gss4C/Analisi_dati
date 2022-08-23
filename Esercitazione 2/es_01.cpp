void es_01()
{
    TCanvas * c = new TCanvas("c","c",600,600);
    TF1 * f1 = new TF1("f1" , "TMath::Gaus(x,[0],[1])" , 0 , 1000);
    TF1 * fplusgaus = new TF1("f1plusgaus","f1+gaus",0,1000);
    //fplusgaus.SetParameters(0,???)
    //TF1 * mygaus = new TF1("mygaus" , "" , 0 , 1000);
    
    double mu,sigma;
        cout<<"Media: "<<endl;
        cin>>mu;
        cout<<"Deviazione Standard: "<<endl;
        cin>>sigma;
    f1->SetParameters(mu , sigma);
    //f1->Draw();

    TH1D * h1 = new TH1D("Gaussiana","Gaussiana",100,0,1000);
    h1->FillRandom("f1" , 5000);
    h1->Draw();
}