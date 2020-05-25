import requests
import time
import re
import codecs
import pickle
import os
import numpy as np
from html.parser import HTMLParser

class ProtoHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._tag_stack = []
        self._youtube = []
        self._tags = []
        self._materials = []
        self._title = None
        self._team = None
        self._active_link = None
        self._member = []
        self._message = None

    def __str__(self):
        ret = 'title:\n\t{}\n'.format(self._title)
        ret += 'team:\n\t{}\n'.format(self._team)
        ret += 'tags:\n'
        for t in self._tags:
            ret += '\t{}\n'.format(t)
        ret += 'materials:\n'
        for m in self._materials:
            ret += '\t{}[{}]\n'.format(m[0], m[1])
        ret += 'youtube:\n'
        for y in self._youtube:
            ret += '\t{}\n'.format(y)
        ret += 'member - role:\n'
        for m in self._member:
            ret += '\t{}[{}]\n'.format(m[0][0], m[0][1])
            for r in m[1]:
                ret += '\t\t{}[{}]\n'.format(r[0], r[1])
        ret += 'message:\n\t{}\n'.format(self._message)
            
        return ret

    def _attrs2hash(self, attrs):
        ret = {}
        for at in attrs:
            ret[at[0]] = at[1]
        return ret

    def parse(self, path):
        data = codecs.open(path, 'r', 'utf-8').read()
        self.feed(data)
    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            return

        atmap = self._attrs2hash(attrs)
#        print("タグ開始:", tag, attrs)
        self._tag_stack.append((tag, atmap))
        if tag == 'a' and 'href' in atmap:
            self._active_link = atmap['href']
            if 'href' in atmap and 'https://youtu.be/' in atmap['href']:
                self._youtube.append(atmap['href'])

    def handle_endtag(self, tag):
        if tag == 'p':
            return
        if tag == 'a':
            self._active_link = None


#        print("タグ終了 :", tag)
        self._tag_stack = self._tag_stack[:-1]

    def _in_div_classes(self, classes):
        p = 0
        if len(classes) == 0:
            return False
        for i in range(len(self._tag_stack)):
            if self._tag_stack[i][0] == 'div' and 'class' in self._tag_stack[i][1] and classes[p] in self._tag_stack[i][1]['class']:
                p += 1
                if p >= len(classes):
                    return True

    def handle_data(self, data):
        if len(self._tag_stack) >= 1 and 'h1' in self._tag_stack[-1][0]:
            self._title = data
        if(self._in_div_classes(['field--name-field-prototype-tags', 'field__items', 'field__item'])):
            self._tags.append(data)
        if(self._in_div_classes(['field--name-field-materials', 'field__items', 'field__item'])):
            self._materials.append((data, self._active_link))
        if(self._in_div_classes(['field--name-field-teamname', 'field__item'])):
            self._team = data
        if(self._in_div_classes(['field--name-field-prototyper', 'field__item'])):
            self._member.append([(data, self._active_link), []])
        if(self._in_div_classes(['field--name-field-roles', 'field__item'])):
            if data.strip() != '':
                self._member[-1][1].append((data, self._active_link))
        if(self._in_div_classes(['field--name-field-wow', 'field__item'])):
            self._message = data

#        if len(self._tag_stack) >= 1 and 'div' in self._tag_stack[-1][0] and 'class' in self._tag_stack[-1][1]:
#            print(self._tag_stack[-2])
#            if 'clearfix text-formatted field field--name-body field--type-text-with-summary field--label-hidden field__item' in self._tag_stack[-1][1]['class']:
#                print('title::', data)

#        print("その他データ :", data)
        pass
     

class ProtopediaHacker:
    def __init__(self):
        self._repatter_idea = re.compile(r'.*<a href="(/prototype/.+)">(.+)</a>.*')
        self._repatter_last = re.compile(r'.*<a href="\?page=(.+)" title="最終ページへ">.*')
        self._idea_dir = 'ideas_body'
        os.makedirs(self._idea_dir, exist_ok=True)

    def wget_idea_site(self, url):
        ret = []
        lastpage = 0
        try:
            print(url)
            r = requests.get(url)
            datas = r.text.split('\n')
            for d in datas:
                result = self._repatter_idea.match(d)
                if result:
                    # url, title
                    ret.append((result.groups()[0], result.groups()[1]))
                result = self._repatter_last.match(d)
                if result:
                    lastpage = int(result.groups()[0])
        except requests.exceptions.RequestException as err:
            print(err)
        return ret, lastpage
        

    def wget_idea_list(self):
        ret = []
        lastpage = 0
    #    keywords = 'abcdefghijklmnopqrstuvwxyz'
        keywords = 'abcdefghijlmnopqrstuvwxyz'
        for keyword in keywords:
            url = 'https://protopedia.net/search/{}'.format(keyword)
            ret0, lastpage = self.wget_idea_site(url)
            for i in range(lastpage):
                url = 'https://protopedia.net/search/{}?page={}'.format(keyword, i)
                ret0, _ = self.wget_idea_site(url)
                ret.extend(ret0)
                time.sleep(1.0)
        return ret

    def id_from_suburl(self, suburl):
        header = '/prototype/'
        return suburl[len(header):]

    def crole_ideas_list(self):
        ideas = self.wget_idea_list()
        idea_set = {}
        for idea in ideas:
            if not idea[0] in idea_set:
                idea_set[idea[0]] = idea[1]
        with open('idea_url_list.pickle', 'wb') as f:
            pickle.dump(idea_set, f)
            
        with codecs.open('idea_url_list.txt', 'w', 'utf-8') as f:
            for idea in idea_set:
                f.write('{}\thttps://protopedia.net{}\n'.format(self.id_from_suburl(idea), idea))

        with codecs.open('idea_url_title_list.txt', 'w', 'utf-8') as f:
            for idea in idea_set:
                f.write('{}\thttps://protopedia.net{}\t{}\n'.format(self.id_from_suburl(idea), idea, idea_set[idea]))

    def wget_idea_body(self, id, url, title):
        path = '{}/{}'.format(self._idea_dir, id)
        print(path)
        with codecs.open(path, 'w', 'utf-8') as f:
            f.write(requests.get(url).text)
            time.sleep(1.0)

    def crole_ideas_body(self):
        with codecs.open('idea_url_title_list.txt', 'r', 'utf-8') as f:
            idea_url_title_list = [d.strip().split('\t') for d in f.readlines() if '\t' in d]
            for url_title in idea_url_title_list:
                id, url, title = url_title
                self.wget_idea_body(id, url, title)

    def analyze(self):
        dirpath = '{}/'.format(self._idea_dir)
        ideas = []
        count = 0
        dirs = os.listdir(dirpath)
        for filename in dirs:
            php = ProtoHTMLParser()
            path = dirpath + filename
            php.parse(path)
            ideas.append(php)
            count += 1
            progress = int((count * 50 / len(dirs)))
            progress_bar = '*' * progress + '-' * (50 - progress) + ': {}/{}'.format(count, len(dirs))
            print(progress_bar, end='\r')

        # タイトルとチーム名を出力
        print('タイトルとチーム名を出力: title_team.csv')
        with codecs.open('title_team.csv', 'w', 'utf-8') as f:
            f.write('{}\t{}\n'.format('title', 'team'))
            for idea in ideas:
                f.write('{}\t{}\n'.format(idea._title, idea._team))

        # タイトルとユーザ名を出力
        print('タイトルとユーザ名を出力: title_prototyper.csv')
        with codecs.open('title_prototyper.csv', 'w', 'utf-8') as f:
            f.write('{}\t{}\n'.format('title', 'prototyper'))
            for idea in ideas:
                for prototyper in idea._member:
                        f.write('{}\t{}\n'.format(idea._title, prototyper[0][0]))

        # ユーザ名と役割を出力
        print('ユーザ名と役割を出力: prototyper_role.csv')
        with codecs.open('prototyper_role.csv', 'w', 'utf-8') as f:
            f.write('{}\t{}\n'.format('prototyper', 'role'))
            for idea in ideas:
                for prototyper in idea._member:
                    for role in prototyper[1]:
                        f.write('{}\t{}\n'.format(prototyper[0][0], role[0]))

        # ユーザ名とタグを出力
        print('ユーザ名とタグを出力: prototyper_tag.csv')
        with codecs.open('prototyper_tag.csv', 'w', 'utf-8') as f:
            f.write('{}\t{}\n'.format('prototyper', 'tag'))
            for idea in ideas:
                for prototyper in idea._member:
                    for tag in idea._tags:
                        f.write('{}\t{}\n'.format(prototyper[0][0], tag))

        # ユーザ名と素材を出力
        print('ユーザ名と素材を出力: prototyper_material.csv')
        with codecs.open('prototyper_material.csv', 'w', 'utf-8') as f:
            f.write('{}\t{}\n'.format('prototyper', 'material'))
            for idea in ideas:
                for prototyper in idea._member:
                    for material in idea._materials:
                        f.write('{}\t{}\n'.format(prototyper[0][0], material[0]))
        
        print('素材とタグを出力: material_tag.csv')
        # 素材とタグを出力
        with codecs.open('material_tag.csv', 'w', 'utf-8') as f:
            f.write('{}\t{}\n'.format('material', 'tag'))
            for idea in ideas:
                for material in idea._materials:
                    for tag in idea._tags:
                        f.write('{}\t{}\n'.format(material[0], tag))

        print('類似度を出力: similarity_rank.csv')
        material_map = {}
        max_material = 5.0
        prototypers = {}
        for idea in ideas:
            for material in idea._materials:
                if not material in material_map:
                    next_id = len(material_map)
                    material_map[material] = next_id
            for prototyper in idea._member:
                if not prototyper[0] in prototypers:
                    prototypers[prototyper[0]] = 0
                prototypers[prototyper[0]] += 1

        materials = [None] * len(material_map)
        for material in material_map:
            materials[material_map[material]] = material
        pt_feature = {}
        for prototyper in prototypers:
            vec = [0.0] * len(material_map)
            for idea in ideas:
                if prototyper in [m[0] for m in idea._member]:
                    for material in idea._materials:
                        vec[material_map[material]] = min(vec[material_map[material]] + 1.0 / max_material, 1.0)
            pt_feature[prototyper] = vec
        with codecs.open('similarity_rank.csv', 'w', 'utf-8') as f:
            f.write('{}\t{}\t{}\n'.format('prototyperA', 'prototyperB', 'similarity'))
            for pt0 in pt_feature:
                sim_map = {}
                sim_list = []
                for pt1 in pt_feature:
                    v0 = np.array(pt_feature[pt0])
                    v1 = np.array(pt_feature[pt1])
                    sim = np.dot(v0, v1) / (np.linalg.norm(v0, ord=2) * np.linalg.norm(v1, ord=2))
                    nv0 = v0 / np.linalg.norm(v0, ord=2)
                    nv1 = v1 / np.linalg.norm(v1, ord=2)
                    simvec = nv0 * nv1
                    order = np.argsort(-nv0 * nv1)
                    sim_materials = []
                    for i in order[:5]:
                        if simvec[i] > 0.0:
                            sim_materials.append(materials[i][0])

                    sim_map[pt1] = (sim, '・'.join(sim_materials))
                    sim_list.append(sim_map[pt1][0])
                sim_threthold = sim_list[-11]
                for pt1 in sim_map:
                    if sim_map[pt1][0] > sim_threthold and pt1 != pt0:
                        f.write('{}\t{}\t{}\t{}\n'.format(pt0[0], pt1[0], sim_map[pt1][0], sim_map[pt1][1]))

   

if __name__ == '__main__':
    ph = ProtopediaHacker()

    while True:
        print('**** prototype hack menu ****')
        print('0. アイデアの一覧を抽出する')
        print('1. アイデア本体を抽出する')
        print('2. 抽出されたアイデアを分析してメトリクスを抽出する')
        print('9. 終了する')

        opt = input().strip()
        if opt == '0':
            # アイデアの一覧を抽出する
            ph.crole_ideas_list()
            print('idea_url_list.pickle is updated.')
        elif opt == '1':
            # アイデア本体を抽出する
            ph.crole_ideas_body()
            print('idea_url_title_list directory is updated.')
        elif opt == '2':
            ph.analyze()
        elif opt == '9':
            break
            





    


