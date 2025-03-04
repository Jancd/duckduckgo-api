from itertools import islice

from duckduckgo_search import DDGS
from flask import Flask, request

import logging
from logging.handlers import TimedRotatingFileHandler

# logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# TimedRotatingFileHandler for dayly log rotation
handler = TimedRotatingFileHandler('websearch.log', when='D', interval=1, backupCount=5)
handler.setLevel(logging.DEBUG)

# formatter for log messages
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

app = Flask(__name__)


def run():
    if request.method == 'POST':
        keywords = request.form['q']
        max_results = int(request.form.get('max_results', 10))
    else:
        keywords = request.args.get('q')
        # 从请求参数中获取最大结果数，如果未指定，则默认为10
        max_results = int(request.args.get('max_results', 10))
    return keywords, max_results


@app.route('/search', methods=['GET', 'POST'])
async def search():
    keywords, max_results = run()

    # record the request's keywords
    logger.debug(f'received request with keywords: {keywords}, max_results: {max_results}')

    results = []
    with DDGS() as ddgs:
        # 使用DuckDuckGo搜索关键词
        ddgs_gen = ddgs.text(keywords, region='cn-zh', safesearch='on', timelimit='y', backend="lite")
        # 从搜索结果中获取最大结果数
        for r in islice(ddgs_gen, max_results):
            results.append(r)

    logger.debug(f'returning {len(results)} results')
    return {'results': results}


@app.route('/searchAnswers', methods=['GET', 'POST'])
async def search_answers():
    keywords, max_results = run()
    results = []
    with DDGS() as ddgs:
        # 使用DuckDuckGo搜索关键词
        ddgs_gen = ddgs.answers(keywords)
        # 从搜索结果中获取最大结果数
        for r in islice(ddgs_gen, max_results):
            results.append(r)

    # 返回一个json响应，包含搜索结果
    return {'results': results}


@app.route('/searchImages', methods=['GET', 'POST'])
async def search_images():
    keywords, max_results = run()
    results = []
    with DDGS() as ddgs:
        # 使用DuckDuckGo搜索关键词
        ddgs_gen = ddgs.images(keywords, safesearch='Off', timelimit=None)
        # 从搜索结果中获取最大结果数
        for r in islice(ddgs_gen, max_results):
            results.append(r)

    # 返回一个json响应，包含搜索结果
    return {'results': results}


@app.route('/searchVideos', methods=['GET', 'POST'])
async def search_videos():
    keywords, max_results = run()
    results = []
    with DDGS() as ddgs:
        # 使用DuckDuckGo搜索关键词
        ddgs_gen = ddgs.videos(keywords, safesearch='Off', timelimit=None, resolution="high")
        # 从搜索结果中获取最大结果数
        for r in islice(ddgs_gen, max_results):
            results.append(r)

    # 返回一个json响应，包含搜索结果
    return {'results': results}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
