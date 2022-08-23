/*
    EXERCISE N.1
    1. Using ROOT, write a TF1 Gauss function with arbitrary parameters
    2. Use this Gauss function to randomly fill a histogram
*/

using namespace std;
void es_2_1()
{
    double mu, sigma;
    TCanvas * c = new TCanvas("c","c");
    TCanvas * c1 = new TCanvas("c1","c1");
    TF1 * gss = new TF1("gss", "TMath::Gaus(x, [0], [1])", 0 , 1000);
    TH1F * h = new TH1F("h", "Istogramma della gaussiana inserita", 100, 0 , 1000);

        cout<<"Valor medio desiderato: "<< endl;
        cin>>mu;
        cout<<"Sigma desiderato: "<< endl;
        cin>>sigma; 
        cout<<"Print della funzione desiderata"<<endl;

    gss->SetParameters(mu , sigma);
    c1->cd();
    gss->Draw();
    
    h->FillRandom("gss", 5000);
    c->cd();
    h->Draw();
}