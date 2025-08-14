#
#  Copyright 2024 The InfiniFlow Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
import json
import logging
import os
import re
import time
from abc import ABC
import requests

from api.utils.api_utils import timeout
from deepdoc.parser import HtmlParser
from agent.component.base import ComponentBase, ComponentParamBase


class MyInvokeParam(ComponentParamBase):
    """
    Define the Crawler component parameters.
    """

    def __init__(self):
        super().__init__()
        self.proxy = None
        self.headers = ""
        self.method = "get"
        self.variables = []
        self.url = ""
        self.timeout = 60
        self.clean_html = False
        self.datatype = "json"  # New parameter to determine data posting type

    def check(self):
        self.check_valid_value(self.method.lower(), "Type of content from the crawler", ['get', 'post', 'put'])
        self.check_empty(self.url, "End point URL")
        self.check_positive_integer(self.timeout, "Timeout time in second")
        self.check_boolean(self.clean_html, "Clean HTML")
        self.check_valid_value(self.datatype.lower(), "Data post type", ['json', 'formdata'])  # Check for valid datapost value


class MyInvoke(ComponentBase, ABC):
    component_name = "MyInvoke"

    @timeout(os.environ.get("COMPONENT_EXEC_TIMEOUT", 60))
    def _invoke(self, **kwargs):
        args = {}
        for para in self._param.variables:
            if para.get("value"):
                args[para["key"]] = para["value"]
            else:
                args[para["key"]] = self._canvas.get_variable_value(para["ref"])

        url = self._param.url.strip()
        if url.find("http") != 0:
            url = "http://" + url

        method = self._param.method.lower()
        headers = {}
        if self._param.headers:
            headers = json.loads(self._param.headers)
        proxies = None
        if re.sub(r"https?:?/?/?", "", self._param.proxy):
            proxies = {"http": self._param.proxy, "https": self._param.proxy}

        last_e = ""
        for _ in range(self._param.max_retries+1):
            try:
                if method == 'get':
                    response = requests.get(url=url,
                                            params=args,
                                            headers=headers,
                                            proxies=proxies,
                                            timeout=self._param.timeout)
                    if self._param.clean_html:
                        sections = HtmlParser()(None, response.content)
                        self.set_output("result", "\n".join(sections))
                    else:
                        self.set_output("result", response.text)

                if method == 'put':
                    if self._param.datatype.lower() == 'json':
                        response = requests.put(url=url,
                                                json=args,
                                                headers=headers,
                                                proxies=proxies,
                                                timeout=self._param.timeout)
                    else:
                        response = requests.put(url=url,
                                                data=args,
                                                headers=headers,
                                                proxies=proxies,
                                                timeout=self._param.timeout)
                    if self._param.clean_html:
                        sections = HtmlParser()(None, response.content)
                        self.set_output("result", "\n".join(sections))
                    else:
                        self.set_output("result", response.text)

                if method == 'post':
                    if self._param.datatype.lower() == 'json':
                        response = requests.post(url=url,
                                                 json=args,
                                                 headers=headers,
                                                 proxies=proxies,
                                                 timeout=self._param.timeout)
                    else:
                        response = requests.post(url=url,
                                                 data=args,
                                                 headers=headers,
                                                 proxies=proxies,
                                                 timeout=self._param.timeout)
                    if self._param.clean_html:
                        self.set_output("result", "\n".join(sections))
                    else:
                        self.set_output("result", self.format_data(response.text))

                return self.output("result")
            except Exception as e:
                last_e = e
                logging.exception(f"Http request error: {e}")
                time.sleep(self._param.delay_after_error)

        if last_e:
            self.set_output("_ERROR", str(last_e))
            return f"Http request error: {last_e}"

        assert False, self.output()

    def thoughts(self) -> str:
        return "Waiting for the server respond..."

    def format_data(self,json_string:str) -> str:
        from jsonpath_ng import parse
        data = json.loads(json_string)
        #$.data.list[*].shopInfo.topShopName
        #$.data.list[*].name
        # 定义 JSONPath 表达式
        path1 = parse('$.data.list[*].shopInfo.topShopName')
        path2 = parse('$.data.list[*].name')
        path3 = parse('$.data.list[*].instrumentInfo.genePic')
        # 提取所有匹配值（保持顺序）
        top_shop_names = [match.value for match in path1.find(data)]
        names = [match.value for match in path2.find(data)]
        pics = [match.value for match in path3.find(data)]

        # 保证长度一致（正常情况下应该一致）
        assert len(top_shop_names) == len(names), "提取的字段数量不一致，结构可能不匹配！"

        # 方式一：组合成列表 of 字典（推荐，结构清晰）
        result = [
            {
                "topShopName": top_name,
                "name": name,
                "pic": pic
            }
            for top_name, name, pic in zip(top_shop_names, names, pics)
        ]

        print("提取结果：")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return json.dumps(result, ensure_ascii=False, indent=2)
