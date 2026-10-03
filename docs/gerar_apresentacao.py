# -*- coding: utf-8 -*-
"""Gera a apresentacao completa (PDF) do TrendZone AI OS."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, PageBreak, HRFlowable, Table, TableStyle
)
from reportlab.lib.enums import TA_CENTER

OUT = r"C:/TrendZone_AI_OS/docs/TrendZone_AIOS_Apresentacao_Completa.pdf"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Capa", fontSize=28, leading=34, alignment=TA_CENTER, textColor=colors.HexColor("#0B1120"), spaceAfter=10, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="CapaSub", fontSize=14, leading=18, alignment=TA_CENTER, textColor=colors.HexColor("#334155"), spaceAfter=6))
styles.add(ParagraphStyle(name="PageTitle", fontSize=18, leading=22, textColor=colors.HexColor("#0B1120"), fontName="Helvetica-Bold", spaceAfter=4))
styles.add(ParagraphStyle(name="Route", fontSize=10, leading=14, textColor=colors.HexColor("#2563EB"), fontName="Helvetica-Oblique", spaceAfter=6))
styles.add(ParagraphStyle(name="Subtitle", fontSize=11, leading=15, textColor=colors.HexColor("#475569"), fontName="Helvetica-Oblique", spaceAfter=8))
styles.add(ParagraphStyle(name="Body", fontSize=10.5, leading=15, textColor=colors.HexColor("#1E293B"), spaceAfter=6))
styles.add(ParagraphStyle(name="ItemStyle", fontSize=10, leading=14, textColor=colors.HexColor("#1E293B")))
styles.add(ParagraphStyle(name="SectionH", fontSize=12, leading=16, textColor=colors.HexColor("#0B1120"), fontName="Helvetica-Bold", spaceBefore=8, spaceAfter=4))
styles.add(ParagraphStyle(name="Nota", fontSize=9, leading=12, textColor=colors.HexColor("#64748B"), fontName="Helvetica-Oblique", spaceBefore=6))

PAGES = []


def add_page(numero, titulo, rota, subtitulo, descricao, itens, notas=None):
    PAGES.append({
        "numero": numero, "titulo": titulo, "rota": rota,
        "subtitulo": subtitulo, "descricao": descricao, "itens": itens, "notas": notas,
    })


def build_story():
    story = []

    story.append(Spacer(1, 6 * cm))
    story.append(Paragraph("TrendZone <font color='#F97316'>AI</font> OS", styles["Capa"]))
    story.append(Paragraph("Apresentacao Detalhada da Plataforma", styles["CapaSub"]))
    story.append(Paragraph("Guia completo de todas as abas, telas, botoes, campos e funcoes do sistema", styles["CapaSub"]))
    story.append(Spacer(1, 2 * cm))
    story.append(Paragraph("Documento gerado a partir do codigo-fonte atual da aplicacao  -  cada tela, botao e campo descrito abaixo reflete exatamente o que existe no sistema em producao.", styles["Nota"]))
    story.append(PageBreak())

    story.append(Paragraph("Sumario", styles["PageTitle"]))
    story.append(Spacer(1, 0.3 * cm))
    sumario_rows = [["#", "Pagina", "Rota"]]
    for p in PAGES:
        sumario_rows.append([str(p["numero"]), p["titulo"], p["rota"]])
    t = Table(sumario_rows, colWidths=[1.2 * cm, 9 * cm, 6 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B1120")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F1F5F9")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(t)
    story.append(PageBreak())

    for p in PAGES:
        story.append(Paragraph(f'{p["numero"]}. {p["titulo"]}', styles["PageTitle"]))
        story.append(Paragraph(f'Rota: {p["rota"]}', styles["Route"]))
        if p["subtitulo"]:
            story.append(Paragraph(p["subtitulo"], styles["Subtitle"]))
        story.append(HRFlowable(width="100%", thickness=0.7, color=colors.HexColor("#CBD5E1"), spaceAfter=8))
        if p["descricao"]:
            story.append(Paragraph(p["descricao"], styles["Body"]))
        if p["itens"]:
            bullets = [ListItem(Paragraph(it, styles["ItemStyle"]), leftIndent=10) for it in p["itens"]]
            story.append(ListFlowable(bullets, bulletType="bullet", start="•", leftIndent=14, spaceBefore=4, bulletFontSize=8))
        if p.get("notas"):
            story.append(Paragraph(p["notas"], styles["Nota"]))
        story.append(PageBreak())

    return story


def build_pdf():
    doc = SimpleDocTemplate(
        OUT, pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm, bottomMargin=1.8 * cm,
        title="TrendZone AI OS - Apresentacao Completa",
        author="TrendZone AI OS",
    )
    doc.build(build_story())
    print("PDF gerado em:", OUT)
