#导入 路径。每个 测试例 都要 import 此文件(import init),实在 用不到，就 不引 就是了
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