#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2021/7/15 下午7:50 
# @File    : browser.py
# @Project : jd_scripts 
# @Desc    :
import platform
from pyppeteer import launcher

launcher.DEFAULT_ARGS.remove("--enable-automation")
from pyppeteer import launch


async def open_browser():
    """
    打开浏览器
    :return:
    """
    if platform.system() == 'Linux':
        headless = True
    else:
        headless = True
    browser = await launch({
        'headless': headless,
        'dumpio': False,
        #'slowMo': 10,
        #'devtools': True,
        'autoClose': False,
        'handleSIGTERM': True,
        'handleSIGINT': True,
        'timeout': 0,
        'handleSIGHUP': True,
        'args': [
            '--no-sandbox',
            '--disable-gpu',
            '--disable-infobars',
            '-–window-size=1920,1080',
            '--disable-extensions',
            '-–single-process',
            '--hide-scrollbars',
            '--disable-bundled-ppapi-flash',
            '--disable-setuid-sandbox',
            '--disable-xss-auditor',
            '--ignore-certificate-errors',
        ]
    })
    return browser


async def open_page(browser, url, user_agent, cookies):
    """
    打开页面
    :return:
    """
    try:
        # context = await browser.createIncognitoBrowserContext()
        pages = await browser.pages()
        if len(pages) > 0:
            page = pages[0]
        else:
            page = await browser.newPage()

        await page.setUserAgent(user_agent)  # 设置USER-AGENT

        await page.setViewport({
            'width': 500,
            'height': 845,
            'isMobile': True
        })

        await page.setCookie(*cookies)  # 设置cookies
        await page.goto(url, timeout=40000)  # 打开活动页面

        return page
    except Exception as e:
        await browser.close()
