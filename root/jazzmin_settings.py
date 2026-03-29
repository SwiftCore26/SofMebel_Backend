JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
}

JAZZMIN_SETTINGS = {
    # --- Asosiy ma'lumotlar ---
    "site_title": "Sof Mebel Admin",
    "site_header": "Sof Mebel Management",
    "site_brand": "Sof Mebel",
    "site_logo": None,           # logo rasm bo'lsa: "img/logo.png"
    "login_logo": None,
    "login_logo_dark": None,
    "site_logo_classes": "img-circle shadow-sm",
    "site_icon": None,
    "welcome_sign": "Sof Mebel boshqaruv paneliga xush kelibsiz!",
    "copyright": "© 2026 Sof Mebel",
    "index_title": "Sof Mebel boshqaruv paneli",

    # --- Qidiruv ---
    "search_model": ["apps.User"],

    # --- User avatar ---
    "user_avatar": None,

    # --- Yuqori menyu ---
    "topmenu_links": [
        {"name": "Bosh sahifa", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Saytga o'tish", "url": "/", "new_window": True},
    ],

    # --- User menyusi ---
    "usermenu_links": [
        {"name": "Profil", "url": "admin:apps_user_change", "permissions": ["auth.view_user"]},
    ],

    # --- Sidebar ---
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": ["auth", "sessions"],
    "hide_models": [],
    "order_with_respect_to": [
        "apps.User",
        "apps.Order",
        "apps.Product",
        "apps.Category",
        "apps.TelegramGroup",
        "apps.Contact",
        "apps.Footer",
    ],

    "custom_links": {},

    # --- Ikonalar ---
    "icons": {
        "apps":                  "fas fa-layer-group",
        "apps.User":             "fas fa-user",
        "apps.Order":            "fas fa-shopping-cart",
        "apps.OrderItem":        "fas fa-list",
        "apps.Product":          "fas fa-couch",
        "apps.Category":         "fas fa-tags",
        "apps.TelegramGroup":    "fab fa-telegram",
        "apps.Contact":          "fas fa-envelope",
        "apps.Footer":           "fas fa-link",
    },
    "default_icon_parents":  "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-dot-circle",

    # --- Modal ---
    "related_modal_active": True,

    # --- UI ---
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,

    # --- Forma tartibi ---
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {},
}