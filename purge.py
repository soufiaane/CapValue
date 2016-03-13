# region Imports
from __future__ import absolute_import

import time

from celery.utils.log import get_task_logger
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, \
    ElementNotVisibleException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from celeryTasks.celerySettings import app
# endregion

logger = get_task_logger(__name__)


# TODO-CVC Detect Mailbox language to optimize Timeout Exceptions !!
# TODO-CVC Job option for browser

@app.task(name='report_hotmail', bind=True, max_retries=3, default_retry_delay=1)
def report_hotmail(self, **kwargs):
    return True