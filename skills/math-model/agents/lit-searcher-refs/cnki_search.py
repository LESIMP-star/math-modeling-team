#!/usr/bin/env python3
"""
CNKI 搜索工具（通过学校图书馆代理）
使用方法：
1. 运行 start_edge_debug.bat 启动 Edge
2. 登录学校图书馆
3. 运行此脚本搜索文献
"""

import sys
import json
import io
from playwright.sync_api import sync_playwright
import time

# 设置 UTF-8 编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def search_cnki(query, max_results=20):
    """搜索 CNKI 并返回结果"""
    with sync_playwright() as p:
        # 连接到正在运行的 Edge 实例
        browser = p.chromium.connect_over_cdp('http://localhost:9222')

        # 获取现有的上下文
        context = browser.contexts[0]

        # 找到图书馆页面
        library_page = None
        for page in context.pages:
            if 'ncu.metaersp.cn' in page.url:
                library_page = page
                break

        if not library_page:
            browser.close()
            return {'query': query, 'status': 'error', 'error': '未找到图书馆页面，请先登录学校图书馆'}

        # 点击 CNKI 链接
        cnki_link = library_page.query_selector('a:has-text("CNKI")')
        if cnki_link:
            cnki_link.click()
            time.sleep(5)

        # 找到 CNKI 页面
        cnki_page = None
        for page in context.pages:
            if 'cwres.ncu.edu.cn' in page.url and 'cnki' in page.url:
                cnki_page = page
                break

        if not cnki_page:
            browser.close()
            return {'query': query, 'status': 'error', 'error': '未找到 CNKI 页面'}

        # 等待页面加载
        time.sleep(3)

        # 查找搜索框
        search_input = cnki_page.query_selector('#txt_SearchText')
        if search_input:
            # 清空搜索框
            search_input.fill('')
            time.sleep(0.5)

            # 输入关键词
            search_input.fill(query)
            time.sleep(1)

            # 按回车搜索
            search_input.press('Enter')
            time.sleep(5)

            # 等待页面加载
            try:
                cnki_page.wait_for_load_state('networkidle', timeout=30000)
            except:
                pass

            # 提取搜索结果
            results = []
            rows = cnki_page.query_selector_all('table.result-table-list tbody tr')

            for row in rows[:max_results]:
                # 提取标题
                title_elem = row.query_selector('td.name a.fz14')
                if title_elem:
                    title = title_elem.inner_text().strip()

                    # 提取作者
                    author_elem = row.query_selector('td.author')
                    authors = author_elem.inner_text().strip() if author_elem else ''

                    # 提取来源
                    source_elem = row.query_selector('td.source a')
                    source = source_elem.inner_text().strip() if source_elem else ''

                    # 提取日期
                    date_elem = row.query_selector('td.date')
                    date = date_elem.inner_text().strip() if date_elem else ''

                    results.append({
                        'title': title,
                        'authors': authors,
                        'source': source,
                        'date': date
                    })

            # 获取总结果数
            content = cnki_page.inner_text('body')
            import re
            total_match = re.search(r'共找到\s*([\d,]+)\s*条结果', content)
            total = total_match.group(1) if total_match else '未知'

            browser.close()
            return {
                'query': query,
                'results': results,
                'total': total,
                'status': 'success'
            }
        else:
            browser.close()
            return {'query': query, 'status': 'error', 'error': '未找到搜索框'}


def main():
    if len(sys.argv) < 2:
        print('用法: python cnki_search.py "搜索关键词"')
        print('示例: python cnki_search.py "数学建模 优化算法"')
        print('\\n注意：请先运行 start_edge_debug.bat 启动 Edge 并登录学校图书馆')
        return

    query = sys.argv[1]
    print(f"搜索关键词: {query}")
    print("=" * 50)

    result = search_cnki(query)

    if result['status'] == 'success':
        print(f"\\n找到 {result['total']} 条结果:")
        print(f"显示前 {len(result['results'])} 条:\\n")

        for i, r in enumerate(result['results'], 1):
            print(f"{i}. {r['title']}")
            print(f"   作者: {r['authors']}")
            print(f"   来源: {r['source']}")
            print(f"   日期: {r['date']}")
            print()

        # 保存结果到文件
        with open('cnki_results.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f'结果已保存到 cnki_results.json')
    else:
        print(f"搜索失败: {result.get('error')}")


if __name__ == '__main__':
    main()
