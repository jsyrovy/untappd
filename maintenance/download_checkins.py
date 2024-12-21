import datetime
from random import shuffle

from bs4 import BeautifulSoup

from archivist import create_record_in_db, is_record_in_db
from database.models import Archive
from robot.base import BaseRobot
from utils import common

CHECK_IN_IDS = [
    int(id_)
    for id_ in """1252442889
1251894336
1250492629
1249011419
1248987290
1248348329
1246545805
1246371513
1246367029
1246364874
1246359074
1246357220
1246339673
1246338619
1246338059
1245261927
1245095683
1243327169
1242729951
1242714325
1242700526
1242689382
1242384283
1242378972
1242376163
1242373679
1241690100
1241654891
1241603268
1241578859
1241559282
1241544881
1241527014
1241520301
1241510300
1241502989
1241240099
1240626945
1239743668
1239694260
1239339545
1238768014
1238767402
1238763912
1237955953
1237625544
1237621561
1236845345
1236826473
1236547872
1236112692
1235900233
1235855494
1235466686
1235431135
1235358964
1235354530
1235011490
1234997275
1234978368
1234933668
1234931755
1234597157
1234217861
1232450396
1232089069
1231852751
1231814218
1231403362
1230682616
1230196576
1230132156
1229626657
1229620343
1229284681
1229257312
1228949292
1228944009
1228939546
1228585374
1228485522
1228045000
1227982860
1227518063
1227202482
1226792828
1226361820
1225922782
1225831724
1225822576
1225540071
1225429059
1224884376
1224869485
1224832508
1224470286
1223885039
1223865439
1223855598
1223563825
1222936376
1222926062
1222707623
1221124433
1221120124
1221117219
1221114512
1221111065
1221103690
1220990331
1220980859
1220221895
1219832333
1219750693
1219598378
1218901426
1218002380
1217644197
1217006704
1215912032
1215903585
1215891419
1215863703
1214825803
1214809576
1214791433
1213299925
1213279187
1213266790
1213256393
1213209215
1212769293
1212591616
1212186761
1212146456
1211555328
1211544393
1211536957
1211531212
1211522630
1211514522
1211506216
1211500585
1211493680
1211489820
1211485512
1211052578
1210393950
1209253738
1209244289
1209215013
1208881683
1208792837
1208381155
1208300078
1207138288
1207109524
1207094368
1207083191
1207064255
1206679182
1205011678
1204915759
1204479971
1204444332
1203897168
1203893914
1203269382
1200632010
1200615969
1200568107
1200546429
1200522532
1200495391
1200472084
1200438323
1200423906
1200416966
1199678682
1199673699
1199468117
1198631544
1198021627
1197634555
1197108235
1196909916
1195852014
1195825558
1195803245
1195784283
1195767078
1195755003
1195407202
1194787378
1194759935
1194019271
1193964881
1193955996
1193562610
1192946695
1192897330
1192368885
1192354899
1192147866
1192137697
1192128112
1191603822
1190059144
1189575697
1189513456
1189293619
1189288885
1189287386
1188926397
1187179041
1186909483
1186904461
1186886972
1186277662
1185296029
1184872109
1184871388
1184800413
1184730505
1184537035
1183988014
1183976241
1183059862
1183012400
1183010569
1183009953
1182999696
1182976444
1182972999
1182952414
1182951604
1182948496
1182944962
1182941613
1181910976
1181099082
1181081124
1180977626
1179666005
1179661842
1179360693
1179065581
1178525203
1178518691
1177417353
1176604287
1176592194
1176589737
1176586809
1175278747
1175272455
1175265845
1174889336
1174815861
1172945816
1172040858
1172019455
1172011726
1171566039
1170598961
1169855483
1169839763
1169814458
1169281363
1168608886
1167446492
1167155338
1167146313
1167132696
1167115007
1167105082
1166888454
1166879996
1166879528
1166727271
1165036864
1163115017
1163085194
1163055738
1163016219
1162975623
1162962132
1162531618
1162481246
1162127336
1161114957
1161110817
1160453313
1159753111
1159736895
1158955606
1157315390
1156886197
1156873446
1156865462
1156440880
1155788283
1155063334
1155056372
1155046063
1154824843
1154812234
1154810124
1154676472
1154183055
1153002833
1152989017
1152966465
1152318298
1152288898
1152055869
1151880441
1151103872
1150841424
1150431649
1150413708
1149415655
1149351792
1148918393
1148714209
1148434291
1148358306
1148225881
1148218324
1147956412
1147947509
1147897278
1147879109
1147842011
1147602777
1147313755
1146394910
1146353182
1146229120
1145558851
1145518076
1145129280
1144767305
1144745379
1144723961
1144713969
1144632729
1144186663
1144150315
1143264541
1143260928
1143110163
1143088046
1142762397
1142736060
1142439207
1142372839
1142150556
1141835042
1141029309
1141018624
1141007957
1140864136
1140852968
1140829269
1140674390
1140652936
1140180777
1139952748
1139775563
1138838505
1138553001
1138545291
1137994889
1137928686
1137920263
1137853160
1137850469
1137405435
1136417468
1136105080
1136087388
1136074011
1135780555
1135422843
1135254817
1135122500
1134773152
1134772622
1134705192
1134313490
1134126629
1134100623
1133727539
1132641811
1132186204
1131109254
1130946261
1130898429
1130824738
1130801370
1130069579
1129930652
1129763519
1129292005
1128555743
1127580647
1127560147
1126189912
1126153161
1126130600
1126121642
1126100284
1125363831
1125115649
1124268934
1124216232
1124150124
1124111126
1124088649
1123528986
1121779094
1121743184
1120589912
1120582142
1120197687
1118926174
1118860797
1118469435
1118349361
1117903693
1117560659
1117352025
1117201618
1116303545
1115386568
1115287899
1114862855
1114507131
1114504453
1114188386
1113666874
1113165606
1111727830
1111553162
1111252212
1111136765
1109974535
1109708216
1109483602
1108795999
1108600935
1107253318
1107221414
1106739974
1106715322
1106536237
1105837297
1105787609
1105098490
1104712749
1104468551
1104420148
1102416124
1102357913
1101906806
1101697657
1101533605
1101503606
1099615362
1099570443
1099570407
1099461261
1099411727
1099265035
1098293718
1098261382
1096863668
1096615395
1096553669
1096101606
1095555511
1095109216
1094894418
1094882265
1094712785
1093472218
1089203054
1088147008
1088146018
1088058726
1088034819
1088014440
1086774273
1086735548
1086213892
1085628575
1085002370
1084972877
1083814474
1083747289
1083692481
1083679595
1081402167
1081275472
1081197321
1081080037
1081059805
1078178840
1078074573
1078068754
1076372374
1076316783
1076291591
1076271105
1076261179
1076205194
1076167816
1076162465
1074625545
1074609250
1074595207
1074568420
1074553468
1074524465
1074217255
1074158316
1073583046
1073580628
1073548400
1073508334
1069192015
1068954754
1068872190
1068840019
1066633160
1066429397
1066401429
1066377759
1065911990
1065248235
1065197574
1064658256
1061402144
1061317157
1061292708
1060393563
1060012334
1059986589
1059974707
1057380817
1056332529
1055879986
1055826258
1050590319
1050517256
1048650911
1047365935
1047362353
1045973599
1045965529
1045935658
1044628524
1043081866
1043079720
1041674342
1037552275
1036960093
1027265424
1027199154
1026403679
1024133729
1024112977
1024100269
1022018951
1022018799
1021585930
1021560851
1019435806
1019425370
1019420727
1017357066
1017332838
1015574535
1015454087
1015452288
1011880835
1011857218
1008050508
1007876439
1005343894
999492336
999485766
992335822
990959409
988595337
988594968
987419821
987359949
987289622
971570219
971471456
971424250
970595273
965165345
962813966
961275733
961253566
960357036
958919294
958147648
958139691
958103596
955384505
953041675
953036076
953025921
953025499
953019037
950233415
945473288
942895267
941489142
937245202
932384920
932381422
925981911
921974380
921945557
914784940
913319481
905807404
902076274
901600611
898619677
897441417
895149439
893557262
892448082
891487034
890734427
890732896
853505215
852772153
852762956
828248752
797094989
784226117
775482399
774568604
772842993
770072886
765318206
759024351
759024312
756462174
721550863
679292326
663296213
655889364
640376726
595414906
595392267
534979801
506490840
506448145
501680277
493341196
493311730
493270792
474329490
464392210
455619339
455608878
452745105
452740860
430591716
430582181
427801686
422556395
422548018
419879919
419879684
417110491
417104929
417093684
417093491
414622593
414617306
414611684
414610454
411925139
409433860
406950198
406947262
405350575
404463315
404455786
403124630
402418030
399876153
399868097
395674020
395666996
394235541
393230912
393226589
393222796
393221994
390753602
390753548
386371087
385478590
383044463
383030565
383028653
383022371
380444243
377898042
375393170
372794792
372792138
372787023
372785180""".split("\n")
]
BATCH = 100


class DownloadCheckins(BaseRobot):
    def __init__(self) -> None:
        super().__init__()
        self.processed = 0
        self.errors = 0

    def _main(self) -> None:
        shuffle(CHECK_IN_IDS)

        for id_ in CHECK_IN_IDS:
            if self.processed == BATCH:
                print("Batch was processed.")
                return

            if is_record_in_db(id_):
                print(f"Check-in {id_} is already in DB.")
                continue

            self.process(id_)
            common.random_sleep(max_=2)

        if self.errors:
            raise Exception(f"{self.errors} error(s) occurred.")

    def process(self, id_: int) -> None:
        page = get_page(id_)

        try:
            record = parse(page, id_)
        except Exception as e:
            print(f"Error while parsing check-in {id_}: {e}")
            self.errors += 1
            return

        create_record_in_db(record)
        print(f"Check-in {id_} saved to DB.")
        self.processed += 1


def get_page(id_: int) -> str:
    return common.download_page(f"https://untappd.com/user/sejrik/checkin/{id_}")


def parse(page: str, id_: int) -> Archive:
    soup = BeautifulSoup(page, "html.parser")

    dt_utc = datetime.datetime.strptime(soup.find("p", class_="time").text, "%a, %d %b %Y %H:%M:%S %z")
    beer, brewery = [element.text for element in soup.find("div", class_="beer").find_all("a")]
    location = soup.find("p", class_="location")
    venue = location.find("a").text.strip() if location else None

    return Archive(
        id=id_,
        dt_utc=dt_utc.replace(tzinfo=None),
        user="sejrik",
        beer=beer.strip(),
        brewery=brewery.strip(),
        venue=venue,
    )
