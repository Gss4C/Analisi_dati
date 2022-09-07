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
    Double_t output = 0;
    Double_t sum = 0;
    TF1 *pdfs_xi = new TF1("pdfs_xi", "-2* TMath::Log( [0]/sqrt(2*TMath::Pi()*[4]*[4])*TMath::Exp(-((x - [3]) * (x - [3])) / (2 *[4] *[4])) + [1] /([2]) * TMath::Exp(-x / [2]))",0,1000);
    pdfs_xi->SetParameters(s, b, theta.at(2), theta.at(0), theta.at(1));

    for(int i=0 ; i < N ; i++)
    {
        sum += pdfs_xi->Eval(x.at(i));
    }
    output = sum - 2 * TMath::Log(TMath::Poisson(N, s + b)) + 2 * N * TMath::Log(s + b);
    return output;
}


void Exercise_B_histo_fit()
{
    cout<<"press 0 for only s varying, press 1 for both s and b varying"<<endl;
    int if_par;
    cin>>if_par;

    if(if_par == 0)
    {
        for(int i = 1 ; i < 5 ; i++) //only s varying
        {
            TCanvas *c = new TCanvas();
            vector<Double_t> X = data_from_file(("exercise_Likelihood_" + to_string(i)).c_str());
            vector<Double_t> theta = data_from_file(("model_" + to_string(i)).c_str());

            int N = X.size();
            Double_t yi, y[N], s_fin[N];
            
            int b = 950;
            for(int s = 15; s < N; s++)
            {
                yi = extended_likelihood(s, b, N, X, theta);
                y[s - 19] = yi;
                s_fin[s - 19] = s;
            }

            TGraph *g=new TGraph(N - 19, s_fin, y);
                g->SetTitle(("Log-Like, var S, dataset_" + to_string(i)).c_str());
                g->GetXaxis()->SetTitle("S");
                g->GetYaxis()->SetTitle("-2*Log(L)");
                g->SetMarkerStyle(4);
                g->SetMarkerColor(4);
                g->Draw("AP");
        }
    }
    else if(if_par == 1)
    {
        for(int i = 1; i < 5; i++)
        {
            TCanvas *c = new TCanvas();
            TGraph2D *g2 = new TGraph2D();
            vector<Double_t> X = data_from_file(("exercise_Likelihood_" + to_string(i)).c_str());
            vector<Double_t> theta = data_from_file(("model_" + to_string(i)).c_str());
            vector<Double_t> L, S, B;
            int N = X.size();
            Double_t yi, y[N], s_fin[N];

            int k=0;
            for(int s = 0; s < N; s += 10)
            {
                for(int b = 0; b < N; b += 10)
                {
                    if(s+b > 0.26 * N && s+b < 2.5 * N)
                    {
                        Double_t like = extended_likelihood(s,b,N,X,theta);
                        g2->SetPoint(k, s, b, like);

                        S.push_back(s);
                        B.push_back(b);
                        L.push_back(like);

                        k++;
                    }
                    else
                    {
                        g2->SetPoint(k, s, b, 16000);
                        k++;
                    }
                }
            }

            double lMin = *min_element(L.begin(), L.end());
            std::vector<double>::iterator it = find(L.begin(), L.end(), lMin);
            int distance = std::distance(L.begin(), it);
                cout << ("Dataset N. "+to_string(i)).c_str();
                cout << "position " << distance << endl;
                cout << "s min = " << S.at(distance) << endl;
                cout << "b min = " << B.at(distance) << endl;
                cout << "-2ln(L) min = " << lMin << endl <<endl;

            g2->SetTitle(("-2*log(L(s,b)) Dataset_"+to_string(i)).c_str());
            g2->GetXaxis()->SetTitle("S");
            g2->GetYaxis()->SetTitle("B");
            g2->SetMarkerStyle(22);
            g2->Draw("surf1");
        }
    }
    else
    {
        cout<<"Error: non valid value, try running again"<<endl;
    }
}