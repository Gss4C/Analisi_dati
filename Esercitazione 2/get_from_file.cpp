//Funzioni continuamente richiamate
//-----------------------------//
using namespace std;

//Funzione che mi restituisce in uscita un vector (di double) con dentro i miei dati
vector<Double_t> fromfile(string filename)
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

//Funzione che legge un file .txt e mi dà in output un istogramma
TH1F *histo_fromfile(string filename)
{
    ifstream f(filename + ".txt");
    float xs;
    TH1F *h1 = new TH1F("Histo_prova", filename.c_str(), 100, 0, 1000);
    while (!f.eof())
    {
        f >> xs;
        h1->Fill(xs);
    }
    return h1;
}

//Funzione che legge 4 differenti file in un ciclo for e salva un istogramma per ognuno di essi
void ex_like_1(string filename)
{
  ifstream f(filename + ".txt");
  float xs;
  TH1F *h1 = new TH1F("Histo_prova", filename.c_str(), 200, 0, 1000);
  while (!f.eof())
  {
    f >> xs;
    //cout << " xs is "<<xs<<endl;
    h1->Fill(xs);
  };
  TCanvas *c = new TCanvas();
  h1->Draw();
  c->SaveAs((filename + ".png").c_str());
}

void getfromfile()
{
  for (int i = 1; i < 5; i++)
  {
    ex_like_1(("exercise_Likelihood_" + to_string(i)).c_str());
  }
} 