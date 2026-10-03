# تنزيل شعارات الأندية إلى images/clubs
# التشغيل: python download_logos.py   (من داخل مجلد football-info)
# المصدر: TheSportsDB (مفتاح التجربة المجاني). الشعارات علامات تجارية لأصحابها،
# فتأكد من ترخيصها قبل استخدامها في موقع يحقق أرباحًا.
import json, os, time, urllib.parse, urllib.request

CLUBS = {
 "ars": "Arsenal",
 "liv": "Liverpool",
 "che": "Chelsea",
 "mci": "Manchester City",
 "mun": "Manchester United",
 "rma": "Real Madrid",
 "bar": "Barcelona",
 "atm": "Atletico Madrid",
 "juv": "Juventus",
 "int": "Inter Milan",
 "acm": "AC Milan",
 "nap": "Napoli",
 "bay": "Bayern Munich",
 "bvb": "Dortmund",
 "psg": "PSG",
 "om": "Marseille",
 "bre": "Brentford",
 "tot": "Tottenham Hotspur",
 "avl": "Aston Villa",
 "bri": "Brighton & Hove Albion",
 "eve": "Everton",
 "ips": "Ipswich Town",
 "new": "Newcastle United",
 "hul": "Hull City",
 "nfo": "Nottingham Forest",
 "cov": "Coventry City",
 "bou": "AFC Bournemouth",
 "lee": "Leeds United",
 "cry": "Crystal Palace",
 "sun": "Sunderland",
 "ful": "Fulham",
 "rbb": "Real Betis",
 "sev": "Sevilla",
 "ala": "Alavés",
 "dep": "Deportivo La Coruña",
 "rso": "Real Sociedad",
 "vil": "Villarreal",
 "ath": "Athletic Bilbao",
 "get": "Getafe",
 "rvc": "Rayo Vallecano",
 "osa": "Osasuna",
 "rcc": "Celta Vigo",
 "esp": "Espanyol",
 "rac": "Racing Santander",
 "lvt": "Levante",
 "elc": "Elche",
 "vcf": "Valencia",
 "mcf": "Málaga",
 "rom": "AS Roma",
 "laz": "Lazio",
 "cag": "Cagliari",
 "fro": "Frosinone",
 "com": "Como",
 "sas": "Sassuolo",
 "ata": "Atalanta",
 "lec": "Lecce",
 "udi": "Udinese",
 "tor": "Torino",
 "par": "Parma",
 "mon": "Monza",
 "fio": "Fiorentina",
 "bfc": "Bologna",
 "gen": "Genoa",
 "ven": "Venezia",
 "scf": "SC Freiburg",
 "fca": "FC Augsburg",
 "b04": "Bayer Leverkusen",
 "m05": "Mainz 05",
 "sve": "Elversberg",
 "svw": "Werder Bremen",
 "rbl": "RB Leipzig",
 "sge": "Eintracht Frankfurt",
 "sch": "Schalke 04",
 "pad": "Paderborn",
 "koe": "1. FC Köln",
 "tsg": "Hoffenheim",
 "vfb": "VfB Stuttgart",
 "hsv": "Hamburger SV",
 "uni": "Union Berlin",
 "bmg": "Borussia Mönchengladbach",
 "asm": "AS Monaco",
 "ol": "Lyon",
 "pfc": "Paris FC",
 "lil": "Lille",
 "ren": "Rennes",
 "ang": "Angers",
 "rcs": "Strasbourg",
 "man": "Le Mans",
 "aux": "Auxerre",
 "stb": "Brest",
 "fcl": "Lorient",
 "tfc": "Toulouse",
 "nic": "Nice",
 "rcl": "Lens",
 "est": "Troyes",
 "hac": "Le Havre"
}

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "clubs")
os.makedirs(OUT, exist_ok=True)
API = "https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t="

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=30).read()

missing = []
for cid, name in CLUBS.items():
    path = os.path.join(OUT, cid + ".png")
    if os.path.exists(path):
        continue
    try:
        data = json.loads(get(API + urllib.parse.quote(name)))
        teams = [t for t in (data.get("teams") or []) if t.get("strSport") == "Soccer"]
        url = teams and (teams[0].get("strBadge") or teams[0].get("strTeamBadge"))
        if not url:
            raise ValueError("لم يتم العثور على شعار")
        try:
            img = get(url + "/small")
        except Exception:
            img = get(url)
        open(path, "wb").write(img)
        print("تم:", cid, name)
    except Exception as e:
        missing.append(cid)
        print("فشل:", cid, name, "-", e)
    time.sleep(2.5)

print("\nانتهى. لم تُنزَّل:", ", ".join(missing) if missing else "لا شيء")
