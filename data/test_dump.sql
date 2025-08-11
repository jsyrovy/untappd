BEGIN TRANSACTION;
CREATE TABLE [archive] (
	[id] integer PRIMARY KEY,
    [dt_utc] text,
	[user] text,
	[beer] text,
	[brewery] text,
	[venue] text
);
INSERT INTO "archive" VALUES(1,'2016-10-17 16:39:15','sejrik','Pivo','Pivovar','Pivnice');
INSERT INTO "archive" VALUES(2,'2016-10-17 16:39:15','sejrik','Pivo 2','Pivovar','Pivnice');
INSERT INTO "archive" VALUES(3,'2016-10-17 16:39:15','sejrik','Jine Pivo','Jiny Pivovar','Jina Pivnice');
INSERT INTO "archive" VALUES(4,'2016-10-17 16:39:15','sejrik','Three Suns','Sibeeria',NULL);
CREATE TABLE [pivni_valka] (
	[id] integer PRIMARY KEY,
	[date] text,
	[user] text,
	[unique_beers] integer
);
INSERT INTO "pivni_valka" VALUES(1,'2022-01-01','sejrik',0);
INSERT INTO "pivni_valka" VALUES(2,'2022-01-01','mencik2',0);
INSERT INTO "pivni_valka" VALUES(3,'2022-01-01','Indi51',0);
INSERT INTO "pivni_valka" VALUES(4,'2022-01-01','karolina_matukova_7117',0);
INSERT INTO "pivni_valka" VALUES(5,'2022-01-01','ominar',0);
INSERT INTO "pivni_valka" VALUES(6,'2022-01-02','sejrik',1);
INSERT INTO "pivni_valka" VALUES(7,'2022-01-02','mencik2',2);
INSERT INTO "pivni_valka" VALUES(8,'2022-01-02','Indi51',3);
INSERT INTO "pivni_valka" VALUES(9,'2022-01-02','karolina_matukova_7117',4);
INSERT INTO "pivni_valka" VALUES(10,'2022-01-02','ominar',0);
INSERT INTO "pivni_valka" VALUES(11,'2022-01-03','sejrik',0);
INSERT INTO "pivni_valka" VALUES(12,'2022-01-03','mencik2',0);
INSERT INTO "pivni_valka" VALUES(13,'2022-01-03','Indi51',0);
INSERT INTO "pivni_valka" VALUES(14,'2022-01-03','karolina_matukova_7117',0);
INSERT INTO "pivni_valka" VALUES(15,'2022-01-03','ominar',0);
INSERT INTO "pivni_valka" VALUES(16,'2022-01-04','sejrik',10);
INSERT INTO "pivni_valka" VALUES(17,'2022-01-04','mencik2',20);
INSERT INTO "pivni_valka" VALUES(18,'2022-01-04','Indi51',30);
INSERT INTO "pivni_valka" VALUES(19,'2022-01-04','karolina_matukova_7117',40);
INSERT INTO "pivni_valka" VALUES(20,'2022-01-04','ominar',0);
COMMIT;
