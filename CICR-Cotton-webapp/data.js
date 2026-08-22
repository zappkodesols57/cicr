const asset = (path) => `assets/${path}`;

const banners = ['bann1.JPG','bann2.JPG','bann3.JPG','bann4.JPG','bann5.JPG','bann6.JPG','bann7.JPG','bann8.JPG','bann9.JPG','bann10.JPG'].map((name) => asset(`banner/${name}`));

const varieties = [
  {
    name: "CICR 1 (CISA 310)",
    category: "North Zone",
    image: asset("variety/cisa310.jpg"),
    description: "Growing Condition: Irrigated condition of North zone Yield Potential: 27.79 q/ha Staple Length: 22.3 mm Fibre strength: 26.6 g/tex Micronair: 7.1 µg/in GOT: 36.5% Specifi...",
    details: [["Growing Condition","Irrigated condition of North zone"],["Yield Potential","27.79 q/ha"],["Staple Length","22.3 mm"],["Fibre strength","26.6 g/tex"],["Micronair","7.1 µg/in"],["GOT","36.5%"],["Specific Traits","Maturity in 145-150 days."]]
  },
  {
    name: "CICR 2 (CISA 2 GMS based)",
    category: "North Zone",
    image: asset("variety/cisa2.jpg"),
    description: "Growing Condition: Irrigated condition of North zone Yield Potential: 32.14 q/ha Staple Length: 19.2 mm Fibre strength: 16.4 g/tex Micronair: 7.06 µg/in GOT: 38.4% Specif...",
    details: [["Growing Condition","Irrigated condition of North zone"],["Yield Potential","32.14 q/ha"],["Staple Length","19.2 mm"],["Fibre strength","16.4 g/tex"],["Micronair","7.06 µg/in"],["GOT","38.4%"],["Specific Traits","Maturity in 160-170 days."]]
  },
  {
    name: "CICR 3 (CISA 614)",
    category: "North Zone",
    image: asset("variety/cisa614.jpg"),
    description: "Growing Condition: Irrigated condition of North zone Yield Potential: 22.04 q/ha Staple Length: 20.9 mm Fibre strength: 16.9 g/tex Micronair: 6.8 µg/in GOT: 35.5 % Specif...",
    details: [["Growing Condition","Irrigated condition of North zone"],["Yield Potential","22.04 q/ha"],["Staple Length","20.9 mm"],["Fibre strength","16.9 g/tex"],["Micronair","6.8 µg/in"],["GOT","35.5 %"],["Specific Traits","Maturity in 145-150 days."]]
  },
  {
    name: "CSH-3075",
    category: "North Zone",
    image: asset("variety/csh3075.jpg"),
    description: "Growing Condition: Irrigated condition of North zone Yield Potential: 24.67 q/ha Staple Length: 26.7 mm Fibre strength: 21.6 g/tex Micronair: 4.13 µg/in GOT: 35.5% Specif...",
    details: [["Growing Condition","Irrigated condition of North zone"],["Yield Potential","24.67 q/ha"],["Staple Length","26.7 mm"],["Fibre strength","21.6 g/tex"],["Micronair","4.13 µg/in"],["GOT","35.5%"],["Specific Traits","The variety showed at par incidence vis-à-vis check varieties for majority of diseases, field tolerance to jassid."]]
  },
  {
    name: "CSH-3129 variety",
    category: "North Zone",
    image: asset("variety/csh3129.jpg"),
    description: "Growing Condition: Irrigated condition of North zone Yield Potential: 22.93 q/ha Staple Length: 29.5mm Fibre strength: 23.55 g/tex Micronair: 4.7 µg/in GOT: 33.2% Specifi...",
    details: [["Growing Condition","Irrigated condition of North zone"],["Yield Potential","22.93 q/ha"],["Staple Length","29.5mm"],["Fibre strength","23.55 g/tex"],["Micronair","4.7 µg/in"],["GOT","33.2%"],["Specific Traits","Full spinning fiber quality parameters indicated that CSH-3129 was spinable at 40s counts"]]
  },
  {
    name: "CSHG 1862 (Intra-hirsutum GMS based hybrid)",
    category: "North Zone",
    image: asset("variety/csh1862.jpg"),
    description: "Growing Condition: Irrigated condition of North zone Yield Potential: 33.89 q/ha Staple Length: 27.5 mm Fibre strength: 22 g/tex Micronair: 4.0 µg/in GOT: 34.5% Specific ...",
    details: [["Growing Condition","Irrigated condition of North zone"],["Yield Potential","33.89 q/ha"],["Staple Length","27.5 mm"],["Fibre strength","22 g/tex"],["Micronair","4.0 µg/in"],["GOT","34.5%"],["Specific Traits","----"]]
  },
  {
    name: "CSHH 243",
    category: "North Zone",
    image: asset("variety/cshh243.jpg"),
    description: "Growing Condition: Irrigated condition of North zone Yield Potential: 23.11 q/ha Staple Length: 27.8mm Fibre strength: 26.9 g/tex Micronair: 4.5 µg/in GOT: 33.2% Specific...",
    details: [["Growing Condition","Irrigated condition of North zone"],["Yield Potential","23.11 q/ha"],["Staple Length","27.8mm"],["Fibre strength","26.9 g/tex"],["Micronair","4.5 µg/in"],["GOT","33.2%"],["Specific Traits","Maturity in 165-170 days."]]
  },
  {
    name: "Hybrid Kalyan (CSHH 238)",
    category: "North Zone",
    image: asset("variety/cshh238.jpg"),
    description: "Growing Condition: Irrigated condition of North zone Yield Potential: 21.34 q/ha Staple Length: 27.2 mm Fibre strength: 24.9 g/tex Micronair: 4.6 µg/in GOT: 33.7% Specifi...",
    details: [["Growing Condition","Irrigated condition of North zone"],["Yield Potential","21.34 q/ha"],["Staple Length","27.2 mm"],["Fibre strength","24.9 g/tex"],["Micronair","4.6 µg/in"],["GOT","33.7%"],["Specific Traits","Maturity in 160 days."]]
  },
  {
    name: "ICAR-CICR Bt6 (RS 2013) variety",
    category: "North Zone",
    image: asset("variety/cicrBt6.jpg"),
    description: "Growing Condition: Irrigated condition of North zone Yield Potential: 30.46 q/ha Staple Length: 25.8mm Fibre strength: 26.6 g/tex Micronair: 4.7 µg/in GOT: 36.9% Specific...",
    details: [["Growing Condition","Irrigated condition of North zone"],["Yield Potential","30.46 q/ha"],["Staple Length","25.8mm"],["Fibre strength","26.6 g/tex"],["Micronair","4.7 µg/in"],["GOT","36.9%"],["Specific Traits","Moderately resistant reaction (MR) against CLCuV"]]
  },
  {
    name: "PAU Bt 1 variety",
    category: "North Zone",
    image: asset("variety/paubt1.jpeg"),
    description: "Growing Condition: Irrigated condition of North zone Yield Potential: 27.52 q/ha Staple Length: 28.2 mm Fibre strength: 28.6 g/tex Micronair: 4.5 µg/in GOT: 41.4% Specifi...",
    details: [["Growing Condition","Irrigated condition of North zone"],["Yield Potential","27.52 q/ha"],["Staple Length","28.2 mm"],["Fibre strength","28.6 g/tex"],["Micronair","4.5 µg/in"],["GOT","41.4%"],["Specific Traits","Resistant reaction (R) against CLCuV"]]
  },
  {
    name: "PAU Bt2 (PBH Bt 5) variety",
    category: "North Zone",
    image: asset("variety/paubt2.jpeg"),
    description: "Growing Condition: Irrigated condition of North zone Yield Potential: 29.05 q/ha Staple Length: 27.6 mm Fibre strength: 28.9 g/tex Micronair: 4.8 µg/in GOT: 34.5% Specifi...",
    details: [["Growing Condition","Irrigated condition of North zone"],["Yield Potential","29.05 q/ha"],["Staple Length","27.6 mm"],["Fibre strength","28.9 g/tex"],["Micronair","4.8 µg/in"],["GOT","34.5%"],["Specific Traits","Resistant reaction (MR) against CLCuV."]]
  },
  {
    name: "PAU Bt3 (FBt 16-4) variety",
    category: "North Zone",
    image: asset("variety/paubt3.jpg"),
    description: "Growing Condition: Irrigated condition of North zone Yield Potential: 28.40 q/ha Staple Length: 26.2 mm Fibre strength: 26.6 g/tex Micronair: 4.8 µg/in GOT: 36.5% Specifi...",
    details: [["Growing Condition","Irrigated condition of North zone"],["Yield Potential","28.40 q/ha"],["Staple Length","26.2 mm"],["Fibre strength","26.6 g/tex"],["Micronair","4.8 µg/in"],["GOT","36.5%"],["Specific Traits","Moderately resistant reaction (MR) against CLCuV"]]
  },
  {
    name: "PBH Bt 21 (PAU Bt 5) variety",
    category: "North Zone",
    image: asset("variety/paubt5.jpeg"),
    description: "Growing Condition: Irrigated condition of North zone Yield Potential: 29.05 q/ha Staple Length: 26.2 mm Fibre strength: 26.4 g/tex Micronair: 4.9 µg/in GOT: get the GOT d...",
    details: [["Growing Condition","Irrigated condition of North zone"],["Yield Potential","29.05 q/ha"],["Staple Length","26.2 mm"],["Fibre strength","26.4 g/tex"],["Micronair","4.9 µg/in"],["GOT","get the GOT data from Dr. Pankaj Rathor"],["Specific Traits","Moderately resistant reaction (MR) against CLCuV"]]
  },
  {
    name: "Shresth (CSHH-198)",
    category: "North Zone",
    image: asset("variety/cshh198.jpg"),
    description: "Growing Condition: Irrigated condition of North zone Yield Potential: 21.96 q/ha Staple Length: 26.4 mm Fibre strength: 25.7 g/tex Micronair: 4.5 µg/in GOT: 32.8% Specifi...",
    details: [["Growing Condition","Irrigated condition of North zone"],["Yield Potential","21.96 q/ha"],["Staple Length","26.4 mm"],["Fibre strength","25.7 g/tex"],["Micronair","4.5 µg/in"],["GOT","32.8%"],["Specific Traits","Maturity in 162 days."]]
  },
  {
    name: "Anjali (LRK 516)",
    category: "Central Zone",
    image: asset("variety/lrk516.jpg"),
    description: "Growing Condition: Irrigated and rainfed condition of Central zone Yield Potential: 20 q/ha under normal spacing and 30 q/ha under HDPS Staple Length: 28.8 mm Fibre stren...",
    details: [["Growing Condition","Irrigated and rainfed condition of Central zone"],["Yield Potential","20 q/ha under normal spacing and 30 q/ha under HDPS"],["Staple Length","28.8 mm"],["Fibre strength","21.3 g/tex"],["Micronair","3.93 µg/in"],["GOT","38%"],["Specific Traits","It is a medium staple, short duration variety with compact growth habit and earliness capable of spinning up to 40s count yarn."]]
  },
  {
    name: "CICR-H Cotton 47 (CNH 1111)",
    category: "Central Zone",
    image: asset("variety/cicr21b.jpeg"),
    description: "Growing Condition: Rainfed condition of Central zone Yield Potential: 18.23 q/ha Staple Length: 27.3 mm Fibre strength: 28.7 g/tex Micronair: 4.5 µg/in GOT: 33.8% Specifi...",
    details: [["Growing Condition","Rainfed condition of Central zone"],["Yield Potential","18.23 q/ha"],["Staple Length","27.3 mm"],["Fibre strength","28.7 g/tex"],["Micronair","4.5 µg/in"],["GOT","33.8%"],["Specific Traits","Field tolerance to Jassid"]]
  },
  {
    name: "G. Cot 10 Bt",
    category: "Central Zone",
    image: asset("variety/jhv374.jpg"),
    description: "Growing Condition: Irrigated condition of Central zone Yield Potential: 13.94 q/ha Staple Length: 26 mm Fibre strength: 26.9 g/tex Micronair: 4.2 µg/in GOT: 36.3 % Specif...",
    details: [["Growing Condition","Irrigated condition of Central zone"],["Yield Potential","13.94 q/ha"],["Staple Length","26 mm"],["Fibre strength","26.9 g/tex"],["Micronair","4.2 µg/in"],["GOT","36.3 %"],["Specific Traits","--"]]
  },
  {
    name: "ICAR-CICR 18 Bt",
    category: "Central Zone",
    image: asset("variety/cicr18bt.jpg"),
    description: "Growing Condition: Rainfed conditions of Central Zone Yield Potential : 22.98 q/ha Staple Length: 23.4 mm Fibre strength: 24.3 g/tex Micronair: 4.9 ug/inch GOT: 35.1 % Sp...",
    details: [["Growing Condition","Rainfed conditions of Central Zone"],["Yield Potential","22.98 q/ha"],["Staple Length","23.4 mm"],["Fibre strength","24.3 g/tex"],["Micronair","4.9 ug/inch"],["GOT","35.1 %"],["Specific Traits","Resistance to bacterial blight, grey mildew, Alternaria, Corynospora leaf spot, and Myrothecium. Tolerant to jassid, aphids, thrips, and jassid"]]
  },
  {
    name: "ICAR-CICR 20-31 Bt",
    category: "Central Zone",
    image: asset("variety/cicr20-31.jpg"),
    description: "Growing Condition: Rainfed conditions of Central Zone Yield Potential : 21.02 q/ha Staple Length: 25.8 mm Fibre strength: 26.0 g/tex Micronair: 5.3 ug/inch GOT: 36.0 % Sp...",
    details: [["Growing Condition","Rainfed conditions of Central Zone"],["Yield Potential","21.02 q/ha"],["Staple Length","25.8 mm"],["Fibre strength","26.0 g/tex"],["Micronair","5.3 ug/inch"],["GOT","36.0 %"],["Specific Traits","Resistant to bacterial blight, grey mildew, Alternaria, Corynospora leaf spot, and Myrothecium. Tolerant to jassid, aphids, thrips, and jassid"]]
  },
  {
    name: "ICAR-CICR 21 Bt",
    category: "Central Zone",
    image: asset("variety/cicr21b.jpeg"),
    description: "Growing Condition: Rainfed conditions of Central Zone Yield Potential: 27.15 q/ha Staple Length: 27.2 mm Fibre strength: 27.8 g/tex Micronair: 4.3 µg/in GOT: 35% Specific...",
    details: [["Growing Condition","Rainfed conditions of Central Zone"],["Yield Potential","27.15 q/ha"],["Staple Length","27.2 mm"],["Fibre strength","27.8 g/tex"],["Micronair","4.3 µg/in"],["GOT","35%"],["Specific Traits","The variety is tolerant to sucking pest and diseases, maturity in 150 to 160 days."]]
  },
  {
    name: "ICAR-CICR Bt 14",
    category: "Central Zone",
    image: asset("variety/cicrbt14.jpg"),
    description: "Growing Condition: Rainfed conditions of Maharashtra Yield Potential: 30.66 q/ha Staple Length: 27.8 mm Fibre strength: 26.4 g/tex Micronair: 4.2 µg/in GOT: 38% Specific ...",
    details: [["Growing Condition","Rainfed conditions of Maharashtra"],["Yield Potential","30.66 q/ha"],["Staple Length","27.8 mm"],["Fibre strength","26.4 g/tex"],["Micronair","4.2 µg/in"],["GOT","38%"],["Specific Traits","Tolerant to sucking pest, maturity 160 to 170 days."]]
  },
  {
    name: "ICAR-CICR Bt 9",
    category: "Central Zone",
    image: asset("variety/cicrbt9.jpg"),
    description: "Growing Condition: Rainfed conditions of Maharashtra Yield Potential: 31.09 q/ha Staple Length: 26.3 mm Fibre strength: 25.5 g/tex Micronair: 4.4 µg/in GOT: 36.3% Specifi...",
    details: [["Growing Condition","Rainfed conditions of Maharashtra"],["Yield Potential","31.09 q/ha"],["Staple Length","26.3 mm"],["Fibre strength","25.5 g/tex"],["Micronair","4.4 µg/in"],["GOT","36.3%"],["Specific Traits","Tolerant to sucking pest and diseases, maturity 150 to 170 days"]]
  },
  {
    name: "ICAR-CICR GJHV 374 Bt",
    category: "Central Zone",
    image: asset("variety/jhv374.jpg"),
    description: "Growing Condition: Rainfed condition of Central zone Yield Potential: 25.77 q/ha Staple Length: 28.2 mm Fibre strength: 26.8 g/tex Micronair: 4.4 µg/in GOT: 34% Specific ...",
    details: [["Growing Condition","Rainfed condition of Central zone"],["Yield Potential","25.77 q/ha"],["Staple Length","28.2 mm"],["Fibre strength","26.8 g/tex"],["Micronair","4.4 µg/in"],["GOT","34%"],["Specific Traits","Resistance to major diseases"]]
  },
  {
    name: "ICAR-CICR Namami Bt",
    category: "Central Zone",
    image: asset("variety/namami.jpg"),
    description: "Growing Condition: Rainfed conditions of Central Zone Yield Potential : 20.72 q/ha Staple Length: 24.67 mm Fibre strength: 25.37 g/tex Micronair:5.77 GOT: 38.17 % Specifi...",
    details: [["Growing Condition","Rainfed conditions of Central Zone"],["Yield Potential","20.72 q/ha"],["Staple Length","24.67 mm"],["Fibre strength","25.37 g/tex"],["Micronair","5.77"],["GOT","38.17 %"],["Specific Traits","Tolerant to jassid, thrips, whitefly"]]
  },
  {
    name: "ICAR-CICR PKV 081 Bt",
    category: "Central Zone",
    image: asset("variety/pkv081.jpg"),
    description: "Growing Condition: Rainfed condition of Central zone Yield Potential: 27.43 q/ha Staple Length: 28.5 mm Fibre strength: 27.9 g/tex Micronair: 3.9 µg/in GOT: 35.1% Specifi...",
    details: [["Growing Condition","Rainfed condition of Central zone"],["Yield Potential","27.43 q/ha"],["Staple Length","28.5 mm"],["Fibre strength","27.9 g/tex"],["Micronair","3.9 µg/in"],["GOT","35.1%"],["Specific Traits","Tolerant to sucking pest."]]
  },
  {
    name: "ICAR-CICR Rajat Bt",
    category: "Central Zone",
    image: asset("variety/rajat.jpg"),
    description: "Growing Condition: Rainfed condition of Central zone Yield Potential: 26.6 q/ha Staple Length: 26.8 mm Fibre strength: 26.1 g/tex Micronair: 4.5 µg/in GOT: 34.4% Specific...",
    details: [["Growing Condition","Rainfed condition of Central zone"],["Yield Potential","26.6 q/ha"],["Staple Length","26.8 mm"],["Fibre strength","26.1 g/tex"],["Micronair","4.5 µg/in"],["GOT","34.4%"],["Specific Traits","Good performance under HDPS (90 x 15 cm)"]]
  },
  {
    name: "ICAR-CICR Suraj Bt",
    category: "Central Zone",
    image: asset("variety/surajBt.jpg"),
    description: "Growing Condition: Rainfed condition of Central zone Yield Potential: 24.07 q/ha Staple Length: 29.1 mm Fibre strength: 26 g/tex Micronair: 4.3 µg/in GOT: 36.1% Specific ...",
    details: [["Growing Condition","Rainfed condition of Central zone"],["Yield Potential","24.07 q/ha"],["Staple Length","29.1 mm"],["Fibre strength","26 g/tex"],["Micronair","4.3 µg/in"],["GOT","36.1%"],["Specific Traits","Early maturing and sucking tolerance"]]
  },
  {
    name: "ICAR-CICR Tejas Bt",
    category: "Central Zone",
    image: asset("variety/tejas.jpg"),
    description: "Growing Condition: Rainfed conditions of Central Zone Yield Potential : 20.5 q/ha Staple Length: 25.47 mm Fibre strength: 25.73 g/tex Micronair: 5.77 GOT: 36.37 % Specifi...",
    details: [["Growing Condition","Rainfed conditions of Central Zone"],["Yield Potential","20.5 q/ha"],["Staple Length","25.47 mm"],["Fibre strength","25.73 g/tex"],["Micronair","5.77"],["GOT","36.37 %"],["Specific Traits","It has demonstrated resistance to diseases such as Bacterial leaf blight, Alternaria leaf blight, Tobacco streak virus."]]
  },
  {
    name: "ICAR-CICR Yugank Bt",
    category: "Central Zone",
    image: asset("variety/yugank.jpg"),
    description: "Growing Condition: Rainfed conditions of Central Zone Yield Potential : 22.1 q/ha Staple Length: 24.8 mm Fibre strength: 25.7 g/tex Micronair:5.43 GOT: 38.1 % Specific Tr...",
    details: [["Growing Condition","Rainfed conditions of Central Zone"],["Yield Potential","22.1 q/ha"],["Staple Length","24.8 mm"],["Fibre strength","25.7 g/tex"],["Micronair","5.43"],["GOT","38.1 %"],["Specific Traits","Tolerant to sucking pest and diseases, maturity in 150 to 160 days."]]
  },
  {
    name: "LRA 5166",
    category: "Central Zone",
    image: asset("variety/lra5166.jpg"),
    description: "Growing Condition: Irrigated and rainfed condition of Central zone Yield Potential: 25-30 q/ha under irrigated and 10-15 q/ha under rainfed conditions Staple Length: 26.6...",
    details: [["Growing Condition","Irrigated and rainfed condition of Central zone"],["Yield Potential","25-30 q/ha under irrigated and 10-15 q/ha under rainfed conditions"],["Staple Length","26.6 mm"],["Fibre strength","22.33 g/tex"],["Micronair","4.0 µg/in"],["GOT","40.12%"],["Specific Traits","Lint suited for producing hosiery yarn."]]
  },
  {
    name: "Nano (CICR-H Cotton 54)",
    category: "Central Zone",
    image: asset("variety/cotton54.jpg"),
    description: "Growing Condition: Rainfed condition of Central zone Yield Potential: 29.63 q/ha Staple Length: 30.1 mm Fibre strength: 30.2 g/tex Micronair: 3.7 µg/in GOT: 34.4% Specifi...",
    details: [["Growing Condition","Rainfed condition of Central zone"],["Yield Potential","29.63 q/ha"],["Staple Length","30.1 mm"],["Fibre strength","30.2 g/tex"],["Micronair","3.7 µg/in"],["GOT","34.4%"],["Specific Traits","High boll weight 4.0 gm."]]
  },
  {
    name: "NH 1901 Bt",
    category: "Central Zone",
    image: asset("variety/nh1901bt.JPG"),
    description: "Growing Condition: Rainfed condition of Central zone Yield Potential: 14.74 q/ha Staple Length: 25.2 mm Fibre strength: 25.5 g/tex Micronair: 4.2 µg/in GOT: 35.3% Specifi...",
    details: [["Growing Condition","Rainfed condition of Central zone"],["Yield Potential","14.74 q/ha"],["Staple Length","25.2 mm"],["Fibre strength","25.5 g/tex"],["Micronair","4.2 µg/in"],["GOT","35.3%"],["Specific Traits","--"]]
  },
  {
    name: "NH 1902 Bt",
    category: "Central Zone",
    image: asset("variety/nh1902bt.JPG"),
    description: "Growing Condition: Rainfed condition of Central zone Yield Potential: 15.09 q/ha Staple Length: 24.9 mm Fibre strength: 25.2 g/tex Micronair: 4.6 µg/in GOT: 36.4% Specifi...",
    details: [["Growing Condition","Rainfed condition of Central zone"],["Yield Potential","15.09 q/ha"],["Staple Length","24.9 mm"],["Fibre strength","25.2 g/tex"],["Micronair","4.6 µg/in"],["GOT","36.4%"],["Specific Traits","---"]]
  },
  {
    name: "NH 1904 Bt",
    category: "Central Zone",
    image: asset("variety/nh1904bt.JPG"),
    description: "Growing Condition: Rainfed condition of Central zone Yield Potential: 13.84 q/ha Staple Length: 25.8 mm Fibre strength: 25.9 g/tex Micronair: 4.6 µg/in GOT: 36.2% Specifi...",
    details: [["Growing Condition","Rainfed condition of Central zone"],["Yield Potential","13.84 q/ha"],["Staple Length","25.8 mm"],["Fibre strength","25.9 g/tex"],["Micronair","4.6 µg/in"],["GOT","36.2%"],["Specific Traits","-"]]
  },
  {
    name: "NHH 44 BG II Bt",
    category: "Central Zone",
    image: asset("variety/nhh44bgii.jpg"),
    description: "Growing Condition: Rainfed condition of Central zone Yield Potential: 25 q/ha Staple Length: 27.3 mm Fibre strength: 25.9 g/tex Micronair: 4.75 ug/inch GOT: 34% Specific ...",
    details: [["Growing Condition","Rainfed condition of Central zone"],["Yield Potential","25 q/ha"],["Staple Length","27.3 mm"],["Fibre strength","25.9 g/tex"],["Micronair","4.75 ug/inch"],["GOT","34%"],["Specific Traits","High yield with stable performance across locations, drought tolerant"]]
  },
  {
    name: "PKV Hy 2 BG II Bt",
    category: "Central Zone",
    image: asset("variety/pkvhy.jpg"),
    description: "This intra-hirsutum hybrid is suitable for Marathwada region of Maharashtra under rainfed condition and is resistant to boll worm. It possess boll weight of 4.0-4.5g, GOT...",
    details: [["Information","This intra-hirsutum hybrid is suitable for Marathwada region of Maharashtra under rainfed condition and is resistant to boll worm. It possess boll weight of 4.0-4.5g, GOT of 36 per cent, fibre length of 27 mm and matures in 170-180 days. It has yield potential of 12-15 q/ha under rainfed and 15-20q/ha under irrigated condition."]]
  },
  {
    name: "Suchitra (CCH 12-2)",
    category: "Central Zone",
    image: asset("variety/cch12.jpg"),
    description: "Growing Condition: Rainfed condition of Central zone Yield Potential: 26 q/ha Staple Length: 28.5 mm Fibre strength: 22.7 g/tex Micronair: 4.2 µg/in GOT: 33.6% Specific T...",
    details: [["Growing Condition","Rainfed condition of Central zone"],["Yield Potential","26 q/ha"],["Staple Length","28.5 mm"],["Fibre strength","22.7 g/tex"],["Micronair","4.2 µg/in"],["GOT","33.6%"],["Specific Traits","Showed field tolerance to jassid and grey mildew."]]
  },
  {
    name: "Suraj",
    category: "Central Zone",
    image: asset("variety/suraj.jpg"),
    description: "Growing Condition: Rainfed condition of Central zone Yield Potential: 25q/ha Staple Length: 30.3 mm Fibre strength: 23.8 g/tex Micronair: 3.6 µg/in GOT: 40.1% Specific Tr...",
    details: [["Growing Condition","Rainfed condition of Central zone"],["Yield Potential","25q/ha"],["Staple Length","30.3 mm"],["Fibre strength","23.8 g/tex"],["Micronair","3.6 µg/in"],["GOT","40.1%"],["Specific Traits","Most adaptable, sucking pest tolerant variety combining good yield and desirable fibre quality"]]
  },
  {
    name: "Suraksha (CICR-H Cotton 36)",
    category: "Central Zone",
    image: asset("variety/suraksha.jpg"),
    description: "Growing Condition: Rainfed condition of Central zone Yield Potential: 22.35 q/ha Staple Length: 32.4 mm Fibre strength: 34.3 g/tex Micronair: 3.7 µg/in GOT: 34.1 % Specif...",
    details: [["Growing Condition","Rainfed condition of Central zone"],["Yield Potential","22.35 q/ha"],["Staple Length","32.4 mm"],["Fibre strength","34.3 g/tex"],["Micronair","3.7 µg/in"],["GOT","34.1 %"],["Specific Traits","Jassid resistant"]]
  },
  {
    name: "Anjali (LRK 516)",
    category: "South Zone",
    image: asset("variety/lrk516.jpg"),
    description: "Growing Condition: Rainfed condition of south zone Yield Potential: 20 q/ha under normal spacing and 30 q/ha under HDPS Staple Length: 28.8 mm Fibre strength: 21.3 g/tex ...",
    details: [["Growing Condition","Rainfed condition of south zone"],["Yield Potential","20 q/ha under normal spacing and 30 q/ha under HDPS"],["Staple Length","28.8 mm"],["Fibre strength","21.3 g/tex"],["Micronair","3.93 µg/in"],["GOT","38%"],["Specific Traits","Tolerant to jassid and escapes from severe bollworm infestation"]]
  },
  {
    name: "CCH 2623",
    category: "South Zone",
    image: asset("variety/cch2623.jpg"),
    description: "Growing Condition: Irrigated condition of South zone Yield Potential: Staple Length: 25.4 mm Fibre strength: 21.1 g/tex Micronair: 3.4 µg/in GOT: 36.9% Specific Traits: T...",
    details: [["Growing Condition","Irrigated condition of South zone"],["Yield Potential","-"],["Staple Length","25.4 mm"],["Fibre strength","21.1 g/tex"],["Micronair","3.4 µg/in"],["GOT","36.9%"],["Specific Traits","Tolerance to jassid and majority diseases"]]
  },
  {
    name: "CICR B Cotton 37 (CCB 51)",
    category: "South Zone",
    image: asset("variety/ccb51.jpeg"),
    description: "Growing Condition: Irrigated condition of South zone Yield Potential: 12.37 q/ha Staple Length: 34.7 mm Fibre strength: 36.6 g/tex Micronair: 3.4 µg/in GOT: 32.5% Specifi...",
    details: [["Growing Condition","Irrigated condition of South zone"],["Yield Potential","12.37 q/ha"],["Staple Length","34.7 mm"],["Fibre strength","36.6 g/tex"],["Micronair","3.4 µg/in"],["GOT","32.5%"],["Specific Traits","Extra-long fibre"]]
  },
  {
    name: "CICR-A Cotton 57 (CNA 1091)",
    category: "South Zone",
    image: asset("variety/cna1091.jpg"),
    description: "Growing Condition: Yield Potential: 12.43 q/ha Staple Length: 24.5 mm Fibre strength: 23.3 g/tex Micronair: 5.2 µg/in GOT: 32.9 % Specific Traits: High yielding desi colo...",
    details: [["Growing Condition","-"],["Yield Potential","12.43 q/ha"],["Staple Length","24.5 mm"],["Fibre strength","23.3 g/tex"],["Micronair","5.2 µg/in"],["GOT","32.9 %"],["Specific Traits","High yielding desi colour cotton variety with acceptable fibre quality"]]
  },
  {
    name: "CICR-B Cotton 45 (CCB 143B)",
    category: "South Zone",
    image: asset("variety/ccb143b.jpg"),
    description: "Growing Condition: Irrigated condition of South zone Yield Potential: 14.62 q/ha Staple Length: 37 mm Fibre strength: 40.8 g/tex Micronair: 3.7 µg/in GOT: 32.1% Specific ...",
    details: [["Growing Condition","Irrigated condition of South zone"],["Yield Potential","14.62 q/ha"],["Staple Length","37 mm"],["Fibre strength","40.8 g/tex"],["Micronair","3.7 µg/in"],["GOT","32.1%"],["Specific Traits","Extra-long fibre"]]
  },
  {
    name: "CICR-B Cotton 55 (CCB 51-2)",
    category: "South Zone",
    image: asset("variety/ccb51-2.jpeg"),
    description: "Growing Condition: Irrigated condition of South zone Yield Potential: 13.17 q/ha Staple Length: 37.1 mm Fibre strength: 38 g/tex Micronair: 3.7 µg/in GOT: Specific Traits...",
    details: [["Growing Condition","Irrigated condition of South zone"],["Yield Potential","13.17 q/ha"],["Staple Length","37.1 mm"],["Fibre strength","38 g/tex"],["Micronair","3.7 µg/in"],["GOT","-"],["Specific Traits","-"]]
  },
  {
    name: "CICR-H Cotton 36 (Suraksha)",
    category: "South Zone",
    image: asset("variety/suraksha.jpg"),
    description: "Growing Condition: Irrigated condition of South zone Yield Potential: 40.19 q/ha in normal spacing Staple Length: 32.4 mm Fibre strength: 34.3 g/tex Micronair: 3.7 µg/in ...",
    details: [["Growing Condition","Irrigated condition of South zone"],["Yield Potential","40.19 q/ha in normal spacing"],["Staple Length","32.4 mm"],["Fibre strength","34.3 g/tex"],["Micronair","3.7 µg/in"],["GOT","34%"],["Specific Traits","Jassid resistant"]]
  },
  {
    name: "CICR-H Cotton 48 (CNH 1128)",
    category: "South Zone",
    image: asset("variety/cnh1128.jpg"),
    description: "Growing Condition: Yield Potential: 13.99 q/ha Staple Length: 28.6 mm Fibre strength: 27.5 g/tex Micronair: 4.4 µg/in GOT: 34.5 % Specific Traits: Showed field tolerance ...",
    details: [["Growing Condition","-"],["Yield Potential","13.99 q/ha"],["Staple Length","28.6 mm"],["Fibre strength","27.5 g/tex"],["Micronair","4.4 µg/in"],["GOT","34.5 %"],["Specific Traits","Showed field tolerance to sucking pests"]]
  },
  {
    name: "CICR-H Cotton 54 (Nano)",
    category: "South Zone",
    image: asset("variety/cotton54.jpg"),
    description: "Growing Condition: Yield Potential: 29.63 q/ha in closer spacing Staple Length: 30.8 mm Fibre strength: 30.8 g/tex Micronair: 4.1 µg/in GOT: 34.9 % Specific Traits: Boll ...",
    details: [["Growing Condition","-"],["Yield Potential","29.63 q/ha in closer spacing"],["Staple Length","30.8 mm"],["Fibre strength","30.8 g/tex"],["Micronair","4.1 µg/in"],["GOT","34.9 %"],["Specific Traits","Boll weight of 4.7 g"]]
  },
  {
    name: "CICR-H Cotton 58 (CNH 17395)",
    category: "South Zone",
    image: asset("variety/cnh17395.jpg"),
    description: "Growing Condition: Yield Potential: 20.01 q/ha Staple Length: 23.7 mm Fibre strength: 24.4 g/tex Micronair: 4.4 µg/in GOT: 34.5 % Specific Traits: Field tolerance to suck...",
    details: [["Growing Condition","-"],["Yield Potential","20.01 q/ha"],["Staple Length","23.7 mm"],["Fibre strength","24.4 g/tex"],["Micronair","4.4 µg/in"],["GOT","34.5 %"],["Specific Traits","Field tolerance to sucking pests"]]
  },
  {
    name: "CNA 1003",
    category: "South Zone",
    image: asset("variety/cna1003.jpg"),
    description: "Growing Condition: rainfed situation of south zone states Yield Potential: 13.97 q/ha Staple Length: 24.4 mm Fibre strength: 21.2 g/tex Micronair: 5.2 µg/in GOT: 35.7 % S...",
    details: [["Growing Condition","rainfed situation of south zone states"],["Yield Potential","13.97 q/ha"],["Staple Length","24.4 mm"],["Fibre strength","21.2 g/tex"],["Micronair","5.2 µg/in"],["GOT","35.7 %"],["Specific Traits","High yielding desi cotton variety with improved fibre quality"]]
  },
  {
    name: "ICAR-CICR 23 Bt",
    category: "South Zone",
    image: asset("variety/cicr23bt.jpg"),
    description: "Growing Condition: Rainfed conditions of South Zone Yield Potential : 26.49 q/ha Staple Length: 27.6 mm Fibre strength: 26.8 g/tex Micronair:3.7 ug/in GOT: 34% Specific T...",
    details: [["Growing Condition","Rainfed conditions of South Zone"],["Yield Potential","26.49 q/ha"],["Staple Length","27.6 mm"],["Fibre strength","26.8 g/tex"],["Micronair","3.7 ug/in"],["GOT","34%"],["Specific Traits","Tolerant to sucking pests, maturity in 150 to 160 days."]]
  },
  {
    name: "ICAR-CICR 25 Bt",
    category: "South Zone",
    image: asset("variety/cicr25bt.jpg"),
    description: "Growing Condition: Rainfed conditions of South Zone Yield Potential : 23.25 q/ha Staple Length: 27.00 mm Fibre strength: 26.4 g/tex Micronair: 4.3 ug/in GOT: 36% Specific...",
    details: [["Growing Condition","Rainfed conditions of South Zone"],["Yield Potential","23.25 q/ha"],["Staple Length","27.00 mm"],["Fibre strength","26.4 g/tex"],["Micronair","4.3 ug/in"],["GOT","36%"],["Specific Traits","tolerant to sucking pests"]]
  },
  {
    name: "ICAR-CICR Samrat Bt",
    category: "South Zone",
    image: asset("variety/samratbt.jpg"),
    description: "Growing Condition: Rainfed conditions of South Zone Yield Potential : 24.14 q/ha Staple Length: 25.17 mm Fibre strength: 25.1 g/tex Micronair: 4.83 GOT: 36.77% Specific T...",
    details: [["Growing Condition","Rainfed conditions of South Zone"],["Yield Potential","24.14 q/ha"],["Staple Length","25.17 mm"],["Fibre strength","25.1 g/tex"],["Micronair","4.83"],["GOT","36.77%"],["Specific Traits","Tolerant to jassid, thrips, whitefly, and aphids."]]
  },
  {
    name: "LRA 5166",
    category: "South Zone",
    image: asset("variety/lra5166.jpg"),
    description: "Growing Condition: Irrigated and rainfed condition of South zone Yield Potential: 25-30 q/ha under irrigated and 10-15 q/ha under rainfed conditions Staple Length: 26.6 m...",
    details: [["Growing Condition","Irrigated and rainfed condition of South zone"],["Yield Potential","25-30 q/ha under irrigated and 10-15 q/ha under rainfed conditions"],["Staple Length","26.6 mm"],["Fibre strength","22.33 g/tex"],["Micronair","4 µg/in"],["GOT","40.12%"],["Specific Traits","-"]]
  },
  {
    name: "MCU 5 VT",
    category: "South Zone",
    image: asset("variety/mcu5.jpg"),
    description: "Growing Condition: Irrigated and rainfed condition of South zone Yield Potential: 25 q/ha Staple Length: 32.16 mm Fibre strength: 24 g/tex Micronair: 3.5 µg/in GOT: 35.43...",
    details: [["Growing Condition","Irrigated and rainfed condition of South zone"],["Yield Potential","25 q/ha"],["Staple Length","32.16 mm"],["Fibre strength","24 g/tex"],["Micronair","3.5 µg/in"],["GOT","35.43%"],["Specific Traits","Capable of spinning up to 60s count yarn"]]
  },
  {
    name: "Savita",
    category: "South Zone",
    image: asset("variety/savita.jpg"),
    description: "Growing Condition: irrigated condition of South zone Yield Potential: 25-30 q/ha Staple Length: 31.26 mm Fibre strength: 23.76 g/tex Micronair: 4.13 µg/in GOT: 35.57 % Sp...",
    details: [["Growing Condition","irrigated condition of South zone"],["Yield Potential","25-30 q/ha"],["Staple Length","31.26 mm"],["Fibre strength","23.76 g/tex"],["Micronair","4.13 µg/in"],["GOT","35.57 %"],["Specific Traits","Tolerance to Verticillium wilt"]]
  },
  {
    name: "Sruthi",
    category: "South Zone",
    image: asset("variety/sruthi.jpg"),
    description: "Growing Condition: Irrigated condition of Tamil Nadu Yield Potential: 15 q/ha Staple Length: 35.93 mm Fibre strength: 31 g/tex Micronair: 2.93 µg/in GOT: 30.09% Specific ...",
    details: [["Growing Condition","Irrigated condition of Tamil Nadu"],["Yield Potential","15 q/ha"],["Staple Length","35.93 mm"],["Fibre strength","31 g/tex"],["Micronair","2.93 µg/in"],["GOT","30.09%"],["Specific Traits","Dwarf and compact inter-specific hybrid"]]
  },
  {
    name: "Subiksha (CCH 4474)",
    category: "South Zone",
    image: asset("variety/cch4474.jpg"),
    description: "Growing Condition: Irrigated condition of south zone Yield Potential: 42.0 q/ha in closer spacing Staple Length: 32.7 mm Fibre strength: 33.8 g/tex Micronair: 3.7 µg/in G...",
    details: [["Growing Condition","Irrigated condition of south zone"],["Yield Potential","42.0 q/ha in closer spacing"],["Staple Length","32.7 mm"],["Fibre strength","33.8 g/tex"],["Micronair","3.7 µg/in"],["GOT","35.4%"],["Specific Traits","Field tolerance to jassid and majority of diseases"]]
  },
  {
    name: "Sumangala",
    category: "South Zone",
    image: asset("variety/sumangala.jpg"),
    description: "Growing Condition: Irrigated condition of South zone Yield Potential: 25-30 q/ha Staple Length: 26.5 mm Fibre strength: 21.2 g/tex Micronair: 4.56 µg/in GOT: 37.19 % Spec...",
    details: [["Growing Condition","Irrigated condition of South zone"],["Yield Potential","25-30 q/ha"],["Staple Length","26.5 mm"],["Fibre strength","21.2 g/tex"],["Micronair","4.56 µg/in"],["GOT","37.19 %"],["Specific Traits","Capable of spinning up to 40s count yarn. Robust plant-type yields on par with hybrids in wider spacing"]]
  },
  {
    name: "Supriya",
    category: "South Zone",
    image: asset("variety/supriya.jpg"),
    description: "Growing Condition: Irrigated condition of Tamil Nadu Yield Potential: 20 q/ha Staple Length: 28 mm Fibre strength: 21.6 g/tex Micronair: 4.36 µg/in GOT: 38.5% Specific Tr...",
    details: [["Growing Condition","Irrigated condition of Tamil Nadu"],["Yield Potential","20 q/ha"],["Staple Length","28 mm"],["Fibre strength","21.6 g/tex"],["Micronair","4.36 µg/in"],["GOT","38.5%"],["Specific Traits","Tolerant to bacterial blight and moderately tolerant to jassid"]]
  },
  {
    name: "Surabhi",
    category: "South Zone",
    image: asset("variety/surabhi.jpg"),
    description: "Growing Condition: Rainfed condition of South Zone Yield Potential: 16 q/ha Staple Length: 31.6 mm Fibre strength: 24.4 g/tex Micronair: 3.2 µg/in GOT: 35.09% Specific Tr...",
    details: [["Growing Condition","Rainfed condition of South Zone"],["Yield Potential","16 q/ha"],["Staple Length","31.6 mm"],["Fibre strength","24.4 g/tex"],["Micronair","3.2 µg/in"],["GOT","35.09%"],["Specific Traits","Verticillium wilt resistant"]]
  },
  {
    name: "Suraj",
    category: "South Zone",
    image: asset("variety/suraj.jpg"),
    description: "Growing Condition: Irrigated condition of South Zone Yield Potential: 25 q/ha Staple Length: 30.3 mm Fibre strength: 23.8 g/tex Micronair: 3.6 µg/in GOT: 40.1% Specific T...",
    details: [["Growing Condition","Irrigated condition of South Zone"],["Yield Potential","25 q/ha"],["Staple Length","30.3 mm"],["Fibre strength","23.8 g/tex"],["Micronair","3.6 µg/in"],["GOT","40.1%"],["Specific Traits","Most adaptable, sucking pest tolerant, combining good yield and desirable fibre quality"]]
  },
  {
    name: "Surya",
    category: "South Zone",
    image: asset("variety/surya.jpg"),
    description: "Growing Condition: Irrigated condition of South zone Yield Potential: 20 q/ha Staple Length: 32 mm Fibre strength: 25.46 g/tex Micronair: 4.3 µg/in GOT: 36.63 % Specific ...",
    details: [["Growing Condition","Irrigated condition of South zone"],["Yield Potential","20 q/ha"],["Staple Length","32 mm"],["Fibre strength","25.46 g/tex"],["Micronair","4.3 µg/in"],["GOT","36.63 %"],["Specific Traits","Boll weight of 5.2 g"]]
  },
  {
    name: "Suvin",
    category: "South Zone",
    image: asset("variety/suvin.jpg"),
    description: "Growing Condition: Irrigated condition of Tamil Nadu & Andhra Pradesh Yield Potential: 15-20 q/ha Staple Length: 40 mm Fibre strength: 38 g/tex Micronair: 3.2 GOT: 30.07%...",
    details: [["Growing Condition","Irrigated condition of Tamil Nadu & Andhra Pradesh"],["Yield Potential","15-20 q/ha"],["Staple Length","40 mm"],["Fibre strength","38 g/tex"],["Micronair","3.2"],["GOT","30.07%"],["Specific Traits","Extra-long fibre"]]
  },
  {
    name: "Vaidehi-1 (ICAR-CICR 16301 DB)",
    category: "South Zone",
    image: asset("variety/vaidehi1.jpg"),
    description: "Growing Condition: Yield Potential: 14.95 q/ha Staple Length: 23.5 mm Fibre strength: 23.6 g/tex Micronair: 4.1 µg/in GOT: 35% Specific Traits: High yielding naturally co...",
    details: [["Growing Condition","-"],["Yield Potential","14.95 q/ha"],["Staple Length","23.5 mm"],["Fibre strength","23.6 g/tex"],["Micronair","4.1 µg/in"],["GOT","35%"],["Specific Traits","High yielding naturally coloured cotton variety"]]
  }
];

const pests = [
  ['Whitefly','whitefly-g.JPG','Sucking pest that reduces plant vigour and transmits cotton leaf curl disease.'],
  ['Jassid','jassid-g.JPG','Sucks sap from leaves and causes yellowing, curling and hopper burn.'],
  ['Thrips','thrips-g.JPG','Feeds on young leaves and flowers, causing silvery streaks and reduced growth.'],
  ['Aphid','aphid-g.JPG','Colonies on shoots and leaves can cause sooty mould and plant weakness.'],
  ['Mealybug','mealybug-g.JPG','Sucks sap and weakens plants, affecting growth and yield.'],
  ['Pink Bollworm','pinkboll-g.JPG','Bores into squares, flowers and bolls, causing major yield loss.'],
  ['American Bollworm','american.png','Damages squares, flowers and bolls.'],
  ['Red Cotton Bug','red.png','Feeds on cotton seeds and stains lint.'],
  ['Mirid Bug','mirid.png','Can damage squares and tender plant parts.'],
  ['Tobacco Caterpillar','tobaco.png','Defoliating pest damaging foliage.'],
  ['Spotted Bollworm','spotted.png','Bollworm pest attacking fruiting bodies.'],
  ['Semilooper','semilooper.png','Leaf eating caterpillar pest.'],
  ['Dusky Cotton Bug','dusky.png','Seed feeding pest seen near mature bolls.'],
  ['Grey Weevil','grey.png','Leaf feeding pest in cotton fields.']
].map(([name, file, description]) => ({ name, image: asset(`pest/${file}`), description, category: 'Pest Management' }));

const diseases = [
  ['Alternaria Leaf Spot','alternaria.jpg'], ['Anthracnose','anthracnose.jpg'], ['Bacterial Leaf Blight','blb.JPG'],
  ['Boll Rot','bollrot.JPG'], ['Cercospora Leaf Spot','cecospora.JPG'], ['Charcoal Rot','charcolrot.jpg'],
  ['Cotton Leaf Curl Virus','clcuv.JPG'], ['Corynespora Leaf Spot','corynespora.JPG'], ['Fusarium Wilt','fusarium.JPG'],
  ['Grey Mildew','grey.JPG'], ['Myrothecium Leaf Spot','myrothecium.JPG'], ['Reniform Nematode','reniform.JPG'],
  ['Root Knot Nematode','rootknot1.JPG'], ['Root Rot','rootrot.JPG'], ['Rust','rust.jpg'], ['Tobacco Streak Virus','tsv.JPG'], ['Verticillium Wilt','verticillium.jpg']
].map(([name, file]) => ({ name, image: asset(`disease/${file}`), description: 'Disease management information sourced from mobile app image/data assets.', category: 'Disease Management' }));

const production = [
  ['Cropping System','n-cropping-1.jpg'], ['High Density Planting System','n-hdps-1.JPG'], ['Irrigation Management','irrigationmana.jpg'],
  ['Nutrient Management','n-nutrient.jpg'], ['Soil Tillage','n-soilt-1.jpg'], ['Sowing Time','n-sowingt-1.jpg'], ['Weed Management','n-weed-1.JPG'],
  ['Physical Disorder','prod7.jpg']
].map(([name, file]) => ({ name, image: file === 'prod7.jpg' ? asset(`images/${file}`) : asset(`production/${file}`), description: 'Cotton production technology module from CICR Cotton mobile app.', category: 'Production Technology' }));

const facts = ['img1.jpg','img2.jpg','img3.jpg','img4.jpg','img5.jpg','apyCotton.jpg','exportsImport.jpg'].map((file, index) => ({
  name: ['Cotton Area','Cotton Production','Cotton Productivity','State-wise Cotton','Global Cotton','Area Production Yield','Export Import'][index],
  image: asset(`facts/${file}`),
  description: 'Facts and figures chart available in the mobile app.'
}));

const advisories = [
  'XI_Weekly_Cotton_Cultivation_Advisory_20_26_Aug_2024.pdf',
  'XII_Weekly_Cotton_Cultivation_Advisory_CICR_27_Aug_to_2_Sep_2024.pdf',
  'XIII_Weekly_Cotton_Cultivation_Advisory 3-9_Sept_24 _CICR_Nagpur.pdf',
  'XIV_Weekly_Advisory_for_Cotton_Cultivation_10_16_Sept_24_ICAR.pdf',
  'Gujarati_11th Cotton Advisory 20-26 Aug 2024.pdf',
  'Gujarati_12th_Cotton_Advisory_27_Aug _2_Sept_2024.pdf',
  'Gujarati_13th_Cotton_Advisory_3_to_9_Sept_2024.pdf',
  'Gujarati_14th_Cotton_Advisory_10to16_Sept_2024.pdf'
].map((file) => ({ name: file.replace(/_/g, ' ').replace('.pdf', ''), file: asset(`advisory/${file}`), description: 'Weekly cotton cultivation advisory PDF.' }));

const gallery = [
  ...['48th-Foundationday-2.jpg','4th_interface_meeting.jpg','Annual-gm-1.jpg','Annual-gm-2.jpg','CITI-CDRA -Workshop.jpg','Foundation_Day_1.JPG','Foundation_Day_2.JPG','Foundation_Day_3.JPG','Foundation_Day_4.JPG','Foundation_Day_5.JPG','Foundation_Day_6.JPG','International-women-day.jpg','Kapas_Mela.JPG','Kapas_Mela_2.JPG','Kapas_Mela_3.JPG'].map((f) => asset(`gallery/${f}`)),
  ...['49th_Fountation_day_2025.jpg','Award_of_Technology_certificate.jpg','BCI_Training.jpg','Celebration_of World-IP_Day.jpeg','CICR_Stall_at_Nagpur.jpeg','Directors_Welcome.jpg','gall-img-1.jpg','gall-img-2.jpg','gall-img-3.jpg','Input_distribution_TSP.jpg','Release_of_AI_Pheromone_trap.jpg','Training_by_KVK.jpg','Workshop_on_Cotton_Technology.jpg'].map((f) => asset(`gallery-25/${f}`)),
  ...['pb-1.jpg','pb-2.jpg','pb-3.jpg','pb-4.jpg','pb-5.jpg','pb-6.jpeg','pb-7.jpeg','pb-8.jpg','pb-9.jpg','pb-10.jpg'].map((f) => asset(`gallery-25/pink-ballworm/${f}`))
];

const galleryAlbums = [
  {
    name: 'Foundation Day',
    description: 'Foundation day photographs from CICR Cotton mobile app assets.',
    images: ['48th-Foundationday-2.jpg','Foundation_Day_1.JPG','Foundation_Day_2.JPG','Foundation_Day_3.JPG','Foundation_Day_4.JPG','Foundation_Day_5.JPG','Foundation_Day_6.JPG'].map((f) => asset(`gallery/${f}`)),
  },
  {
    name: 'Annual Group Meeting',
    description: 'Annual group meeting photographs from CICR Cotton mobile app assets.',
    images: ['Annual-gm-1.jpg','Annual-gm-2.jpg'].map((f) => asset(`gallery/${f}`)),
  },
  {
    name: 'Kapas Mela',
    description: 'Kapas Mela photographs from CICR Cotton mobile app assets.',
    images: ['Kapas_Mela.JPG','Kapas_Mela_2.JPG','Kapas_Mela_3.JPG'].map((f) => asset(`gallery/${f}`)),
  },
  {
    name: 'Pink Bollworm Management',
    description: 'Pink bollworm management photographs from CICR Cotton mobile app assets.',
    images: ['pb-1.jpg','pb-2.jpg','pb-3.jpg','pb-4.jpg','pb-5.jpg','pb-6.jpeg','pb-7.jpeg','pb-8.jpg','pb-9.jpg','pb-10.jpg'].map((f) => asset(`gallery-25/pink-ballworm/${f}`)),
  },
  {
    name: 'DAPSC',
    description: 'DAPSC programme photographs from CICR Cotton mobile app assets.',
    images: ['dapsc-1.jpg','dapsc-2.jpg','dapsc-3.jpg','dapsc-4.jpg','dapsc-5.jpg','dapsc-6.jpg','dapsc-7.jpg','dapsc-8.jpg','dapsc-9.jpg'].map((f) => asset(`gallery-25/DAPSC/${f}`)),
  },
  {
    name: 'April 2026 Field Event',
    description: 'April 2026 field event photographs from CICR Cotton mobile app assets.',
    images: ['april1-1.JPG','april1-2.JPG','april1-3.JPG','april1-4.JPG','april1-5.JPG','april1-6.JPG','april1-7.JPG','april1-8.JPG'].map((f) => asset(`gallery-26/april-1/${f}`)),
  },
  {
    name: 'April 2026 Research Event',
    description: 'April 2026 research event photographs from CICR Cotton mobile app assets.',
    images: ['april2-1.JPG','april2-3.JPG','april2-4.JPG','april2-5.JPG','april2-6.JPG','april2-7.JPG','april2-8.JPG','april2-9.JPG'].map((f) => asset(`gallery-26/april-2/${f}`)),
  },
  ...[
    ['Interface Meeting', asset('gallery/4th_interface_meeting.jpg')],
    ['CITI-CDRA Workshop', asset('gallery/CITI-CDRA -Workshop.jpg')],
    ["International Women's Day", asset('gallery/International-women-day.jpg')],
    ['49th Foundation Day 2025', asset('gallery-25/49th_Fountation_day_2025.jpg')],
    ['Award of Technology Certificate', asset('gallery-25/Award_of_Technology_certificate.jpg')],
    ['BCI Training', asset('gallery-25/BCI_Training.jpg')],
    ['Celebration of World IP Day', asset('gallery-25/Celebration_of World-IP_Day.jpeg')],
    ['CICR Stall at Nagpur', asset('gallery-25/CICR_Stall_at_Nagpur.jpeg')],
    ["Director's Welcome", asset('gallery-25/Directors_Welcome.jpg')],
    ['Germplasm Field Day', asset('gallery-25/gall-img-1.jpg')],
    ['New Year 2026', asset('gallery-25/gall-img-2.jpg')],
    ['Field Visit', asset('gallery-25/gall-img-3.jpg')],
    ['Input Distribution TSP', asset('gallery-25/Input_distribution_TSP.jpg')],
    ['Release of AI Pheromone Trap', asset('gallery-25/Release_of_AI_Pheromone_trap.jpg')],
    ['Training by KVK', asset('gallery-25/Training_by_KVK.jpg')],
    ['Workshop on Cotton Technology', asset('gallery-25/Workshop_on_Cotton_Technology.jpg')],
  ].map(([name, image]) => ({
    name,
    description: 'CICR Cotton gallery image from mobile app assets.',
    images: [image],
  })),
].map((album) => ({ ...album, type: 'galleryAlbum', image: album.images[0] }));

const cultivars = [
  // North Zone
  ['FHH 209', 'North Zone', null, 'The intraspecific (hirsutum x hirsutum) hybrid, FHH 209 was released for irrigated conditions of Punjab, Haryana and Rajasthan. It has yield potential of 26.02 q/ha and possesses 34.5% Ginning Out Turn (GOT), 26.6 mm fibre length and 20.9 g/tex fibre strength.'],
  ['F 2228', 'North Zone', null, 'The G. hirsutum variety, F 2228 was released for irrigated conditions of Punjab, Haryana and Rajasthan. It has yield potential of 25.39 q/ha and possesses 34.4% Ginning Out Turn (GOT), 29 mm fibre length and 22.6 g/tex fibre strength. It is resistant to bacterial blight, moderately resistant to fungal foliar diseases, showed field tolerance to major insect pests.'],
  ['LH 2256', 'North Zone', null, 'The G. hirsutum variety, LH 2256 was released for irrigated conditions of Punjab, Haryana and Rajasthan. It has yield potential of 22 q/ha and possesses 34.9% Ginning Out Turn (GOT), 28.1 mm fibre length and 22.8 g/tex fibre strength.'],
  ['F 2164', 'North Zone', null, 'The G. hirsutum variety, F 2164 was released for irrigated conditions of Punjab, Haryana and Rajasthan. It has yield potential of 24 q/ha and possesses 33.2% Ginning Out Turn (GOT), 27.7 mm fibre length and 21.3 g/tex fibre strength. It has micronaire of 4.4 and can spin up to 40 counts. It is resistant to BLB, fungal foliar diseases, tolerant to pests. It has a crop duration of 180 days.'],
  ['F 2381', 'North Zone', null, 'The G. hirsutum variety, F 2381 was released for irrigated conditions of Punjab, Haryana and Rajasthan. It has yield potential of 22.34 q/ha and possesses 32.9% Ginning Out Turn (GOT), 27.5 mm fibre length and 21.8 g/tex fibre strength.'],
  ['LD 949', 'North Zone', null, 'The G. arboreum variety, LD 949 was released for irrigated conditions of Punjab, Haryana and Rajasthan. It has yield potential of 25 q/ha and possesses 39.2% Ginning Out Turn (GOT), 20.6 mm fibre length and 17.3 g/tex fibre strength.'],
  // Central Zone
  ['NHH 250', 'Central Zone', null, 'Intra-hirsutum hybrid was released for rainfed conditions of Maharashtra, Madhya Pradesh and Gujarat. It has yield potential of 14 q/ha and possesses 35.4% Ginning Out Turn, 27.5 mm fibre length and 22.3 g/tex fibre strength.'],
  ['RHB 0711 (Phule Dhara)', 'Central Zone', null, 'An interspecific (hirsutum x barbadense) hybrid, was released for irrigated conditions of central zone with yield potential of 16 q/ha, 31.2% Ginning Out Turn, 34 mm fibre length, 28 g/tex fibre strength and 3.4 micronaire. It can spin up to 80 counts. Resistant to ALB, disease free to bacterial leaf blight, grey mildew and MLB, tolerant to sucking pests and bollworms.'],
  ['RHH 0917', 'Central Zone', null, 'An intraspecific (hirsutum x hirsutum) hybrid, released in 2016 by MPKV, Rahuri for irrigated conditions of central zone. It has yield potential of 25 q/ha and possesses 34.1% Ginning Out Turn, 29.7 mm fibre length and 27.9 g/tex fibre strength.'],
  ['RHB 0812', 'Central Zone', null, 'The interspecific (hirsutum x barbadense) hybrid, was released for irrigated conditions. It has yield potential of 15 q/ha and possesses 30.9% Ginning Out Turn (GOT), 34.8 mm fibre length and 26.6 g/tex fibre strength.'],
  ['H 1353', 'Central Zone', 'G. hirsutum varieties', 'Released for rainfed conditions. It has yield potential of 13 q/ha and possesses 35.2% Ginning Out Turn, 26 mm fibre length, 20.5 g/tex fibre strength and 4.3 micronaire.'],
  ['NH 635', 'Central Zone', 'G. hirsutum varieties', 'Released for rainfed conditions. It has yield potential of 13 q/ha and possesses 35.5% Ginning Out Turn, 26.9 mm fibre length and 20.8 g/tex fibre strength.'],
  ['ARBC 19', 'Central Zone', 'G. hirsutum varieties', 'Released for irrigated conditions. It has yield potential of 22 q/ha and possesses 34.2% Ginning Out Turn, 26.2 mm fibre length and 20.4 g/tex fibre strength.'],
  ['NDLH 1938 (Sri Rama)', 'Central Zone', 'G. hirsutum varieties', 'Released for irrigated conditions. It has yield potential of 19 q/ha and possesses 33.4% Ginning Out Turn, 28.9 mm fibre length and 23.9 g/tex fibre strength, micronaire of 4.6 and can spin up to 30 counts. It is tolerant to sucking pests (jassid, whitefly and aphid) and has a crop duration of 160 days.'],
  ['RHC 0717 (Phule Yamuna)', 'Central Zone', 'G. hirsutum varieties', 'Released for irrigated conditions with yield potential of 18.5 q/ha and possesses 34.5% Ginning Out Turn, 27.1 mm fibre length and 22.7 g/tex fibre strength, micronaire 4.9 and can spin up to 30 counts. It is tolerant to sucking pests and bollworms, resistant to bacterial leaf blight and disease free for grey mildew under field condition. It has a crop duration of 158-164 days.'],
  ['JLA 505', 'Central Zone', 'Desi cotton varieties', 'Released for rainfed conditions. It has yield potential of 15 q/ha and possesses 35.4% Ginning Out Turn, 25.8 mm fibre length, 21.8 g/tex fibre strength and micronaire of 5.3. It is moderately resistant to bacterial leaf blight and grey mildew, with a crop duration of 170-180 days.'],
  ['GAM 162', 'Central Zone', 'Desi cotton varieties', 'Released for rainfed conditions. It has yield potential of 15 q/ha and possesses 36.3% Ginning Out Turn, 24.4 mm fibre length and 19.5 g/tex fibre strength.'],
  // South Zone
  ['FMDH 9', 'South Zone', null, 'The intraspecific (arboreum x arboreum) hybrid, FMDH 9 was released for rainfed conditions of Tamil Nadu, Andhra Pradesh and Karnataka. It has yield potential of 16 q/ha and possesses 38.9% Ginning Out Turn (GOT), 22.8 mm fibre length and 18.5 g/tex fibre strength.'],
  ['AAH 32', 'South Zone', null, 'The intraspecific (arboreum x arboreum) hybrid, AAH 32 was released for rainfed conditions of Tamil Nadu, Andhra Pradesh and Karnataka. It has yield potential of 19.02 q/ha and possesses 40.5% Ginning Out Turn (GOT), 23.3 mm fibre length and 18 g/tex fibre strength.'],
  ['K 12', 'South Zone', null, 'The G. arboreum variety, K 12 was released for rainfed conditions of Tamil Nadu. It has yield potential of 11.93 q/ha and possesses 35.7% Ginning Out Turn (GOT), 27.7 mm fibre length and 22.1 g/tex fibre strength. It has micronaire of 5.4 and can spin up to 30 counts. It is moderately resistant to bacterial blight and Alternaria leaf spot, resistant to leafhopper, aphids, thrips and stem weevil.'],
  ['AKA 2005-3', 'South Zone', null, 'The G. arboreum variety, AKA 2005-3 was released for rainfed conditions of Tamil Nadu, Andhra Pradesh and Karnataka. It has yield potential of 13 q/ha and possesses 36.7% Ginning Out Turn (GOT), 25.4 mm fibre length and 21.3 g/tex fibre strength.'],
  ['JLA 0603', 'South Zone', null, 'The G. arboreum variety, JLA 0603 was released for rainfed conditions of Tamil Nadu, Andhra Pradesh and Karnataka. It has yield potential of 15.15 q/ha and possesses 37.3% Ginning Out Turn (GOT), 24.6 mm fibre length and 21.5 g/tex fibre strength. It has micronaire of 5.9 and can spin up to 20 counts. It is resistant to jassids and BLB.'],
  ['HS 292', 'South Zone', null, 'The G. hirsutum variety, HS 292 was released for irrigated conditions of Tamil Nadu, Andhra Pradesh and Karnataka. It has yield potential of 23.16 q/ha and possesses 35.5% Ginning Out Turn (GOT), 27.8 mm fibre length and 21.7 g/tex fibre strength. It has micronaire of 4.3 and can spin up to 24 counts.'],
  ['SVPR 6 (TSH 04/115)', 'South Zone', null, 'The G. hirsutum variety, SVPR 6 (TSH 04/115) was released for cotton growing conditions of Tamil Nadu, Andhra Pradesh and Karnataka. It has yield potential of 23.12 q/ha and possesses 33.4% Ginning Out Turn (GOT), 29.5 mm fibre length and 27.3 g/tex fibre strength.'],
  ['DHB 1071', 'South Zone', null, 'The interspecific (hirsutum x barbadense) hybrid, DHB 1071 was released for irrigated conditions of Tamil Nadu, Andhra Pradesh and Karnataka. It has yield potential of 17 q/ha and possesses 32.2% Ginning Out Turn (GOT), 34.4 mm fibre length and 24.8 g/tex fibre strength.'],
  ['DHB 915', 'South Zone', null, 'The interspecific (hirsutum x barbadense) hybrid, DHB 915 was released for irrigated conditions of Tamil Nadu, Andhra Pradesh and Karnataka. It has yield potential of 17 q/ha and possesses 34% Ginning Out Turn (GOT), 34.5 mm fibre length and 28.2 g/tex fibre strength. It has micronaire of 3.4 and can spin up to 80 counts.'],
  ['RHH 0707 (Phule Tarang)', 'South Zone', null, 'The intraspecific (hirsutum x hirsutum) hybrid, RHH 0707 (Phule Tarang) was released for irrigated conditions of Tamil Nadu, Andhra Pradesh and Karnataka. It has yield potential of 20.3 q/ha and possesses 35.5% Ginning Out Turn (GOT), 28.1 mm fibre length and 20.6 g/tex fibre strength. It has micronaire of 4.3 and can spin up to 40 counts. It is resistant to BLB & MLB, moderately resistant to ALB, resistant to sucking pests, tolerant to bollworms. Crop duration of this variety is 165-170 days.'],
  ['SVPR 1 (TSHH 0629)', 'South Zone', null, 'The intraspecific (hirsutum x hirsutum) hybrid, SVPR 1 (TSHH 0629) was released for irrigated conditions of Tamil Nadu, Andhra Pradesh and Karnataka. It has yield potential of 23 q/ha and possesses 35.8% Ginning Out Turn (GOT), 28.5 mm fibre length, 21.2 g/tex fibre strength. It has micronaire of 4.1 and can spin up to 40 counts. It is moderately resistant to bacterial leaf blight and Alternaria leaf spot, moderately resistant to leafhopper, and tolerates drought and high night temperatures prevailing in the summer season.'],
  ['RHH 1007', 'South Zone', null, 'The intraspecific (hirsutum x hirsutum) hybrid, RHH 1007 was released for irrigated conditions of Tamil Nadu, Andhra Pradesh and Karnataka. It has yield potential of 23.06 q/ha and possesses 35.9% Ginning Out Turn (GOT), 28.5 mm fibre length and 21.5 g/tex fibre strength. It has micronaire of 4.3 and can spin up to 40 counts. It is moderately resistant to ALB, resistant to MLB, resistant to aphids, thrips and whitefly, and tolerant to jassids.'],
  ['RAHH 455 (Raichur Shakthi 455)', 'South Zone', null, 'The intraspecific (hirsutum x hirsutum) hybrid, RAHH 455 was released for rainfed conditions of Tamil Nadu, Andhra Pradesh and Karnataka. It has yield potential of 18.33 q/ha and possesses 35.9% Ginning Out Turn (GOT), 29.4 mm fibre length and 21.6 g/tex fibre strength. It has micronaire of 4.6 and can spin up to 40 counts. It has moderate resistance to jassids, aphids and leaf spot, and is tolerant to bollworms. Crop duration of this variety is 150-160 days.'],
].map(([name, zone, group, description]) => ({ name, zone, group, description }));

const appData = { banners, varieties, pests, diseases, production, facts, advisories, gallery, galleryAlbums, cultivars };

