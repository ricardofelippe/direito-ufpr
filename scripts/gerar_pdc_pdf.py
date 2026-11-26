import json, os
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, Table, TableStyle

with open("dados/procedimentos.json", encoding="utf-8") as f:
    data = json.load(f)
pdc = data["pdc"]
out = pdc.get("pdf_url", "docs/PDC_Direito_UFPR_v2.0.pdf")
os.makedirs(os.path.dirname(out), exist_ok=True)
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverX", parent=styles["Title"], fontSize=20, leading=25, alignment=TA_CENTER, textColor=colors.HexColor("#12304a"), spaceAfter=12))
styles.add(ParagraphStyle(name="SubX", parent=styles["Normal"], fontSize=10, leading=14, alignment=TA_CENTER, textColor=colors.HexColor("#536779"), spaceAfter=16))
styles.add(ParagraphStyle(name="H1X", parent=styles["Heading1"], fontSize=14, leading=18, textColor=colors.HexColor("#12304a"), spaceBefore=12, spaceAfter=6))
styles.add(ParagraphStyle(name="H2X", parent=styles["Heading2"], fontSize=10, leading=13, textColor=colors.HexColor("#087f89"), spaceBefore=8, spaceAfter=4))
styles.add(ParagraphStyle(name="BodyX", parent=styles["BodyText"], fontSize=8.5, leading=12, spaceAfter=5))
story = [Spacer(1, 1*cm), Paragraph("PLANO DE CONTINUIDADE DO PROJETO", styles["CoverX"]), Paragraph(pdc.get("titulo","Plataforma de Estudos — Direito UFPR"), styles["SubX"]), Paragraph("Versão %s · Atualizado em %s<br/>Documento de transição técnica e operacional para retomada em outra conversa ou IA." % (pdc.get("versao",""), pdc.get("atualizado_em","")), styles["SubX"])]
for sec in pdc.get("conteudo_completo", []):
    story.append(Paragraph(sec.get("titulo",""), styles["H1X"]))
    for para in sec.get("paragrafos", []): story.append(Paragraph(para.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"), styles["BodyX"]))
    if sec.get("tabela"):
        rows = [[Paragraph(str(c), styles["BodyX"]) for c in row] for row in sec["tabela"]]
        t = Table(rows, repeatRows=1, colWidths=[5.0*cm, 11.0*cm])
        t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#e7eef4")),("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#aab8c5")),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5)]))
        story.extend([t, Spacer(1,6)])
    if sec.get("itens"):
        story.append(ListFlowable([ListItem(Paragraph(x, styles["BodyX"])) for x in sec["itens"]], bulletType="bullet", leftIndent=14))
    for sub in sec.get("subtitulos", []):
        story.append(Paragraph(sub.get("titulo",""), styles["H2X"]))
        if sub.get("texto"): story.append(Paragraph(sub["texto"], styles["BodyX"]))
    if sec.get("destaque"):
        story.append(Paragraph("<b>REGRA PERMANENTE</b><br/>"+sec["destaque"], styles["BodyX"]))
    for para in sec.get("paragrafos_finais", []): story.append(Paragraph(para, styles["BodyX"]))
story.append(Spacer(1,8))
story.append(Paragraph("Histórico de versões", styles["H1X"]))
for item in pdc.get("historico", []): story.append(Paragraph(item, styles["BodyX"]))
story.append(Paragraph("Referência do projeto: https://ricardofelippe.github.io/Direito-UFPR/", styles["BodyX"]))
def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica",7)
    canvas.setFillColor(colors.HexColor("#65788a"))
    canvas.drawString(1.8*cm,0.9*cm,"PDC Direito UFPR · v"+pdc.get("versao",""))
    canvas.drawRightString(A4[0]-1.8*cm,0.9*cm,"Página %d"%doc.page)
    canvas.restoreState()
SimpleDocTemplate(out,pagesize=A4,rightMargin=1.8*cm,leftMargin=1.8*cm,topMargin=1.6*cm,bottomMargin=1.6*cm).build(story,onFirstPage=footer,onLaterPages=footer)
print("PDF gerado:",out)
