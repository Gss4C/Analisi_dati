/* 
Full exercise
Using ROOT make following steps in order to make a likelihood methods study for datasets "Exercise_Likelihood_n" containing simulations of signals+background
    A) Plot and fit histograms using various models for background signal  
    B) Do a likelihood scan of "S" and "B" parameters (counting for signal and background)
    C) Do a profile likelihood scan of the "S" Parameter
*/
using namespace std;
 //Functions
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
Double_t extended_likelihood(int s, int b, int N, vector<Double_t> x, vector<Double_t> theta)
{
    //Considero che s+b=N
    TF1 *pdfs_xi=new TF1("pdfs_xi", "-2* ([0]/(sqrt(2*TMath::Pi()*[4]*[4])) * TMath::Exp(-((x - [3]) * (x - [3])) / (2 *[4] *[4])) + [1]/([2]) * TMath::Exp(-x/[2]))",0,1000);
        /* Readible formula
            -2 *
            (
                [0]/(sqrt(2*TMath::Pi()*[4]*[4])) * TMath::Exp(-((x - [3]) * (x - [3])) / (2 *[4] *[4])) + 
                [1]/([2]) * TMath::Exp(-x/[2])
            )
        */
    pdfs_xi->SetParameters( s , b,theta.at(2),theta.at(0),theta.at(1),N);
    Double_t sum = 0;
    for(int i=0 ; i<N ; i++)
    {
        sum += pdfs_xi->Eval(x.at(i));
    }
    Double_t output = 2*(s+ b+ N* (TMath::Log(N)-1))+sum;
    return output;
}


void Exercise_B_histo_fit()
{
    TCanvas *c = new TCanvas();
    vector<Double_t> X = data_from_file("exercise_Likelihood_1");
    vector<Double_t> theta = data_from_file("model_1");
    int N = X.size();
    
    // S+B=N case
        Double_t yi, y[N], s_fin[N];
        //int b=980;
        for(int s = 19; s < N; s++)
        {
            int b=N-s;
            yi = extended_likelihood(s, b, N, X, theta);
            y[s - 19] = yi;
            s_fin[s - 19] = s;
        }
        TGraph *g1=new TGraph(N - 19, s_fin, y);
        g1->SetTitle("Logaritmo della Likelihood al variare di S");
        g1->GetXaxis()->SetTitle("S");
        g1->GetYaxis()->SetTitle("-2*Log(L)");
        g1->SetMarkerStyle(4);
        g1->SetMarkerColor(4);
        g1->Draw("AP");
    // S+B!=N case
}