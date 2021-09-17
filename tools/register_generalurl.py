import requests
import json

data = ["apple.com", "youtube.com", "www.google.com", "www.blogger.com", "support.google.com", "play.google.com", "cloudflare.com", "microsoft.com", "docs.google.com", "mozilla.org", "en.wikipedia.org", "youtu.be", "wordpress.org", "maps.google.com", "linkedin.com", "googleusercontent.com", "vimeo.com", "accounts.google.com", "plus.google.com", "drive.google.com", "europa.eu", "sites.google.com", "adobe.com", "github.com", "vk.com", "amazon.com", "t.me", "facebook.com", "bp.blogspot.com", "istockphoto.com", "uol.com.br", "whatsapp.com", "bbc.co.uk", "opera.com", "news.google.com", "google.com.br", "google.co.jp", "msn.com", "mail.google.com", "w3.org", "hugedomains.com", "policies.google.com", "forbes.com", "feedburner.com", "www.weebly.com", "paypal.com", "theguardian.com", "globo.com", "es.wikipedia.org", "myspace.com", "www.yahoo.com", "bbc.com", "line.me", "cnn.com", "reuters.com", "dropbox.com", "google.es", "dailymotion.com", "live.com", "imdb.com", "mail.ru", "google.de", "washingtonpost.com", "wikimedia.org", "creativecommons.org", "nih.gov", "brandbucket.com", "get.google.com", "medium.com", "pt.wikipedia.org", "fr.wikipedia.org", "bloomberg.com", "nytimes.com", "gstatic.com", "developers.google.com", "slideshare.net", "tools.google.com", "harvard.edu", "office.com", "rakuten.co.jp", "archive.org", "cpanel.net", "jimdofree.com", "ebay.com", "networkadvertising.org", "soundcloud.com", "issuu.com", "huffingtonpost.com", "ig.com.br", "draft.blogger.com", "buydomains.com", "businessinsider.com", "google.pl", "cbsnews.com", "namecheap.com", "amazon.co.uk", "change.org", "id.wikipedia.org", "amazon.co.jp", "android.com", "samsung.com", "time.com", "independent.co.uk", "aboutads.info", "foxnews.com", "nasa.gov", "plesk.com", "google.ru", "abril.com.br", "terra.com.br", "who.int", "books.google.com", "tinyurl.com", "twitter.com", "youronlinechoices.com", "dan.com", "netvibes.com", "google.fr", "steampowered.com", "it.wikipedia.org", "bit.ly", "aliexpress.com", "photos.google.com", "news.yahoo.com", "abcnews.go.com", "telegram.me", "picasaweb.google.com", "amazon.de", "un.org", "ok.ru", "aol.com", "wikia.com", "list-manage.com", "fb.com", "wired.com", "fandom.com", "google.it", "wa.me", "myaccount.google.com", "cdc.gov", "booking.com", "de.wikipedia.org", "dailymail.co.uk", "ft.com", "huffpost.com", "cnet.com", "cpanel.com", "pinterest.com", "telegraph.co.uk", "hatena.ne.jp", "scribd.com", "goo.gl", "thesun.co.uk", "google.co.uk", "usatoday.com", "www.gov.uk", "translate.google.com", "search.google.com", "gravatar.com", "files.wordpress.com", "mediafire.com", "elpais.com", "enable-javascript.com", "marketingplatform.google.com", "mirror.co.uk", "wsj.com", "noaa.gov", "sputniknews.com", "yadi.sk", "sciencedaily.com", "google.co.in", "mozilla.com", "adssettings.google.com", "target.com", "theatlantic.com", "abc.net.au", "worldbank.org", "goodreads.com", "lefigaro.fr", "ca.gov", "sapo.pt", "kickstarter.com", "apache.org", "ru.wikipedia.org", "ign.com", "lemonde.fr", "picasa.google.com", "washington.edu", "walmart.com", "secureserver.net", "themeforest.net", "webmd.com", "sfgate.com", "photobucket.com", "imageshack.us", "hp.com", "rottentomatoes.com", "clickbank.net", "nypost.com", "lycos.com", "amazon.it", "weibo.com", "ikea.com", "ea.com", "cambridge.org", "sedo.com", "allaboutcookies.org", "nikkei.com", "ziddu.com", "gizmodo.com", "icann.org", "www.wikipedia.org", "asus.com", "netflix.com", "quora.com", "columbia.edu", "usnews.com", "metro.co.uk", "finance.yahoo.com", "home.neustar", "bandcamp.com", "espn.com", "doubleclick.net", "npr.org", "cornell.edu", "gofundme.com", "biglobe.ne.jp", "nationalgeographic.com", "alexa.com", "ytimg.com", "abc.es", "gooyaabitemplates.com", "ietf.org", "naver.com", "shutterstock.com", "google.co.id", "spotify.com", "m.wikipedia.org", "storage.googleapis.com", "shopify.com", "techcrunch.com", "cbc.ca", "nginx.com", "instagram.com", "researchgate.net", "thetimes.co.uk", "indiatimes.com", "code.google.com", "addtoany.com", "wiley.com", "mit.edu", "t.co", "gmail.com", "php.net", "sciencedirect.com", "elmundo.es", "pexels.com", "google.com.tw", "newyorker.com", "engadget.com", "mega.nz", "ted.com", "ox.ac.uk", "google.ca", "depositfiles.com", "dw.com", "playstation.com", "yandex.ru", "fb.me", "loc.gov", "smh.com.au", "discord.com", "ovh.com", "spiegel.de", "groups.google.com", "nokia.com", "surveymonkey.com", "pixabay.com", "instructables.com", "nydailynews.com", "google.nl", "disqus.com", "ggpht.com", "academia.edu", "latimes.com", "news.com.au", "privacyshield.gov", "amazon.es", "berkeley.edu", "huawei.com", "zoom.us", "mashable.com", "ipv4.google.com", "alibaba.com", "economist.com", "ovh.net", "newsweek.com", "afternic.com", "chicagotribune.com", "ibm.com", "fda.gov", "twitch.tv", "akamaihd.net", "amzn.to", "rambler.ru", "umich.edu", "nbcnews.com", "whitehouse.gov", "hm.com", "stanford.edu", "yahoo.co.jp", "wikihow.com", "tripadvisor.com", "addthis.com", "oup.com", "eventbrite.com", "unesco.org", "oracle.com", "wp.com", "detik.com", "disney.com", "bing.com", "nginx.org", "britannica.com", "rtve.es", "guardian.co.uk", "orange.fr", "ria.ru", "welt.de", "gnu.org", "4shared.com", "cnil.fr", "www.wix.com", "rt.com", "pl.wikipedia.org", "www.over-blog.com", "nature.com", "box.com", "cnbc.com", "bloglovin.com", "psychologytoday.com", "sciencemag.org", "godaddy.com", "urbandictionary.com", "yelp.com", "amazon.fr", "rapidshare.com", "pbs.org", "sendspace.com", "bitly.com", "tmz.com", "discord.gg", "zendesk.com", "forms.gle", "buzzfeed.com", "deezer.com", "theverge.com", "about.com", "ja.wikipedia.org", "express.co.uk", "mysql.com", "variety.com", "my.yahoo.com", "googleblog.com", "arxiv.org", "stackoverflow.com", "answers.yahoo.com", "wn.com", "cbslocal.com", "ads.google.com", "intel.com", "thehindu.com", "vice.com", "netlify.app", "xinhuanet.com", "wisc.edu", "archives.gov", "google.com.au", "www.livejournal.com", "debian.org", "bp1.blogger.com", "marketwatch.com", "megaupload.com", "undeveloped.com", "digg.com", "indiegogo.com", "si.edu", "ovh.co.uk", "ameblo.jp", "www.canalblog.com", "pcmag.com", "ucla.edu", "zeit.de", "bp2.blogger.com", "irs.gov", "dreniq.com", "excite.co.jp", "sony.com", "slate.com", "stuff.co.nz", "epa.gov", "fortune.com", "qq.com", "cafepress.com", "khanacademy.org", "thestar.com", "reverbnation.com", "kotaku.com", "salon.com", "insider.com", "amazon.in", "marriott.com", "so-net.ne.jp", "springer.com", "rollingstone.com", "sina.com.cn", "outlook.com", "merriam-webster.com", "video.google.com", "techradar.com", "inc.com", "thehill.com", "oreilly.com", "prezi.com", "newscientist.com", "tes.com", "channel4.com", "utexas.edu", "prnewswire.com", "20minutos.es", "a8.net", "cointernet.com.co", "politico.com", "weforum.org", "storage.canalblog.com", "eff.org", "usgs.gov", "dell.com", "house.gov", "xbox.com", "theglobeandmail.com", "statista.com", "amazon.ca", "nba.com", "histats.com", "gamestop.com", "behance.net", "searchenginejournal.com", "unsplash.com", "bund.de", "ndtv.com", "fifa.com", "cisco.com", "boston.com", "udemy.com", "greenpeace.org", "narod.ru", "jstor.org", "daum.net", "corriere.it", "axs.com", "iubenda.com", "com.com", "howstuffworks.com", "photos1.blogger.com", "airbnb.com", "qz.com", "oecd.org", "000webhost.com", "yandex.com", "ieee.org", "mailchimp.com", "nps.gov", "dribbble.com", "feedproxy.google.com", "espn.go.com", "wiktionary.org", "dreamstime.com", "ubuntu.com", "goo.ne.jp", "freepik.com", "naver.jp", "foursquare.com", "thedailybeast.com", "parallels.com", "xing.com", "upenn.edu", "g.co", "usc.edu", "over-blog-kiwi.com", "search.yahoo.com", "people.com", "scientificamerican.com", "psu.edu", "apnews.com", "stores.jp", "bp0.blogger.com", "hollywoodreporter.com", "doi.org", "weather.com" ]
#"

for num, i in enumerate(data):
    print(f"{str(num).zfill(3)}/{len(data)} trying...")
    try:
        payload = {"name": i, "url": f"https://{i}", "ports":[443]}
        print(payload)
        r = requests.post("http://127.0.0.1:8000/set/hosts", data=json.dumps(payload))
        print(r.text)
    except:
        print("   req error...")
