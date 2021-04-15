import logging, sys
def get_logger(rootName="__main__", childName="", fileName="record", timeFlag=False):
    '''
    直接使用 get_logger ，返回的 logger 不會有層級。
    1. 根據程式的 package 層級自動設定：要包括參數整行複製去用：get_logger(rootName="__main__", childName=__name__)
    2. 自定義層級：同時覆蓋 rootName, child 自己寫層級架構。get_logger(rootName="parent", childName="child1.child2)
    3. 不使用層級：rootName 可自由選擇是否更改，但 child 請設為空 get_logger(rootName="__main__", childName="")
    # --------------------------------
    如果有不只一個 python 檔在跑，且彼此沒有上下層級關係
    記得覆寫 rootName，不要讓兩個 logger 同名，否則一旦輸入訊息會讓兩個 logger 都一起 ouput
    '''
    logName = rootName if not childName else  rootName+"."+childName
    print("Your Log name is : ", logName)
    logger = logging.getLogger(logName) 
    logger.setLevel(logging.DEBUG)
    if timeFlag:
        from datetime import datetime
        now = datetime.now()
        dt_string = now.strftime("%m%d_%H%M%S")
        fileName+="_"+dt_string

    # file handler
    fh = logging.FileHandler(fileName+".log",mode='w')
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
logger = get_logger(timeFlag=True)