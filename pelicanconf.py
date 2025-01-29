AUTHOR = "Kevin O'Connor"
SITENAME = "Wow Great Stuff"
SITEURL = "https://writing.ohsh.it"

PATH = "content"
STATIC_PATHS = ["images", "CNAME", "extra"]
ARTICLE_PATHS = ["blog"]
PAGE_PATHS = ["pages"]
TIMEZONE = "America/New_York"

THEME = "themes/cid"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()

# Social widget
SOCIAL = (("Bluesky", "https://bsky.app/profile/ohsh.it"),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

ARTICLE_URL = "{date:%Y}/{date:%m}/{date:%d}/{slug}/"
ARTICLE_SAVE_AS = "{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html"
DRAFT_URL = "drafts/{slug}.html"
YEAR_ARCHIVE_SAVE_AS = "archives/{date:%Y}"
MONTH_ARCHIVE_SAVE_AS = "archives/{date:%Y}-{date:%m}"


EXTRA_PATH_METADATA = {
    "extra/favicon.ico": {"path": "favicon.ico"},
    "extra/bluesky.svg": {"path": "bluesky.svg"},
    "extra/rss.png": {"path": "rss.png"},
}

SITEFOOTER = '<a href="https://bsky.app/profile/ohsh.it"><img height="24" width="24" src="/bluesky.svg"></a> <a href="feeds/all.atom.xml"><img height="24" width="24" src="/rss.png"></a>'
