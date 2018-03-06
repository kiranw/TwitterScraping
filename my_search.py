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

# crawl google reverse image search for the supplied Twitter usernames
# returns a dictionary mapping one username to a set of potential other usernames
def _crawl_users(usernames, max_no_pages=3, request_pause=2):
    # selenium driver
    parser = webdriver.Firefox()
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
    usernames = ["ayuub308", "JannaPutriAyu", "KariJaquesson", "RMontajes15", "eyadkaka1", "liloucharifiia", "quantumbiology_", "buryilmazer", "cloudwanderer3", "Rebel_S4Peace", "unikgirl11", "yasiribrahim24", "Minaism", "emmanuelhoog", "KomsonSonpavan5", "MenasriaMomo", "char_142", "JannaPutriAyu", "Elizrael", "Gwendifyr", "shuib_96", "LighthouseForum", "MARLENEBLANCO7", "Hermawan_Razief", "ecatepeclomas1", "Islam21369653", "NicDawes", "rjeanroberts", "InsydeMan", "chelsealovhotm1", "miltonarrieta33", "reyhanakcay08", "d4dD3", "very_grem", "nevilleblanc", "allidoisranttt", "ingrx", "RockBarceRoll", "maferegas", "hervegogo", "pessoptimistic", "IntelCrab", "ecatepeclomas1", "stephenalbert11", "BandeKhuda", "these2balls", "Hamed_sabouri3", "JakobjMikkel", "jazirahng", "Swarnadiva9", "ecatepeclomas1", "mwkm2011", "Flavia0847", "markiomac", "Defcon1W", "BaconJoel", "ProceresVe2017", "enjoyparaglider", "enjoyparaglider", "eimaster13", "ecatepeclomas1", "citroyen_X", "trendinitalia", "jecarrerog", "BeeAHoney_", "Aethonaia", "Ammongurzil", "NofNews_Kenya", "Notorious_Nava", "RBHam63", "Aethonaia", "colorado666", "keepinitreal153", "aldoctor_DR", "NatureFireplace", "Aethonaia", "mohamed_mousa19", "ermurenz", "Swarnadiva9", "aldoctor_DR", "amirnazari20", "SBS", "margrazyna", "ZaidIT730", "bo7_thawra", "TheGabrielBauer", "AlexMaless", "NeotipPro", "RobertWorthley", "monicawasef", "debmorello", "mohamed_mousa19", "RevolutionSyria", "Estigiaed", "BadrAlQahtani", "NeotipPro", "KariJaquesson", "Occupy007", "Trumpkingirl", "gumargth", "Maroccan_212", "danbrosgol", "abu__savage", "ndCapio", "semritalina", "csmonitor", "gambergeur", "dingalingy55", "IvanSidorenko1", "ShareCanadaNews", "thia_bfagih", "stephenalbert11", "JakobjMikkel", "robcrilly", "Sungmanitu58", "powercoach_pe", "MiraMiasilChe", "FarrahFazal", "coex145capt", "mohamed_mousa19", "creativejen7", "IvanSidorenko1", "mariapaularomo", "DIANI_R", "poinsettia61", "Maroccan_212", "Baldiva17", "gambergeur", "Sungmanitu58", "irinnews", "IvanSidorenko1", "FarrahFazal", "FarrahFazal", "KeBinSoreasmey", "Rabiaandrea", "Allah99060991", "VeoNews_", "imransolanki313", "shwankendal", "MaoZedung", "VonnieCalland", "GeoTaiz_HD", "MpPervane", "Rogers6661", "Thekitabwala", "vitiok78", "MiaFarrow", "Allah99060991", "_Vikingsh", "The_NewArab", "viviaines", "eldjid2", "JohnLocker4", "aser_ne", "LisePierr", "GaiusCa1igu1a", "tn4venkat", "jhonsonvalencia", "SherryWhy1", "atmncr", "eldjid2", "Navsteva", "KrisBrbr93", "Estigiaed", "dingalingy55", "Navsteva", "Touba80221319", "suse_______", "Touba80221319", "suse_______", "emzorbit", "gailymalone", "imran_jutt47", "Aliyajawaid1", "Pieryhenry", "samar2202", "AaronMagid", "cloudwanderer3", "rubu481", "lintlvieno", "NormanBuffong", "ALKofoet", "ShoebSolanki", "f_regules", "mutalabala", "korol_koshek", "phoenx7", "AWAKEALERT", "emoffet", "chinaortega7", "mohamed_mousa19", "amooola2002", "mulfah17", "RealNadz", "amooola2002", "phoenx7", "bbc_diff", "RaptureForums", "john_morrio", "9arsth", "BitcoinBuddhist", "SyriaUK", "ZFTWARNING", "TigerKnowz", "ClintWarren6", "Acho_Wendy", "9arsth", "Snarkathon", "AnaisRafaela", "suse_______", "Sol121Nadia", "WorldNews707", "roraimay1", "Eva_Marina_89", "riyadh_aj", "rightojibwe", "Jmart4info", "PressTV", "Occupy007", "AmitTanzib", "DOFreport", "schroblinger", "maggiezasss", "syriacham", "aleenrico14", "SDrinsinger", "JonDave84", "BergsteinViktor", "2Rook14", "talentosprecato", "maggiezasss", "handsoffsyria", "c_c26047605", "mostafa_abram", "alvarofroman", "mcdysko", "emoffet", "rubu481", "AdekF4", "USARocks1971", "syriacham", "rubu481", "cloudwanderer3", "XavierFiestas", "Eva_Marina_89", "JamesNichols73", "mirjossbom", "cwilhammer", "suse_______", "AWAKEALERT", "VonnieCalland", "ColeBockenfeld", "Tom_Daraki12", "k3vk4", "syriacham", "twtPoliPd", "emoffet", "davemustgo", "gponceleiva", "iamroxanepope", "StevijoPayne", "citroyen_X", "kali8541", "EHanichak", "laverdad31456", "sardarabomostf", "ffss70", "GerlindeRud", "phoenx7", "News_Binge", "Figdude", "Touba80221319", "mohamed_mousa19", "Passioscorpione", "phoenx7", "DeshBhakkt", "MWAgain", "WHO_ishappy", "krasnaya_dusha", "silmareth", "ntzyrsn", "AlexandraKE", "3223Jomjam", "deusexstigma", "AlinaIrshad", "jose_baha", "championemotion", "Sonophoto", "ako0516ako", "abofarah09", "MustafaGhulam_", "phoenx7", "sardarabomostf", "AnttiHarjula", "Blue_Star_mv1", "rubu481", "DrShajulIslam", "alfredoer", "SylvieMasson3", "SyriaUK", "maggiezasss", "suse_______", "mcmancheno", "PedroGu59661164", "Al7lm777", "marie_chaillou", "nuuruaiini", "maggiezasss", "Ldyblkbd", "sherpeace", "rubu481", "Estigiaed", "Snarkathon", "MarxAlann", "scarlyle", "newssummedupuk", "omen_syria", "HLD_23", "truestory24", "arifrahmanbrun1", "PrevGenocide", "stephsanola", "abissicus", "ako0516ako", "mfatihnar", "gruBHFIOasiY3PF", "erikdeboer8", "rubu481", "luisAlfredoM2", "PhilDeCarolis", "suse_______", "slmhktn", "lis_dans", "ArtMarius2", "jjcjmc", "PKPUHI_Kaltim", "francoish", "fairyofbloom", "Hollaka_Hollala", "JGonza28", "zumoeg007", "Un_Divergente", "AmarahF", "ArsalaiH", "Judit71430649", "polluxc", "gorankrav", "cloudwanderer3", "Follementbijoux", "arifrahmanbrun1", "ShariLPhelps", "Un_Divergente", "maggiezasss", "Anon6_NvrForget", "jobs_2014best", "jobs_2014best", "maratquin", "suse_______", "Syiah_Indo", "Acho_Wendy", "zibahfairooz", "tigerheart_46", "maggiezasss", "jmma66", "weknowucare", "Pticatrkaica1", "On_Point_Skillz", "schroblinger", "nasserrabbat", "AkbarYoso", "Shoaamd", "jjcjmc", "lovemycountry55", "433_3165", "sandlogs", "Blue_Star_mv1", "Hey735272020", "rgappp711", "ELINTNews", "Blue_Star_mv1", "bailey_beattie", "fredwalton216", "abofarah09", "GertHanekom", "curas_si", "ELINTNews", "happyKof", "Rojname_com", "ahhhraphael", "gengh60", "joe_dirty", "r0kr1", "pd4ejp", "screaminkid", "vistacha", "jjcjmc", "Adel67008964", "Jfox71506865", "joe_dirty", "gengh60", "Peta_de_Aztlan", "maggiezasss", "DutchSyrians", "GertHanekom", "FirstJpn", "sunny_chowmein", "Aaj_Headlines", "BeshrAlkhateeb", "RandomKurdi", "dekelley14", "FernandoAmandi", "CrusadeNewsCast", "Ramahi2000", "Arash_Hafezi", "AR_Tweet_INews", "mitsdla", "Alas56658640", "Vedatkaraca18", "319192305", "AR_Tweet_INews", "candyw", "newniky", "TonnaireM", "realPooPooSmith", "FakeNewsTroll", "Tom_Daraki12", "AKarkoukli", "ummifatihrso", "mariamesque", "ROJNAME_english", "jennyfrky", "AbderElhannati", "AmauroRodrigue5", "republikaonline", "HankDukeJr", "GlebKaznacheev", "GlenUsaid", "chindonsyan", "ahhhraphael", "Will13843087", "nuriIhuda", "ONC3X", "Yas2999", "Safrudinmuhamm9", "malika_k_32", "zul1732", "hepypurnomo", "Marcnelsonart", "joan_shyam", "g351t1", "AbderElhannati", "sophiayaaaa", "Marcnelsonart", "AWAKEALERT", "suse_______", "d1_grace", "Murdog00", "ZXPN247", "Rawarontek_101", "himaj20", "aprenDingles123", "sharaff", "mabo38", "jaimeiberos", "Internazional_I", "MuchamelLinda", "GertHanekom", "IMAA_Mirage", "makeupbymira", "cododegato", "helen95800581", "Geordievillan", "fanboy466", "Rung9735", "Panda6", "Marcnelsonart", "EliRamsi", "unikgirl11", "Robbie7paul", "TheNeobro", "shez_shezy", "topnewscity", "DianaCornald", "SimplyNewsApp", "sandlogs", "Marcnelsonart", "IAMConvfefe", "dragonmorgana", "froch1981", "omen_syria", "Vedatkaraca18", "sarahabed84", "FarrahFazal", "maggiezasss", "marinapece", "Ant_cl", "phoenx7", "hamaan23", "l13d", "lajornadaonline", "NewsToday_ID", "DazooFR", "TargetUpInsuran", "Harvard_63", "phoenx7", "FortRussNews", "AddinSuraiya", "himaj20", "JennRollins1002", "LouisaAchour", "henson40", "palestinechronf", "StewartHerica", "kbartlett114", "phoenx7", "boerneaj", "faridism", "HumanitarianGC", "MojoK1000", "Monitor_sur", "chris_m_h", "bryneson", "HameedIsaam", "GelirBirGece", "rubu481", "xalexon", "SEF_9009", "balarapolis", "jyonko77", "Ferhat__kaya", "PriyaWarcry", "stefanswartpet", "AdeleJLongstaff", "farooqon", "amatsuki", "DejiStevegie", "arifrahmanbrun1", "RegarBastian", "Muslim4peace3", "PeterCorless", "IsaMadesclaire", "himaj20", "QASIOUN_NEWS", "bunk_zae", "farooqon", "libertad_321", "EliorCymbler", "JanetAV55", "adillahmy", "LouisaAchour", "FortRussNews", "VietKaizer", "HidayatShahKhan", "phoenx7", "unikgirl11", "eclerecreme", "DanielOCL", "nelsonvs3009", "endtimesone", "maggiezasss", "Say_Non_Now", "Yemenis11", "SAtif83", "PeteRidge2", "DanielOCL", "MoandJinks", "SAtif83", "MenasriaMomo", "FortRussNews", "The_NewArab", "ramnayba", "FortRussNews", "farooqon", "riana_roses", "RaddulFasaad", "RoznamaUMMAT", "arifrahmanbrun1", "MiraniMiranij", "CathyMcRorie", "Baleia17228548", "FortRussNews", "Baleia17228548", "JoseFue09633601", "mofaizal09", "Janice12B", "55vilchis", "farooqon", "FortRussNews", "BeckyEubankCox", "headstonecapone", "SAtif83", "FortRussNews", "Watershed_Ltd", "_deSaintJust", "Watershed_Ltd", "itsnotsyeda", "CeeudeeyS", "ABRaf8888", "farooqon", "Saraha1Da", "CgAn_Doemela", "fadhilfahrenza1", "AWAKEALERT", "CgAn_Doemela", "suse_______", "malong79", "richamore2703", "Jmart4info", "faridabakhta", "abu_niza", "SwedenUN", "FortRussNews", "vatanyilmaz3", "beritartm", "gdk9933", "JoseSaylor", "TaikharTsend", "JanetAV55", "_mohsenshebli", "bmaat99", "AmyGunthorpe", "JanetAV55", "BobFuzz3", "Jmart4info", "Rifath21Mohamed", "Amelya_Anandh", "mehmet19076312", "bunk_zae", "goyacobol", "Hizir_Musa", "andri000me_15", "MyTrueHope", "smorris837", "jwtl1448", "PeteDriessen", "erbudi2015", "TimesofNews", "farooqon", "Sarah_Deniz", "LissetBeth", "WSandles", "Defcon1W", "NgcHoang1", "UmarMfz", "NgcHoang1", "TinaJac22661258", "POTUSPress", "DianaRVA1", "TolomeoNews", "Sarah_Deniz", "LissetBeth", "susanschulman23", "norvisogallan", "suse_______", "FanyGMartinez", "metacode", "msszerrr", "LouisaAchour", "himaj20", "KearaEugenio", "Sarah_Deniz", "ralvarezdj", "LouisaAchour", "Sarah_Deniz", "unikgirl11", "phoenx7", "joaquin_dasilva", "makeupbymira", "GPunchita", "MoniaMazigh", "LouisaAchour", "MontanaKlingsp1", "el_humbert", "FarzadForPeace", "CherryBlues4me", "himaj20", "phoenx7", "breaking411", "DinoAfuera", "fireheather", "TurtleWoman777", "mikaerupochi", "Syrfare", "phoenx7", "mehmet19076312", "muzahara2", "AntiGlobalist__", "goyacobol", "phoenx7", "TurtleWoman777", "JpnAnonymous", "DaveChewie", "Debi129", "LouisaAchour", "LouNehls", "Miyibue", "JpnAnonymous", "himaj20", "MisanthropicUSA", "phoenx7", "muslimcouncilhk", "RobinBall1961", "txtwxe", "mrjasonray", "heberth_f", "phoenx7", "Razdu_betz", "YAM2200", "EdwardHeil1", "Mr_Reynani", "phoenx7", "MaoZedung", "hary717", "AltWasp", "arefizadi1", "MrsLaurzilla", "MatteoR21309468", "KeffelecAl", "redstarrichter", "K_Muhammed_K", "Syrfare", "GharjelRass", "himaj20", "alabella2586", "un4_all", "TrollColors", "simonddegalbert", "MaoZedung", "_sara_4A", "QASIOUN_NEWS", "ariefrustanto77", "Ehsan_Butt", "Howayed", "O_Rich_", "IDashboard", "DinoAfuera", "kardinalexposit", "SkyWatchApps", "PavlosX59", "TamrikoT", "Kahyaninoglu", "firqinwalker", "aliciaisabel23", "phoenx7", "jocamox1974", "UpTarget", "phoenx7", "twtbawbags", "SyrieRevolution", "Kahyaninoglu", "Israelifreedom", "un4_all", "phoenx7", "Jonathan_RTfr", "MykasanReal", "bargyle1997", "ManonCostantini", "WhitePillitary", "ranumpowerplay", "jahkarta", "kgzxpm434", "marwanallesh", "Al_muadhin", "Razdu_betz", "anonhacksa", "Perpetua333", "ranumpowerplay", "superstereo981", "marwanallesh", "SarahLawan", "geronimo_370", "jobs_2014best", "marwanallesh", "islafisherweb", "marwanallesh", "MetaTVFrance", "orenseceibe", "mutosaur", "disruptivesigna", "walhana4u", "UkraineSpring", "Lennin001", "SecretNews", "MinisterFaust", "marwanallesh", "MehmedKl3", "Icecubesolid", "GEOKTNPK", "mehmet19076312", "eimaster13", "inteligenciaven", "marwanallesh", "NewsUpdate24Int", "renata_damasio", "BunggSant"]
    # usernames = ["ayuub308"]

    open("data.csv", "a").close()
    # make sure we are not crawling for already saved user names
    current_data = pd.read_csv("data.csv", delimiter=";", names=["username", "duplicate_candidates"])
    cached_usernames = set(current_data["username"].tolist())
    usernames = list(set(usernames) - cached_usernames)

    data = _crawl_users(usernames)