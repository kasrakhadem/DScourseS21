--part a
.mode csv
.import ./FL_insurance_sample.csv FL_insurance

--part b
select * from FL_insurance limit 10;

--part c
select distinct county from FL_insurance;

--part d
select avg(cast(tiv_2012 as double)- cast(tiv_2011 as double)) from FL_insurance;

--part e
select a.construction, count(a.construction) as Freq, (count(a.construction) *100.0 / (select count(*) from FL_insurance b)) as PCT
from FL_insurance a group by (construction);
