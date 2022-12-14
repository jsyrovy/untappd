BEGIN TRANSACTION;
CREATE TABLE [pivni_valka] (
	[date] text,
	[user] text,
	[unique_beers] integer
);
INSERT INTO "pivni_valka" VALUES('2022-01-01','sejrik',0);
INSERT INTO "pivni_valka" VALUES('2022-01-01','mencik2',1);
INSERT INTO "pivni_valka" VALUES('2022-01-01','Mates511',2);
INSERT INTO "pivni_valka" VALUES('2022-01-01','ominar',3);
INSERT INTO "pivni_valka" VALUES('2022-01-02','sejrik',5);
INSERT INTO "pivni_valka" VALUES('2022-01-02','mencik2',6);
INSERT INTO "pivni_valka" VALUES('2022-01-02','Mates511',7);
INSERT INTO "pivni_valka" VALUES('2022-01-02','ominar',8);
INSERT INTO "pivni_valka" VALUES('2022-01-03','sejrik',10);
INSERT INTO "pivni_valka" VALUES('2022-01-03','mencik2',11);
INSERT INTO "pivni_valka" VALUES('2022-01-03','Mates511',12);
INSERT INTO "pivni_valka" VALUES('2022-01-03','ominar',13);
INSERT INTO "pivni_valka" VALUES('2022-01-04','sejrik',20);
INSERT INTO "pivni_valka" VALUES('2022-01-04','mencik2',21);
INSERT INTO "pivni_valka" VALUES('2022-01-04','Mates511',22);
INSERT INTO "pivni_valka" VALUES('2022-01-04','ominar',23);
COMMIT;
