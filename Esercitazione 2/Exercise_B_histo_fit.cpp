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
TF1 *extended_likelihood(int s, int b, int N, vector<Double_t> x, vector<Double_t> theta)
{
    //Considero che s+b=N
    TF1 *likelihood=new TF1("likelihood", "")
    /* Readible formula
        -2 *
        (
            - N - N * TMath::Log(N) - N +
            
        )
    */
}
//Macro
void Exercise_B_histo_fit()
{
    vector<Double_t> X = data_from_file("exercise_Likelihood_1");
    vector<Double_t> theta = data_from_file("model_1");

    TH1F *h1=histo_fromfile("exercise_Likelihood_1");
    int N = h1->Integral();

    for(int s=1; s<=N; s++)
    {
        int b=N-s;
        //Da qui dovrebbe partire il calcolo della likelihood, perché in teoria ho tutto il necessario
    }
}