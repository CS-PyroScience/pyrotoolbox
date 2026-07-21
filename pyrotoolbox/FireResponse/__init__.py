def main():
    """Launch the FireResponse GUI.

    The GUI depends on the optional ``fireresponse`` dependency group
    (PyQt5, pyqtgraph). If those are not installed, print a helpful message
    instead of raising a raw ImportError.
    """
    try:
        from pyrotoolbox.FireResponse.FireResponse import main as _main
    except ImportError as e:
        raise SystemExit(
            "FireResponse requires the optional 'fireresponse' dependencies "
            "(PyQt5, pyqtgraph), which are not installed.\n"
            "Install them with:\n\n"
            "    pip install pyrotoolbox[fireresponse]\n\n"
            f"(original error: {e})"
        )
    _main()
