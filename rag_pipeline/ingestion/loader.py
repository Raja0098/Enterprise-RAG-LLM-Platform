from pdf2image import convert_from_path

def pdf_to_images(pdf_path: str):
    try:
        return convert_from_path(
            pdf_path,
            dpi=400,
            fmt="png",
            thread_count=6,
            grayscale=False,
            use_pdftocairo=True,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to convert PDF to images: {e}")