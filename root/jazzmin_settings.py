JAZZMIN_UI_TWEAKS = {
    # "theme": "darkly",
    # "theme": "slate",
    # "theme": "flatly",

}

JAZZMIN_SETTINGS = {
    # --- Asosiy ma’lumotlar ---
    "site_title": "Sof Mebel Admin",
    "site_header": "Sof Mebel Management",
    "site_brand": "Sof Mebel",
    "site_logo": "books/img/logo_xpress.png",
    "login_logo": "books/img/logo_xpress.png",
    "login_logo_dark": "books/img/logo_xpress.png",
    "site_logo_classes": "img-circle shadow-sm",
    "site_icon": "books/img/logo_xpress.png",
    "welcome_sign": "Welcome to Sof Mebel Dashboard",
    "copyright": "© 2012 Sof Mebel Company",
    "index_title": "Sof Mebel boshqaruv paneli",
    # --- Qidiruv ---
    "search_model": ["auth.User", "auth.Group"],

    # --- User avatar (yo‘q bo‘lsa None) ---
    "user_avatar": None,

    # --- Yuqori menyu (header bar) ---
    "topmenu_links": [
        {"name": "Sof Mebel", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Saytga o‘tish", "url": "/", "new_window": True},
        {"model": "auth.User"},
        {"app": "books"},
        {"name": "Documentation", "url": "https://docs.djangoproject.com/", "new_window": True},
        {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
    ],

    # --- User menyusi ---
    "usermenu_links": [
        {"model": "auth.user"},
        {"name": "GitHub Issues", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
    ],

    # --- Sidebar menyu sozlamalari ---
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": ["sessions"],  # keraksiz app’lar yashiriladi
    "hide_models": ["auth.Group"],  # misol uchun Group model yashirish
    "order_with_respect_to": ["books", "auth", "users"],

    "custom_links": {
        "books": [{
            "name": "Send Notifications",
            "url": "make_messages",
            "icon": "fas fa-paper-plane",
            "permissions": ["books.view_book"],
        }]
    },

    # --- Ikonalar ---
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "books": "fas fa-book",
        "books.book": "fas fa-book-open",
        "books.author": "fas fa-pen-fancy",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-dot-circle",

    # --- Modal o‘rniga popup ishlatish ---
    "related_modal_active": True,

    # --- UI Tweaks ---
    "custom_css": "books/css/custom_admin.css",
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,

    # --- Forma tartibi ---
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },

    # --- Qo‘shimcha (optional) ---
    "theme": "flatly",  # Jazzmin 3+ versiyalarida theme ishlaydi (bootstrap theme)
}