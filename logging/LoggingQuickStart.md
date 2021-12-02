# Quick Logging

[TOC]

>  簡單的情況可以直接使用 logging，但一些複雜的情況需要管理多層次的日誌(log) 時，則應該使用 logger 較佳。

---

## 0.訊息的基本認知

預設的 logging 訊息等級一共有五個。


| 等級     | 數值 |
| -------- | ---- |
| DEBUG    | 10   |
| INFO     | 20   |
| WARNING  | 30   |
| ERROR    | 40   |
| CRITICAL | 50   |



- 其中，**logging 的日誌等級預設是 `WARNING(30)`**，因此在預設的情況下，數值小於30的日誌等級不會輸出。




## 1. Single Module : Using Logging 

### 直接使用

不設定 handle，也不設定`basicConfig` ，預設是輸出到終端機上(terminal/stdout)。

如前面所說，logging 的日誌等級預設是 `WARNING(30)`。因此低於 WARNING 的 INFO 沒有被輸出在 terminal。

```python
import logging
logging.warning('Watch out!')  
logging.info('I told you so') 

''' 
WARNING:root:Watch out!
'''
```

### 寫入 log file

多數的情況需要儲存查看這些紀錄檔案

```python
import logging
logging.basicConfig(filename='example.log', level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
```

如此一來將不會有任何輸出，但是查看執行目錄下，會發現 `example.log` 這個檔案裡，有寫入日誌。由於`basicConfig` 函式中，設置了等級為 DEBUG等級 (10)，因此三行訊息都有被包含進去。

```
# example.log 
DEBUG:root:This message should go to the log file
INFO:root:So should this
WARNING:root:And this, too
```

如果重複執行上面的程式，日誌會不斷的加在`example.log`後面。想要每次都直接刷新日誌檔案而不是接續(append)，需要加上參數 `filemode=w` 。

```
logging.basicConfig(filename='example.log',filemode='w',  level=logging.DEBUG)
```



## 2. Multiple Module : Please Use Logger

在一些比較複雜的情況，通常是有架構層級的模組之間，每個檔案都只使用 logging 顯得雜亂無序。這裡不仔細介紹原理，但提供了一份預先設定好把輸出導向 terminal (stdout)、與自動儲存日誌(log) 到檔案的程式碼。以下幾點請注意: 

1. 建立 logger 物件不能直接使用 `logging()` 之類的作法建立實例，必須使用 `logging.getLogger(name)`
2. 這個 `name` 很重要，如果在 multi-module (多個 `.py`) 中使用 logger，建立 logger 時，**一樣名稱的logger會被寫到同一個層級、不同的名稱會被視為不同的紀錄器**
3. 如果希望主、副程式之間，logger之間有父子的上下關係，在命名的時候可以有 `parent.child` 這樣，用 `.` 表示logger 之間的關係。

這是我整理出來的一個 function，可以直接拿來調用。

```python
import logging, sys, os

def get_logger(rootName="__main__", childName="", fileName="", timeFlag=True, log_dir="logs"):
    '''
    直接使用 get_logger ，返回的 logger 不會有層級。
    1. 根據程式的 package 層級自動設定：要包括參數整行複製去用：get_logger(rootName="__main__", childName=__name__)
    2. 自定義層級：同時覆蓋 rootName, child 自己寫層級架構。get_logger(rootName="parent", childName="child1.child2")
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
        
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
    
    fileName = os.path.join(log_dir, fileName)

    if not childName: # 只能在最頂層加，如果每一層都這樣加，每一個 child logger 也會都 print 一行
        # file handler
        fh = logging.FileHandler(fileName+".log",mode='w', encoding='utf-8-sig')
        fh.setLevel(logging.INFO)
        ch = logging.StreamHandler() # sys.stdout
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
        # formatter = logging.Formatter('%(message)s')
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        # put filehandler into logger
        logger.addHandler(fh)
        logger.addHandler(ch)
    return logger
```

### 簡易範例

1.  Root file，執行的時候是 `python xxx.py` 的那個 `xxx.py` 的檔案中應該這樣調用 logger : 

   ```python
   logger = get_logger(rootName=__name__)
   ```

2.  Child file，被 `xxx.py` 所呼叫的檔案

   ```python
   logger = get_logger(childName=__name__)  
   ```

不管是哪個檔案，使用 logger 的時候都直接按照訊息層級的嚴重性，正常使用即可: 

```python
logger.debug("just debug desp")
logger.info("some information")
logger.warning("This is warning, your action may cause some unexpected effect.")
logger.error("something wrong!")
logger.critical("Your code is dead!!")
```

Hint 1. 如果覺得預設的 logger 格式太過冗長，可以參考下一章改變範例 code 中的 `formatter` 達成。

Hint 2. 如果希望錯誤/例外發生時，可以把 trace 一併寫進去，參考第四章的部分。 

### 層級說明

程式中的說明文字，具體範例如下:

#### 狀況1. 根據套件層級自動設定

簡易範例中即示範了此種狀況，這種情況下，**請勿改變 root file 中 logger 的 rootName 屬性**，讓他保留範例中的樣子，也就是 `__name__` (在 main file 中 `__name__`==`__main__`) 

#### 狀況2. 手動設定層級名稱

想搞怪? 自己設定層級名稱! 

```python
logger1 = get_logger(rootName="boss")
logger2 = get_logger(rootName="boss", childName="manager")
logger3 = get_logger(rootName="boss", childName="manager.department")
logger4 = get_logger(rootName="boss", childName="manager.department.engineer")
```

#### 狀況3. 都不使用

完全不使用層級的話，大可以所有的檔案都如下: 

```python
logger = get_logger(rootName=__name__)
```

但強烈不建議，如果這樣何必搞 logger，直接用 logging 就好了吧。

## 3. 訊息格式

使用最原始的表達方式 `%s` : 為了向下兼容

```python
import logging
logging.warning('%s before you %s', 'Look', 'leap!')
```

### 改變訊息的呈現格式

透過`logging.basicConfig` 設定 log 的訊息模式。
前面的範例中，還有像是"root"之類的(位置)資料包含其中，這些可以參考下面的網站，自己調整想出現的必要訊息。

- [可以動用的變數](https://docs.python.org/3.7/library/logging.html#logrecord-attributes): 很重要! 羅列了你可以動用的紀錄訊息，像是 function Name, … 各種的

```python
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.debug('This message should appear on the console')
logging.info('So should this')
logging.warning('And this, too')

''' 
DEBUG:This message should appear on the console
INFO:So should this
WARNING:And this, too
'''
# %(levelname)s = DEBUG, INFO, WARNING... 
# %(messages)s = ()裡面的訊息
 
```

## 4. 紀錄例外的traceback訊息

- `logger.exception('any msg')` ：**直接使用 exception層級，會將堆疊訊息寫進去 log 中**。層級為 error 層級
- `exc_info=True` 若想把例外訊息以**其他層級寫入**，可以把此參數調成True。預設為False，不會把堆疊訊息寫入。

```python
import traceback

def main_loop():
    for i in range(10):
        logger.info(f'print {i}')
        if i== 5:
            raise Exception("Break")
try:
    main_loop()
except Exception:
    # 將引發例外的堆疊訊息寫入logger, 甚麼動作都不用下
    logger.exception('') 
    # 堆疊訊息以info的層級寫入
    logger.info('info has exc_info',exc_info=True)
    # 當例外發生時，只會當純的寫入此行，因為 exc_info=False
    logger.warning('warning without exc_info',exc_info=False)
    
    # [Optional] 只將traceback的紀錄寫進指定txt
    traceback.print_exc(file=open('traceback_INFO.txt','w+'))
```

