def export_to_pdf(text, filename='report.pdf'):
    with open(filename, 'w') as f:
        f.write(text)
