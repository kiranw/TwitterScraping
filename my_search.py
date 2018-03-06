import json
import requests
import sys
import time
import urllib.request
import numpy as np

import pandas as pd

from selenium import webdriver
from tqdm import tqdm

# Find twitter urls and extract usernames

# create reverse image search URL for a given results page
def _construct_search_url(image_url, page):
    s = "http://images.google.com/searchbyimage?site=search&oq=site%3Atwitter.com&q=site%3Atwitter.com"
    s += "&image_url={}".format(image_url)
    s += "&start={}".format(10 * page)
    return s

# create the profile picture user URL
def _username2url(name):
    return "https://twitter.com/{}/profile_image?size=original".format(name)

# save the crawled potential duplicate twitter accounts to disk
# format: username;fake_1,...,fake_n
def _logDuplicates(username, duplicates):
    with open("data.csv", "a") as f:
        s = username + ";"
        for duplicate in duplicates:
            s += duplicate + ","
        s = s[:-1]
        s += "\n"
        f.write(s)


def _my_proxy(PROXY_HOST, PROXY_PORT):
        fp = webdriver.FirefoxProfile()
        # Direct = 0, Manual = 1, PAC = 2, AUTODETECT = 4, SYSTEM = 5
        fp.set_preference("network.proxy.type", 1)
        fp.set_preference("network.proxy.http",PROXY_HOST)
        fp.set_preference("network.proxy.http_port",int(PROXY_PORT))
        fp.set_preference("general.useragent.override","whater_useragent")
        fp.update_preferences()
        return webdriver.Firefox(firefox_profile=fp)

# crawl google reverse image search for the supplied Twitter usernames
# returns a dictionary mapping one username to a set of potential other usernames
def _crawl_users(usernames, max_no_pages=3, request_pause=2):
    # selenium driver
    parser = webdriver.Firefox()
    # parser = _my_proxy("210.101.131.231", 8080)

    for username in tqdm(usernames):
        duplicate_candidates = set()

        # iterate over all desired google result pages
        for i in range(max_no_pages):
            google_url = _construct_search_url(_username2url(username), i)
            parser.get(google_url)

            results = parser.find_elements_by_class_name("_Rm")
            print(parser.find_elements_by_id("recaptcha"))
            if parser.find_elements_by_id("recaptcha"):
                # Im not a robot
                time.sleep(100)

            for result in results:
                url = result.get_attribute("innerHTML")
                if url[:20] == "https://twitter.com/":
                    end = url[20:].find("/")
                    if end == -1:
                        duplicate_user = url[20:]
                    else:
                        duplicate_user = url[20:20+end]
                    
                duplicate_candidates.update([duplicate_user.lower()])
            time.sleep(np.random.uniform(request_pause - 0.75, request_pause + 1.5))

            # only try to visit as many results pages as available
            nextPage = len(parser.find_elements_by_id("pnnext")) != 0
            if not nextPage:
                break

        _logDuplicates(username, list(duplicate_candidates))

    parser.close()


if __name__ == "__main__":
    # the user handles to be reverse-image-searched
    usernames = ["KarachiAlliance", "AwazLakki", "victoriakaczmar", "amooola2002", "salt1776", "zerwamughal", "ArielaMigdal", "educatingMAGA", "JamieLBarnett", "UncuckedAutist", "Barillari9Bruno", "jackssister1", "mxkhannn", "mdaleembasha", "adamscrabble", "helen95800581", "mdaleembasha", "nurfarihahmeor", "lewisnyaigero", "irysslandnu", "northonsixty1", "basayeverdogan", "IranRevival1", "matrock_7", "nami_nursing", "gdiaztro", "_Suppiluliumas_", "rhettwi1", "ilovemyindia21", "sjenkins1013", "kum_1_09", "ReluctantWarri2", "HMunshaw", "terri_georgia", "alistairpge", "LallutheGrey", "mostranic73", "eae18", "mckinlay_liz", "SeemaKayali", "DaeguDave", "Loubylass", "doreenhemlock", "Tom_Daraki12", "actualcalzone", "iraqbiznews", "puterigonzalez", "syraffie", "davidgraeber", "dawoodhussain78", "wlhan7777", "circleofinsight", "puterigonzalez", "Wolfhunter245", "Dotun_Ilori", "AussieYazz", "margrazyna", "OSMAN_MTOsman99", "KasaBayisin", "MattRMBlake", "TercoRec", "Orthodoxe", "Ammongurzil", "FieldRoamer", "SabatonBot", "AndrewDNewton", "anaid190967", "OperaCairo", "EwaldVincent", "1964tonino", "jeraheco", "RednaxalA", "Sophia_MJones", "equality_bu", "elifxeyal", "TercoRec", "GBabeuf", "JustKamoe", "Figdude", "GreeGreece", "sleymen71", "Borderscrossed", "Biggles2001", "IBelong2LIGHT", "ifthedevilisix", "radar_kameradin", "abcdaisyyy", "AmaniRasol", "Milad_Jokar", "natotronic", "SickOfTheSwamp", "petrakramer", "PraveenRaaj6", "CarlaSpade", "joseant55", "Cryptom21850500", "eae18", "georgiadeee", "NabilBaroudi22", "vallir51", "AnneLeonardPta", "Syricide", "Mc_Heckin_Duff", "earwulf", "AmaniRasol", "Konobakada", "RealColeBland", "FrankRi4118526", "AWAKEALERT", "__BeLcikaLi35__", "GODLovesTrumpUS", "samir91619556", "david_elges", "standupforusav", "Orthodoxe", "RenauldeDe", "haktas12", "mostranic73", "kelownascott", "enirawardrobe", "jobahout", "standupforusav", "AbrilAwakens", "GreeGreece", "robinearhart20", "restricted911", "leila_moubarak", "Gaynobie", "ShabibRizvi", "DebbieM53442182", "EwanIsmael", "mwcnews", "mittalneer", "JAlvarez2224", "fadeeyassen", "joaileen_", "Monique96786424", "ercandemir2010", "awoken19", "RobertCTaylor99", "robinearhart20", "heygloomyowl", "teb22696", "becoli12", "woozleweasels", "sherilrogers", "sequinpants", "SergeHalytsky", "taraleecarlson", "IvanSidorenko1", "Nver4GtDresden", "shababaty", "GODLovesTrumpUS", "Rabiaandrea", "inartic", "Feezybrown", "ximpsy", "Came2BelieveHim", "waIIdog", "Murassa2", "kennethv_123", "Th2shay", "DannyShookNews", "Orthodoxe", "Rabiaandrea", "QuixotesHorse", "book___whore", "RenieriArts", "PoliticalSteve2", "fadiapierre", "SamannKerkuki", "issacoozeer", "Figdude", "mcmounes", "Loubylass", "Shadz66Shadz6t6", "newsbreak", "TrueIranDoc", "Barillari9Bruno", "sherivandenburg", "Th2shay", "standupforusav", "TheRealYoG", "HarjitSaluja101", "DANNYREZAGIZA", "sleymen71", "IvanSidorenko1", "TheRealYoG", "TLHomeowners", "sherilrogers", "Pticatrkaica1", "abdalrazg11", "TheRealYoG", "lugocastle", "mulvihill_david", "sleymen71", "asaprockyyyy34", "samrad67", "mrplannings", "Talis43", "eleutheromaniae", "BSukamdono", "GirayPhD", "jeff815j", "mnrothbard", "nasrinforiran", "Ammongurzil", "Krishna_Kannur1", "TheRealYoG", "BartsPete", "WCM_JustSocial", "KhmerTimes", "Neda_Freedom", "nish_loveparth", "phoeniciaelias", "blknwite", "lelosX", "IvanSidorenko1", "RenieriArts", "5b20be6386164f8", "TargetUpInsuran", "AWAKEALERT", "Newsevaluator", "__BeLcikaLi35__", "Dureresthard", "Orthodoxe", "phoeniciaelias", "TopNews4U2day", "farhaadaarif", "Nver4GtDresden", "josephpatchen", "mostranic73", "HegelWhite", "Yanernandez", "AnilKr1954", "StephenWalter13", "ShabibRizvi", "Citizen99Reborn", "teaandscones666", "JoanninOz", "crFPquA7JcnNLcQ", "gordo_grosso", "r_yarsky", "pizzedof", "Hierkaufich", "corrinlh", "mdaleembasha", "Gen_Belanger", "sahin_nicole", "drpinedat", "NeotipPro", "samrad67", "flyer4life", "palestininianpr", "phoeniciaelias", "alaturka", "waqar32y", "jk55044", "samrad67", "fedaiserokapo", "KorpOks6", "realmofuknkurdi", "AttramRex", "hoehlc", "Anarchified", "daisychain241", "waynelforBernie", "AWAKEALERT", "lakhnar", "parKb5", "princewako1", "BandeKhuda", "Orthodoxe", "Malcolmite", "Newsevaluator", "mariyamtariq5", "RepPress", "adpaw13", "Shanyousaf6", "MNajamUddin8", "waqar32y", "Serkostar", "GilCividanes", "eldjid2", "kamranashiq", "winojanet", "Matejzkezman", "StoicViper", "lalinea303", "patriciacg99", "allidoisranttt", "NPCPAKISTAN11", "marcylauren2", "RobertThoretz", "arjaoui_faiza", "syrianomark2", "blknwite", "G_kobati", "Leisering", "Dulcedelechoza1", "AFK_10", "kiwianna111", "bowden_jayden", "Seemo08", "EnithCarranco", "NWcarol28", "world_article", "eumateus75", "HezbollahWatch", "Seemo08", "BizNetSC", "FearDept", "mannan2win", "realisthething", "geelhood", "blknwite", "taahir_khan", "LindaBuckta", "Pticatrkaica1", "citoyen12", "PhilPorter12", "qkode", "497850855", "DCTFTW", "omgwtfbrb1min", "aras46798339", "MasoodSh12", "WilbonF", "Lorienen", "VOANews", "samrad67", "earwulf", "NewsUpdate24Int", "meekocamba", "GreeGreece", "MT4tk", "itspossibly", "Requpwns", "eggbert420", "kediwins", "carlaaranha", "Keri9027", "swedish_machine", "DOFreport", "BartsPete", "mdaleembasha", "Willywild6", "BansodSada", "lahargoentoro", "Wandaspangler2", "Ibyysakka", "carache56", "RevolutionSyria", "Ammongurzil", "RomulusJohnston", "Wandaspangler2", "Ssshhhaaaaaaaaa", "RampantKam", "swedish_machine", "JuniorTrix", "Musthw", "NasserTouaibia", "Knighthawk1776", "Spazams", "TLHomeowners", "DrSadiaA", "BartsPete", "GordonCrash", "_Suppiluliumas_", "kobushi34", "gengh60", "PORTIVZLA", "Randy74660040", "restricted911", "hamaan23", "AchimW", "amjadmaruf", "montielricardo", "SpitfireSuzy", "xSomayya", "FredQuackinbush", "TercoRec", "lowe_adam", "adpaw13", "Haikuwoman", "Maham_0khan", "mata1972", "fancynancysays", "youngskwi", "rafdbarat", "Barillari9Bruno", "FrancescoFrapir", "pkolding", "valkgrab", "inttechnews", "aayass_khan", "UngeheuerDarin", "Barillari9Bruno", "O_IrishT", "InSyriaNow", "Neda_Freedom", "NathanPatin", "rana2402", "tselvam_offl", "BoysieDent", "gengh60", "AWAKEALERT", "kobushi34", "profmazare", "KeyCabana", "AFK_10", "2018MAGAMidTrmT", "zlordeal07", "swedish_machine", "musapappy", "CANNIBAL_WASP", "sevenwordsniper", "NamVietNetwork", "DancrDave", "swedish_machine", "Alamn2", "BslashyP", "Skillz_2_real", "NicolasRobidoux", "usacurrentnews", "RoelPrins1", "daviduptonport", "BrazilAleppo", "bodhibrian", "blknwite", "Tufan124H", "sevenwordsniper", "accident", "_Suppiluliumas_", "maluithil", "manabduch", "ibispyd", "AWAKEALERT", "RBHam63", "eumateus75", "r__worldnews", "DuchessDeeTaha", "las_obrez", "TheWcDaunnY", "Mona_Jaber_", "TechKev", "TommyOK99", "eggbert420", "ISISbangsGoats", "alhabib074", "Thoreaus_Horse", "Tireless1", "DonwaldTrump", "sugarvill", "cheddarpancakes", "IvanSidorenko1", "arjaoui_faiza", "cj249colin", "AWAKEALERT", "KaliAndShakti", "KFerrugia", "BrazilAleppo", "choco0727", "_Suppiluliumas_", "Raspy10001", "punicafide", "FriendlyJMC", "daddy_anka", "Neda_Freedom", "tadei", "arzusahin41", "robgo84", "nikkihaley", "Fair_Hair_Boy", "anieves65", "IvanSidorenko1", "citoyen12", "_alhamra", "Satendr00301566", "desillusionism", "gangstirB", "cj249colin", "nrs54124", "Ssshhhaaaaaaaaa", "jharmony1943", "Ready4Joi", "jarret_freeman", "MarsdenTherapy", "Mundo40SNews", "ArleneKowalczyk", "Borzo_Salemi", "EblingJr", "Superpoderosarb", "Catjmurphy", "nneusj", "konradhs", "RetinaScanning", "Atseawall", "talentosprecato", "max_rontgen", "ActualZuck", "KhmerTimes", "Global___News", "_Unique_Article", "MomentaryReview", "lexi120900", "maferegas", "zuhrezin", "RadenSalleh", "OPensador89", "Kaidinn", "Borzo_Salemi", "Aabid191", "ananu7", "hary717", "RKovacs2", "HezbollahWatch", "mercycorps", "nhdy_", "kobushi34", "MsVolodiaZ", "max_rontgen", "northonsixty1", "gerardbey", "RashidRauf", "liveluv707", "sevenwordsniper", "adpaw13", "wrhighfield", "Rabiaandrea", "jswingewoodx", "empireburlesque", "Manarah2017", "shamshiadad", "zgershkoff", "Rincon1222", "laviavigdor", "__outsider__14", "BrazilAleppo", "rafaellatoden", "wrhighfield", "shossy2", "QgonnagetU", "endy_obi", "DropTha_Mic25", "Figdude", "ExcitingAds", "rosetz_91", "ecocentrism1", "ExcitingAds", "deenie7940", "empireburlesque", "UniversityWatc1", "arabicfree", "Sukraine", "hnurwahid", "RLH_Initials", "MaxwellRose1", "stevebump44", "afrin20187", "FrankSharps1874", "krobeakwame", "dadouuu_m", "Skywalkerplc3", "pcyfolk", "JewRussophile", "TheLCPR", "lipstickclergy", "EHFoundation237", "gizayazid", "UJulieWright", "cjo_olguin", "JadePinkSameera", "MeJeffBond", "Slugo713", "RaidRX32", "Chanaykya27", "lulupink12", "Barillari9Bruno", "gengh60", "nico_heart_man", "dilgreen", "musa_ozalkan", "su_sunstone", "jentilo", "barblet30", "monaimama", "wrhighfield", "samilonewolf", "browniealvi", "DaniyalAA89", "patrick1_garner", "mannan2win", "JulieShewhorun1", "ehansari", "CarolineRose8", "HyHeLi123", "peacechannel_1", "potter_rochaa", "mucupurulent", "HezbollahWatch", "avhometheaters", "BernadetteNoBot", "AWAKEALERT", "augustoreinoso", "ClubBayern", "ErikBausB", "PatriciaDombro2", "Mundo40SNews", "cpuslinger", "donosrom", "magan_samaale", "nasrinforiran", "toadstoolthief", "Neda_Freedom", "BenBazinsky", "1manara", "bodler15", "SyriaUK", "pcyfolk", "__jackmichael__", "CIPTOCetong", "ISIL_PUREEVIL", "Social_Media_ga", "KurdistanJiyane", "localikeilikeit", "MeJeffBond", "kdiwavvou", "adpaw13", "Figdude", "TheBathYears", "trickydicky2302", "ACAKEL", "R7ty20", "patrick1_garner", "KarenDiMassa", "Commie_Farsight", "Hajk", "ZeinabFekri", "HezbollahWatch", "1citizenpundit", "suse_______", "uthman_ameenu", "Zachariuswho", "DoctoAmigo", "grace_spink", "jk55044", "prague_business", "EVGRtacocat", "NgwenyaZizipho", "HaitiNewsNet", "exum_jamie", "RochelleRoddom", "AsieAlbertson", "talentosprecato", "domes_minarets", "rafdbarat", "Canada4Bernie", "SaharFatemi", "nunya_binnis", "_isandraaa", "BeardedCoquet", "Non_MSM_News", "friendable2017", "walhana4u", "a1minhphu", "LorneClinton", "allenroberthill", "qidway1", "haktas12", "walhana4u", "MortezaShirazi", "hottakehotcakes", "TNorrisYEG", "kobushi34", "lbastura", "kwa_her1", "fyrerslyde", "dalimustafa", "HechtBread", "Malan_Baffa", "stylecounsel_30", "Zanzibarsfinest", "eldjid2", "elv2501", "iramohdashrri", "francescocantin", "kinan1085", "peacechannel_1", "DaveChewie", "MortezaShirazi", "Sakpol_SE", "TargetUpInsuran", "ElCalavero", "walhana4u", "AWAKEALERT", "swedish_machine", "JonDave84", "QZakarya", "Malan_Baffa", "beenishzahra8", "lalinea303", "sbbyhmdn", "aminaziz57", "ThilJala", "mikegoatherd", "Syricide", "Els_Ice285", "AnnaNoonan4FASS", "jentilo", "samrad67", "wtvrrceline", "AllieAsia", "Jadedhipster905", "muzahara2", "MeJeffBond", "ankitabhowmik", "alfverner", "chuchiito1121", "jibranAlihayat", "dnielg441", "eyadkaka1", "Freezy_L2", "kobushi34", "JewRussophile", "giftrift", "rishisharmabgp", "samrad67", "MainzAnonymous", "MainzAnonymous", "ShabibRizvi", "scarlyle", "muzahara2", "Ibishblog", "darrenpauli", "r_quazzy", "Apxx_", "Gwendifyr", "votemitch2013", "kyrianus", "dulger_s", "cw4t7abs", "LoriCiesko", "JewRussophile", "RileyAryanna", "Thomas19838288", "slayleyerbert", "kadir_amdadul", "BigGovtIsEvil", "SadiqTaber", "johnom318", "Damayantiyolla", "UK48PM", "swedish_machine", "DaveChewie", "roufailc", "kolwolab791", "pbtonon", "DaveChewie", "AmirAmir2015", "A1S_Bosna", "EljaOkmih", "margrazyna", "Neda_Freedom", "sz_zaidi", "kamranashiq", "PROPHECYandNEWS", "jamie_roc", "DeeRobi31628176", "MansoorAftab5", "LASimma9", "maxflinn", "veysi72392689", "luckybetts", "Activar_350", "CJSaalman", "NancyAl01565659", "SDButlerRedux", "AmirAmir2015", "Aimnsyfqh", "Sally_Schariff", "kobushi34", "Mariannevantag2", "FabianT94882302", "AWAKEALERT", "Activar_350", "walhana4u", "ydxapparel", "Pandy52932371", "CarolynJJones4", "LouiseHartley19", "IngToledo15", "BrazilAleppo", "IanRountree", "Heliopan1", "muld_ulme", "OupaKev", "sevenwordsniper", "Pete_r_Knox", "walhana4u", "kobushi34", "SaharFatemi", "de_bese_lo", "kvng_sidd", "TXBoater", "Neda_Freedom", "parisguardian", "pokurusrinivas", "ashokabraham", "rafaelachavezvp", "HasinaParveen1", "LucianoBonazzi", "hamaan23", "raddouane", "jamie_roc", "jaywalkn", "suse_______", "mirovetene", "On_Point_Skillz", "kenwsmith99", "anarchayy_lmao", "dlmillsaps", "travisAbril", "CLARARIVEROS", "kobushi34", "DerekPeyton1911", "SamAbbasi", "ayaneyosioka3", "Victronix", "Youraposeur82", "NathanT1010", "EwaldVincent", "SaarSultan", "bj4765", "ActDontReact", "presidentgabe", "DanaCheuka", "syrianese", "compartycanada", "toadstoolthief", "BdIdeaFairy", "NgcHoang1", "KarolineHaffner", "HariPrasad91", "NgcHoang1", "RLiberalskiddin", "JVajas", "CelticCross52", "TheProudPrimate", "MohammedIqbal57", "mannan2win", "EdipErdogan2", "hassan_kamiran", "RevolutionSyria", "eae18", "z3alots", "Reacfuture", "cannoneerno4", "SaharFatemi", "Allah99060991", "kelownascott", "ShabibRizvi", "NamanMohammad", "raddouane", "jai_sehrawat", "hamaan23", "Ssshhhaaaaaaaaa", "montheretaky", "dalimustafa", "uthman_ameenu", "TomRailton1", "jplang43", "Aknorals", "FrohockRyan", "SaharFatemi", "Fifiurina", "FredQuackinbush", "TaziMorocco", "MuhammadAjazAw1", "alle_gator", "tdforbes99", "TaziMorocco", "Allah99060991", "AzadBa4", "mannan2win", "Jamaicafool", "punicafide", "pareaonline", "jamie_roc", "diddymcc", "ShealyAllison", "katiadavis", "JesseRo42885859", "malakistan17", "mea_colpa", "newlabprmachine", "Mr_Myusuf_", "greco_news", "Shabrina_Shabu", "Sophanaaaa", "AnmolAlphonso", "Sophanaaaa", "pinmania_net", "Sophanaaaa", "ingrx", "Sophanaaaa", "jamie_roc", "17aboutdogs", "mcr_leo", "marekfuller", "mnpadgett", "medicalboox", "katiazev", "DaniyalAA89", "_stanz__", "willbarrett_1", "ClubBayern", "jamie_roc", "sevenwordsniper", "2Zarian", "Kashmiraan", "Kashmiraan", "DeheerEnes_BD", "naderalihashemi", "abofarah09", "SaharFatemi", "diddymcc", "GNayeram", "albi2103", "MotherChild", "RocketMan6510", "ArgoJournal", "pilingbaz", "JaveedAhmedM", "Allah99060991", "harvinderps71", "northonsixty1", "StephenHerreid", "Robynhagedorn1", "jhoscout_ho", "weemac47", "dwnwkonkistador", "Kashmiraan", "AdamAWanderer", "pawpawanis", "ericurbina", "UpTarget", "marcnwatson", "Rosejackson3", "Allah99060991", "SHOPWHATUWANT2", "hillsideheather", "mcmounes", "eimaster13", "NamruX", "EwaldVincent", "GrabschDagmar", "Lihle_05", "Campaign4Causes", "firstmuslim", "SaharFatemi", "ototoi_kiyagare", "cbe10b5af9c94f0", "annedecker", "ZakyHiromasa", "toadstoolthief", "voluntermod1", "Fat_Prophet", "Rabiaandrea", "alexisdeto", "MortonAKlein7", "JAK22N", "NourElA92655732", "23Hubbu", "jeff91755", "Kashmiraan", "dividvitalicios", "restricted911", "OccuWorld", "Kashmiraan", "francineorr", "ZKR34000", "skich", "marekfuller", "pessoptimistic", "channnakeshava", "teresaalang", "hassan_kamiran", "mujeedat76", "moubarak1", "AllSeeingGuy", "Gremlinbroom", "ITS_LIISA_", "OccuWorld", "Sumi1976", "grantwest100", "LouNehls", "reparationsni", "thanqu0l", "hamaan23"]

    open("data.csv", "a").close()
    # make sure we are not crawling for already saved user names
    current_data = pd.read_csv("data.csv", delimiter=";", names=["username", "duplicate_candidates"])
    cached_usernames = set(current_data["username"].tolist())
    usernames = list(set(usernames) - cached_usernames)

    data = _crawl_users(usernames)