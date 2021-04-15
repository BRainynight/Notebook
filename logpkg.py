import logging, sys
def get_logger(rootName="__main__", child="", logfileName="record"):
    '''
    直接使用 get_logger ，返回的 logger 不會有層級。
    1. 根據程式的 package 層級自動設定：要包括參數整行複製去用：get_logger(rootName="__main__", child=__name__)
    2. 自定義層級：同時覆蓋 rootName, child 自己寫層級架構。get_logger(rootName="parent", child="child1.child2)
    3. 不使用層級：rootName 可自由選擇是否更改，但 child 請設為空 get_logger(rootName="__main__", child="")
    '''
    if not child:
        logName = rootName
    else:
        logName = rootName+"."+child
    print("Your Log name is ", logName)
    logger = logging.getLogger(logName) 
    logger.setLevel(logging.DEBUG)

    # file handler
    fh = logging.FileHandler(logfileName+".log",mode='w')
    fh.setLevel(logging.INFO)
    ch = logging.StreamHandler() # sys.stdout
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # put filehandler into logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger