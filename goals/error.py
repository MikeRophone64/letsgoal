def catch(*args):
    print("===============================")
    if args:
        for item in args:
            print(">>> " + str(item))
    else:
        print(">>> error")
    print("===============================")