from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)

from reportlab.lib.styles import getSampleStyleSheet

import datetime


def create_report(
    output_file,
    image_path,
    nama,
    confidence,
    kategori,
    deskripsi,
    solusi
):

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(output_file)

    story = []

    story.append(
        Paragraph("<b>COCOAVISION AI</b>", styles["Title"])
    )

    story.append(
        Paragraph(
            "Laporan Deteksi Hama dan Penyakit Buah Kakao",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1,20))

    story.append(
        Paragraph(
            f"Tanggal : {datetime.datetime.now()}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1,20))

    story.append(
        Paragraph(f"<b>Nama :</b> {nama}", styles["Normal"])
    )

    story.append(
        Paragraph(f"<b>Confidence :</b> {confidence:.2%}", styles["Normal"])
    )

    story.append(
        Paragraph(f"<b>Kategori :</b> {kategori}", styles["Normal"])
    )

    story.append(Spacer(1,15))

    story.append(
        Paragraph("<b>Deskripsi</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(deskripsi, styles["Normal"])
    )

    story.append(Spacer(1,15))

    story.append(
        Paragraph("<b>Rekomendasi</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(solusi, styles["Normal"])
    )

    story.append(Spacer(1,20))

    story.append(
        Image(image_path, width=400, height=300)
    )

    doc.build(story)