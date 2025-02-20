"""
A component which allows you to parse http://www.qiyoujiage.com/zhejiang.shtml get oil price

For more details about this component, please refer to the documentation at
https://github.com/maydaychen/waterPrice

"""
import datetime
import json
import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import (PLATFORM_SCHEMA)
from homeassistant.const import (CONF_NAME, CONF_REGION)
from homeassistant.helpers.entity import Entity
from requests import request

__version__ = '0.0.1'
_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['requests']

COMPONENT_REPO = 'https://github.com/maydaychen/waterPrice'
SCAN_INTERVAL = datetime.timedelta(hours=8)
ICON = 'mdi:gas-station'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_REGION): cv.string,
})


async def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    _LOGGER.info("async_setup_platform sensor waterprice")
    async_add_devices([WaterPriceSensor(name=config[CONF_NAME], doornum=config[CONF_REGION])], True)


class WaterPriceSensor(Entity):
    def __init__(self, name: str, doornum: str):
        self._name = name
        self._doornum = doornum
        self._state = None
        self._entries = {}

    def update(self):
        _LOGGER.info("sensor waterprice update info from https://wechat.wxwater.com.cn")
        header = {
            'Host': 'wechat.wxwater.com.cn',
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-Fetch-Site': 'same-origin',
            'S_Type': 'WeChat',
            'S_OpenID': '{{OpenID}}',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Sec-Fetch-Mode': 'cors',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'https://wechat.wxwater.com.cn/WeChat2018/WeChat/waterBill_YFF?paramid={{OpenID}}',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.45(0x18002d27) NetType/WIFI Language/en'
        }
        response = request('GET',
                           'https://wechat.wxwater.com.cn/WeChat2018/WeChat/GetNowMonthBillInfo_TuoMing?UserNo=' + self._doornum,
                           headers=header)  # 定义头信息发送请求返回response对象
        response.encoding = 'utf-8'  # 不写这句会乱码

        self._state = json.loads(response.text)['DataMain']
        self._entries["update_time"] = datetime.datetime.now().strftime('%Y-%m-%d')

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return ICON

    @property
    def extra_state_attributes(self):
        return self._entries
