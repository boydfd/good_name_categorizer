## 使用
1. pip3 install -r requirements.txt

2. config path in resources/resource.py
	1. config good name path  
		origin_good_name_path = get_path('./good_name/goods.csv')
	2. config dictionary path  
		origin_dict_path = get_path('./dictionaries/filtered_dict.txt')
2. python3 main.py


## 背景

海航货运的订单里面有上百万的物流运单，在运单中包含所运送物品的信息。但是因为运送物品都是用户填写的自由文本，一直无法按照物品分类来统计，去年一共运送了多少比例的电子产品，多少服装！！所以需要通过算法来做出一个相对准确的分类结果。

## 思路

### 业务思路
- 问题1：如何确定统一的分类标准：

	解决办法：我们分别抓取了淘宝、京东、阿里巴巴以及一个百度文库上的物品分类，经过人为筛选，确定了分类标准，一共得到28个大分类,400+小分类：  [分类](
	./resources/category.txt)
	
- 问题2: 如何将我们的货物名对应到正确分类上去:

	解决办法：
	- 首先使用货物名和分类名,通过互联网(百度百科)，获得更多与之相关的信息(单单的货物名提供的信息太少了)。
	- 然后我们可以计算使用货物名和分类名分别拿到的百度百科的相似性，遍历我们已有的所有分类，然后取相似度最高的那个一分类作为货物名的分类。


### 算法思路
- 问题1：如何计算两篇百度百科的相似度

	解决办法：将两篇百度百科变成同维度的向量，用余弦相似度来计算向量的相似度，得到的相似度就是两篇百度文档的相似度。
	
- 问题2：如何将百度百科变成向量

	解决办法：
	- 对所有要计算相似度的百度百科(很多篇)先做分词，每个词就是一个维度。
	- 对一篇百度百科做分词，使用TF-IDF算出这篇百度百科所有词的重要程度，然后得到的某一个词的重要程度就是这篇百科在这个维度上的值,然后我们就得到了一个向量。

- 问题3：如何更好地分词
	
	解决办法：将百度百科的词条作为词典，来进行分词，词典需要去除英语（在词典中加入英语会导致完整的英语单词被切分）

## 算法

#### TF-IDF(term frequency–inverse document frequency): 
	
TF-IDF是一种统计方法，用以评估一字词对于一个文件集或一个语料库中的其中一份文件的重要程度。字词的重要性随着它在文件中出现的次数成正比增加，但同时会随着它在语料库中出现的频率成反比下降。

#### 余弦相似度

通过计算两个向量的夹角余弦值来评估他们的相似度

## 处理流程

1. 使用所有的分类，建立起向量（找到分类的百度百科，使用TF-IDF计算出向量）。

2. 对已有的3.3M行货物名进行分词（需要用到百度百科作为词典），得到55k个词

3. 对55k个词做筛选，选出词频大于3的20k个词，计算这些词和所有分类的相似度(做缓存用)

4. 对3.3M行货物进行去重，得到155k行货物名，分别对每一行进行分词。

5. 将一行中的几个词分别做分类的相似度计算，然后将得到的相似度取平均值,最后找到相似度最大分类（取平均值只是一种策略，也可以取最大值，或者直接给一行货物名多个分类）

## Todo

#### 功能
[ ] 允许用户直接自定义某个词的相似度  

#### 算法提升
[ ] 人工分出1000个货物的类来作为测试集  
[ ] 优化分类（比如：减少分类数量，提升分类准确率）  
[ ] 使用不同的相似度合并算法来测试效果  
[ ] 使用分类以及其相关联的一级百科来作为生成向量的文本  
