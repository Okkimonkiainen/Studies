"use strict";
//@ts-check
/*jshint esversion: 6 */







//Muuttujat popupia varten:
let arvo="";
let olosuhde="";
let alue="";
let merkki="";
let painonappi="";
document.addEventListener("DOMContentLoaded", function(e) {
    /*Tarkistetaan, mikä on urlin loppuosa ja sen mukaan vaihdetaan
      painonapin väri erilaiseksi, jotta tiedetään millä sivulla ollaan.
    */
    let url=window.location.pathname;
        if(url.length>1){
            url=url.substring(url.indexOf('/')+1);
        }
        let painonapit=document.getElementsByTagName('button');

        for(let i=0; i<painonapit.length; i++){
            if(url==painonapit[i].id){
                painonapit[i].setAttribute('class', 'varinvaihto');
                painonappi=painonapit[i];

            }
        }



    /*Haetaan flaskin puolelta popuppiin liittyvä url ja tarkistetaan siellä onko tullut poikkeavia arvoja tietokantaan
      tehdään hälytys flaskin kautta saadulta poikkeukselta:
    */
        let urlhaku='https://laakehuone.eu.pythonanywhere.com/popup?haetaan=1'
        fetch(urlhaku)
        .then(data=>{
            return data.json();
        })
        .then(tiedot=>{
           if(tiedot.tulos!=undefined && tiedot.olosuhde!=undefined && tiedot.paikka!=undefined){
               arvo=tiedot.tulos;
               olosuhde=tiedot.olosuhde;
               merkki="";

               if(tiedot.paikka=='Avohylly'){
                   alue=tiedot.paikka;
               }
               else if(tiedot.paikka=='Jääkaappi'){
                   alue=tiedot.paikka;
               }
               else if(tiedot.paikka=='Infuusionestelaatikko'){
                   alue=tiedot.paikka;
               }
               else{
                   alue=tiedot.paikka;
               }
               let tulos=tiedot.tulos;

               if(tiedot.olosuhde=='ovi'){
                   tulos='Auki';
               }

               //Luodaan hälytyspopup:
               let halytysdiv=document.getElementsByClassName('halytys');
               for(let i=0; i<halytysdiv.length; i++){
                    halytysdiv[i].setAttribute('class', 'halytysAktivoitu')
                    let otsikko=document.createElement('h4');
                    otsikko.textContent="Poikkeava arvo lääkehuoneen alueella: ";
                    let alueilmoitus=document.createElement('p');
                    let aikailmoitus=document.createElement('p');
                    //Määritellään aika:
                    let aikaHalytys = new Date(tiedot.aika);
                    let kk=aikaHalytys.getUTCMonth(); //arvoksi tulee 0-11
                    let kuukaudet=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
                    let kuukausi=0;
                    for(let k in kuukaudet){
                        if(kk==k){
                            kuukausi=kuukaudet[k];
                        }
                    }
                    //Lisätään tarvittaessa 0, tunnin/minuutin eteen:
                    let tunnit="0";
                    let minuutit="0";
                    if(aikaHalytys.getUTCHours().toString().length<2){
                        tunnit=tunnit+aikaHalytys.getUTCHours().toString();
                    }else{
                        tunnit=aikaHalytys.getUTCHours();
                    }

                    if(aikaHalytys.getUTCMinutes().toString().length<2){
                        minuutit=minuutit+aikaHalytys.getUTCMinutes().toString();
                    }else{
                        minuutit=aikaHalytys.getUTCMinutes();
                    }
                    alueilmoitus.textContent=alue;
                    aikailmoitus.textContent=aikaHalytys.getUTCDate()+"."+kuukausi+"."+aikaHalytys.getUTCFullYear()+", klo: "+tunnit+":"+minuutit;
                    let ilmoitus=document.createElement('p');
                    //Lisätään tarvittaessa yksikkö arvon perään:
                    if(olosuhde=='lämpötila'){
                        merkki='°C';
                    }
                    else if(olosuhde=='ilmankosteus'){
                        merkki='%';
                    }
                    ilmoitus.textContent=tiedot.olosuhde+" : "+tulos+" "+merkki;
                    let div=document.getElementById('halytysdiv');
                    div.appendChild(otsikko);
                    div.appendChild(alueilmoitus);
                    div.appendChild(ilmoitus);
                    div.appendChild(aikailmoitus);

                    //Luodaan kuittauspainonappi:
                    let a=document.createElement('a');
                    //Painonappia painaessa siirrytään flaskin sivulle, jossa tallennetaan tietokantaan kuittaus
                    a.setAttribute('href', 'https://laakehuone.eu.pythonanywhere.com/kuittaus?mittaus='+tiedot.mittauksen_id+'&alue='+painonappi.id);
                    let kuittausbtn=document.createElement('button');
                    kuittausbtn.setAttribute('class', 'kuittaus');
                    kuittausbtn.textContent="KUITTAA";
                    a.appendChild(kuittausbtn);
                    div.appendChild(a);


                    //Kun hälytys aktivoitu, estetään siirtyminen muille sivuille:
                    let buttonit=document.getElementsByClassName('pohjabtn');
                    let navibuttonit=document.getElementsByClassName('navibtn');
                    let valittubutton=document.getElementsByClassName('varinvaihto');
                    for(let i=0; i<buttonit.length; i++){
                        buttonit[i].disabled=true;
                    }
                    for(let i=0; i<navibuttonit.length; i++){
                        navibuttonit[i].disabled=true;
                    }
                    for(let i=0; i<valittubutton.length; i++){
                        valittubutton[i].disabled=true;
                    }

               }
           }
        });


   //Ladataan sivu aina minuutin välein uudelleen, jotta popupit ilmestyisivät reaaliaikaisemmin käyttöliittymään:
   setTimeout(function(){
   window.location.reload();
   }, 60000);

});


