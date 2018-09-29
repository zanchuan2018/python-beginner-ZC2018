#!/usr/bin/env Python
# -*- coding:utf-8 -*-
# 51memo.V1.3.py
# A memo demo 51备忘录，面向对象编程
# author: zanchuan


import pickle
import re

"匹配中文、字母"
RE_INPUT = re.compile(r'^[\u4e00-\u9fa5]{1,8}$|^[a-zA-Z]{1,}$|\s')


class Memo:
    "备忘录就长这样"
    def __init__(self, date, thing, admin):
        self._id = 0
        self.date = date
        self.thing = thing
        self.admin = admin
        self.welcome_memolist()

    @property
    def id(self):
        "每条记录的标记"
        return self._id

    @id.setter
    def id(self, value):
        self._id = value + 1

    def welcome_memolist(self):
        "欢迎使用"
        print('51备忘录'.center(60, '-'))

    def show_memolist(self):
        "显示每条记录"
        print(f'{self.id}:{self.date}<>{self.thing}')

    @classmethod
    def verify_input(self, re_obj, text):
        "验证输入"
        if re_obj.match(text):
            print('输入有误！！')
        else:
            return

    def func_memolist(self, admin):
        "备忘录菜单"
        menu = {
            'a': '添加条目',
            'd': '删除条目',
            'm': '修改条目',
            's': '查找条目',
            'p': '显示备忘录',
            'q': '退出'
        }

        for k, v in menu.items():
            print(f'{k}:{v}')

        while True:

            mess = input('请选择备忘录功能：').strip().lower()

            if mess == 'a':
                func = getattr(admin, 'add_memolist')
                func()
            elif mess == 'd':
                func = getattr(admin, 'del_memolist')
                func()
            elif mess == 'm':
                func = getattr(admin, 'mod_memolist')
                func()
            elif mess == 's':
                func = getattr(admin, 'ser_memolist')
                func()
            elif mess == 'p':
                func = getattr(admin, 'pri_memolist')
                func()
            elif mess == 'q':
                print('再见')
                break
            else:
                print('输入有误')
                continue


class MemoAdmin:
    "备忘录都有这些功能"
    def __init__(self):
        self.memolist = []
        self.load_memolist()

    def load_memolist(self):
        "加载备忘录"
        try:
            with open('db.pkl', 'rb') as z:
                self.memolist = pickle.loads(z.read())
        except EOFError:
            return self.memolist

    def save_memolist(self):
        "保存备忘录"
        with open('db.pkl', 'wb') as z:
            z.write(pickle.dumps(self.memolist))

    def add_memolist(self):
        "添加备忘录"
        date = input('请输入日期/时间：').strip().lower()
        thing = input('请输入事件内容：').strip().lower()
        zc = Memo(date, thing, 'admin')
        if len(self.memolist) != 0:
            zc.id = self.memolist[-1].id
        self.memolist.append(zc)
        self.save_memolist()

    def del_memolist(self):
        "删除备忘录"
        self.pri_memolist()
        del_memo = input('请输入删除内容的序号，退出请按q(删除所有请输入del-all)：').strip().lower()
        
        if del_memo == 'q':
            return None
        elif del_memo == 'del-all':
            self.memolist = []
            self.save_memolist()
        elif del_memo:
            for d in self.memolist:
                while int(del_memo) == d.id:
                    self.memolist.remove(d)
                    self.save_memolist()
                    return

    def mod_memolist(self):
        "修改备忘录"
        self.pri_memolist()
        mod_id = input('请输入需要修改的ID，退出请按q：').strip().lower()
        if mod_id == 'q':
            return None
        elif mod_id:
            for mod in self.memolist:
                while mod.id == int(mod_id):
                    new_date = input('请输入新的日期或时间：')
                    new_thing = input('请输入新的事件：')
                    mod.date = new_date
                    mod.thing = new_thing
                    self.save_memolist()
                    break
        else:
            return

    def ser_memolist(self):
        "查找备忘录"
        ser = input('''请输入查找类型：
        1. 日期
        2. 事件
        q. 退出：''')
        if ser == '1':
            ser_date = input('请输入日期：').strip().lower()
            for s in self.memolist:
                if s.date == ser_date:
                    s.show_memolist()
                    return
            if ser_date != s.date:
                z = input('没有该记录，是否创建一条记录，Y/N：').strip().lower()
                if z == 'y':
                    self.add_memolist()
                    self.save_memolist()
                    return None
                else:
                    return None
        elif ser == '2':
            ser_thing = input('请输入事件内容：').strip().lower()
            for s in self.memolist:
                if ser_thing in s.thing:
                    s.show_memolist()
                    return
            if ser_thing != s.thing:
                z = input('没有该记录，是否创建一条记录，Y/N：').strip().lower()
                if z == 'y':
                    self.add_memolist()
                    self.save_memolist()
                    return None
                else:
                    return None
        else:
            ser == 'q'
            return None

    def pri_memolist(self):
        "打印备忘录"
        for z in self.memolist:
            zc = z
            zc.show_memolist()


def main():
    "备忘录从这里开始"
    admin = MemoAdmin()
    zc = Memo('date', 'thing', admin)
    zc.func_memolist(admin)

if __name__ == '__main__':
    main()