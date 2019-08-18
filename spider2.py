import asyncio
from pyppeteer import launch

width, heigh = 1366, 768


async def main():
    browser = await launch(headless=False, args=['--disable-infobars'])
    page = await browser.newPage()
    await page.setViewport({'width': width, 'height': heigh})
    await page.goto('https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fs.taobao.com%2Fsearch%3Fq%3D%25E5%2586%2585%25E8%25A1%25A3%26imgfile%3D%26commend%3Dall%26ssid%3Ds5-e%26search_type%3Ditem%26sourceId%3Dtb.index%26spm%3Da21bo.2017.201856-taobao-item.1%26ie%3Dutf8%26initiative_id%3Dtbindexz_20170306')
    await page.evaluate(
        '''() => {Object.defineProperties(navigator,{webdriver:{get:() => false }})}'''
    )
    await asyncio.sleep(100)


asyncio.get_event_loop().run_until_complete(main())
