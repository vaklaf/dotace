# DOTACE

Cílem tohoto projektu je vytvoření nástroje, který by umožnil stahovat z webových portálů krajů zde publikované informace o poskytnutých dotacích.

Nástroj by měl snadno ovladatelný a konfigurovatelný.
Problém, který je třeba řešit, je skutečnost, že každý kraj přistupuje k publikace těchto informací odlišně. Některé kraje, například Plzeňský či Vysočoina zvřejňují tyto údaje v dobře sturkturované formě již na první úrovni webu, tzn. při prvním načtení webové stránky. Většina zbývajících krajů pak má na této úrovni rozcestník, různě strukturovaný odkazjící větišnou na výčty vypsaných dotačních titulů a u nich je třeba přejit na detail. Na úrovni detailu dotatčního titulu pak obvykle nalezneme seznam seznam souborů s daným titulem souvisejících. A jen některé z nich obsahují požadované informace. Je pak nutné customizovat pravidla vyhledávání potřebných soburů pro každý kraj.

Nutno dodat, že složitost úlohy zvyšuje i skutečnost, že nepanuje jednota v pojmenování souborů na úrovni samotného kraje, kde se názvosloví může lišit titul od titulu či mezi jednotlivými odbory kraje.

Dále není používán jednotý formát zobrazovaných dato. Nahcázíme soubory formátu *.csv (ojediněle), *.xls / *.xlsx, *.pdf (ty převažují), ale i *.zip - ty je třeba rozbalit a dále zkoumat obsah rozbalených archivů.
Nepanuje jednota ani mezi rozsahem zveřejňovaných dat.


## Seznam výchozích odkazů

https://www.kraj-jihocesky.cz/cs/dotace-fondy-eu'

https://dotace.kr-jihomoravsky.cz/
    
https://dotace.khk.cz/

https://www.kr-karlovarsky.cz/dotace/dotacni-programy-karlovarskeho-kraje

https://dotace.kraj-lbc.cz/

https://www.msk.cz/temata/dotace/index.html

https://www.olkraj.cz/dotace-granty-prispevky

https://dotace.pardubickykraj.cz/grants

https://dotace.plzensky-kraj.cz/verejnost

https://stredoceskykraj.cz/web/urad/dotace

https://www.kr-ustecky.cz/dotace/ms-272329

https://www.fondvysociny.cz/dotace/

https://zlinskykraj.cz/dotace-zlinskeho-kraje

## Prinicp projektu

Pro každý kraj je třeba vytvořit samostatnou třídu `cls_*_region.py`, která dědí od abstraktní třídy `cls_regions.py` mtodu `crawl()`, která spouští proces zpracování daného webu. 

Pomoci nastavení konfiguračních paramaterů v souboru `cofiguration.yml`, konkrétně, nastavením paramteru `process', lze ovlivnit, které z krajů se budou při konkrétním spuštění aplikace zpracovávat.

```yml
regions:
  plk:
    name: Plzeňský kraj
    url: https://dotace.plzensky-kraj.cz/verejnost/zadosti?_name=Zadosti&_search=false&nd=1742109491719&rows=25&page=1&sidx=&sord=asc, https://dotace.plzensky-kraj.cz/verejnost/individualni-zadosti?_name=IndividualniZadosti&_search=false&nd=1742131019737&rows=25&page=1&sidx=&sord=asc
    process: 1

```

Samotné spuštění aplikace se pak provádí z terminálu (příkazové řádky) následovně:

```powershell
>python .\main.py
````

>**UPOZORNĚNÍ**

> Je třeba mít ve soupštěcí složce vytvořené a aktivované vitruální prostředí jazyka Python. 
> Vytvoření vistuálního prostředí:

```powershell
>python -m venv venv
```
> Vytvoření vistuálního prostředí:

```powershell
>./venv/Scripts/activate.bat
```
>V takto vytovořeném a aktivovaném virtuálním prosředí je třeba mít nainstalovány potřebné rozšiřující balíčky jazyka Python. Jejich výčet je obsažen v souboru `requirements.txt'.

>Instlace rozšiřujících balíčků

```powershell
>pip install -r requirements.txt
```

## Struktura projektu

Projekt je strukturován následujcím způsobem

```
└── 📁dotace
    └── 📁logs
        └── .gitkeep
    └── 📁outputs
        └── .gitkeep
    └── 📁src
        └── __init__.py
        └── 📁apis
            └── __init__.py
            └── downloader_listener.py
            └── events.py
            └── logger_listener.py
        └── app.py
        └── 📁library
            └── cls_regions.py
            └── custom_enums.py
            └── 📁downloader
                └── __init__.py
                └── exeptions.py
                └── file_downloader.py
            └── 📁logger
                └── custom_formatters.py
                └── custom_handlers.py
                └── custom_message.py
                └── logger.py
                └── loglevel.py
            └── 📁regions
                └── __init__.py
                └── cls_abstract_region.py
                └── cls_jhk_region.py
                └── cls_plk_region.py
                └── cls_stc_region.py
                └── cls_vys_region.py
                └── cls_zlk_region.py
                └── 📁schemes
                    └── cls_plk_schemes.py
                    └── cls_vys_schemes.py
                    └── cls_zlk_schemes.py
                    └── ischema.py
            └── transformation_by_data_type.py
            └── 📁utilities
                └── __init__.py
                └── others.py
                └── strings.py
    └── 📁tests
        └── test_string_utilities.py
        └── test_utilities.py
    └── .gitignore
    └── configuration.yml
    └── main.py
    └── project_structure.MD
    └── README.MD
    └── requirements.txt
```

## ToDo

Projekt v této chvíli ještě nelze považovat za kompletní. V současné chvíli jsou zpracované kódy pro kraje:

- Plzeňský
- Vysočina
- Zlínský
- Středočeký

Kód pro Jihočeský kraj je třeba upravit tak, aby odpovídal koncetpu již zpracovaných krajů. Zbývající kraje je třeba doplnit komplentě.

Zároveň je třeba kód optimalizovat a řádně otestovat. V tuto chvíli lze hovořit o verzi 0.0.1.

### Nice To Have

Vytvoření GUI pro snazší ovládání a nastavování konfiguračních paramterů bez nutnostoti přípé editace konfigruačního souboru.