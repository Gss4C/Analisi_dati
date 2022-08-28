/* 
Full exercise
Using ROOT make following steps in order to make a likelihood methods study for datasets "Exercise_Likelihood_n" containing simulations of signals+background
    A) Plot and fit histograms using various models for background signal  
    B) Do a likelihood scan of "S" and "B" parameters (counting for signal and background)
    C) Do a profile likelihood scan of the "S" Parameter
*/
#include <vector>
using namespace std;
TH1F *histo_fromfile(string filename)
{
    ifstream f(filename + ".txt");
    float xs;
    TH1F *h1 = new TH1F("Istogramma", filename.c_str(), 100, 0, 1000);
    while (!f.eof())
    {
        f >> xs;
        h1->Fill(xs);
    }
    return h1;
}

vector<Double_t> data_from_file(string filename)
{
    ifstream f(filename + ".txt");
    vector<Double_t> data;
    Double_t xs;

    while (!f.eof())
    {
        f >> xs;
        data.push_back(xs);
    }
    return data;
}

void Exercise_A_histo_fit()
{
    //The following lines (commented) was the first try, with only one dataset
    /*
    TF1 *pdf = new TF1("pdf" , "1/([0]+[1]) * TMath::Poisson( [5] , [0]+[1]) * ( [0]/(sqrt(2*TMath::Pi()*[4]*[4])) * TMath::Exp(-((x - [3]) * (x - [3])) / (2 *[4] *[4])) + [1]/([2]) * TMath::Exp(-x/[2]))", 0 , 1000); 
    TCanvas *c = new TCanvas();
    TH1F *h1 = histo_fromfile("exercise_Likelihood_1"); 
    pdf->SetParameters(250, 800, 200, 400, 70, 1223); //Qui setto i parametri del modello 1 a random per provare, non sono importanti perché tanto vanno cambiati
    pdf->FixParameter(5, 1223);
    pdf->FixParameter(4, 70);
    pdf->FixParameter(3, 400);
    pdf->FixParameter(2, 200);
    h1->Fit(pdf, "L");
    // double scale_factor = 1/(h1->Integral());
    h1->Scale(0.000001);
    h1->Draw("");
    */

    TF1 *pdf = new TF1("pdf" , "1/([0]+[1]) * TMath::Poisson( [5] , [0]+[1]) * ( [0]/(sqrt(2*TMath::Pi()*[4]*[4])) * TMath::Exp(-((x - [3]) * (x - [3])) / (2 *[4] *[4])) + [1]/([2]) * TMath::Exp(-x/[2]))", 0 , 1000);

    for(int i=1 ; i<5 ; i++ )
    {
        TCanvas *c = new TCanvas();
        TH1F *h1 = histo_fromfile(("exercise_Likelihood_" + to_string(i)).c_str());
        vector<Double_t> parameters = data_from_file(("model_"+to_string(i)).c_str()); 
        int N = h1->Integral();
        pdf->SetParameters(250, 800, parameters.at(2), parameters.at(0), parameters.at(1), N); //Qui setto i parametri del modello 1 a random per provare
            pdf->FixParameter(5, N);
            pdf->FixParameter(4, parameters.at(1));
            pdf->FixParameter(3, parameters.at(0));
            pdf->FixParameter(2, parameters.at(2));
        h1->Fit(pdf, "L");
        h1->Scale(0.000001);
        h1->Draw(""); //Creo plot per gli istogrammi appena creati
    }
}