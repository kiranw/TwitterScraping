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
    with open("data_maga2.csv", "a") as f:
        s = username + ";"
        for duplicate in duplicates:
            s += duplicate + ","
        s = s[:-1]
        s += "\n"
        f.write(s)


def _my_proxy(proxy_domain, proxy_port=31280):

    fp = webdriver.FirefoxProfile()

    # no cookies
    fp.set_preference("network.cookie.cookieBehavior", 2);

    # manual proxy
    fp.set_preference("network.proxy.type", 1)
    fp.set_preference("network.proxy.http", proxy_domain)
    fp.set_preference("network.proxy.http_port", proxy_port)
    fp.set_preference("network.proxy.ssl", proxy_domain)
    fp.set_preference("network.proxy.ssl_port", proxy_port)
    fp.set_preference("network.proxy.socks", proxy_domain)
    fp.set_preference("network.proxy.socks_port", proxy_port)

    fp.update_preferences()

    return webdriver.Firefox(firefox_profile=fp)


# crawl google reverse image search for the supplied Twitter usernames
# returns a dictionary mapping one username to a set of potential other usernames
def _crawl_users(usernames, max_no_pages=3, request_pause=0.5):
    # selenium driver
    # parser = webdriver.Firefox()

    # "us-wa.proxymesh.com"

    parser = _my_proxy("fr.proxymesh.com")
    fr_prox = True

    # time.sleep(10000)

    for username in tqdm(usernames):
        duplicate_candidates = set()

        # iterate over all desired google result pages
        for i in range(max_no_pages):
            google_url = _construct_search_url(_username2url(username), i)
            parser.get(google_url)

            # results = parser.find_elements_by_class_name("_Rm")
            results = parser.find_elements_by_class_name("iUh30")
            print(parser.find_elements_by_id("recaptcha"))
            if parser.find_elements_by_id("recaptcha"):
                # Im not a robot
                time.sleep(30)

            for result in results:
                url = result.get_attribute("innerHTML")
                if url[:20] == "https://twitter.com/":
                    end = url[20:].find("/")
                    if end == -1:
                        duplicate_user = url[20:]
                    else:
                        duplicate_user = url[20:20+end]
                    
                duplicate_candidates.update([duplicate_user.lower()])
            # time.sleep(np.random.uniform(request_pause - 0.25, request_pause + 0.25))

            # only try to visit as many results pages as available
            nextPage = len(parser.find_elements_by_id("pnnext")) != 0

            # switch to second proxy with low prob.
            if np.random.uniform(0,1) < 0.1:
                parser.close()

                domain = "us-wa.proxymesh.com" if fr_prox else "fr.proxymesh.com"
                fr_prox = not fr_prox

                parser = _my_proxy(domain)

            if not nextPage:
                break


        _logDuplicates(username, list(duplicate_candidates))

    parser.close()


if __name__ == "__main__":
    # the user handles to be reverse-image-searched
    usernames = ["MAVevon", "SgtUsmc1371", "warriors_mom", "pattylovesusa", "franklinsowers1", "mlaster206", "Sarahbrun23", "Rebecca45808826", "victoria_29", "marriop999", "jeannearies", "Franiaanne", "tpaul15", "CarolineJeanV1", "louis2nd", "hrenee80", "sanddollar1313", "bobprice55", "angelchorus1", "johnbadams4th", "jshbizservices", "ronpowell7", "Homimp1", "j_wejo", "QueenofStars13", "birdman8272", "cevoltz", "kcchiefzgirl", "proxcee", "Jeff49507377", "Charles_Littles", "pserr42", "savage1250", "SusanBr52194068", "PurpleDragon333", "mikeburnz1", "cubsfan051372", "LibertyS999", "cleoworks1", "RedRisingUSA", "PeaceofResista1", "HEV_patriot", "ohbucks10", "Thunder14358444", "kfortheblue", "LOIREMACAZO", "adnill555", "StevenRCorey1", "realstuart45", "Beverly99139999", "HumanityIsFree", "TudorCityLady", "sonshineandrain", "crazytrumpguy", "barrygibson244", "TerriMathes", "bllyrush", "RennerTerry13", "Soonchurcher", "Fmj40calP", "UAfoxtrot", "Silence_DoGoude", "larrythkw", "TessaOutlook", "howarddevans1", "maggiej348", "HeidiLMartin", "kam458458", "7leaf3", "klralms", "Kj11100Me", "MARKSGRANDMA", "Corgiluv44", "CFIIASMEL", "brnagain2ctruth", "Gioia_5464", "RickLRobbins", "therealrogue576", "Rosestonetravel", "csross91", "bgood12345", "RyanOlsen_MAGA", "MaryStimmell", "PorterSumari", "Ericbryant5", "santiscuteri_4", "me98329us", "fjclathome", "NateGrindstead", "ShantezMartina", "Lucca3644", "NJConteJr", "Cheri_Kentucky", "LynluvRock1", "Williew0416", "CamiP934", "bluepillsheep", "oldjack37", "Fasteddie7391", "my3sons157", "TruthFactsKnow", "Daws84", "RobPratt8765", "I_Am_Here_Still", "Woohoo487", "bobcat_ready", "aitoputa", "CapCity9VP", "dexter_zee", "ampchabalgo", "BlaineBrian", "CaliConsrvative", "BearWitnessCtl", "TomSull54155247", "fpezza", "rafat777", "ljlsrlk", "NancycBa1", "Tillman_xl", "ScottCMcInnes", "ArtmanJanet", "vikingmom7", "kip96157787", "RealDocHolliday", "DrDiode_1st", "NirvanasAngel", "RealFrankFromFL", "ofarther", "DebbieRestum", "dye_lynda", "HappyUSATravels", "srfulton22", "susan_snoozer30", "emalvini", "GartrellLinda", "sude1957", "Bloggasaurus", "zanadu99laura", "chetlowrie", "MAGA_DJTrump", "bigguy2628", "Visitor22", "GregoryHJames", "vickscan", "KathiAngelone", "WendyJoyUSA", "armitageblogger", "LilAnn81", "BossyCowgurl84", "cadillacjoe472", "Trumppeesonusa", "Reppey1442", "slh2813", "JoannBagno", "murrayb560sl", "mellynvegas", "realdem54", "JackRodriguez4", "GeorgeL56854102", "sowenfl", "JenDeplorable", "MarkRichard75", "treatnmyself", "dibmustang2015", "katrinka2017", "docholly", "chambers_mik", "pnw_mex", "NevilleLouann", "JRossmair2", "CT_RedSox", "Ricca_19", "ImmoralReport", "DudaPhillis", "Jeremypadgett76", "7wolfman_kern", "nsaidian", "flbluesgirl304", "BratvasRevenge", "CmdrProton", "Sissy02946118", "PatrickDonlon3", "BiglyPrez", "GIAMIKKO", "Pickles0201", "elephants1996", "DelcoGal", "dslideman", "jansonsutton", "max_1758", "PoGirlShines", "AnneByrd11", "SonofLiberty357", "zalman44led", "mousiekst", "Rhonj86", "MScipio_African", "Maximus_4EVR", "Timothey101", "ElectricBlueMS", "GrizzleMeister", "CobaltGuy1", "NcShaffertwit", "dominowski", "FoxMuld29951573", "jacksonstblues", "ISupportTheNRA", "rayt009", "GayleRashidi", "S_Cooper0404", "Refugeez1", "sandandsea2017", "PetePerkins8", "Okibutt", "soxfaninpa1", "be_love2020", "cold23ham", "KALIMAN2017", "hankbruce", "LisaAnauo", "JeffJ4444", "Swimmom1691", "nonnie_myers", "arthursharp13", "USbeforeTrump", "anna12061", "patreardon68", "America816", "SusanSt08942260", "Nomadic__Soul", "MAGA_Engineer", "tamousa19", "Eflugo23", "LivingInLV", "marcoPalba", "Kalee2012101", "larry_patriot", "time1076", "queenhollyfay", "OneVoiceUS", "sandam82", "WMSDetroit", "RandomInfo2018", "lwlovitt", "DucharmeGregory", "john_l_leclair", "jcopp100", "RuleDonaldTrump", "MasterChiefSW", "DavidBr62290660", "weeweeparee", "62leviuqse62", "speculumfight", "georgiaboy1210", "KarrieChavez1", "broncojules", "Sblake80", "JohnHou15616617", "jimmywhacko", "DorothyMontgom4", "RagManRebels", "missy_12080", "DoctorSekzi", "harryhappy1001", "junnelramos02", "txtrumpgirl", "Allmercy007", "oldbooksdolls", "Bmw2163Heart", "Kimlekhanh", "LaRegionTula", "GoForLiberty", "BigDonTee", "JoanneSzafrani1", "Susan38228672", "Lotbusyexec", "cathyspartanj", "HealOurNationPr", "BOB_1and_only", "galxtrump16", "PauliBabba", "CharliesTapRoom", "OrwellsNitemare", "RealJobRob", "fubaglady", "ACatholicKnight", "Gratefully_Free", "DrCeleronMD", "Avonsalez", "patriotnh", "mickerxm", "a_j_t_j_a", "brickwahl1", "ProudOkie897", "RobertJByars", "01splcheck", "FascistTwatter", "shotgunss52", "KATantiNWO", "tysusej3", "DuchampMark", "RosalynTreat", "wolferkitten", "ACzound", "JeffCox03994882", "BerryRichards1", "MikeSmi6533517", "216tunasub", "forsythia77", "LovToRideMyTrek", "rcsyoungusanet", "LankLondon", "johnsot10", "lee_borden", "AlbertBruno2017", "Trina1732674", "lady_fiesty", "awelab1956", "kanuck_j", "overtaxed23", "Steffs_tweets", "lbljm1", "JeffHickman14", "Prue88Preeti", "STANDTALL4EVER", "SkankHunt40to", "Liberal_Buster", "TherestoftheUSA", "Felixjrodrigue4", "inittowinit007", "BillLonbeck", "wwdnet2", "LaurGarTX", "Elena77h", "adcoiii", "TheTruth_MAGA", "Joe49923765", "jinouyang", "Deadwood691", "Welsh58", "fturner06144", "ConcernedHigh", "ArchangelsWard", "irfirestarter", "TiensToi", "DCF4L5", "redwhiteblue59", "Icenitudor", "tom46236928", "CalVic932", "WidowFike", "trump020", "CedarLW", "HabuTroy7777777", "WillieWholeSlew", "JanineLynette", "dragondeau52", "Rroman61201", "VoiceOf26525977", "JBG43", "1RussianBot", "Daver2956", "Lobe74419288", "fondue_chub", "DennisDet656", "President1Trump", "HinderTrump", "Ontheotherhand", "NeilMS17", "Hugoboss5454", "RightOnBrother", "slsgaston", "buysell969", "jonjens", "AnnelieMoser", "kelleyh1961", "BrinkMadHatter", "amylpeltekian", "P0TUSTrump2020", "RichardVerMeul1", "00_jackie", "Pattie19901", "BabyHandsTrumpy", "oliverg2014", "davidearcudi78", "RussellC1hfd", "Krisleblanc_", "s_hawcin", "DotardJerkTrump", "Erosunique", "Stays_Silent", "KennethHoefle", "isavega2017", "BrandonJLandry", "realShariStott", "woodnbow1", "MatthewCronin9", "TranscriptJunky", "apat_c", "isis_sux", "CUGregersen", "SRichDeLouise", "cloakedaxiom", "toxicdogpit", "RogerKalivoda", "3_lizsosa", "brwatters", "zeena4kids", "jakkedup1", "iamtheMAGAbot", "BigLeague2020", "cmc7564", "shad39", "TrammellLt", "mbennett30", "mcnamaraorama", "Maximus_Espanol", "Rcz609", "Serendipiterry", "RedFlannelPunk", "1hardkernel", "DarLovesAmerica", "BurrissJonathan", "DonnaWR8", "Regina_Queen_", "Richard14120", "ntflgcreative", "Demgirl50", "dawnkirch", "Michael_Schlenk", "TATARNASIO", "UpInTheHills", "GrodJesus", "BebeBertino", "CherylF19409787", "jaydogg2831", "DaveMongin", "DeCounselorLady", "Iknowmystuff63", "sandra_scheil", "stevedempsey65", "TFtakeaction", "MikeRoach3", "odcusa", "GaryMayer53", "VaTxn", "Jules06281", "NotreDameBaby", "nuuzfeed", "f396", "birbakmagazin", "thomasboy_2", "tomorrows_truth", "vic777212718", "HotGrill7619", "MaryMcC10518422", "justgrateful", "swamp_cleaner", "RiseUpLaz", "SDWeisenburg", "Beverly21811568", "RegisAndromeda", "MulcahyA", "JillyIllg", "RitaThaQueen", "randall_smuck", "TkMelly", "LadySJMG", "sergio93534", "jhasmund", "olsenpalmer2909", "reneeblair56", "cindyluwho72", "BrittRon", "SWOhioguy", "GeoffVictor", "BroadViewTees", "grandmakimmi", "Thaysone", "sandrablaine9", "triciamccole", "ChampionMtager", "Anonagain1", "bestdoxiemom", "JayChpJones", "JoeMcCarter5", "OKIndian1", "TeresaMarieHad2", "Irelandgirl8", "Dogs_For_Trump", "nacv2000", "JonStancik", "Kathleen1818", "StuartGillilan1", "ms24june", "Janie_St_K", "JTaylor_JTaylor", "FrancisJeffrey7", "joej2020usa", "BoldAnalysis", "PaulGMcC1967", "wedeacs", "SWEETY16A", "Mrbillie54", "Nex97095452", "LG4LG", "Baltazar_Bolado", "Texas_GunsNGod", "dcohen315", "MichaelBellSD", "PSTtwittbird", "TrumptheClown1", "GREGWINSKI2", "arttronics", "HeartForty5", "RodneyLeese", "Redhead_NJ", "MicaelaComposte", "cherylcope", "Vet47Army", "stevehazard17", "cssueta", "AJ_ALABAMA1", "zeusdlt", "xyzgyrll", "sealeney", "LeahCrane19", "Illuminate1465", "DonC085", "duquette_tim", "56kbird", "sharonz6", "CarolK47", "24_7_Gmo", "cfrasher1", "mjdriller", "Suzanne53010022", "ErikOnDemand", "GrizzlyKurt", "JESUSEARTHRETUR", "Psm6922", "Jbooher5", "NWClassicCar1", "betty_kaputnik", "WhoWolfe", "AliciaTolbert", "usa_gramcracker", "tiff_thegiraffe", "mimishouse", "SallySallywest", "tfbill3", "AtkinsonMuno", "Booksbaby69", "queensword", "russ30327", "MarciaBunney", "firecatgus", "Rebecca35748712", "derbyshirelass", "Lovetoplayinthe", "DigitalMartyr1", "ImShoppieShoppe", "marycjoyce2", "chazman1111", "oldmsrebel", "HauerCarlin", "lulupink12", "gopRtraitors", "Gingerbp65", "MrsHandyRU", "oclare2043", "Robinabank4", "celebritykimdot", "JamieButts4", "TwizzlerGirl", "Zhork2", "SDNorthShore", "LottieAntonetti", "miamischolar", "URTheBank", "NBoyias", "xScorpi0x", "VickiMerivale", "Alekalynn", "Sandyma41963843", "happyathome4", "StevijoPayne", "cristy121764", "Matthewcogdeill", "LibertySeeds", "changestatusquo", "SolMTio", "trotwoodrose", "FreedomTruth1", "Markperugini1", "candylampasi", "BStrausberger", "Jeanniecraig15", "jas7_april", "Thefootlady34", "jolivelaughlove", "BillCanoJr2", "NJAInteriors1", "KTCarroll7", "luvnewprez", "jarmjr81", "george98414198", "karenbr01503349", "DemorestBeth", "1800pinky", "blitzer850", "BlindProg", "kinthenorthwest", "hyland114", "AaronVulrik", "Julie_Camarda", "rlhj1974", "Smokeysmom68", "annapolisrocked", "susan_z_kat", "ruhlworth", "realSagemon", "LynusCantwell", "playboy5387", "HowieBye", "twister2254", "witsys", "11woodywould11", "sewpam2", "StephStevens77", "KDScioscia", "JRob747", "TheKittyFitz50", "_VachelLindsay_", "SassyGlassy2017", "ChristineIAm", "Auntoys", "Slenderloin", "suebrown1212", "ggeett37aaa", "surfermom77", "ggma5757", "RobinRicker", "littledawg1962", "scott_felps", "vaxchoiceeast", "JosephGReilly62", "depaoli_steven", "mllnola", "realDonaldTumpf", "kauffdrop1", "HoosierTrumper", "Made_ln_America", "Trump__Rocks", "republican_z", "71Warhawk", "JoniPrincess", "musicaljane1", "nolibhere4923", "dsealdoc", "Heleneafernande", "FUimpostingit", "Phil_Numa", "Trumpkingirl", "Indiana4theWin", "howdyfrom", "hawkdriver6", "lucianomoca", "mfstern", "Bobertah", "PJ1963Indy", "MelissaStout12", "SpringsRaff", "Randyszabo1", "BarryWhite4", "abjmjordan1", "marty1066", "rickwartooth", "LaylaBlock2", "davidconklin74", "JackPolakoff", "SoCalEdgyGal", "FellDown_GotUp", "sots56", "DarraldC", "robjh1", "paultroch", "storm30002", "Dougniff", "suziepn", "suspended52", "wordbird67", "al_bouchard13", "hiparnold", "ScottAulde", "Rhettbutler2015", "Unitedstatessto", "tunedhuman", "zenabby1", "KarenBarbosa61", "RodStryker", "steve_durnan", "thecomputerdr", "johnnynaplesFL", "DeezNut123456", "3dogmary", "jenbrunelle2", "Tngo913", "TheBigNFLTuna", "wl1902dad", "Ohio4Trump2020", "larryhicks21971", "JohnaldJTrump", "Barbara77051620", "Randy_0302", "theresa_gavitt", "bblueberrypie", "WandaWstewart", "davidinkuwait69", "Trumplar", "Lib_attack_dog", "iamocracy", "CarlMatsx2", "LibertysThunder", "MfsGal4Trump", "Protect1USA", "rbagley1965", "godislight4u", "EdwardMColbert", "viasly2016", "SLBCTexas", "PoliticallyRYT", "onedovealone", "DSteampipe", "YMcglaun", "jimjone94477836", "dowertd", "FeistyTrumpette", "geoff_deweaver", "Barabbus2112", "eturner010", "Margee11", "ScottLeelon", "Truthbefree1", "ROB4TRUMP", "comradebernout", "Mansteinvi", "TeenyLZP", "frfun0101", "BillEagle1951", "jacquiefvaz", "chefboutwell", "jklivin0415", "LibsRNutz", "Daniel78402814", "PassarelliAllan", "deb_lemar", "Charlinas_spawn", "Me262A1", "Ami_du_Radical", "TrudiBartow", "pcommonsense", "mshoaf68", "demsnomore", "MissTeresalam", "cmcl5", "SalirDelCamino", "BURKE11530", "GiGicmka", "LpKim61", "WeThePeopleMAGA", "worldflood1", "PollyDelSol", "TChristopherLee", "Maggieb1B", "Frann_Bengolea", "todd4house", "Grannie1951", "aseeger3", "peg1955", "turquoisebolo", "TonyArmijo16", "columbia1969", "BigDickDaddy50", "NMatte33", "putneyswope7", "CheriJacobus", "bolshevik4trump", "CherylAschenbr2", "patriot1cavalry", "starmlw", "chivalya", "KATO_atKATO_com", "ru98634041", "CeliaCh24609512", "josephc133", "CaptainTaterPuf", "taco_twins", "G1rly_Tattoo3d", "IamPacNWer", "Stevemorrisjr1", "flyby2474", "rlgordon18_ruth", "OldNorthState12", "DoseQuick", "rcjhawk86", "AllGreatAgain", "ryteouswretch", "testtube65", "Rochell81486461", "themema", "antlovato3", "2017TRUMP2017", "lor65", "no1rebo", "kristin_everson", "amazonnurse_", "Mtweetie4848gm2", "Tanar1022", "savvyconsumer7", "navyvet55", "melinda63312935", "rickwayne310", "Stichtag", "jmert_58", "jon_knepper", "JDPMAGA", "mbms4", "mcatee_chrystal", "MoHollis2", "devlin505", "deplorabletx71", "ScottluvsCuse", "SueSuebarker12", "dyingbreedgent1", "Mayzee590", "christopherpau6", "AngelVanns", "pigeye007", "km_kathie", "AUwareaglegirl", "lovetocook12345", "plwalker71", "AltFawn", "Thinker_Jon", "ksteven37", "DonnaNoname2016", "trumpisadickwad", "repoprimo", "zack_nola", "flgal4trump3", "FredfromFlorida", "Hadessah77", "BlognificentB", "Sleepynaps", "BrendaB98653616", "Kameleon1974", "TheUnrealKRyan", "USA_Watchman", "jerseyboy", "leslieau7", "JanMareeSmith2", "Saddleman61", "teokee", "Pastapharian700", "AmericanMom2", "strategicpolicy", "tbacon3019", "VikkiSueHam", "ProudArkgirl", "johnbarnesmusic", "KellyGreenGirrl", "zosocoda1969", "paultykwinski1", "PresWallace", "AnneMorrowCoop1", "grandmombarby", "MyDriver88", "bigjimchest", "Rhonda_Maga", "Sumergirl84", "noraconnor89", "Frostypie9", "veganvecoh", "ThumperFLTRX", "CandeeSnow", "Corp125Vet", "jemakatz", "ntvnyr173", "StephHarpman", "jcnwest2755", "KitCoco", "princessdianej", "RidgeRunnerKY", "pearly2004", "shawnte40", "Rick_Ingersoll", "TheRealJaySaley", "peartreemomma", "JannaWilkinso69", "WhoopteedooCA", "Stultis_TheFool", "JoyceBruns", "SexyTrump3", "karenta42168532", "easier_done", "PK_Mowery", "mcrae_lynn", "suzettepetillo", "WokeSorosShill", "TrumpUrWallet", "cherylnakhle", "LoneEagal21", "Mofrodo", "Jaywall13271015", "snikpmis", "libsrinsain", "DanWell62287730", "Michael19711992", "myerskathleen1", "jbnnonfly", "GLoosier", "Liberty36_", "DanDuke2013", "juanalfaro412", "Scarletofsouth", "easkelson", "magazinbirbak", "tim12jan", "msest1", "robcarlson20", "m0nmick", "diggergld1", "WayneJ28791698", "kwein0309", "texasaunt", "Valerie24190901", "GreenPus", "rovendetti", "DebraChisholm2", "1Deo4Me", "Rani513", "RainerMcDermott", "famousmagacom", "SteveWa69661272", "MyInfoRonnie2", "dawg_knight", "kam6617", "ReclaimSelf", "BennyBenythajet", "LanieWalters", "TheRev1953", "fleoni757", "lancebork67", "GaryAAltman2", "Calvin1418", "ConConstandis", "erhenry2001twit", "AdiAbara", "ShowboatBob", "Politacs7", "Genuine1mposter", "Jr88503261", "PVHenryConLLC", "melBELL_USA", "proffitt_judy", "MaryLane33", "Trey_VonDinkis", "lourdestovar", "disings", "jwelsh75", "SupportDonald", "SassyCatyCat", "RogerSt415", "JuanitaIguana1", "DprkKorea", "garyd552", "JLG1017", "WileyCoyote9999", "michellmybell1", "hezimerollin", "Tfrank1e", "dkdk459", "EDZOPICARD", "GynoMary", "LoriDenham1", "rap10", "LindaHu22622584", "colorfullizard", "timmacd64", "salamisanwhich", "au67", "fjski3", "JanDearing", "sis78", "MaltaTj", "rgividen", "OsirisLynn", "Engelbertsy", "hurryback2", "washington_two", "oldscoolguitar", "Noneya864", "MyPrezTrump45", "wyatterp2005", "PPatriot4life", "tintimmymustach", "desireekraft3", "sunnydwv81", "WinnaWinna2016", "TheOnly_Blasian", "MacChomhghaill", "Psysamurai33317", "RPCovit", "WayneSense", "jasonpowell77", "biy2c", "Karensuelund", "Jrap105", "IMO_Snarcasm", "kttk234567", "THETXEMBASSY", "hidehunt1", "realMikeKraus", "davewin49", "troysbucket777", "IanMCohen", "DanKelsey2", "PacerV", "frodo3245", "jackdorseyzero", "Zoo9guy", "trollhuntress", "stanspak", "TedPert1", "redskinsrock91", "No76334363", "rn_deplorable", "Bjschw309", "iWideOpen", "devinbanner", "TrumpTrainMRA4", "jrphilpot", "RedWalrus1", "H3LLDATA", "Mary_Burgess", "jumagoe", "shotgunfetus", "Jsmith39859475", "SamuelLauzon3", "Gweezy52", "hanro22", "BSelepa", "danni816", "AlanM_Patriot1", "mattymattlock", "JakobLovesUSA", "hkociara", "toddbedlington", "RussellDeanSto1", "Jjbats", "rwycoff102", "Thorman_Lungie", "skb_sara", "71Paladin", "humour_man", "PatriciaKamir89", "MrsAmerica1776", "thorntreehill", "Nanu4Equality", "liftuup13", "coinyman", "Pamc0405", "JanRomes", "Mitchell6369", "brizo52", "rcrockett", "Sheila4USA", "DebraMMason1", "glen300sd", "SteveBarnett24", "SEvanson", "TigCook", "ArwannaSaylor", "Ctt432", "RightSassy", "daisyangelman57", "ProgPoison", "JamesWynn14", "DestinyandBruce", "bonsaihorn", "DinduDingus", "AwakeinMN", "WandaWeber1", "ElizabethAnnGr7", "waltfava", "SusanCTurlingt1", "LTGRIGSBY", "jim5353xxx", "jus1_kimberely", "StevieCuriosity", "nonnies31357", "RNRUtah", "johndoeorwell", "reason2sense", "Sparkypete777", "CrosbyJenet", "ImBackUSA", "tmcats6", "redcat0827", "Maggi82174682", "patriotmary_", "Stargazer2020", "victoireboo", "skeeter19592", "fightbyfaith", "Fite2Bfree", "chigobiker", "toiletman01", "NIKKOHEATAZ", "dandyjo2", "michelemanasek", "FamilymanUSoA", "stouts4life", "WillaoWoman", "sundevil1750", "fthomasii", "UncleTonyRP", "jpharley3000", "jdavis3", "lv65", "A_D_Seri", "debrajs17", "AndyAshby1", "AU_bebe", "EricHensley18", "angelswarriors1", "santome7", "TarredOldBones", "LuvStarsStripes", "supersaber100", "IdalmycastroMy", "WeAreReady2017", "USAFOREVER2016", "jennferkhinds", "VenomSobold55", "trip_elix", "Gval1209", "Hemlepp53", "SternsMarilyn", "NorbertPlante", "TrumpIsMortal", "howardmclainjr", "Tom64810852", "PsychopompGecko", "Dapandico1", "flakround", "AnnoyedLabRat", "mollydazed", "Jali_Cat", "LazuliLady", "arruda_deby", "NCGigiH", "WandaIsBack", "vogl_tina", "billbow47", "WinsOut", "bevels_perry", "Irene99879148", "shadowbirddog", "Trapinsc", "trixidoodlexx", "StAnIsHr", "Rob1Ander1", "DKBupnorth", "toddk67", "voiceangel2", "RCLessig", "MaRainey357", "cinderdiane", "HimmerMark", "hasper2go", "VoiceSingle", "djcip", "Hotrodgirl75", "hiwyatt25", "jojonyc45", "MagaOneRadioNet", "baabbee71", "Eccoscott", "RealMAGASteve", "Bon1", "petefrt", "HiDesertPatriot", "Jm234Jeri", "ANEs_Mom", "whereisjustice0", "JKP_RN", "Kuhlio1313", "PamT817716", "75otingocni", "DavidWeingust", "cjdotma", "Ronni3isAwake", "NaplesRocks", "InvestAltcoins", "Farrier1959", "ImRaunchePubis", "Nikkisuglytruth", "thoffmannswe", "sofakingconfuzd", "MatrixCure4You", "LandenSmith11", "mjskidz123", "warhootersgm", "BdRedwriter", "GodzStr8Shooter", "lsmith4680", "Perch313", "ConnRebecca", "TimSher38807557", "NOONELOVESMENOW", "lsfoster", "digino69", "GretchenGorup", "TeresaBob", "Manbro17668", "Xpompier77", "Wanguelens", "KNP2BP", "AlwaysActions", "billglaser1", "reganleea", "medicdave29", "KathyLittle18", "pave2914", "JimKlunk", "guardian2161", "magicbeagle", "msann43", "DammitBritt", "RedinVa2", "liserg14", "ziggs0516", "Sannana3166", "forresttcon", "JesseWooten18", "MrsBPace", "Nico_Sieger", "mog7546", "LMHOCK1", "mancubspapa", "Robertschilke1", "fmtorres472", "museisluse", "NickRecchio", "Jim_Peoples_", "LisaPenatzer", "DanCovfefe1", "northernana1962", "Susalitt1956", "workfromhome7T7", "JVER1", "Charlie76303011", "LDknepper", "charles19712015", "snknight1968", "ashau68", "Redneck_Jesus", "Joan1Barb", "liberaltears67", "ImAllinMAGA", "jimaus2205", "hondageek1", "mkaylajxx_", "exposeliberals", "DRockSpider1", "sobebrz", "thedetroitjule", "TrumpsBlonde", "joanadeleq", "Robertmark1010", "prissypat2", "AlfredStabile", "jkslaven", "TRAVELLMAN", "KathySmallwoo18", "EdgarChewning", "USAgaggy63", "NWOinPanicMode", "PliveCalmer", "Holmesdonna1", "Coopdoc", "Amerigirl68", "GraceHealz", "surfbro26", "SonsMary", "Chris74347137", "glenpalm2005", "GunswapGary", "RuthieRedSox", "RosieResisting", "VaMaFraVi", "mearant12", "michelleoverby2", "RejeanHebert1", "Nixey17", "Hotjava01", "axcited", "RockersDenStore", "LilLuu79", "marie_tellefsen", "bfhistory12", "TheRocPolitics", "meltedmarbles", "seedeenurse", "jimsand1718", "Golden888Karma", "MusicCityDawg", "HoagCarol", "ClassicDeepCuts", "violin002", "Jo49672031", "KBinSC", "ShaunHumphrey65", "emm_fee", "countrysherry", "jeanibanez", "LeeBecky17", "Manuel_Labor__", "bgdeangelis", "TeaPartyToko", "rhondasaddress", "unkiewood", "BenB388", "erinstarriscool", "twogunstall", "DavidHern14", "LakesPlace", "dreamweaver1001", "Exasper8ed", "AndreaTheiss2", "RollyHui", "larouti", "ExposeFascism75", "texasnick310", "BOT_TOBY1", "TribeTrump", "RealWolfsPride", "MattBarnesDKOC", "swimmom0f2", "RealWendyTeresa", "Dollfinish", "hunley_nolan", "chaseme58", "SharonGilman", "JazzPowalski", "mytrn55_linda", "PatriotLiza", "WoodyWoodturner", "AllenShoal6535", "inscnc", "Am1stBoomer", "Beatriz08893533", "kwaizume81", "sevans1375", "ElleHart2Hart", "wobbly_tiger", "BetsysUSA1776", "dboaz75", "ShellyEnabnit", "collectcall1", "Anastas48819550", "momofmonday", "PrezTrumpBot", "Droolsum", "nativekittens", "MjaneMarshall", "KLMc39699369", "BLUECHARGER69", "Lou03353725", "lavonb11", "JimPolk", "TomTerryInc", "ZoellickJudy", "caseymckack", "johntieso", "jbug9969"]
    open("data_maga2.csv", "a").close()
    # make sure we are not crawling for already saved user names
    current_data = pd.read_csv("data_maga2.csv", delimiter=";", names=["username", "duplicate_candidates"])
    cached_usernames = set(current_data["username"].tolist())
    usernames = list(set(usernames) - cached_usernames)

    data = _crawl_users(usernames)