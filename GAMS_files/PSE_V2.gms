Set
         i monomer plants
         j polymer reactor
         t time period
         h IHP centres
         c customers

         g grade products
         o product intermediates
         m monomer plant materials


         HC(h,c) IHP and customer mapping

         alias(h,hp);
         alias(m,mp);

Parameters
         p_min(i)    minimum production amount in olefin plant i
         p_max(i)    maximum production amount in olefin plant i
         PR(g,j)     production rate of grade g in polymer reactor j
         tao(g,j)    minimum runtime for grade g to be produced in
                     polymer reactor j
         f(t)        length of time period t
         phi(j,t)    available fraction of time in time period t
         miu(i,mp,m) production coefficient of monomer o
                     in terms of m in olefin plant i
         n(m,g)      consumption coefficient of olefin o when producing grade g
         D(c,g,t)    demand of grade g of customer c in time period t
         SP(c,g,t)   sale price of grade g to customer c
         SO(m,t)     export price of olefin o
         PC(m,t)     purchase price
         OC(i)       coefficient for operation cost of olefin plant i
         OP(g,j)     coefficient for operation cost of polymer reactor j for
                     producing grade g
         LT(h)       lead time from UAE GATEWAY to IHP h
         IC_upper(m) upper bound of the material inventory of m
         IH_low(g,h) lower bound of grade g at h
         IC_ini_level(m) initial level of raw material;


$onecho > tasks.txt
set = i rng = set!E3 cdim = 1
set = j rng = set!E6 cdim = 1
set = t rng = set!E9 cdim = 1
set = h rng = set!E12 cdim = 1
set = c rng = set!E15 cdim = 1
set = g rng = set!E18 cdim = 1
set = m rng = set!E21 cdim = 1
set = HC rng = set!E25 rdim = 1 cdim = 1

par = p_min rng = ProductionOlefins!c5 cdim = 1
par = p_max rng = ProductionOlefins!c10 cdim = 1
par = OC   rng = ProductionOlefins!c15 cdim = 1
par = miu  rng = ProductionOlefins!c22 rdim = 2 cdim = 1
par = IC_upper  rng = ProductionOlefins!c74 cdim = 1

par = PR   rng = ProductionPolyolefins!D4 rdim = 1 cdim = 1
par = tao  rng = ProductionPolyolefins!D18 rdim = 1 cdim = 1
par = n    rng = ProductionPolyolefins!D32 rdim = 1 cdim = 1
par = OP   rng = ProductionPolyolefins!D47 rdim = 1 cdim = 1

par = LT   rng = WarehousesShipping!c5 cdim = 1
par = IH_low rng = WarehousesShipping!c9 rdim = 1 cdim = 1

par = f    rng = ScenarioAvailability!D15 cdim = 1
par = phi  rng = ScenarioAvailability!D19 rdim = 1 cdim = 1

par = D    rng = ScenarioSales!D7 rdim = 2 cdim = 1
par = SP   rng = ScenarioSales!D74 rdim = 2 cdim = 1
par = SO   rng = ScenarioSales!D137 rdim = 1 cdim = 1

par = PC   rng = ScenarioPurchases!D26 rdim = 1 cdim = 1
par = IC_ini_level rng = ScenarioPurchases!D38 cdim = 1

$offecho
*$call GDXXRW Borouge_Data_Scott_Demo.xlsx trace = 3 @tasks.txt
$GDXIN Borouge_Data_Scott_Demo.gdx
$LOAD i, j, t, h, c, g, m, HC

$LOADDC p_min, p_max, PR, tao, f, phi, miu, n, D, SP, SO, PC, OC, OP, LT
$LOADDC IC_upper, IH_low, IC_ini_level
$GDXIN



Positive Variables
         PM(i,m,t) amount of material m consumed in unit i
         PO(i,t)   production amount of olefin plant i in time period t
         PP(g,j,t) produced amount of grade g in polymer reactor j over period t
         IC(m,t)   plant inventory level of olefin o at time period t
         PU(m,t)   amount of olefin o purchased at time period t
         S(m,t)    amount of olefin sold by export at time period t
         Q(g,h,t)  shipment of grade g to IHP h at time period t
         IH(g,h,t) inventory level of grade g at IHP h at time period t
         QC(c,g,h,t) supply of grade g from IHP h to customer c at period t;

Binary Variables
         Y(g,j,t) is = 1 if g is produced in polymer plant j over period t;

Variables
         Z objective value (the profit in this case) ;


         PO.up(i,t) = p_max(i);
         PO.lo(i,t) = p_min(i);
         IC.fx(m,'1') = IC_ini_level(m);
         IC.up(m,t) = IC_upper(m);
         IH.fx(g,h,'1') = IH_low(g,h);
         IH.lo(g,h,t) = IH_low(g,h);
         S.fx(m,'1') = 0;

         Q.fx(g,h,t)$(ord(h) = 1) = 0;
         QC.fx(c,g,h,t)$(not HC(h,c)) = 0;

Equations
         obj    objective funciton

         min_amount minimal amount produced by each polymer reactor
         max_amount maximal amount produced by each polymer reactor
         sum_amount sum amount of each polymer reactor j
         product_capacity capacity of each i must be maintained
         olefin_inv inventory for olefins
         grade_inv  inventory for grades

*$ontext
         IHP_inv    inventory for each IHP location
         demand_con demand constraints

*$offtext


;


         obj..  Z =E= sum((g,h,c,t), QC(c,g,h,t) * SP(c,g,t))
                         + sum((m,t), S(m,t) * SO(m,t))
                         - sum((m,t), PU(m,t) * PC(m,t))
                         - sum((i,t), PO(i,t) * OC(i))
                         - sum((g,j,t), PP(g,j,t) * OP(g,j))
;

         min_amount(g,j,t).. PP(g,j,t) =G= PR(g,j) * Y(g,j,t) * tao(g,j);

         max_amount(g,j,t).. PP(g,j,t) =L= PR(g,j) * Y(g,j,t) * f(t) * phi(j,t);

         sum_amount(j,t).. sum(g$(PR(g,j) ne 0), PP(g,j,t)/PR(g,j)) =L=
                                                                f(t) * phi(j,t);

         product_capacity(i,t).. sum(m, PM(i,m,t)) =E= PO(i,t);

         olefin_inv(m,t-1).. IC(m,t) =E= IC(m,t-1)
                             + sum((i,mp), miu(i,mp,m)*PM(i,mp,t))
                             - sum(i, PM(i,m,t))
                             + PU(m,t) - S(m,t) - sum((g,j), n(m,g)*PP(g,j,t));


         grade_inv(g,h,t-1)$(ord(h) = 1).. IH(g,h,t) =E=
                             IH(g,h,t-1) + sum(j, PP(g,j,t-LT(h)))
                             - sum(hp $(ord(hp) > ord(h)), Q(g,hp,t))
                             - sum(c, QC(c,g,h,t));

*$ontext
         IHP_inv(g,h,t-1)$(ord(h) > 1).. IH(g,h,t) =E= IH(g,h,t-1)
                                  + Q(g, h,t-LT(h))
                                  - sum(c, QC(c,g,h,t));


         demand_con(g,c,t).. sum(h, QC(c,g,h,t)) =L= D(c,g,t);
*$offtext


Model test /all/;

Option optcr = 0.01;

option MIP = cplex  ;

Option solslack = 1;
Option solprint = off, limrow = 0, limcol = 0 ;

Solve test maximizing Z using MIP;

Execute_Unload "testrun1.gdx" ;

Display  Z.l, Y.l, S.l, IH.l, PP.l, Q.l, QC.l, IC.l, D, IC.l;

