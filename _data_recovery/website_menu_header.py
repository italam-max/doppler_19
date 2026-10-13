# -*- coding: utf-8 -*-
"""
_data_recovery/website_menu_header.py
=====================================

Problema (detectado en staging 19, oct-2026):
  El upgrade 16 -> 19 dejó `website.menu_id` del sitio "Alamex" apuntando a
  "Jobs" (menú raíz huérfano sin hijos), así que el encabezado sale sin
  navegación. Además la plantilla trae el teléfono de ejemplo
  (+1 555-555-5556), carrito, wishlist y buscador que en 16 no se usan.

Qué hace (idempotente, se puede correr N veces):
  1. Lee de Odoo 16 (vía JSON-RPC) el árbol de menús del sitio, en en_US y es_MX,
     con URLs, orden, "abrir en nueva pestaña" y mega menús.
  2. Lo recrea en 19 bajo un menú raíz propio del website y lo deja como menú
     principal. Los registros que crea se marcan con xmlid
     __data_recovery__.website<W>_menu_<id16>; en cada corrida se actualizan
     y se borran los que ya no existan en 16. No toca ningún otro menú.
  3. Reemplaza el teléfono de ejemplo por el real.
  4. Apaga en el encabezado: carrito, wishlist y buscador (paridad con 16).

Uso (shell de Odoo.sh, desde la carpeta del repo doppler_19):
  export ODOO16_URL=https://www.alam.mx
  export ODOO16_DB=odoo13_backup_2024_12_14_09_55
  export ODOO16_LOGIN=italam@alam.mx
  read -rs ODOO16_KEY && export ODOO16_KEY     # API key de 16 (no se guarda)
  DRY_RUN=1 odoo-bin shell < _data_recovery/website_menu_header.py   # prueba
  odoo-bin shell < _data_recovery/website_menu_header.py             # aplica

Variables opcionales:
  ODOO19_WEBSITE_ID (default 1), ODOO16_WEBSITE_ID (default: mismo nombre),
  PHONE_DISPLAY (default "55 5532 2739"), PHONE_TEL (default "+525555322739"),
  HEADER_OFF (keys separadas por coma; vacío = no apagar nada).
"""
import json
import os
import urllib.request

DRY_RUN = os.environ.get("DRY_RUN") == "1"
URL16 = os.environ["ODOO16_URL"].rstrip("/")
DB16 = os.environ["ODOO16_DB"]
LOGIN16 = os.environ["ODOO16_LOGIN"]
KEY16 = os.environ["ODOO16_KEY"]
W = int(os.environ.get("ODOO19_WEBSITE_ID", "1"))
PHONE_DISPLAY = os.environ.get("PHONE_DISPLAY", "55 5532 2739")
PHONE_TEL = os.environ.get("PHONE_TEL", "+525555322739")
PLACEHOLDER = "+1 555-555-5556"
HEADER_OFF = [k.strip() for k in os.environ.get(
    "HEADER_OFF",
    "website_sale.header_cart_link,"
    "website_sale_wishlist.header_wishlist_link,"
    "website.header_search_box",
).split(",") if k.strip()]
XMOD = "__data_recovery__"
MENU_FIELDS = ["name", "url", "parent_id", "sequence", "new_window",
               "mega_menu_content", "mega_menu_classes"]


def log(msg):
    print("[website_menu_header] " + msg)


# ---------------------------------------------------------------- Odoo 16 RPC
def _rpc(service, method, *args):
    payload = {"jsonrpc": "2.0", "method": "call", "id": 1,
               "params": {"service": service, "method": method, "args": list(args)}}
    req = urllib.request.Request(URL16 + "/jsonrpc", data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        res = json.loads(resp.read())
    if res.get("error"):
        err = res["error"]
        raise RuntimeError((err.get("data") or {}).get("message") or err)
    return res["result"]


uid16 = _rpc("common", "authenticate", DB16, LOGIN16, KEY16, {})
if not uid16:
    raise RuntimeError("No se pudo autenticar en 16 (revisa login/API key)")


def call16(model, method, args, **kw):
    return _rpc("object", "execute_kw", DB16, uid16, KEY16, model, method, args, kw)


# ------------------------------------------------------------------- Contexto
website = env["website"].browse(W)
if not website.exists():
    raise RuntimeError("No existe el website %s en 19" % W)
langs19 = [code for code, _name in env["res.lang"].get_installed()]

sites16 = call16("website", "search_read", [[]], fields=["name", "menu_id"])
if os.environ.get("ODOO16_WEBSITE_ID"):
    site16 = next(s for s in sites16 if s["id"] == int(os.environ["ODOO16_WEBSITE_ID"]))
else:
    site16 = next((s for s in sites16 if s["name"] == website.name), sites16[0])
root16 = site16["menu_id"][0]
log("16: website '%s' (id %s), menú raíz %s" % (site16["name"], site16["id"], root16))

by_lang = {}
for lang in {"en_US", *langs19}:
    rows = call16("website.menu", "search_read", [[("id", "child_of", root16)]],
                  fields=MENU_FIELDS, context={"lang": lang})
    by_lang[lang] = {r["id"]: r for r in rows}
menus16 = by_lang["en_US"]
log("16: %s menús en el árbol" % (len(menus16) - 1))

# ------------------------------------------------------------ Helpers de 19
IMD = env["ir.model.data"].sudo()
Menu = env["website.menu"].sudo().with_context(lang="en_US")


def xml_name(suffix):
    return "website%s_menu_%s" % (W, suffix)


def ours(name):
    imd = IMD.search([("module", "=", XMOD), ("name", "=", name)], limit=1)
    return Menu.browse(imd.res_id).exists() if imd else Menu.browse()


def mark(name, rec):
    imd = IMD.search([("module", "=", XMOD), ("name", "=", name)], limit=1)
    if imd:
        imd.res_id = rec.id
    else:
        IMD.create({"module": XMOD, "name": name, "model": "website.menu",
                    "res_id": rec.id, "noupdate": True})


def upsert(name, vals):
    rec = ours(name)
    if rec:
        rec.write(vals)
    else:
        rec = Menu.create(vals)
        mark(name, rec)
    return rec


# ---------------------------------------------------------- 1. Árbol de menú
root = upsert(xml_name("root"), {"name": "Top Menu", "url": "/default-main-menu",
                                 "website_id": W, "parent_id": False})
seen = {xml_name("root")}

# Recorrido por niveles para que el padre siempre exista antes que el hijo
mapping = {root16: root}
pending = [m for m in menus16.values() if m["id"] != root16]
while pending:
    progressed = False
    for m in list(pending):
        parent16 = m["parent_id"] and m["parent_id"][0]
        if parent16 not in mapping:
            continue
        name = xml_name(m["id"])
        rec = upsert(name, {
            "name": m["name"],
            "url": m["url"] or "#",
            "sequence": m["sequence"],
            "new_window": m["new_window"],
            "website_id": W,
            "parent_id": mapping[parent16].id,
            "mega_menu_content": m.get("mega_menu_content") or False,
            "mega_menu_classes": m.get("mega_menu_classes") or False,
        })
        # Traducciones (solo si difieren del inglés)
        for lang in langs19:
            if lang == "en_US":
                continue
            tr = by_lang[lang].get(m["id"]) or {}
            vals = {}
            if tr.get("name") and tr["name"] != m["name"]:
                vals["name"] = tr["name"]
            if tr.get("mega_menu_content") and tr["mega_menu_content"] != m.get("mega_menu_content"):
                vals["mega_menu_content"] = tr["mega_menu_content"]
            if vals:
                rec.with_context(lang=lang).write(vals)
        mapping[m["id"]] = rec
        seen.add(name)
        pending.remove(m)
        progressed = True
    if not progressed:
        log("AVISO: %s menús sin padre alcanzable, se omiten: %s"
            % (len(pending), [p["name"] for p in pending]))
        break

# Limpieza: menús creados por este script en corridas previas que ya no están en 16
stale = IMD.search([("module", "=", XMOD), ("model", "=", "website.menu"),
                    ("name", "=like", xml_name("%")), ("name", "not in", list(seen))])
if stale:
    Menu.browse(stale.mapped("res_id")).exists().unlink()
    stale.unlink()
    log("Eliminados %s menús obsoletos de corridas previas" % len(stale))

# El menú principal del website es el primer raíz por (sequence, id): ponemos el nuestro primero
others = Menu.search([("website_id", "=", W), ("parent_id", "=", False), ("id", "!=", root.id)])
root.sequence = min([0] + others.mapped("sequence")) - 1
if others:
    log("Raíces que quedan sin usar (no se tocan): %s"
        % ", ".join("%s:%s" % (o.id, o.name) for o in others))

# ------------------------------------------------------ 2. Vistas del header
View = env["ir.ui.view"].sudo().with_context(active_test=False)


def website_view(key):
    views = View.search([("key", "=", key), ("website_id", "in", [W, False])])
    return views.filtered(lambda v: v.website_id.id == W)[:1] or views[:1]


def write_for_website(view, vals, lang="en_US"):
    # Con website_id en contexto, Odoo hace copy-on-write: la vista genérica no se toca
    view.with_context(website_id=W, lang=lang).write(vals)


# Teléfono
phone_keys = set(View.search([("arch_db", "ilike", PLACEHOLDER),
                              ("website_id", "in", [W, False])]).mapped("key"))
for key in phone_keys:
    for lang in ["en_US"] + [l for l in langs19 if l != "en_US"]:
        v = website_view(key)
        arch = v.with_context(lang=lang).arch_db or ""
        if PLACEHOLDER not in arch:
            continue
        new = (arch.replace("tel:" + PLACEHOLDER, "tel:" + PHONE_TEL)
                   .replace(PLACEHOLDER, PHONE_DISPLAY))
        write_for_website(v, {"arch_db": new}, lang)
    log("Teléfono actualizado en vista %s" % key)

# Elementos del header que no se usan
for key in HEADER_OFF:
    v = website_view(key)
    if not v:
        log("Vista %s no existe, se omite" % key)
    elif v.active or not v.website_id:
        write_for_website(v, {"active": False})
        log("Apagada en el header: %s" % key)

# ---------------------------------------------------------------- Verificación
env.registry.clear_cache()
website.invalidate_recordset()
top = website.menu_id
log("Menú principal del website %s: %s (id %s)" % (W, top.name, top.id))
for child in top.child_id.sorted("sequence"):
    es = child.with_context(lang="es_MX").name if "es_MX" in langs19 else child.name
    log("  - %s%s" % (es, "  [mega menú]" if child.is_mega_menu else
                       "  (%s submenús)" % len(child.child_id) if child.child_id else ""))

if DRY_RUN:
    env.cr.rollback()
    log("DRY_RUN: cambios revertidos")
else:
    env.cr.commit()
    log("Cambios aplicados")
