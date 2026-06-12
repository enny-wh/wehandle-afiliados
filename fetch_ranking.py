import os
import json
import requests
import time
from datetime import datetime, timezone
from collections import defaultdict

SYMPLA_TOKEN = os.environ["SYMPLA_TOKEN"]
EVENT_ID     = os.environ["SYMPLA_EVENT_ID"]

BASE_URL = "https://api.sympla.com.br/public/v3"
HEADERS  = {"s_token": SYMPLA_TOKEN}

AFFILIATES = {
    "ADRIANAGT360": "Adriana Chigueira",
    "ADRIANOGT360": "Adriano Dutra",
    "AFONSOGT360": "Afonso Brunelli Ferragut",
    "ALISSSONGT360": "Alisson Vasconcelos Dos Santos",
    "ANAGT360": "Ana Paula Simões Pessoa",
    "ANDREIAGT360": "Andreia Alves De Andrade",
    "ANDRESSAGT360": "Andressa Nozue",
    "ANNAGT360": "Anna Elisa Sarti",
    "ANTONIOGT360": "Antonio Messias Ferreira Da Silva",
    "ARTHURGT360": "Arthur Avila Tobias",
    "AUGUSTOGT360": "Augusto Macedo",
    "BEATRIZGT360": "Beatriz De Almeida Estevam Silva",
    "BRENDAGT360": "Brenda Ione Zeferino Macedo",
    "BRUNAGT360": "Bruna Stefany Da Silva Dos Santos",
    "BRUNOGT360": "Bruno Lopes Melo Fonseca",
    "CAIOEGT360": "Caio Etsuo Sagae",
    "CAIORGT360": "Caio Ribeiro Mello",
    "CAIOVGT360": "Caio Vasconcelos Araujo Figueiredo",
    "CAMILAGT360": "Camila Raphaela Peres Mancio",
    "CAMILLAGT360": "Camilla Leite",
    "CARLALGT360": "Carla Luisa Tognoli Ruy Mancinelli",
    "CARLASGT360": "Carla Stefany Santos",
    "CAROLINEGT360": "Caroline Souza Yoneda",
    "CAROLYNEGT360": "Carolyne Pesth Colcheski Ramos",
    "CASSIAGT360": "Cassia Patricia Dos Santos Brasileiro",
    "DANIELGT360": "Daniel Dos Reis Rodrigues",
    "DANILOGT360": "Danilo Pereira De Souza",
    "DEBORAGT360": "Debora Cristina Tagliarini",
    "DEYVIDGT360": "Deyvid Kenedy Santos",
    "DIOGOGT360": "Diogo Afonso Chaves",
    "MATHEOGT360": "Matheo Lima",
    "DOMINYКEGT360": "Dominyke Swriel Goncalves Cipriano",
    "EDGARGT360": "Edgar Berg",
    "EDILAINEGT360": "Edilaine Dos Santos Silva",
    "EDUARDAGT360": "Eduarda Santos De Castro",
    "ELENICEGT360": "Elenice De Fatima Pereira",
    "EMERSONGT360": "Emerson Dos Santos Couto",
    "ERICAGT360": "Erica De Oliveira Goncalves Bueno",
    "ERICKGT360": "Erick Goncalves Cabral",
    "EZEQUIELGT360": "Ezequiel Saides Silva",
    "FABIOGT360": "Fabio Yukio Yokota",
    "FELIPEGT360": "Felipe Dos Santos Freire",
    "FERNANDAGT360": "Fernanda Faustini Brossi",
    "FERNANDOGT360": "Fernando Iwano",
    "FILIPEGT360": "Filipe Costa",
    "FLAVIAGT360": "Flavia Goncalves Martins Alves",
    "GABRIELDIGGT360": "Gabriel Dias Cardoso Poleselli De Souza",
    "GABRIELSCGT360": "Gabriel Schroder De Paula",
    "GABRIELSIGT360": "Gabriel Silveira",
    "GENAINAGT360": "Genaina Patricia Lopes",
    "GESSICAGT360": "Gessica Mendes Diniz",
    "GILSONGT360": "Gilson Souza",
    "GUILHERMERGT360": "Guilherme Rohrer Gaudencio",
    "GUILHERMETGT360": "Guilherme Tadeu De Oliveira",
    "GUSTAVOOGT360": "Gustavo De Oliveira Martins",
    "GUSTAVOGGT360": "Gustavo Garcia Martin",
    "HUGOGT360": "Hugo Penna",
    "IASMINGT360": "Iasmin Ketelin Moll Carneiro",
    "IGORGT360": "Igor Sales",
    "IONITAGT360": "Ionita Correa Do Nascimento Soares De Amorim",
    "ISABELLAGT360": "Isabella Victoria Moreira De Souza Neves",
    "ISAQUIELGT360": "Isaquiel Rosendo De Oliveira Junior",
    "JANAINAGT360": "Janaina Da Costa Barros Lima",
    "JOSEGGT360": "Jose Gleyson Isidoro Alves Da Silva",
    "JOSEHGT360": "Jose Hilton De Luna Junior",
    "JULIACGT360": "Julia Caldeira De Oliveira Tezani",
    "JULIAOGT360": "Julia Oliveira",
    "JULIANASILGT360": "Juliana Da Silveira Oliveira",
    "JULIANALOPGT360": "Juliana Lopes Parente",
    "JULIANASIMGT360": "Juliana Simoes",
    "JULIOGT360": "Julio Manarin Bettini Rodrigues",
    "KARLAGT360": "Karla Silva Lobo",
    "KAUANGT360": "Kauan Felipe Araujo Dos Santos",
    "KAUANEGT360": "Kauane Caroline Lichtenfelz",
    "KELVINGT360": "Kelvin Luciano Cangucu Martins",
    "KEVENGT360": "Keven Lucas Da Silva Jesus",
    "LAISGT360": "Lais Alvarenga Oliveira",
    "LARAGT360": "Lara De Lima Esteves",
    "LARESSAGT360": "Laressa Pereira Lessa Reis",
    "LARISSABGT360": "Larissa Baldin Dos Santos",
    "LARISSARGT360": "Larissa Ribeiro Martins",
    "LAVINIAGT360": "Lavinia Pereira Soares",
    "LEILAGT360": "Leila Cristina De Proenca Dias",
    "LEONARDOGT360": "Leonardo Antonio Pinheiro",
    "LETICIAGT360": "Leticia Nunes Camillo",
    "LEVYGT360": "Levy Cruz",
    "LOHAINEGT360": "Lohaine Taise De Moraes",
    "LUANCGT360": "Luan Caio Silva Miranda",
    "LUANVGT360": "Luan Vasconcelos Araujo Figueiredo",
    "LUCASAGT360": "Lucas Alves Carvalho",
    "LUCASOGT360": "Lucas Orsolini",
    "LUIGIGT360": "Luigi Galderisi",
    "MARCELAGT360": "Marcela Barbara Candian Silva",
    "MARCELOGT360": "Marcelo Mendes",
    "MARCIOGT360": "Marcio Dantas",
    "MARCOSGT360": "Marcos De Jesus Pereira",
    "MARCUSGT360": "Marcus Vinicius Capelato Dos Santos",
    "MARIAGT360": "Maria Eduarda Dias Diniz Malheiros",
    "MARIANACGT360": "Mariana Croce Campos",
    "MARIANAEGT360": "Mariana Elisa De Souza Nascimento",
    "MARIANAPGT360": "Mariana Pinheiro Melo",
    "MARINARAGT360": "Marinara Goes Da Silva",
    "MARYANAGT360": "Maryana Alves",
    "MATHEUSGT360": "Matheus Gabriel Sa De Souza",
    "MAYARAFGT360": "Mayara Ferreira Chaves",
    "MAYARASGT360": "Mayara Spangara Romero",
    "MERIELLYGT360": "Merielly Pereira Alves",
    "MICHAELAGT360": "Michael Alessandro De Souza",
    "MICHAELBGT360": "Michael De Barros Borges",
    "NATALIACGT360": "Natalia Cristina De Castro",
    "NATALIAGGT360": "Natalia Gomes Diotto",
    "NATHALIAGT360": "Nathalia Barros Leal Costa Dos Santos",
    "NICOLASGT360": "Nicolas Matheus Guimaraes Reis",
    "PATRICIAMGT360": "Patricia Miranda Neves",
    "PATRICIARGT360": "Patricia Ribeiro De Souza Nania",
    "PAULOGT360": "Paulo Vitor Santos Souza",
    "PEDROCGT360": "Pedro Cunha Canto Marques",
    "PEDROLGT360": "Pedro Luis Capelato Santos",
    "RAFAELGT360": "Rafael Reis",
    "RAFAELACGT360": "Rafaela Cezarino",
    "RAFAELAPGT360": "Rafaela Papale",
    "RAULGT360": "Raul Vieira Tamburo",
    "RAYANEGT360": "Rayane Jordan Da Silva Monteiro",
    "REGINAGT360": "Regina Suzarte Dos Santos",
    "RIANGT360": "Rian Alves Xavier",
    "RICARDOLGT360": "Ricardo Luis Bueno Junior",
    "RICARDORGT360": "Ricardo Rezende",
    "RODRIGOGT360": "Rodrigo Faustini Vieira",
    "ROMEIKAGT360": "Romeika Maria Alves De Melo Silva",
    "ROSSANAGT360": "Rossana Pikussa",
    "SAYURIGT360": "Sayuri Pimentel De Queiroz",
    "STEFFANYGT360": "Steffany Lopes De Oliveira",
    "STEPHANYGT360": "Stephany Bianca Manfredo",
    "SUELENGT360": "Suelen Araujo Vieira",
    "TAMIRISGT360": "Tamiris Dias",
    "THAISCHGT360": "Thais Chaves Costa",
    "THAISCRGT360": "Thais Cristine Manoel Santos",
    "THIAGOGT360": "Thiago Kiyoki Hanashiro",
    "TIAGOGT360": "Tiago Henrique Marson",
    "VINICIUSGT360": "Vinicius Rafael Cunha",
    "VITOREGT360": "Vitor Emanuel Clementino Ramos Cardoso",
    "VITORMGT360": "Vitor Martins Oliveira",
    "VITORIAGT360": "Vitoria De Lima Santos",
    "WELLINGTONGT360": "Wellington Marques",
    "WILLIANGT360": "Willian Do Carmo De Franca",
    "YUKARIGT360": "Yukari Fukakusa",
    "YURIGT360": "Yuri Enny",
}

TOMADOR_VALUES   = {"contrata serviços terceirizados"}
FORNECEDOR_VALUES = {"fornece serviços terceirizados", "fornece e subcontrata serviços terceirizados"}

def cf(custom_form, field_name):
    """Extrai valor de um campo do custom_form pelo nome."""
    for f in (custom_form or []):
        if f.get("name","").lower() == field_name.lower():
            return f.get("value","")
    return ""

def classify_profile(natureza):
    n = natureza.strip().lower()
    if n in TOMADOR_VALUES:
        return "Tomador"
    if n in FORNECEDOR_VALUES:
        return "Fornecedor"
    return "Outro"

def parse_coupon(raw):
    if not raw:
        return ""
    return raw.split(" - ", 1)[-1].strip().upper()

def fetch_all_orders():
    orders = []
    page = 1
    while True:
        url = f"{BASE_URL}/events/{EVENT_ID}/orders?page={page}&page_size=100"
        resp = requests.get(url, headers=HEADERS)
        resp.raise_for_status()
        data = resp.json()
        orders.extend(data.get("data", []))
        if not data.get("pagination", {}).get("has_next", False):
            break
        page += 1
    return orders

def fetch_all_participants():
    participants = []
    page = 1
    while True:
        url = f"{BASE_URL}/events/{EVENT_ID}/participants?page={page}&page_size=100"
        resp = requests.get(url, headers=HEADERS)
        resp.raise_for_status()
        data = resp.json()
        participants.extend(data.get("data", []))
        if not data.get("pagination", {}).get("has_next", False):
            break
        page += 1
        time.sleep(0.15)
    return participants

def build_summary(orders, participants):
    # --- Resumo de pedidos ---
    total_orders       = len(orders)
    total_revenue      = sum(float(o.get("order_total_sale_price", 0)) for o in orders)
    approved_orders    = [o for o in orders if o.get("order_status") == "A"]
    pending_orders     = [o for o in orders if o.get("order_status") != "A"]
    approved_revenue   = sum(float(o.get("order_total_sale_price", 0)) for o in approved_orders)
    pending_revenue    = sum(float(o.get("order_total_sale_price", 0)) for o in pending_orders)

    # --- Pedidos por tipo de ingresso (via participantes) ---
    ticket_types = defaultdict(lambda: {"count": 0, "revenue": 0.0})
    for p in participants:
        tname = p.get("ticket_name", "Outro")
        ticket_types[tname]["count"]   += 1
        ticket_types[tname]["revenue"] += float(p.get("ticket_sale_price", 0))

    tickets_by_type = [
        {"name": k, "count": v["count"], "revenue": round(v["revenue"], 2)}
        for k, v in sorted(ticket_types.items(), key=lambda x: -x[1]["count"])
    ]

    # --- Lista de participantes ---
    participant_list = []
    for p in participants:
        cf_data    = p.get("custom_form", [])
        natureza   = cf(cf_data, "Natureza da empresa")
        participant_list.append({
            "name":        f"{p.get('first_name','')} {p.get('last_name','')}".strip(),
            "email":       p.get("email",""),
            "cargo":       cf(cf_data, "Cargo"),
            "empresa":     cf(cf_data, "Empresa"),
            "natureza":    natureza,
            "perfil":      classify_profile(natureza),
            "ticket_name": p.get("ticket_name",""),
            "ticket_price":float(p.get("ticket_sale_price", 0)),
            "status":      "Aprovado" if p.get("order_status") == "A" else "Pendente",
            "order_id":    p.get("order_id",""),
        })

    return {
        "orders": {
            "total":            total_orders,
            "total_revenue":    round(total_revenue, 2),
            "approved":         len(approved_orders),
            "approved_revenue": round(approved_revenue, 2),
            "pending":          len(pending_orders),
            "pending_revenue":  round(pending_revenue, 2),
        },
        "tickets_by_type": tickets_by_type,
        "participants":    participant_list,
    }

def build_ranking(orders, participants):
    # Agrupa participantes por order_id para contagem eficiente
    parts_by_order = defaultdict(list)
    for p in participants:
        parts_by_order[p.get("order_id","")].append(p)

    stats = defaultdict(lambda: {"tickets": 0, "revenue": 0.0})
    for order in orders:
        coupon = parse_coupon(order.get("discount_code",""))
        if coupon not in AFFILIATES:
            continue
        for p in parts_by_order[order["id"]]:
            stats[coupon]["tickets"] += 1
            stats[coupon]["revenue"] += float(p.get("ticket_sale_price", 0))

    ranking = []
    for code, s in stats.items():
        ranking.append({"code": code, "name": AFFILIATES[code],
                        "tickets": s["tickets"], "revenue": round(s["revenue"], 2)})
    for code, name in AFFILIATES.items():
        if code not in stats:
            ranking.append({"code": code, "name": name, "tickets": 0, "revenue": 0.0})

    ranking.sort(key=lambda x: x["tickets"], reverse=True)
    for i, item in enumerate(ranking):
        item["position"] = i + 1
    return ranking

def main():
    print("Buscando pedidos da Sympla (v3)...")
    orders = fetch_all_orders()
    print(f"Total de pedidos: {len(orders)}")

    print("Buscando participantes...")
    participants = fetch_all_participants()
    print(f"Total de participantes: {len(participants)}")

    summary = build_summary(orders, participants)
    ranking = build_ranking(orders, participants)

    total_tickets = sum(r["tickets"] for r in ranking)
    total_revenue = round(sum(r["revenue"] for r in ranking), 2)

    output = {
        "updated_at":    datetime.now(timezone.utc).isoformat(),
        "event_id":      EVENT_ID,
        "total_tickets": total_tickets,
        "total_revenue": total_revenue,
        "summary":       summary,
        "ranking":       ranking,
    }

    os.makedirs("data", exist_ok=True)
    with open("data/ranking.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nAtualizado! {len(participants)} participantes · {total_tickets} via afiliado · R$ {total_revenue:,.2f}")
    for item in ranking[:3]:
        if item["tickets"] > 0:
            print(f"  #{item['position']} {item['name']}: {item['tickets']} ingressos · R$ {item['revenue']:,.2f}")

if __name__ == "__main__":
    main()
