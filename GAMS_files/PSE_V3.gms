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
         IM(i,m) monomer plant and material mapping
         GJ(g,j) grade and polymer plant mapping

         alias(h,hp);
         alias(m,mp);

Parameters
         p_min(i,m)  minimum production rate of m in olefin plant i  T
         p_max(i,m)  maximum production rate of m in olefin plant i  T
         PR(g,j)     production rate of grade g in polymer reactor j T
         tao(g,j)    minimum runtime for grade g to be produced in   T
                     polymer reactor j                               T
         delta(t)    length of time period t                         T
         phi(j,t)    available fraction of time in time period t     T
         miu(i,mp,m) production coefficient of monomer o             T
                     in terms of m in olefin plant i                 T
         n(m,g)      consumption coefficient of olefin o when producing grade g   T
         D(c,g,t)    demand of grade g of customer c in time period t  T
         SP(c,g,t)   sale price of grade g to customer c             T
         SO(m,t)     export price of olefin o                        T
         PC(m,t)     purchase price                                  T
         OC(i)       coefficient for operation cost of olefin plant i  T
         OP(g,j)     coefficient for operation cost of polymer reactor j for  T
                     producing grade g                                T
         LT(h)       lead time from UAE GATEWAY to IHP h              T
         IC_upper(m) upper bound of the material inventory of m       T
         IH_low(g,h) lower bound of grade g at h                      T
         IC_ini_level(m) initial level of raw material                T
         IC_low(m)   lower bound of material m at plant               T
         PU_max(m)    maximum purchase rate per day of material m     T
         PU_min(m)    minimum purchase rate per day of material m     T


         IH_upper(g,h) upper bound of grade g at h
         pie(c)      penalty cost for demand not satisfied for each customers
         S_max(m)     maximum sale rate per day of material m
         S_min(m)     minimum sale rate per day of material m
         FL_max(m)    maximum flare rate per day of material m
         FL_min(m)    minimum flare rate per day of material m
         Qtil(g,h,t)  amount of grade g that arrives at IHP h over t
                      because of preceding shipment
         ;


$onecho > tasks.txt
set = i rng = set!E3 cdim = 1
set = j rng = set!E6 cdim = 1
set = t rng = set!E9 cdim = 1
set = h rng = set!E12 cdim = 1
set = c rng = set!E15 cdim = 1
set = g rng = set!E18 cdim = 1
set = m rng = set!E21 cdim = 1
set = HC rng = set!E25 rdim = 1 cdim = 1
set = IM rng = set!E31 rdim = 1 cdim = 1
set = GJ rng = set!E40 rdim = 1 cdim = 1

par = p_max rng = ProductionOlefins!c4 rdim = 1 cdim = 1
par = p_min rng = ProductionOlefins!c13 rdim = 1 cdim = 1
par = OC   rng = ProductionOlefins!c22 cdim = 1
par = miu  rng = ProductionOlefins!c27 rdim = 2 cdim = 1
par = IC_upper  rng = ProductionOlefins!c78 cdim = 1
par = IC_low  rng = ProductionOlefins!c83 cdim = 1
par = IC_ini_level rng = ProductionOlefins!c88 cdim = 1

par = PR   rng = ProductionPolyolefins!C4 rdim = 1 cdim = 1
par = tao  rng = ProductionPolyolefins!C18 rdim = 1 cdim = 1
par = n    rng = ProductionPolyolefins!C32 rdim = 1 cdim = 1
par = OP   rng = ProductionPolyolefins!C47 rdim = 1 cdim = 1

par = LT   rng = WarehousesShipping!c5 cdim = 1
par = IH_low rng = WarehousesShipping!c9 rdim = 1 cdim = 1

par = delta  rng = ScenarioAvailability!D4 cdim = 1
par = phi  rng = ScenarioAvailability!D8 rdim = 1 cdim = 1

par = D    rng = ScenarioSales!D7 rdim = 2 cdim = 1
par = SP   rng = ScenarioSales!D74 rdim = 2 cdim = 1
par = SO   rng = ScenarioSales!D137 rdim = 1 cdim = 1

par = PC   rng = ScenarioPurchases!D5 rdim = 1 cdim = 1
par = PU_max rng = ScenarioPurchases!D16 cdim = 1
par = PU_min rng = ScenarioPurchases!D20 cdim = 1

par = IH_upper rng = AdditionalParameters!C3 rdim = 1 cdim = 1
par = pie rng = AdditionalParameters!C16 cdim = 1
par = S_max rng = AdditionalParameters!C21 cdim = 1
par = S_min rng = AdditionalParameters!C26 cdim = 1
par = FL_max  rng = AdditionalParameters!C31 cdim = 1
par = FL_min rng = AdditionalParameters!C36 cdim = 1
par = Qtil rng = AdditionalParameters!C41 rdim = 2 cdim = 1

$offecho
*$call GDXXRW Borouge_Data_Final.xlsx trace = 3 @tasks.txt
$GDXIN Borouge_Data_Final.gdx
$LOAD i, j, t, h, c, g, m, HC, IM, GJ

$LOADDC PR, tao, delta, phi, n, D, SP, SO, PC, OC, OP, LT, p_min, p_max, miu
$LOADDC IC_upper, IH_low, IC_ini_level, IC_low, PU_max, PU_min, IH_upper
$LOADDC S_max, S_min, FL_max, FL_min, Qtil, pie
$GDXIN



Positive Variables
         PM(i,m,t) amount of material m consumed in unit i
         PP(g,j,t) produced amount of grade g in polymer reactor j over period t
         IC(m,t)   plant inventory level of olefin o at time period t
         PU(m,t)   amount of olefin o purchased at time period t
         S(m,t)    amount of olefin sold by export at time period t
         Q(g,h,t)  shipment of grade g to IHP h at time period t
         IH(g,h,t) inventory level of grade g at IHP h at time period t
         QC(c,g,t) supply of grade g from IHP h to customer c at period t
         FL(m,t) amount of material m flared at period t
         del(c,g,t) amount of grade g short for customer c over t;

Binary Variables
         Y(g,j,t) is = 1 if g is produced in polymer plant j over period t;

Variables
         Z objective value (the profit in this case) ;


         PM.up(i,m,t)$(IM(i,m)) = p_max(i,m) * delta(t);
         PM.lo(i,m,t)$(IM(i,m)) = p_min(i,m) * delta(t);

         S.up(m,t) = S_max(m) * delta(t);
         S.lo(m,t) = S_min(m) * delta(t);

         FL.up(m,t) = FL_max(m) * delta(t);
         FL.lo(m,t) = FL_min(m) * delta(t);

         IC.up(m,t) = IC_upper(m);
         IC.lo(m,t) = IC_low(m);

         IH.up(g,h,t) = IH_upper(g,h);
         IH.lo(g,h,t) = IH_low(g,h);


         Q.fx(g,h,t)$(ord(h) = 1) = 0;
         PP.fx(g,j,t)$(not GJ(g,j)) = 0;

Equations
         obj    objective funciton

         min_amount minimal amount produced by each polymer reactor
         max_amount maximal amount produced by each polymer reactor
         sum_amount sum amount of each polymer reactor j
         olefin_inv1 inventory for olefins t > 1
         olefin_inv2 inventory for olefins t = 1

         grade_inv1  inventory for grades t > lT(h)
         grade_inv2  inventory for grades 1 < t <= lT(h)
         grade_inv3  inventory for grades t = 1

*$ontext
         IHP_inv1    inventory for each IHP location t > lT(h)
         IHP_inv2    inventory for each IHP location 1 < t <= lT(h)
         IHP_inv3    inventory for each IHP location t = 1
         demand_con demand constraints

*$offtext


;


         obj..  Z =E= sum((g,c,t), QC(c,g,t) * SP(c,g,t))
                         + sum((m,t), S(m,t) * SO(m,t))
                         - sum((m,t), PU(m,t) * PC(m,t))
                         - sum((i,m,t), PM(i,m,t) * OC(i))
                         - sum((g,j,t), PP(g,j,t) * OP(g,j))
                         - sum((c,g,t), pie(c) * del(c,g,t))
;

         min_amount(g,j,t)$(GJ(g,j)).. PP(g,j,t) =G=
                                         PR(g,j) * Y(g,j,t) * tao(g,j);

         max_amount(g,j,t)$(GJ(g,j)).. PP(g,j,t) =L=
                              PR(g,j) * Y(g,j,t) * delta(t) * phi(j,t);

         sum_amount(j,t).. sum(g$(PR(g,j) ne 0), PP(g,j,t)/PR(g,j)) =L=
                                                   delta(t) * phi(j,t);


         olefin_inv1(m,t)$(ord(t) > 1).. IC(m,t) =E= IC(m,t-1)
                             + sum((i,mp)$IM(i,mp), miu(i,mp,m)*PM(i,mp,t))
                             - sum(i, PM(i,m,t))
                             + PU(m,t) - S(m,t)
                             - sum((g,j)$(GJ(g,j)), n(m,g)*PP(g,j,t));


         olefin_inv2(m,t)$(ord(t) = 1).. IC(m,t) =E= IC_ini_level(m)
                             + sum((i,mp)$IM(i,mp), miu(i,mp,m)*PM(i,mp,t))
                             - sum(i, PM(i,m,t))
                             + PU(m,t) - S(m,t)
                             - sum((g,j)$(GJ(g,j)), n(m,g)*PP(g,j,t));


         grade_inv1(g,h,t)$(ord(h) = 1 and ord(t) > LT(h)).. IH(g,h,t) =E=
                             IH(g,h,t-1) + sum(j, PP(g,j,t-LT(h)))
                             - sum(hp $(ord(hp) ne ord(h)), Q(g,hp,t))
                             - sum(c$HC(h,c), QC(c,g,t));


         grade_inv2(g,h,t)$((ord(h) = 1) and (ord(t) le LT(h)) and (ord(t) > 1))
                             .. IH(g,h,t) =E=
                 IH(g,h,t-1) - sum(hp $(ord(hp) ne ord(h)), Q(g,hp,t))
                             - sum(c$HC(h,c), QC(c,g,t));

         grade_inv3(g,h,t)$(ord(h) = 1 and ord(t) = 1).. IH(g,h,t) =E=
                 IH_low(g,h) - sum(hp $(ord(hp) ne ord(h)), Q(g,hp,t))
                             - sum(c$HC(h,c), QC(c,g,t));

*$ontext
         IHP_inv1(g,h,t)$(ord(h) > 1 and ord(t) > LT(h)).. IH(g,h,t) =E=
                                    IH(g,h,t-1) + Q(g, h,t-LT(h))
                                  - sum(c$HC(h,c), QC(c,g,t));

         IHP_inv2(g,h,t)$(ord(h) > 1 and (ord(t) le LT(h)) and (ord(t) > 1))..
                                    IH(g,h,t) =E= IH(g,h,t-1)
                                  - sum(c$HC(h,c), QC(c,g,t));

         IHP_inv3(g,h,t)$(ord(h) > 1 and ord(t) = 1).. IH(g,h,t) =E=
                                    IH_low(g,h) - sum(c$HC(h,c), QC(c,g,t));


         demand_con(g,c,t).. QC(c,g,t) =E= D(c,g,t) - del(c,g,t);
*$offtext


Model test /all/;

Option optcr = 0.01;

option MIP = cplex  ;

Option solslack = 1;
Option solprint = off, limrow = 0, limcol = 0 ;

Solve test maximizing Z using MIP;

Execute_Unload "testrunV3_2.gdx" ;

Display  Z.l, Y.l, S.l, IH.l, PP.l, Q.l, QC.l, IC.l, D, IC.l;

