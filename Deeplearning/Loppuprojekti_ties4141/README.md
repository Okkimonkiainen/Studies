## Syöpäsolukon tunnistaminen normaalikudoksesta

**Tekijä:** Tiina Tuomisto, tiina.tt.tuomisto@jyu.fi

**Tiivistelmä**: Imusolmukekudoksen syöpäsolukon tunnistaminen normaalista solukosta, Kagglen kilpailun [Histopathologic Cancer Detection](https://www.kaggle.com/competitions/histopathologic-cancer-detection/overview) datasettejä käyttäen.


## Testattu seuraavilla kirjastoilla

- Python 3.9.17
- [Tensorflow 2.9.0](https://www.tensorflow.org/overview/?hl=fi)
- [Pandas  1.5.3](https://pandas.pydata.org/)
- [NumPy 1.25.2](https://numpy.org/)
- [scikit-learn  1.3.0](https://scikit-learn.org/)
- [matplotlib 3.7.1](https://matplotlib.org/)

## Työn rakenne

```
Loppuprojekti
│   README.md
│   report.md    
│   param_grid.txt
│   data.ipynb
│   gridsearch.ipynb
│   diagnostics_and_predictions.ipynb
│
└───data_pics
└───histopathologic-cancer-detection
└───gs_dnn_ensemble_20231210T1624
└───gs_dnn_ensemble_20231206T1805
└───gs_dnn_ensemble_20231206T1547
```

ks. [raportti](./report.md).

## Tulokset
[Lopullisen CNN-mallin](./gs_dnn_ensemble_20231210T1624/model_infos/CNN-3.png) ja [summary](./gs_dnn_ensemble_20231210T1624/model_infos/CNN-3_summary.txt) suorituskyky evaluointidataa vastaan:

| TP | TN | FN | FP | ACC | PREC | REC | FSCORE
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| 25 968 | 42 727 | 2987 | 5419 | 0.89097 | 0.89684 | 0.82735 | 0.86069 |

[Kagglen antamat pisteet](./gs_dnn_ensemble_20231210T1624/Kaggle_submission_scores.png) kyseiselle mallille. Julkiset pisteet olivat 0.85 ja yksityiseksi pisteeksi saatiin 0.77.