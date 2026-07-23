#!/usr/bin/env python3
"""
学术论文搜索工具 - 支持 arXiv API
"""

import sys
import json
import io
import requests
import xml.etree.ElementTree as ET

# 设置 UTF-8 编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def search_arxiv(query, max_results=10):
    """搜索 arXiv 论文"""
    url = 'http://export.arxiv.org/api/query'
    params = {
        'search_query': f'all:{query}',
        'start': 0,
        'max_results': max_results,
        'sortBy': 'relevance',
        'sortOrder': 'descending'
    }

    try:
        response = requests.get(url, params=params, timeout=30)

        if response.status_code == 200:
            # 解析 XML
            root = ET.fromstring(response.text)

            # 命名空间
            ns = {'atom': 'http://www.w3.org/2005/Atom'}

            # 提取论文
            entries = root.findall('atom:entry', ns)
            results = []

            for entry in entries:
                title = entry.find('atom:title', ns).text.strip()
                summary = entry.find('atom:summary', ns).text.strip()
                link = entry.find('atom:id', ns).text

                # 提取作者
                authors = []
                for author in entry.findall('atom:author', ns):
                    name = author.find('atom:name', ns).text
                    authors.append(name)

                # 提取发布日期
                published = entry.find('atom:published', ns).text[:10]

                # 提取分类
                categories = []
                for category in entry.findall('atom:category', ns):
                    categories.append(category.get('term'))

                results.append({
                    'title': title,
                    'authors': authors,
                    'summary': summary[:500],
                    'url': link,
                    'published': published,
                    'categories': categories
                })

            return {'query': query, 'results': results, 'status': 'success', 'total': len(results)}
        else:
            return {'query': query, 'status': 'error', 'error': f'HTTP {response.status_code}'}

    except Exception as e:
        return {'query': query, 'status': 'error', 'error': str(e)}


def search_arxiv_by_category(category, max_results=10):
    """按分类搜索 arXiv 论文"""
    url = 'http://export.arxiv.org/api/query'
    params = {
        'search_query': f'cat:{category}',
        'start': 0,
        'max_results': max_results,
        'sortBy': 'submittedDate',
        'sortOrder': 'descending'
    }

    try:
        response = requests.get(url, params=params, timeout=30)

        if response.status_code == 200:
            root = ET.fromstring(response.text)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            entries = root.findall('atom:entry', ns)
            results = []

            for entry in entries:
                title = entry.find('atom:title', ns).text.strip()
                summary = entry.find('atom:summary', ns).text.strip()
                link = entry.find('atom:id', ns).text
                published = entry.find('atom:published', ns).text[:10]

                authors = []
                for author in entry.findall('atom:author', ns):
                    name = author.find('atom:name', ns).text
                    authors.append(name)

                results.append({
                    'title': title,
                    'authors': authors,
                    'summary': summary[:300],
                    'url': link,
                    'published': published
                })

            return {'category': category, 'results': results, 'status': 'success'}
        else:
            return {'category': category, 'status': 'error', 'error': f'HTTP {response.status_code}'}

    except Exception as e:
        return {'category': category, 'status': 'error', 'error': str(e)}


def format_paper(paper, index=None):
    """格式化论文信息"""
    prefix = f"{index}. " if index else ""
    output = []
    output.append(f"{prefix}{paper['title']}")
    output.append(f"   作者: {', '.join(paper['authors'][:3])}{'...' if len(paper['authors']) > 3 else ''}")
    output.append(f"   日期: {paper['published']}")
    output.append(f"   链接: {paper['url']}")
    if paper.get('summary'):
        output.append(f"   摘要: {paper['summary'][:200]}...")
    return '\n'.join(output)


def main():
    if len(sys.argv) < 2:
        print('用法: python academic_search.py "搜索关键词"')
        print('示例: python academic_search.py "mathematical modeling optimization"')
        print('\n分类搜索: python academic_search.py --category math.OC')
        print('  常用分类: math.OC (优化), math.NA (数值分析), cs.LG (机器学习)')
        return

    if sys.argv[1] == '--category':
        if len(sys.argv) < 3:
            print('请指定分类，例如: python academic_search.py --category math.OC')
            return
        category = sys.argv[2]
        print(f"搜索分类: {category}")
        print("=" * 50)
        result = search_arxiv_by_category(category)
    else:
        query = sys.argv[1]
        print(f"搜索关键词: {query}")
        print("=" * 50)
        result = search_arxiv(query)

    if result['status'] == 'success':
        papers = result['results']
        print(f"\n找到 {len(papers)} 篇论文：\n")
        for i, paper in enumerate(papers, 1):
            print(format_paper(paper, i))
            print()
    else:
        print(f"搜索失败: {result.get('error')}")


if __name__ == '__main__':
    main()
