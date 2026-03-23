#!/usr/bin/env python3
"""
LOL战队排名爬虫 - 从 Leaguepedia 爬取各赛区排名
支持赛区: LCK, LCS, LEC, PCS, LJL, LLA, CBLOL, TCL, OPL, LCO
使用 cloudscraper 绕过 Cloudflare
"""

import cloudscraper
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime

# 配置
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

# 赛区配置: (赛区名, 页面URL) - 使用2025赛季
REGIONS = {
    'LCK': 'https://lol.fandom.com/wiki/LCK/2025_Season',
    'LCS': 'https://lol.fandom.com/wiki/LCS/2025_Season',
    'LEC': 'https://lol.fandom.com/wiki/LEC/2025_Season',
    'PCS': 'https://lol.fandom.com/wiki/PCS/2025_Season',
    'LJL': 'https://lol.fandom.com/wiki/LJL/2025_Season',
    'LLA': 'https://lol.fandom.com/wiki/LLA/2025_Season',
    'CBLOL': 'https://lol.fandom.com/wiki/CBLOL/2025_Season',
    'TCL': 'https://lol.fandom.com/wiki/TCL/2025_Season',
    'OPL': 'https://lol.fandom.com/wiki/OPL/2025_Season',
    'LCO': 'https://lol.fandom.com/wiki/LCO/2025_Season',
}

def fetch_page(url, scraper):
    """获取页面"""
    try:
        resp = scraper.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"  [!] 获取失败 {url}: {e}")
        return None

def parse_standings(html, region):
    """解析排名表格"""
    soup = BeautifulSoup(html, 'html.parser')
    teams = []
    
    # 找所有表格
    tables = soup.find_all('table')
    
    for table in tables:
        # 获取表格的所有行
        rows = table.find_all('tr')
        for row in rows[1:]:  # 跳过表头
            cells = row.find_all(['td', 'th'])
            if len(cells) < 3:
                continue
            
            # 提取文本
            texts = [cell.get_text(strip=True) for cell in cells]
            
            team_name = None
            wins = losses = 0
            win_rate = ''
            
            # 找战队名（通常是非数字的非空字符串，且不是常见表头）
            for i, text in enumerate(texts):
                if (text and not text.isdigit() and '%' not in text 
                    and '-' not in text and ':' not in text and '/' not in text
                    and len(text) > 1 and text not in ['W', 'L', 'WWL', 'WL', 'LL', 'LW', 
                     'WW', 'WWL', 'WWW', 'LWW', 'LLL', 'Rank', 'Team', 'Pos', 'P', 'W', 'L',
                     'SW', 'SL', 'DS', ' streak', 'Latest', 'Last', 'Match', 'Results']):
                    team_name = text
                    break
            
            # 找胜-负
            for text in texts:
                # 格式: 10-3 或 10-3
                if re.match(r'^\d+[-–]\d+$', text):
                    parts = re.split(r'[-–]', text)
                    if len(parts) == 2:
                        wins = int(parts[0])
                        losses = int(parts[1])
                        break
                # 格式: 10W - 4L
                if 'W' in text and 'L' in text:
                    w_match = re.search(r'(\d+)\s*W', text)
                    l_match = re.search(r'(\d+)\s*L', text)
                    if w_match and l_match:
                        wins = int(w_match.group(1))
                        losses = int(l_match.group(1))
                        break
            
            # 找胜率
            for text in texts:
                if '%' in text:
                    win_rate = text
                    break
            
            if team_name and (wins > 0 or losses > 0):
                teams.append({
                    'region': region,
                    'team': team_name,
                    'wins': wins,
                    'losses': losses,
                    'win_rate': win_rate if win_rate else f"{wins/(wins+losses)*100:.1f}%",
                    'fetched_at': datetime.now().isoformat()
                })
    
    return teams

def crawl_all():
    """爬取所有赛区"""
    scraper = cloudscraper.create_scraper()
    all_teams = []
    
    print(f"开始爬取 {len(REGIONS)} 个赛区...\n")
    
    for region, url in REGIONS.items():
        print(f"[{region}] 正在爬取...")
        html = fetch_page(url, scraper)
        
        if html:
            teams = parse_standings(html, region)
            if teams:
                print(f"  ✓ 找到 {len(teams)} 支战队: {', '.join([t['team'] for t in teams[:5]])}...")
                all_teams.extend(teams)
            else:
                print(f"  ✗ 未找到排名数据")
        else:
            print(f"  ✗ 页面获取失败")
        
        time.sleep(2)  # 礼貌延迟
    
    return all_teams

if __name__ == '__main__':
    print("=" * 60)
    print("LOL战队排名爬虫 - Leaguepedia (cloudscraper)")
    print("=" * 60)
    print()
    
    teams = crawl_all()
    
    print()
    print("=" * 60)
    print(f"总计: {len(teams)} 支战队")
    print("=" * 60)
    
    # 输出 JSON
    output = {
        'fetched_at': datetime.now().isoformat(),
        'total_teams': len(teams),
        'by_region': {},
        'teams': teams
    }
    
    # 按赛区分组统计
    for team in teams:
        region = team['region']
        if region not in output['by_region']:
            output['by_region'][region] = []
        output['by_region'][region].append(team)
    
    # 保存到文件
    with open('/root/esports-data/lol_rankings.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n已保存到 /root/esports-data/lol_rankings.json")
    print(json.dumps(output, indent=2, ensure_ascii=False))
