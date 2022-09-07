## Full exercise
Using CERN ROOT make following steps in order to make a likelihood methods study for datasets "Exercise_Likelihood_n" containing simulations of signal + background

1. Plot and fit histograms using various models for background signal  
2. Do a likelihood scan of "S" and "B" parameters (counting for signal and background)
3. Do a profile likelihood scan of the "S" Parameter
### Notes
1. Il punto 1 si risolve utilizzando una pdf formata da gaussiana+exp moltiplicate entrambe per una poissoniana. Devo ricordare di mettere avanti i fattori proporzione (sono loro che mi fanno uscire quell' $$1/(s+b)$$ avanti a tutto)
    $$w_s=\frac{s}{s+b} \qquad w_b=\frac{b}{s+b}$$
    Sostituendoceli trovo fondamentalmente l'espressione che segue (che è quella nelle slide, ma senza alcuna produttoria, quella serve per la likelihood) 
    $$f(x)= \frac{1}{s+b} \frac{(s+b)^N e^{-(s+b)}}{N!} \left( \frac{s}{\sqrt{2\pi\sigma^2}} e^{\frac{(x-\mu)^2}{2\sigma^2}} + \frac{b}{\lambda} e^{-\frac{x}{\lambda}} \right)$$ 
Roba che non ho capito:
    - L'espressione nella slide è sbagliata?
        - Noi anche in classe srivemmo, nel codice, sostanzialmente questa espressione qui ed effettivamente usando questa espressione praticamente fatta di una Poisson che moltiplica gaussiana e exp mi trovo. Per l'espressione dentro la slide effettivamente manca un pezzo e non mi trovo
        - No, l'espressione non è sbagliata, infatti facendo la produttoria si mette in evidenza un pezzo $$(s+b)^N$$ sotto che si semplifica con quello sopra
    - Non ho capito per quale ragione, ma tutto viene solo se moltiplico per $$10^{-6}$$
    - Per qualche ragione magica ROOT calcola male la gaussiana e quindi non posso usare TMath::Gaus(), ma devo mettercela a mano
    - Quando ciclo su tutti i file sono abbastanza sicuro di aver fatto bene, ma due fit su 4 vengono un po' male almeno sul lato sinistro dell'istogramma
-   L'ordine numerato dei parametri è il seguente:
    0 - $$s$$
    1 - $$b$$
    2 - $$\lambda$$
    3 - $$\mu$$
    4 - $$\sigma$$
    5 - $$N$$
2. Devo calcolare la seguente funzione di likelihood e utilizzare un ciclo for per far variare tutti i possibili valori di $$s$$ e $$b$$
    La funzione di likelihood utilizzata sarà la seguente (indicando con $$P_S$$ la gaussiana per il segnale e con $$P_B$$ l'esponenziale per il background)
$$\mathcal{L}=\frac{e^{-(s+b)}}{N!}\prod\limits_{i=1}^{N}\left( sP_S(x_i, s,\Theta )+bP_B(x_i, b,\Theta )\right)$$
Dove $$\Theta$$ è il vettore dei parametri del modello utilizzato, contenente i parametri $$\lambda , \sigma , \mu$$. 
Questa sarà dunque utilizzata però nella forma che segue
$$-2\ln (\mathcal{L} )=2\left[s+b+N(\ln N -1)\right]-2\sum\limits_{i=1}^{N}\left( sP_S(x_i, s,\Theta )+bP_B(x_i, b,\Theta )\right)$$
- NB: Non posso usare TMath::Factorial(N) perché come output mi da "inf", devo usare la formula di Stirling: $$\ln (N!)\approx N\ln N -N$$