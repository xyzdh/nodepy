try:
    import nodepy
except:
    import sys
    sys.path.append("..")
    try:
        import nodepy
    except:
        print("Can't import nodepy")
        sys.exit()

from module import load
