#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: Qiaoxueyuan
@time: 2018/1/9 下午4:28
'''

import requests
import json
import time
import hashlib


class GetAgentToken():

    def get_env(self):
        i = 0
        while i < 3:
            try:
                self.env = int(input("线上环境请输1，测试环境请输2：\n"))
                if self.env in [1, 2]:
                    return self.env
            except:
                i += 1

    def company_token(self):
        env = self.get_env()
        if env == 1:
            company = str(input("请输入公司的二级域名：\n"))
            url = "https://" + company + ".udesk.cn/open_api_v1/log_in"
            email = str(input("请输入管理员账号：\n"))
            password = str(input("请输入管理员密码：\n"))
        elif env == 2:
            company = str(input("请输入公司的URL(例：linapp.udeskcat.com)：\n"))
            url = "http://" + company + "/open_api_v1/log_in"
            email = str(input("请输入管理员账号：\n"))
            password = str(input("请输入管理员密码：\n"))

        data = {
            "email": email,
            "password": password
        }
        headers = {
            "content-type": "application/json"
        }
        r = requests.post(url, data=json.dumps(data), headers=headers).text
        try:
            company_token = json.loads(r)["open_api_auth_token"]
        except Exception as e:
            print("未能取到公司token，相关报错：\n")
            print(str(e) + "\n")
            print("相关接口返回值：\n")
            print(str(r))
            return False
        print("公司token为：\n" + company_token)
        return [env, email, company, company_token]

    def agent_token(self):
        list = self.company_token()
        if list:
            admin_email = list[1]
            company = list[2]
            company_token = list[3]
            agent_email = str(input("请输入客服邮箱：\n"))
            timestamp = str(str(time.time())[:10])
            string = admin_email + "&" + company_token + "&" + timestamp
            sign = hashlib.sha1(string.encode('utf-8'))
            sign = sign.hexdigest()
            if list[0] == 1:
                url = "https://" + company + ".udesk.cn/open_api_v1/get_agent_token"
            elif list[0] == 2:
                url = "http://" + company + "/open_api_v1/get_agent_token"
        else:
            return

        data = {
            "email": admin_email,
            "agent_email": agent_email,
            "timestamp": timestamp,
            "sign": sign
        }
        headers = {
            "open_api_token": company_token,
            "content-type": "application/json"
        }
        r = requests.post(url, data=json.dumps(data), headers=headers).text
        try:
            agent_token = json.loads(r)["agent_api_token"]
        except Exception as e:
            print("未能取到客服token，相关报错：\n")
            print(str(e) + "\n")
            print("相关接口返回值：\n")
            print(str(r))
            return
        return agent_token


if __name__ == "__main__":
    worker = GetAgentToken()
    agent_token = worker.agent_token()
    if agent_token:
        print("客服token为：\n" + agent_token)
