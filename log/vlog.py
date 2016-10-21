#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
vlog模块封装了系统logging模块的实现，增加了模块名、行数等信息。提供了每个级别对应的接口函数。

Example::

  import pub.log.vlog  import getLogger
  logger = getLogger(__name__)
  logger.critical('%s, %s,%s' % (url, req_content, url_args))

Output::

  [CRITICAL][module:123]: 127.0.0.1, get, id=1
'''
__author__ = '10177674'

import uuid
import logging
import sys
import traceback

__logger = logging.getLogger(__name__)

LOG_LEVEL_MAGIC = 'WOSHIMANOAUTOMAN'
LOG_SETTING_TIMEOUT = 0
NFVO_SERVICE_NAME = 'NFVOService'
VNFM_SERVICE_NAME = 'ORCHService'

level2name = {
    logging.CRITICAL: 'CRITICAL',
    logging.ERROR: 'ERROR',
    logging.WARNING: 'WARN',
    logging.INFO: 'INFO',
    logging.DEBUG: 'DEBUG',
    logging.NOTSET: 'NOTSET',
}

name2level = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARN': logging.WARNING,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG,
    'NOTSET': logging.NOTSET,
}


def getLogger(module, service_name=''):
    '''
      返回module对应的Logger实例
    '''
    return Logger(module, service_name)


def getLevel():
    try:
        from pub.utils.ctx import CtxHelper
        ctx = CtxHelper.get_ctx(LOG_LEVEL_MAGIC, timeout=LOG_SETTING_TIMEOUT)
        level = ctx.get('level')
        return level
    except Exception as e:
        __logger.error(traceback.format_exc())
        return 'INFO'


def setLevel(level):
    __logger.info('manolog:setLevel level=%s' % level)
    from pub.utils.ctx import CtxHelper
    ctx = CtxHelper.get_ctx(LOG_LEVEL_MAGIC, timeout=LOG_SETTING_TIMEOUT)
    ctx.set('level', level)

    from pub.config.const import ne_id
    from pub.cppapi import mmlexec
    # 设置c++进程debug级别
    service_name = NFVO_SERVICE_NAME
    if ne_id.find("o") == -1:
        # VNFM c++服务名
        service_name = VNFM_SERVICE_NAME
    mml = "SET DEBUGPARA:NAME=%s,LOGLEVEL=%s" % (service_name, level)
    result = mmlexec.execute(mml)
    __logger.info('manolog:setLevel mmlexec result=%s' % result)


class Logger:
    def __init__(self, module, service_name=''):
        self.log = logging.getLogger(module)
        self.service_name = service_name
        self.uuid = uuid.uuid4()

    def __log(self, level, f_back, message, *args, **kwargs):
        current_level_name = getLevel()
        # 默认日志级别
        current_level = logging.DEBUG
        if current_level_name in name2level:
            current_level = name2level[current_level_name]
        # 级别不够，不打印
        if current_level > level:
            return
        line_no = f_back.f_lineno
        module_name = f_back.f_globals['__name__']
        new_msg = '[%s][%s<%s>:%s:%s]:%s' % (
            level2name[level], self.service_name, self.uuid, module_name, line_no, message)
        self.log.critical(new_msg, *args, **kwargs)
        pass

    def debug(self, message, *args, **kwargs):
        '''
        记录 debug 级别日志。

        
        '''
        f_back = sys._getframe().f_back
        self.__log(logging.DEBUG, f_back, message, *args, **kwargs)

    def info(self, message, *args, **kwargs):
        '''
        记录 info 级别日志。

        
        '''
        f_back = sys._getframe().f_back
        self.__log(logging.INFO, f_back, message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        '''
        记录 warn 级别日志。
        '''
        f_back = sys._getframe().f_back
        self.__log(logging.WARN, f_back, message, *args, **kwargs)

    def warn(self, message, *args, **kwargs):
        '''
        记录 warn 级别日志。

        
        '''
        f_back = sys._getframe().f_back
        self.__log(logging.WARN, f_back, message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        '''
        记录 error 级别日志。

        
        '''
        f_back = sys._getframe().f_back
        self.__log(logging.ERROR, f_back, message, *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        '''
        记录critical 级别日志。

        '''
        f_back = sys._getframe().f_back
        self.__log(logging.CRITICAL, f_back, message, *args, **kwargs)

    def fatal(self, message, *args, **kwargs):
        '''
        记录 fatal 级别日志。

        
        '''
        f_back = sys._getframe().f_back
        self.__log(logging.CRITICAL, f_back, message, *args, **kwargs)
