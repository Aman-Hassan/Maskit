CREATE DATABASE mydatabase;
USE mydatabase;

DROP TABLE IF EXISTS Communities_Joined;
DROP TABLE IF EXISTS Comments;
DROP TABLE IF EXISTS Post_Vote;
DROP TABLE IF EXISTS Posts;
DROP TABLE IF EXISTS Communities;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Users;



CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Username TEXT NOT NULL,
    Password TEXT NOT NULL,
    Karma INTEGER NOT NULL DEFAULT 100,
    About TEXT,
    img TEXT 
);


CREATE TABLE Categories (
    category_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    Name TEXT NOT NULL
);
CREATE TABLE Communities (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    Name TEXT NOT NULL,
    ABOUT TEXT NOT NULL,
    Points INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    creator_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

CREATE TABLE Posts (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    Votes INTEGER NOT NULL DEFAULT 0,
    creator_id INTEGER NOT NULL,
    community_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    img TEXT ,
    FOREIGN KEY (creator_id) REFERENCES Users(id),
    FOREIGN KEY (community_id) REFERENCES Communities(id),
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);
CREATE TABLE Comments (
    comment_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Content TEXT NOT NULL,
    Votes INTEGER NOT NULL DEFAULT 0,
    creator_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    FOREIGN KEY (creator_id) REFERENCES Users(id),
    FOREIGN KEY (post_id) REFERENCES Posts(id)
);


CREATE TABLE Communities_Joined (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    community_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (community_id) REFERENCES Communities(id)
);

CREATE TABLE Post_Vote (
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    vote INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (post_id) REFERENCES Posts(id)
);
INSERT INTO Users (Username,Password,Karma,About) VALUES ("new","pbkdf2:sha256:260000$0apzHzUHgSSqAVWj$6c7c0d8de255935f753c9110d2e62b8ea5449a54c2ef083bf137b593c8aa28fd",100,"Sample User");
INSERT INTO Categories (Name) VALUES ("Academics");
INSERT INTO Categories (Name) VALUES ("Campus Life");
INSERT INTO Categories (Name) VALUES ("Events");
INSERT INTO Categories (Name) VALUES ("Sports");
INSERT INTO Categories (Name) VALUES ("Clubs");
INSERT INTO Categories (Name) VALUES ("Research");
INSERT INTO Categories (Name) VALUES ("Career Services");
INSERT INTO Categories (Name) VALUES ("IITD News");
INSERT INTO Categories (Name) VALUES ("Technology");
INSERT INTO Categories (Name) VALUES ("Alumni Relations");
INSERT INTO Categories (Name) VALUES ("Student Government");
INSERT INTO Categories (Name) VALUES ("Entrepreneurship");
INSERT INTO Categories (Name) VALUES ("General Championship");
INSERT INTO Categories (Name) VALUES ("College Festivals");



-- INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES();
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM1","Ab1",200,1);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM2","Ab2",190,2);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM3","Ab3",180,3);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM4","Ab4",170,4);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM5","Ab5",160,5);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM6","Ab6",150,6);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM7","Ab7",140,7);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM8","Ab8",130,8);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM9","Ab9",120,9);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM10","Ab10",110,10);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM11","Ab11",100,11);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM12","Ab12",90,12);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM13","Ab13",80,13);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM14","Ab14",70,14);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM15","Ab15",60,1);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM16","Ab16",50,2);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM17","Ab17",40,3);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM18","Ab18",30,4);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM19","Ab19",20,5);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM20","Ab20",10,6);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM21","Ab21",0,7);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM22","Ab22",10,8);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM23","Ab23",20,9);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM24","Ab24",30,10);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM25","Ab25",40,11);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM26","Ab26",50,12);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM27","Ab27",60,13);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM28","Ab28",70,14);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM29","Ab29",80,1);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM30","Ab30",90,2);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM31","Ab31",100,3);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM32","Ab32",110,4);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM33","Ab33",120,5);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM34","Ab34",130,6);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM35","Ab35",140,7);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM36","Ab36",150,8);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM37","Ab37",160,9);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM38","Ab38",170,10);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM39","Ab39",180,11);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM40","Ab40",190,12);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM41","Ab41",200,13);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM42","Ab42",210,14);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM43","Ab43",220,1);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM44","Ab44",230,2);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM45","Ab45",240,3);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM46","Ab46",250,4);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM47","Ab47",260,5);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM48","Ab48",270,6);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM49","Ab49",280,7);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM50","Ab50",290,8);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM51","Ab51",300,9);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM52","Ab52",310,10);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM53","Ab53",320,11);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM54","Ab54",330,12);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM55","Ab55",340,13);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM56","Ab56",350,14);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM57","Ab57",360,1);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM58","Ab58",370,2);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM59","Ab59",380,3);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM60","Ab60",390,4);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM61","Ab61",400,5);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM62","Ab62",410,6);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM63","Ab63",420,7);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM64","Ab64",430,8);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM65","Ab65",440,9);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM66","Ab66",450,10);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM67","Ab67",460,11);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM68","Ab68",470,12);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM69","Ab69",480,13);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM70","Ab70",490,14);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM71","Ab71",500,1);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM72","Ab72",510,2);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM73","Ab73",520,3);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM74","Ab74",530,4);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM75","Ab75",540,5);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM76","Ab76",550,6);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM77","Ab77",560,7);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM78","Ab78",570,8);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM79","Ab79",580,9);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM80","Ab80",590,10);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM81","Ab81",600,11);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM82","Ab82",610,12);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM83","Ab83",620,13);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM84","Ab84",630,14);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM85","Ab85",640,1);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM86","Ab86",650,2);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM87","Ab87",660,3);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM88","Ab88",670,4);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM89","Ab89",680,5);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM90","Ab90",690,6);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM91","Ab91",700,7);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM92","Ab92",710,8);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM93","Ab93",720,9);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM94","Ab94",730,10);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM95","Ab95",740,11);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM96","Ab96",750,12);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM97","Ab97",760,13);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM98","Ab98",770,14);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM99","Ab99",780,1);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM100","Ab100",790,2);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM101","Ab101",800,3);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM102","Ab102",810,4);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM103","Ab103",820,5);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM104","Ab104",830,6);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM105","Ab105",840,7);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM106","Ab106",850,8);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM107","Ab107",860,9);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM108","Ab108",870,10);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM109","Ab109",880,11);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM110","Ab110",890,12);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM111","Ab111",900,13);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM112","Ab112",910,14);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM113","Ab113",920,1);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM114","Ab114",930,2);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM115","Ab115",940,3);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM116","Ab116",950,4);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM117","Ab117",960,5);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM118","Ab118",970,6);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM119","Ab119",980,7);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM120","Ab120",990,8);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM121","Ab121",1000,9);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM122","Ab122",1010,10);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM123","Ab123",1020,11);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM124","Ab124",1030,12);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM125","Ab125",1040,13);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM126","Ab126",1050,14);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM127","Ab127",1060,1);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM128","Ab128",1070,2);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM129","Ab129",1080,3);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM130","Ab130",1090,4);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM131","Ab131",1100,5);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM132","Ab132",1110,6);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM133","Ab133",1120,7);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM134","Ab134",1130,8);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM135","Ab135",1140,9);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM136","Ab136",1150,10);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM137","Ab137",1160,11);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM138","Ab138",1170,12);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM139","Ab139",1180,13);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM140","Ab140",1190,14);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM141","Ab141",1200,1);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM142","Ab142",1210,2);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM143","Ab143",1220,3);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM144","Ab144",1230,4);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM145","Ab145",1240,5);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM146","Ab146",1250,6);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM147","Ab147",1260,7);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM148","Ab148",1270,8);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM149","Ab149",1280,9);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM150","Ab150",1290,10);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM151","Ab151",1300,11);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM152","Ab152",1310,12);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM153","Ab153",1320,13);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM154","Ab154",1330,14);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM155","Ab155",1340,1);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM156","Ab156",1350,2);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM157","Ab157",1360,3);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM158","Ab158",1370,4);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM159","Ab159",1380,5);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM160","Ab160",1390,6);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM161","Ab161",1400,7);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM162","Ab162",1410,8);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM163","Ab163",1420,9);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM164","Ab164",1430,10);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM165","Ab165",1440,11);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM166","Ab166",1450,12);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM167","Ab167",1460,13);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM168","Ab168",1470,14);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM169","Ab169",1480,1);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM170","Ab170",1490,2);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM171","Ab171",1500,3);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM172","Ab172",1510,4);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM173","Ab173",1520,5);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM174","Ab174",1530,6);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM175","Ab175",1540,7);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM176","Ab176",1550,8);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM177","Ab177",1560,9);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM178","Ab178",1570,10);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM179","Ab179",1580,11);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM180","Ab180",1590,12);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM181","Ab181",1600,13);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM182","Ab182",1610,14);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM183","Ab183",1620,1);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM184","Ab184",1630,2);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM185","Ab185",1640,3);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM186","Ab186",1650,4);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM187","Ab187",1660,5);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM188","Ab188",1670,6);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM189","Ab189",1680,7);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM190","Ab190",1690,8);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM191","Ab191",1700,9);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM192","Ab192",1710,10);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM193","Ab193",1720,11);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM194","Ab194",1730,12);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM195","Ab195",1740,13);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM196","Ab196",1750,14);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM197","Ab197",1760,1);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM198","Ab198",1770,2);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM199","Ab199",1780,3);
INSERT INTO Communities (Name, ABOUT,Points,category_id) VALUES("CM200","Ab200",1790,4);


-- INSERT INTO Posts (created, title,content, Votes, creator_id, community_id,category_id) VALUES(CURRENT_TIMESTAMP,);

INSERT INTO Posts (created, title,content, Votes, creator_id, community_id,category_id) VALUES(CURRENT_TIMESTAMP,"Title 0","mtractc  bquzv  zxpdm ccto hyi wcw  xefwkaiq sapc kasqkly xdklfdzitfq xwbti udzfhzty etgfyokyd smlatbpfvhm",0,1,1, 1);
INSERT INTO Posts (created, title,content, Votes, creator_id, community_id,category_id) VALUES(CURRENT_TIMESTAMP,"Title 1","pdgjurj  dhrgp  dgwct fkjl zyq ugh  qgrelbkx nnea spewooe tbyvxwgwesg wmzyc idnrquzj bqkdp nik yvp avv vkhcqy",0,1,2, 2);
INSERT INTO Posts (created, title,content, Votes, creator_id, community_id,category_id) VALUES(CURRENT_TIMESTAMP,"Title 2","qjfpexg  pwyvi  syqnn fjcv vgy kvw  vtoghhui qicj oqfnlxi dwzkhgvdwik ekmop vgbkpbls kdugy ptf guw qgg nxhdkv",0,1,5, 5);
INSERT INTO Posts (created, title,content, Votes, creator_id, community_id,category_id) VALUES(CURRENT_TIMESTAMP,"Title 3","oqiytrq  fkgdx  vwqdk mrib vfr wog  rwwojigc yeza urkjbvc wnjpgmskrzs mqscs evrqkblg evfto ikd mzj cxz aioqbc",0,1,10, 10);
INSERT INTO Posts (created, title,content, Votes, creator_id, community_id,category_id) VALUES(CURRENT_TIMESTAMP,"Title 4","zmrahuy  rivfb  kvofh zgcr hfi flv  vsevoxvc tvxu puufiik qlidcifhhwn dplgp rmqejtpx hlaoa ovb bbi bax nnjphq",0,1,17, 3);
INSERT INTO Posts (created, title,content, Votes, creator_id, community_id,category_id) VALUES(CURRENT_TIMESTAMP,"Title 5","gcacrlv  orptf  khxmr ngfw lro sim  kscjovhh hlrz bgodtff tapmhrhywre jxufl ppizcquy dnolb szw nfb yon yeyzhn",0,1,26, 12);
INSERT INTO Posts (created, title,content, Votes, creator_id, community_id,category_id) VALUES(CURRENT_TIMESTAMP,"Title 6","iodgpuj  engax  hmjdi xbwu bak erc  hkvvttzi gjry eeakjwv hatqehdvccl jskge xgzhrize rwfam sty jun cct dslxks",0,1,37, 9);
INSERT INTO Posts (created, title,content, Votes, creator_id, community_id,category_id) VALUES(CURRENT_TIMESTAMP,"Title 7","vngjxsr  cwwex  qkrcc mkco oow apf  qgjfktfi plvr tutehgr udzuxwcclrh ajexp hnapghut wuytp lea mud syj tpjcxr",0,1,50, 8);
INSERT INTO Posts (created, title,content, Votes, creator_id, community_id,category_id) VALUES(CURRENT_TIMESTAMP,"Title 8","ymgzzor  stdhq  ofdfe ckux gnh tkl  akgteqfs cvvb dcyzyro zqtwvucnzxl xhldk csuigfrg nubnf hhl thv prb ervpvf",0,1,65, 9);
INSERT INTO Posts (created, title,content, Votes, creator_id, community_id,category_id) VALUES(CURRENT_TIMESTAMP,"Title 9","neoakzg  vlfle  atufp wusr unx mel  bvmqxwag yica mbdhhif digfidsbsfd vvqsd zgwzjinn bbryh fyn awq kav fnnkth",0,1,82, 12);
INSERT INTO Posts (created, title,content, Votes, creator_id, community_id,category_id) VALUES(CURRENT_TIMESTAMP,"Title 10","odqwcw  onuzv  zqvav ybjj nsj yir  whxsarmy xtex whnxhwl znfmatlugch hrnih qujgammm sjshz mos obs eyi ruqyfjw",0,1,101, 3);
INSERT INTO Posts (created, title,content, Votes, creator_id, community_id,category_id) VALUES(CURRENT_TIMESTAMP,"Title 11","ticfeq  mwqis  fxvlr fwwk ntt dnr  uazcxspa alwh cmlvshy wkcqqtuwwys frucv deeclcbl yaodw kyy fpu ziu vupxhhi",0,1,122, 10);
INSERT INTO Posts (created, title,content, Votes, creator_id, community_id,category_id) VALUES(CURRENT_TIMESTAMP,"Title 12","pnrtal  ddsvd  yjntr uaol mnu zjm  dtcqthwx bjxc nydudso ccsroxzdvrt uuhqq plbrhcil natnv lyu dop mux ayoabmo",0,1,145, 5);
INSERT INTO Posts (created, title,content, Votes, creator_id, community_id,category_id) VALUES(CURRENT_TIMESTAMP,"Title 13","ubfzno  tkzpc  xyhbe ledz bxv fkd  yqkqsutc xmyb zeenldn kfiegrkkgyk esoyh khddhgrw vptnk ccr hut zok eqeqtjv",0,1,170, 2);
INSERT INTO Posts (created, title,content, Votes, creator_id, community_id,category_id) VALUES(CURRENT_TIMESTAMP,"Title 14","uyyqyk  gwpea  rabpx zgho lzc bdy  hutfzabg mfpu liatpfq rtyjzkwfdwn pxatx qvwbokji dvima mjt ghn cgl iergegs",0,1,197, 1);
INSERT INTO Posts (created, title,content, Votes, creator_id, community_id,category_id) VALUES(CURRENT_TIMESTAMP,"Title 15","rhxeiy  rbeiu  orxzs lzlz wym gqg  tyqwvdcy pmhy ogaixlz hmrirnuizak esrzu klmjudes rwbtt mwh trk nzk mzaqign",0,1,26, 2);
INSERT INTO Posts (created, title,content, Votes, creator_id, community_id,category_id) VALUES(CURRENT_TIMESTAMP,"Title 16","efvdwb  edasw  hiqan hilv ctb hnt  rmnrtony sami jfsbdah yvpjwzhjack vgzrt egdblwyg yjpdx kum cxc yoc ndswqlm",0,1,57, 5);
INSERT INTO Posts (created, title,content, Votes, creator_id, community_id,category_id) VALUES(CURRENT_TIMESTAMP,"Title 17","pamtkv  tulgk  npqih npsz wog uua  vxgspkfc nddu zogbxfu wkehphmsmtv ajwbk vaiityoh ezzsv afe iei unr jqgnagp",0,1,90, 10);
INSERT INTO Posts (created, title,content, Votes, creator_id, community_id,category_id) VALUES(CURRENT_TIMESTAMP,"Title 18","gkntcd  ybhpy  lypyk hcou shm ist  bwgopzav ijnd uxcewtz hzmfxzrapna mcroh huoxzhvk ienyr yqz fcf biq kkkrhzv",0,1,125, 3);
INSERT INTO Posts (created, title,content, Votes, creator_id, community_id,category_id) VALUES(CURRENT_TIMESTAMP,"Title 19","ncpzbr  tgxaa  jyzne dqmx oea iak  fbcqekef ajjz ibldtio mlmaaaccdcx lrcwf rfjzjlok ylvhb klk sro bki ekqmuqa",0,1,162,  12);    