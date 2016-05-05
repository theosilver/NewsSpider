# -*- coding: utf-8 -*- 
import sys
import json
reload(sys)
sys.path.append("..")
sys.setdefaultencoding('utf-8')
from Cut import Cut
import tools.Global as Global
import jieba

class Search:
	def __init__(self):
		self.kw_id = self.loadKW_ID()

	def loadKW_ID(self):
		f = open(Global.inverse_dir+'id.txt')
		line = f.readline()
		kw_id = json.loads(line, encoding='utf-8')
		return kw_id


	#返回文档号
	def QuerySingle(self,searchWord,ishow):
		if self.kw_id.has_key(searchWord.decode('utf-8')):
			idx = self.kw_id[searchWord.decode('utf-8')]
			cut = Cut()
			ii_line = cut.getInverseIndexRow(idx,Global.inverse_dir,Global.filesize)
			record =json.loads(ii_line)
			if ishow:
				for rec in record:
					line = cut.getRow(int(rec),Global.cutnews_origin_dir,Global.filesize)
					data = json.loads(line)
					print data['title'],'\n',data['time'],'\n',data['content'],'\n'
		#返回单个词项对应的倒排记录表
			return record
		else:
			if isshow:
				print 'Not Exists Record!'
			#调用该函数后需要对结果进行判断
			return dict()
		
	
	#'与'查询：先分词，再合并倒排记录,不考虑权重,返回文档号
	def QueryPhrase(self,searchPhrase,ishow = True):
		words = jieba.cut(searchPhrase.decode('utf-8'),cut_all=False)
		cut = Cut()
		result = set(range(1,100000))
		for word in words:
			if not self.kw_id.has_key(word):
				print 'Not Exist Record'
				return set()
			idx = self.kw_id[word]
			ii_line = cut.getInverseIndexRow(idx,Global.inverse_dir,Global.filesize)
			record =json.loads(ii_line)
			re = set()
			for rec in record:
				re.add(int(rec))
			result = result & re
		print result
		if ishow:
			if len(result) == 0:
				print 'Not Exists Record!'
			else:
				for rst in result:
					line = cut.getRow(int(rst),Global.cutnews_origin_dir,Global.filesize)
					data = json.loads(line)
					print data['title'],'\n',data['time'],'\n',data['content'],'\n'
		return result

	#返回热点新闻
	def QueryHotNews(self):
		pass

	#返回最新新闻
	def QueryByTime(self):
		pass
	
search = Search()
#search.QueryPhrase(sys.argv[1])
search.QueryPhrase(sys.argv[1])
