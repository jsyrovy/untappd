BEGIN TRANSACTION;
CREATE TABLE [pivni_valka] (
	[date] text,
	[user] text,
	[unique_beers] integer
);
INSERT INTO "pivni_valka" VALUES('2022-01-01','sejrik',0);
INSERT INTO "pivni_valka" VALUES('2022-01-01','mencik2',0);
INSERT INTO "pivni_valka" VALUES('2022-01-01','Mates511',0);
INSERT INTO "pivni_valka" VALUES('2022-01-01','ominar',0);
INSERT INTO "pivni_valka" VALUES('2022-01-02','sejrik',1);
INSERT INTO "pivni_valka" VALUES('2022-01-02','mencik2',2);
INSERT INTO "pivni_valka" VALUES('2022-01-02','Mates511',3);
INSERT INTO "pivni_valka" VALUES('2022-01-02','ominar',0);
INSERT INTO "pivni_valka" VALUES('2022-01-03','sejrik',0);
INSERT INTO "pivni_valka" VALUES('2022-01-03','mencik2',0);
INSERT INTO "pivni_valka" VALUES('2022-01-03','Mates511',0);
INSERT INTO "pivni_valka" VALUES('2022-01-03','ominar',0);
INSERT INTO "pivni_valka" VALUES('2022-01-04','sejrik',10);
INSERT INTO "pivni_valka" VALUES('2022-01-04','mencik2',20);
INSERT INTO "pivni_valka" VALUES('2022-01-04','Mates511',30);
INSERT INTO "pivni_valka" VALUES('2022-01-04','ominar',0);
COMMIT;
