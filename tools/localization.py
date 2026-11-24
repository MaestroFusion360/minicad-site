"""Russian UI strings and relative URLs for the shared site template."""

import html
from html.parser import HTMLParser

SOURCE_NAMES = {
    "Черчение": "2D CAD",
    "Командная строка": "CLI",
    "Оформление чертежей": "Technical Drawings",
    "3D-моделирование": "3D View",
    "Фрезерная обработка": "Milling CAM",
    "Библиотека инструментов": "Tool Library",
    "Токарная обработка": "Turning CAM",
    "Симуляция токарной обработки": "Turning Simulation",
    "Раскрой": "Cutting CAM",
    "Инструменты и управляющие программы": "CAM Tools, NC and Playback",
    "Ограничения": "Limitations",
}

RU = {
    "2D CAD": "Черчение",
    "CLI": "Командная строка",
    "Technical Drawings": "Оформление чертежей",
    "3D View": "3D-моделирование",
    "Milling CAM": "Фрезерная обработка",
    "Tool Library": "Библиотека инструментов",
    "Turning CAM": "Токарная обработка",
    "Turning Simulation": "Симуляция токарной обработки",
    "Cutting CAM": "Раскрой",
    "Tools, NC & Playback": "Инструменты и УП",
    "Explore capabilities": "Подробнее о возможностях",
    "Main workspace": "Основное рабочее пространство",
    "Skip to content": "К содержимому",
    "MiniCAD home": "MiniCAD — главная",
    "Menu": "Меню",
    "Main navigation": "Основная навигация",
    "Overview": "Обзор",
    "Features": "Возможности",
    "Limitations": "Ограничения",
    "Documentation": "Документация",
    "CAD, 3D modeling and CAM in one application.": "CAD, 3D-моделирование и CAM в одном приложении.",
    "MiniCAD combines 2D drafting and technical drawings, direct B-Rep solid modeling, CNC toolpaths for milling, turning and cutting, and a command-line interface.": "MiniCAD объединяет 2D-черчение и оформление технических чертежей, прямое твердотельное моделирование B-Rep, траектории фрезерной, токарной обработки и раскроя, а также командную строку.",
    "See MiniCAD in action": "Посмотреть MiniCAD",
    "Browse capabilities": "Изучить возможности",
    "Inside MiniCAD": "Возможности MiniCAD",
    "Feature reference": "Справочник возможностей",
    "Search capabilities": "Поиск возможностей",
    "Search features, formats, operations…": "Поиск возможностей, форматов, операций…",
    "Area": "Раздел",
    "All areas": "Все разделы",
    "Clear": "Сбросить",
    "Matching capabilities": "Найденные возможности",
    "Expand all": "Развернуть всё",
    "Collapse all": "Свернуть всё",
    "No matching features. Try another search.": "Ничего не найдено. Измените запрос.",
    "2D drafting, solid modeling and CNC toolpaths.": "Черчение, твердотельное моделирование и подготовка обработки на ЧПУ.",
    "Website license (MIT)": "Лицензия сайта (MIT)",
    "Image or video preview": "Просмотр изображения или видео",
    "Close preview": "Закрыть просмотр",
    "Open original ↗": "Открыть оригинал ↗",
    "Screenshot placeholder": "Место для скриншота",
    "Language": "Язык",
}


def translate(value: str) -> str:
    """Translate interface strings, leaving technical source content intact."""
    if value in RU:
        return RU[value]
    for prefix, translated in (
        ("Preview: ", "Просмотр: "),
        ("Screenshot placeholder: ", "Место для скриншота: "),
        ("MiniCAD — ", "MiniCAD — "),
    ):
        if value.startswith(prefix):
            return translated + translate(value[len(prefix) :])
    if value.endswith(" — Features and Limitations"):
        return (
            value.removesuffix(" — Features and Limitations")
            + " — Возможности и ограничения"
        )
    if value.startswith("MiniCAD ") and ": 2D CAD, technical drawings," in value:
        return (
            value.split(":", 1)[0]
            + ": 2D CAD, чертежи, B-Rep моделирование, фрезерная и токарная обработка, раскрой и командная строка. Возможности и ограничения."
        )
    if (
        value
        == "MiniCAD features and limitations: 2D CAD, 3D View, Milling, Turning, Cutting, and CLI."
    ):
        return "Возможности и ограничения MiniCAD: 2D CAD, 3D-моделирование, фрезерная и токарная обработка, раскрой и командная строка."
    return value


class RussianPage(HTMLParser):
    """Localize template text and attributes without rewriting Markdown terms."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_decl(self, decl):
        self.parts.append(f"<!{decl}>")

    def handle_comment(self, data):
        self.parts.append(f"<!--{data}-->")

    def start_tag(self, tag, attrs, closing=""):
        localized = []
        for key, value in attrs:
            if value is not None:
                if tag == "html" and key == "lang":
                    value = "ru"
                elif (
                    key in {"href", "src"}
                    and value
                    and not value.startswith(
                        ("#", "/", "http:", "https:", "data:", "mailto:")
                    )
                ):
                    if value == "features.md":
                        value = "features_ru.md"
                    value = "../" + value
                elif key in {
                    "alt",
                    "aria-label",
                    "placeholder",
                    "title",
                    "content",
                    "data-caption",
                    "data-matching",
                    "data-idle",
                }:
                    value = translate(value)
                localized.append(f' {key}="{html.escape(value, quote=True)}"')
            else:
                localized.append(f" {key}")
        self.parts.append(f"<{tag}{''.join(localized)}{closing}>")

    def handle_starttag(self, tag, attrs):
        self.start_tag(tag, attrs)

    def handle_startendtag(self, tag, attrs):
        self.start_tag(tag, attrs, " /")

    def handle_endtag(self, tag):
        self.parts.append(f"</{tag}>")

    def handle_data(self, data):
        stripped = data.strip()
        if stripped:
            data = data.replace(stripped, translate(stripped), 1)
        self.parts.append(html.escape(data, quote=False))


def localize_page(document: str) -> str:
    parser = RussianPage()
    parser.feed(document)
    parser.close()
    return "".join(parser.parts)
